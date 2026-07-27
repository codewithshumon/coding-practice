# Media Processing — Complete Guide

> **Series:** Media Processing Documentation — Part 1
> This file covers the three core **media-processing tools**: WhisperX (speech-to-text), Playwright (browser capture/automation), and FFmpeg (audio/video conversion). They compose into media pipelines (record → process → transcribe). More topics (streaming protocols, video encoding deep-dive, TTS) will be added later.

---

## Table of Contents

- [Shared Orientation — The Media Pipeline](#shared-orientation--the-media-pipeline)
- **WhisperX**
  - [1. What Is WhisperX?](#1-what-is-whisperx)
  - [2. WhisperX vs OpenAI Whisper](#2-whisperx-vs-openai-whisper)
  - [3. How WhisperX Works](#3-how-whisperx-works)
  - [4. WhisperX Key Concepts](#4-whisperx-key-concepts)
  - [5. Where to Use WhisperX](#5-where-to-use-whisperx)
  - [6. Where NOT to Use WhisperX](#6-where-not-to-use-whisperx)
  - [7. Installing and Setting Up WhisperX](#7-installing-and-setting-up-whisperx)
  - [8. WhisperX Compute and Requirements](#8-whisperx-compute-and-requirements)
  - [9. WhisperX Production Best Practices](#9-whisperx-production-best-practices)
  - [10. WhisperX Real-World Examples](#10-whisperx-real-world-examples)
  - [11. WhisperX Pitfalls](#11-whisperx-pitfalls)
- **Playwright**
  - [12. What Is Playwright?](#12-what-is-playwright)
  - [13. Playwright vs Selenium vs Puppeteer](#13-playwright-vs-selenium-vs-puppeteer)
  - [14. How Playwright Works](#14-how-playwright-works)
  - [15. Playwright Key Concepts](#15-playwright-key-concepts)
  - [16. Where to Use Playwright](#16-where-to-use-playwright)
  - [17. Where NOT to Use Playwright](#17-where-not-to-use-playwright)
  - [18. Installing and Setting Up Playwright](#18-installing-and-setting-up-playwright)
  - [19. Playwright Browsers and Contexts](#19-playwright-browsers-and-contexts)
  - [20. Playwright Production Best Practices](#20-playwright-production-best-practices)
  - [21. Playwright Real-World Examples](#21-playwright-real-world-examples)
  - [22. Playwright Pitfalls](#22-playwright-pitfalls)
- **FFmpeg**
  - [23. What Is FFmpeg?](#23-what-is-ffmpeg)
  - [24. FFmpeg vs Other Media Tools](#24-ffmpeg-vs-other-media-tools)
  - [25. How FFmpeg Works](#25-how-ffmpeg-works)
  - [26. FFmpeg Key Concepts](#26-ffmpeg-key-concepts)
  - [27. Where to Use FFmpeg](#27-where-to-use-ffmpeg)
  - [28. Where NOT to Use FFmpeg](#28-where-not-to-use-ffmpeg)
  - [29. Installing and Setting Up FFmpeg](#29-installing-and-setting-up-ffmpeg)
  - [30. FFmpeg Codecs and Formats](#30-ffmpeg-codecs-and-formats)
  - [31. FFmpeg Production Best Practices](#31-ffmpeg-production-best-practices)
  - [32. FFmpeg Real-World Examples](#32-ffmpeg-real-world-examples)
  - [33. FFmpeg Pitfalls](#33-ffmpeg-pitfalls)
- [Shared Foundations](#shared-foundations)
- [Quick Reference Card](#quick-reference-card)

---

## Shared Orientation — The Media Pipeline

These three tools solve different stages of a **media pipeline**, and they compose naturally:

| Tool | Stage | One-liner |
|---|---|---|
| **Playwright** | Capture | Record/interact with live webcasts & web pages |
| **FFmpeg** | Process | Convert, trim, extract, compress audio/video |
| **WhisperX** | Transcribe | Turn audio into timestamped, speaker-labeled text |

**A real pipeline** (earnings-call transcription):
```
Playwright records a live webcast
   → FFmpeg extracts/cleans the audio
   → WhisperX transcribes it (word timestamps + speakers)
```

**Rule of thumb:** **Playwright** to *get* the media, **FFmpeg** to *transform* it, **WhisperX** to *understand* it. Each is best-in-class at its stage — combine them rather than forcing one to do everything.

---

# WhisperX

## 1. What Is WhisperX?

**WhisperX** is a **GPU-accelerated speech-to-text** tool built on OpenAI's Whisper, adding **word-level timestamps**, **speaker diarization** (who spoke when), and **faster processing** via batched inference.

**One-liner:** fast, accurate transcription with word timestamps and speaker labels.

## 2. WhisperX vs OpenAI Whisper

| | WhisperX | OpenAI Whisper (vanilla) |
|---|---|---|
| Speed | Fast (batched, GPU) | Slower |
| Timestamps | **Word-level** | Segment-level |
| Diarization | **Yes** (who spoke when) | No |
| Alignment | Forced alignment for accuracy | Less precise timing |

**Rule of thumb:** WhisperX when you need **speed, word-level timestamps, and speaker labels**; vanilla Whisper for simple transcription.

## 3. How WhisperX Works

1. **Whisper ASR** transcribes audio to text (segment-level).
2. **Forced alignment** aligns the transcript to audio for **word-level timestamps**.
3. **VAD (voice activity detection)** trims silence for speed/accuracy.
4. **Optional diarization** (pyannote) labels **who spoke when**.
5. All **GPU-accelerated** with batched inference for throughput.

## 4. WhisperX Key Concepts

- **ASR** — automatic speech recognition (Whisper models: tiny → large).
- **Forced alignment** — precise word-level timing.
- **Speaker diarization** — who spoke when (needs a HF token for pyannote).
- **VAD** — skip silence.
- **GPU batching** — process chunks in parallel for speed.

## 5. Where to Use WhisperX

- **Transcription pipelines** (meetings, webcasts, calls).
- **Subtitles/captions** (word-level timing).
- **Searchable audio archives**.
- **Speaker-attributed transcripts** (multi-speaker content).

## 6. Where NOT to Use WhisperX

- **Real-time streaming** transcription (it's batch-oriented).
- **No GPU available** (CPU-only is very slow).
- Languages with **poor Whisper support**.

## 7. Installing and Setting Up WhisperX

```bash
pip install whisperx

# Transcribe with word timestamps
whisperx audio.mp3 --model large-v2 --compute_type float16
# With speaker diarization (needs HF token)
whisperx audio.mp3 --diarize --hf_token <token>
```

## 8. WhisperX Compute and Requirements

- **GPU (CUDA)** strongly recommended — CPU is dramatically slower.
- **Model size vs accuracy** — `large-v2` most accurate, `small`/`base` faster.
- **Diarization** needs a Hugging Face token (pyannote) and adds processing time.

## 9. WhisperX Production Best Practices

1. **Use GPU + batching** — the whole point of WhisperX.
2. **Pick model size** for your accuracy/speed tradeoff.
3. **Enable diarization only when needed** — it slows things down.
4. **Use VAD** to skip silence.
5. **Chunk long audio** — avoid memory issues on huge files.

## 10. WhisperX Real-World Examples

### Example 1 — Timestamped Transcript
**Why:** word-level timestamps let you build clickable, searchable transcripts (jump to any word in the audio).

### Example 2 — Speaker-Attributed Webcast Transcript
**Why:** diarization labels each speaker — earnings calls get "CEO:" / "CFO:" attribution automatically.

## 11. WhisperX Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| No GPU | Extremely slow | Use CUDA GPU |
| Missing diarization token | Diarization fails | Set HF token |
| Large model OOM | Crash on big files | Smaller model / chunk audio |
| Poor audio quality | Bad transcription | Clean audio (FFmpeg) first |
| Not chunking long files | Memory issues | Split into chunks |

---

# Playwright

## 12. What Is Playwright?

**Playwright** is a **browser automation framework** for Chromium, Firefox, and WebKit — programmatically controlling real browsers to record, capture, and interact with web pages (e.g., live webcasts).

**One-liner:** reliable, modern, cross-browser automation.

## 13. Playwright vs Selenium vs Puppeteer

| | Playwright | Selenium | Puppeteer |
|---|---|---|---|
| Browsers | Chromium, Firefox, WebKit | All (via drivers) | Chromium only |
| Auto-waiting | Built-in | Manual | Partial |
| Modern API | Yes | Older | Older |
| Recording/tracing | Built-in | Limited | Limited |

**Rule of thumb:** Playwright for **modern, reliable, cross-browser** automation; Selenium for legacy/enterprise; Puppeteer for Chromium-only quick scripts.

## 14. How Playwright Works

1. **Launch a real browser** (headless or headed).
2. **Navigate + interact** via a clean API (click, fill, wait).
3. **Auto-waits** for elements — no manual sleeps.
4. **Capture** screenshots, **video**, network traffic, traces.

**Key point:** Playwright drives a *real* browser, so it handles JS-heavy pages that simple HTTP clients can't.

## 15. Playwright Key Concepts

- **Browser / context / page** — the hierarchy (contexts = isolated sessions).
- **Selectors** — how you target elements.
- **Auto-waiting** — waits for elements to be actionable.
- **Network interception** — mock/inspect requests.
- **Video/trace recording** — capture sessions for debugging.

## 16. Where to Use Playwright

- **Recording/capturing live webcasts**.
- **Web scraping** JS-heavy pages.
- **E2E testing**.
- **Screenshots / PDF generation**.
- **Automating web workflows** (form fills, clicks).

## 17. Where NOT to Use Playwright

- **Simple HTTP fetches** (use `requests`/`fetch` — much lighter).
- When a **real API exists** (use it instead of scraping).

## 18. Installing and Setting Up Playwright

```bash
# Node.js
npm install playwright && npx playwright install
# Python
pip install playwright && playwright install
```

```typescript
import { chromium } from "playwright";
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("https://example.com");
await page.screenshot({ path: "shot.png" });
await browser.close();
```

## 19. Playwright Browsers and Contexts

- **Chromium / Firefox / WebKit** — pick per target/compatibility.
- **Browser contexts** — isolated sessions (separate cookies/storage) — great for parallel, independent tasks.
- **Headless** (default, fast) vs **headed** (visible, for debugging).

## 20. Playwright Production Best Practices

1. **Use auto-waiting** — never fixed `sleep()` calls (flaky).
2. **Robust selectors** — prefer `data-testid`/role over brittle CSS/XPath.
3. **Browser contexts** for isolated, parallel sessions.
4. **Record video/trace** for debugging failures.
5. **Headless in CI**, headed for local debugging.
6. **Always close browsers/contexts** — avoid resource leaks.

## 21. Playwright Real-World Examples

### Example 1 — Record a Live Webcast
**Why:** launch a browser, navigate to the webcast, capture the stream/video — automated recording of a live event.

### Example 2 — Scrape a JS-Heavy Page
**Why:** a real browser renders the JS; you extract data a plain HTTP client would miss.

### Example 3 — Automated Form + Screenshot
**Why:** fill and submit a form, then screenshot the result — reliable end-to-end web automation.

## 22. Playwright Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Fixed sleeps | Flaky timing bugs | Auto-waiting |
| Brittle selectors | Breaks on UI changes | data-testid / role selectors |
| Not closing browsers | Memory/resource leaks | Always close contexts |
| Anti-bot detection | Blocked automation | Realistic headers, rate-limiting |
| Using for simple fetches | Heavy/slow | Use HTTP client instead |

---

# FFmpeg

## 23. What Is FFmpeg?

**FFmpeg** is a **cross-platform solution for recording, converting, and streaming audio and video** — the universal command-line tool for media processing.

**One-liner:** the Swiss Army knife of audio/video processing.

## 24. FFmpeg vs Other Media Tools

| | FFmpeg | Commercial/GUI editors |
|---|---|---|
| Cost | Free, open-source | Often paid |
| Automation | CLI/scriptable | GUI-focused |
| Capability | Virtually any conversion | Editing-focused |

**Rule of thumb:** FFmpeg for **programmatic media conversion/processing** in pipelines; GUI editors for manual editing.

## 25. How FFmpeg Works

```
input → demux → decode → filter/process → encode → mux → output
```

- You control it via **CLI flags**: input, codecs, filters, bitrate, output.
- **Codecs** compress/decompress; **containers** package streams; **filters** transform.

**Key point:** FFmpeg is a pipeline — you chain operations with flags to transform media exactly as needed.

## 26. FFmpeg Key Concepts

- **Codecs** — H.264, H.265, VP9 (video); AAC, MP3, Opus (audio).
- **Containers** — MP4, MKV, WebM, MP3.
- **Streams** — audio/video/subtitle tracks in a file.
- **Filters** — scale, crop, trim, volume, etc.
- **Bitrate / transcoding** — quality vs size tradeoff.

## 27. Where to Use FFmpeg

- **Transcoding** (convert formats).
- **Trimming/cutting** clips.
- **Extracting audio** from video.
- **Generating thumbnails**.
- **Compression** for size.
- **Streaming** media.

## 28. Where NOT to Use FFmpeg

- **GUI-based editing** (use a video editor).
- When a **managed media service** (e.g., AWS MediaConvert) fits better.

## 29. Installing and Setting Up FFmpeg

```bash
# Install (apt/brew/download), then:
ffmpeg -i input.mp4 output.mp3            # extract audio
ffmpeg -i input.mov -c:v libx264 out.mp4  # convert/transcode
```

## 30. FFmpeg Codecs and Formats

- **Video codec** — H.264 (compatible), H.265 (smaller), VP9 (web).
- **Audio codec** — AAC (compatible), Opus (efficient).
- **Container** — MP4 (universal), WebM (web), MKV (flexible).
- **Bitrate** — higher = better quality = bigger files.

## 31. FFmpeg Production Best Practices

1. **Use `-c copy`** when no re-encode is needed — instant, no quality loss.
2. **Hardware acceleration** (`-hwaccel`) when available — big speedups.
3. **Two-pass encoding** for best quality/size.
4. **Test on short samples** before processing hours of media.
5. **Log output** — FFmpeg is verbose; capture errors.

## 32. FFmpeg Real-World Examples

### Example 1 — Extract Audio for Transcription
```bash
ffmpeg -i webcast.mp4 -vn -acodec libmp3lame audio.mp3
```
**Why:** strip video, keep audio — the exact prep step before WhisperX transcription.

### Example 2 — Trim a Clip (no re-encode)
```bash
ffmpeg -i input.mp4 -ss 00:01:00 -to 00:02:00 -c copy clip.mp4
```
**Why:** `-c copy` cuts without re-encoding — instant and lossless.

### Example 3 — Generate a Thumbnail
```bash
ffmpeg -i input.mp4 -ss 00:00:05 -frames:v 1 thumb.jpg
```
**Why:** grab a frame for previews.

### Example 4 — Compress for Web
```bash
ffmpeg -i input.mov -c:v libx264 -crf 23 -c:a aac output.mp4
```
**Why:** H.264 + reasonable CRF = good quality at web-friendly size.

## 33. FFmpeg Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Re-encoding unnecessarily | Quality loss, slow | Use `-c copy` |
| Wrong codec/container combo | Won't play | Match codec to container |
| High bitrate | Huge files | Tune bitrate/CRF |
| Ignoring hardware accel | Slow processing | Use `-hwaccel` |
| Complex filter syntax errors | Failed commands | Test incrementally on samples |

---

## Shared Foundations

Concepts that recur across **all three tools**:

- **Pipelines over monoliths** — media processing is a chain: capture (Playwright) → transform (FFmpeg) → understand (WhisperX). Compose specialized tools rather than forcing one to do everything.
- **GPU acceleration** — WhisperX (batched inference) and FFmpeg (`-hwaccel`) both benefit hugely from GPUs; CPU-only media work is slow.
- **Batch vs real-time** — these tools are largely batch-oriented; real-time streaming media has different requirements (and tools).
- **Format/codec tradeoffs** — quality vs size vs compatibility is a constant balancing act (FFmpeg codecs, model sizes in WhisperX).
- **Automation-first** — all three are scriptable/CLI-driven, designed to run in automated pipelines, not manual GUIs.

## Quick Reference Card

```
PIPELINE STAGES:
  Capture     → Playwright (record webcasts, scrape JS pages)
  Transform   → FFmpeg (convert, trim, extract, compress)
  Understand  → WhisperX (transcribe with timestamps + speakers)

TOOL PICKER:
  Record/automate a browser?      → Playwright
  Convert/process audio-video?    → FFmpeg
  Transcribe speech to text?      → WhisperX (GPU + diarization)

GOLDEN RULES:
  ✓ Playwright: auto-wait (no sleeps), robust selectors, close contexts
  ✓ FFmpeg: -c copy when possible, hwaccel, test on samples
  ✓ WhisperX: use GPU, chunk long audio, clean audio first (FFmpeg)
  ✓ Compose tools into pipelines — don't force one to do everything
```

---

*This file covers the core media-processing tools. More topics (streaming protocols, video encoding deep-dive, text-to-speech) will be added as separate files in this series over time.*
