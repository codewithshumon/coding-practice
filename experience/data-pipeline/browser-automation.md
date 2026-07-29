# Develop Browser Automation Systems

> **Category:** Data Pipeline & Processing
> **Relevant at:** Codixel (recording live earnings-call webcasts at scale)
> **Related tech docs:** `case/media/media-processing.md` (Playwright §12–22), `case/structures-architecture/backend-systems.md` (Performance Tuning §41–48), `case/cloud-service/cloud-platforms.md` (ECS Fargate §45–55)

---

## 1. What This Means

Developing browser automation systems means building **reliable, scalable infrastructure** that controls real browsers (via Playwright) to record live webcasts and capture content from various sources — handling the challenges of timing, reliability, anti-bot detection, and scale.

**Scope:**
- **Recording live webcasts** — capturing streaming video from earnings calls, events, broadcasts
- **Browser control at scale** — running many browser instances concurrently
- **Reliability** — handling crashes, timeouts, network issues, and anti-bot measures
- **Source diversity** — different webcast platforms have different players, layouts, and protection
- **Production orchestration** — scheduling, queueing, and monitoring automated browser sessions

**Why it matters:** live events happen on a schedule and can't be re-recorded. If the browser automation fails during a live earnings call, that data is gone forever. Reliability isn't a nice-to-have — it's the core requirement.

---

## 2. Real-World Production Application

In production, this responsibility plays out as:

**The Codixel webcast recording pipeline:**
```
Event Schedule → Scheduler triggers recording job
   → Browser Automation (Playwright) launches + navigates to webcast
      → Captures the stream/video
         → Uploads recording to S3
            → Enqueues transcription job
```

**The core engineering challenges:**

1. **Timing is critical** — live webcasts start at a specific time. The browser must be ready and recording BEFORE the event starts.
   - **Solution:** scheduled jobs that launch browsers with buffer time, wait for the stream to appear, then record

