# Build Transcription Pipelines

> **Category:** Data Pipeline & Processing
> **Relevant at:** Codixel (earnings-call transcription with WhisperX + FFmpeg)
> **Related tech docs:** `case/media/media-processing.md` (WhisperX §1–11, FFmpeg §23–33), `case/structures-architecture/backend-systems.md` (Performance Tuning §41–48), `case/cloud-service/cloud-platforms.md` (ECS Fargate §45–55, Lambda §10)

---

## 1. What This Means

Building transcription pipelines means creating systems that convert audio/video into **timestamped, speaker-attributed text** at scale — using GPU-accelerated speech-to-text (WhisperX) and audio processing (FFmpeg) as the core engines, wrapped in production-grade reliability.

**Scope:**
- **Audio preparation** — extracting, cleaning, and chunking audio (FFmpeg)
- **GPU-accelerated transcription** — WhisperX for fast, accurate speech-to-text
- **Word-level timestamps** — precise timing for every word (for search/subtitles)
- **Speaker diarization** — labeling who spoke when (for multi-speaker content)
- **Pipeline orchestration** — queue-based processing that scales with GPU availability
- **Reliability** — retries, error handling, memory management for large files

**Why it matters:** transcription is compute-heavy and slow. Without a proper pipeline architecture, you either process one file at a time (slow) or crash on large files (OOM). The pipeline makes transcription **reliable, scalable, and cost-efficient**.

---

## 2. Real-World Production Application

In production, this responsibility plays out as:

**The Codixel earnings-call pipeline:**
```
Webcast recording (Playwright)
   → Audio extraction (FFmpeg)
      → Transcription (WhisperX, GPU)
         → Speaker diarization (pyannote)
            → Word-level timestamps
               → Classification + Publishing
```

**The core engineering challenges:**

1. **GPU resource management** — WhisperX needs CUDA GPUs; CPU-only is 10-100x slower
   - GPU instances are expensive — you can't keep them idle, but you can't over-provision
   - **Solution:** queue-based processing — files wait in SQS, GPU workers pull as capacity frees up

2. **Large file handling** — a 2-hour earnings call is a big audio file
   - WhisperX loads the whole file into GPU memory → OOM risk
   - **Solution:** chunk long audio into segments (FFmpeg), process independently, stitch results

3. **Diarization adds complexity** — labeling speakers needs a separate model (pyannote)
   - Requires a Hugging Face token
   - Slower processing — enable only when multi-speaker attribution matters

4. **Audio quality affects accuracy** — bad audio = bad transcription
   - **Solution:** FFmpeg pre-processing — normalize volume, remove silence (VAD), clean noise

**The production pipeline:**
- Files arrive in S3 (from the scraping stage)
- SQS queue holds transcription jobs
- GPU workers (ECS Fargate with GPU, or EC2 GPU instances) pull and process
- Results (transcript + timestamps + speakers) stored and indexed

---

## 3. How to Implement

### Stage 1 — Audio Preparation (FFmpeg)

```bash
# Extract audio from video webcast
ffmpeg -i webcast.mp4 -vn -acodec libmp3lame -ar 16000 -ac 1 audio.mp3
# -vn: no video | -ar 16000: Whisper sample rate | -ac 1: mono (better for ASR)

# Chunk long audio into 30-min segments (avoid GPU OOM)
ffmpeg -i audio.mp3 -f segment -segment_time 1800 -c copy chunk_%03d.mp3
# Produces chunk_000.mp3, chunk_001.mp3, ...

# Optional: remove silence (improves speed + accuracy)
ffmpeg -i audio.mp3 -af silenceremove=stop_periods=-1:stop_duration=2:stop_threshold=-50dB cleaned.mp3
```

**Why:** clean, mono, 16kHz audio in manageable chunks maximizes WhisperX accuracy and prevents GPU memory crashes.

### Stage 2 — GPU Worker (WhisperX)