2. **Reliability under failure** — browsers crash, streams lag, networks drop
   - **Solution:** auto-waiting (Playwright's strength), retry logic, health checks during recording, and graceful recovery

3. **Anti-bot detection** — some platforms block automated browsers
   - **Solution:** realistic browser fingerprints, proper headers, rate-limiting, stealth plugins

4. **Scale** — recording many concurrent webcasts from different sources
   - **Solution:** containerized browser instances (one per recording job), queue-based orchestration

5. **Source diversity** — each webcast platform has a different video player, layout, and stream format
   - **Solution:** per-source adapters/configs that know how to find and capture each platform's player

**The production architecture:**
- A scheduler (EventBridge cron) triggers recording jobs at event start times
- Jobs land in an SQS queue
- Browser workers (containerized Playwright instances) pull jobs and record
- Recordings uploaded to S3, transcription jobs enqueued

---

## 3. How to Implement

### The Browser Automation Worker

```python
from playwright.async_api import async_playwright
import asyncio

class WebcastRecorder:
    """Records a live webcast — reliability is the core requirement."""

    def __init__(self, source_config: SourceConfig):
        self.config = source_config   # per-source selectors, URLs, timing

    async def record(self, job: RecordingJob) -> str:
        async with async_playwright() as p:
            # 1. Launch browser (realistic config for anti-bot evasion)
            browser = await p.chromium.launch(
                headless=True,
                args=["--disable-blink-features=AutomationControlled"],
            )
            context = await browser.new_context(
                user_agent="Mozilla/5.0 ... (realistic UA)",
                viewport={"width": 1920, "height": 1080},
            )
            page = await context.new_page()

            try:
                # 2. Navigate + wait for the player to appear (auto-waiting)
                await page.goto(job.url, wait_until="networkidle")
                player = await page.wait_for_selector(
                    self.config.video_selector,
                    timeout=60000,   # wait up to 1 min for stream to start
                )

                # 3. Start recording (capture the video stream)
                recording_path = f"/tmp/{job.event_id}.webm"
                await self._start_capture(page, recording_path)

                # 4. Monitor recording health
                await self._monitor_recording(page, job.duration_seconds)

                # 5. Stop + upload
                await self._stop_capture()
                await s3.upload(f"recordings/{job.event_id}.webm", recording_path)
                return recording_path

            except Exception as e:
                logger.error(f"Recording failed for {job.event_id}: {e}")
                raise
            finally:
                await browser.close()   # ALWAYS close — avoid resource leaks
```

### Reliability Patterns

```python
async def _monitor_recording(self, page, duration: int):
    """Watch for stream issues during recording — don't assume it's working."""
    start = time.time()
    while time.time() - start < duration:
        # Check the player is still alive
        try:
            is_playing = await page.evaluate("document.querySelector('video').readyState > 2")
            if not is_playing:
                logger.warning("Stream stalled — attempting recovery")
                await self._recover_stream(page)
        except Exception:
            logger.error("Player check failed — browser may have crashed")
            raise
        await asyncio.sleep(30)   # health check every 30s
```

### Queue-Based Orchestration

```python
async def recording_worker_loop():
    """Pulls recording jobs, launches browser automation, handles failures."""
    while True:
        messages = await sqs.receive(QueueUrl=RECORDING_QUEUE, MaxNumberOfMessages=1,
                                      VisibilityTimeout=7200)  # 2 hours — webcasts are long
        if not messages:
            await asyncio.sleep(5)
            continue

        job = RecordingJob.from_message(messages[0])
        try:
            recorder = WebcastRecorder(get_source_config(job.source))
            recording_path = await recorder.record(job)

            # Success → enqueue transcription
            await sqs.send(QueueUrl=TRANSCRIBE_QUEUE, MessageBody=json.dumps({
                "event_id": job.event_id,
                "audio_s3_key": f"recordings/{job.event_id}.webm",
            }))
            await sqs.delete(messages[0])

        except Exception as e:
            # Live events can't be re-recorded — alert immediately
            await alert_ops(f"RECORDING FAILED: {job.event_id} — {e}")
            # Move to DLQ (can't retry a live event, but preserve for analysis)
            await move_to_dlq(messages[0], e)
```

### Per-Source Configuration

```python
# Different webcast platforms need different handling
SOURCE_CONFIGS = {
    "zoom_webinar": SourceConfig(
        video_selector="video#wc-webcam",
        login_required=True,
        stealth_mode=False,
    ),
    "youtube_live": SourceConfig(
        video_selector="video.html5-main-video",
        login_required=False,
        stealth_mode=True,   # YouTube sometimes blocks automation
    ),
    "custom_platform": SourceConfig(
        video_selector=".player-container video",
        login_required=True,
        stealth_mode=True,
    ),
}
```

### Browser Automation Checklist

- [ ] **Auto-waiting** (Playwright built-in) — never fixed `sleep()` calls
- [ ] **Realistic browser config** — proper UA, viewport, stealth args
- [ ] **Health monitoring** during long recordings — don't assume it's working
- [ ] **Always close browsers** — resource leaks in long-running workers
- [ ] **One browser per job** — isolate recordings from each other
- [ ] **Queue-based orchestration** — jobs wait their turn, scale horizontally
- [ ] **Generous visibility timeout** — webcasts can be hours long
- [ ] **Per-source configs** — each platform has different players/protection
- [ ] **Immediate alerting on failure** — live events can't be re-recorded
- [ ] **Containerized** — Docker for consistent, isolated browser environments

### Avoid These

- **Fixed `sleep()` waits** — flaky; a stream starting 5 seconds late breaks the recording
- **Not closing browsers** — memory leaks crash long-running workers
- **No health monitoring** — a frozen stream records silence for an hour
- **No anti-bot measures** — platforms detect and block naive automation
- **One browser for all jobs** — a crash takes down all concurrent recordings
- **Synchronous recording** — blocking an API call on a 2-hour webcast
- **No alerting on failure** — a missed live event is gone forever; silence is unacceptable