```python
import whisperx

class TranscriptionWorker:
    def __init__(self):
        self.device = "cuda"        # GPU required
        self.model = whisperx.load_model("large-v2", self.device, compute_type="float16")
        self.align_model, self.metadata = whisperx.load_align_model("en", self.device)

    async def transcribe(self, audio_path: str, event_id: str) -> TranscriptionResult:
        # 1. Load audio (WhisperX handles loading)
        audio = whisperx.load_audio(audio_path)

        # 2. Transcribe (segment-level)
        result = self.model.transcribe(audio, batch_size=16)

        # 3. Align for word-level timestamps
        result = whisperx.align(result["segments"], self.align_model,
                                self.metadata, audio, self.device)

        # 4. Diarize (speaker labels) — needs HF token
        diarize_model = whisperx.DiarizationPipeline(use_auth_token=HF_TOKEN, device=self.device)
        diarize_segments = diarize_model(audio, min_speakers=2, max_speakers=8)
        result = whisperx.assign_word_speakers(diarize_segments, result)

        return TranscriptionResult(
            event_id=event_id,
            segments=result["segments"],    # word-level + speaker
            audio_path=audio_path,
        )
```

### Stage 3 — Pipeline Orchestration (Queue-Based)

```python
async def transcription_worker_loop():
    """GPU worker — pulls jobs from SQS, transcribes, publishes results."""
    whisper = TranscriptionWorker()

    while True:
        messages = await sqs.receive(QueueUrl=TRANSCRIBE_QUEUE, MaxNumberOfMessages=1,
                                      VisibilityTimeout=900)  # 15 min — transcription is slow
        if not messages:
            await asyncio.sleep(5)
            continue

        for msg in messages:
            job = json.loads(msg["body"])
            try:
                # Download audio from S3
                audio_path = await s3.download(job["audio_s3_key"])

                # Chunk if long
                chunks = await ffmpeg.chunk_if_needed(audio_path, max_duration=1800)

                # Transcribe each chunk
                results = [await whisper.transcribe(c, job["event_id"]) for c in chunks]
                merged = merge_transcripts(results)   # stitch chunks + re-align timestamps

                # Upload result + publish to next stage
                await s3.upload(f"transcripts/{job['event_id']}.json", merged.json())
                await sqs.send(QueueUrl=CLASSIFY_QUEUE,
                               MessageBody=json.dumps({"event_id": job["event_id"], ...}))

                await sqs.delete(msg)

            except torch.cuda.OutOfMemoryError:
                # GPU OOM — chunk smaller and retry
                await retry_with_smaller_chunks(msg)
            except Exception as e:
                await handle_failure(msg, e)
```

### Stage 4 — Result Format (Word-Level + Speakers)

```json
{
  "event_id": "earnings-q3-2024",
  "segments": [
    {
      "start": 12.34,
      "end": 18.91,
      "speaker": "SPEAKER_00",
      "text": "Thank you for joining our third quarter earnings call.",
      "words": [
        {"word": "Thank", "start": 12.34, "end": 12.67, "speaker": "SPEAKER_00"},
        {"word": "you", "start": 12.67, "end": 12.89, "speaker": "SPEAKER_00"}
      ]
    }
  ]
}
```

### Transcription Pipeline Checklist

- [ ] **GPU (CUDA) available** — CPU-only is impractically slow
- [ ] **Audio pre-processed** — 16kHz mono, silence removed (FFmpeg)
- [ ] **Long audio chunked** — avoid GPU OOM on multi-hour files
- [ ] **Model size chosen** for accuracy/speed tradeoff (large-v2 vs base)
- [ ] **Diarization enabled** only when speaker attribution needed (slows processing)
- [ ] **HF token set** for diarization (pyannote requires it)
- [ ] **Queue-based processing** — files wait for GPU capacity, don't overwhelm it
- [ ] **Memory monitoring** — GPU OOM caught and handled (retry with smaller chunks)
- [ ] **Visibility timeout** generous (transcription is slow — 15+ min)
- [ ] **Idempotency** — re-transcribing the same file doesn't duplicate results

### Avoid These

- **CPU-only transcription** — 10-100x slower; GPU is essential for production volume
- **Loading entire long files into GPU memory** — OOM crash
- **No audio pre-processing** — background noise/silence degrades accuracy and wastes GPU cycles
- **Diarization when not needed** — adds latency and complexity for single-speaker content
- **Processing synchronously** — blocking an API call on a 30-min transcription
- **Wrong model size** — large-v2 for everything wastes GPU; tiny for important content sacrifices accuracy
