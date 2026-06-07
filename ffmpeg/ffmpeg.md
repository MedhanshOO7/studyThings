---
id: ffmpeg
aliases: []
tags: []
---

# Some Introduction

| Term | Defination |
| -------------- | --------------- |
| Video Stream |  a sequence of compressed image frame|
| Audio Stream | compressed audio data|
| Container | The "wrapper" format, how streams are organized in the file |
|Codec|The algorithm used to compress/decompress the actual video or audio data|

## The Container vs Codec distinction

| Term | What it is? | Examples |
| --------------- | --------------- | --------------- |
| Container | Wrapper format | `mp4`,`.mkv`,`.avi`,`.webm` |
| Codec | algorithm |  `H.264`, `H.265`, `VP9`, `AAC`, `MP3`, `Opus`|

A .mp4 file can contain video encoded with H.264 or H.265. An .mkv file can contain almost anything. The container and the codec are independent — ==this is why "just changing the extension" does absolutely nothing.==

## Bitrate

- **bitrate** :- A bitrate is the amount of data used to store or transmit audio/video per second, usually measured in kbps (kilobits per second) or Mbps (megabits per second).

higher bitrate usually means 
- Better image quality
- Fewer compression artifacts
- Larger file size

### Relationship Between Bitrate and File size

rough formula
``` File Size ≈ Bitrate × Duration
```

### Why not high bitrate?

```bash 
Higher Bitrate
    ↓
Larger File 
    ↓
More Storage
    ↓
More Bandwidth
``` 

This won't be easy for a streaming services
### Bitrate vs Resolution 

Resolution means 
    - how many pixels exists
Bitrate 
    - how much data we have to describe these pixels

Imagine you're describing a beautiful landscape to someone.

### Modle

Low bitrate

`"There is a tree."` 
Very little information.

High bitrate
`"There is a large oak tree with green leaves,
a river behind it, mountains in the distance..."` 

Much more information.

## Why compression exists at all?

- The reason is still the same the redundancy.
- For ex. :- raw, uncompressed video is absurdly large. A single second of 1080p video at 30fps, uncompressed, is roughly 1.5 GB. A 2-hour movie would be ~10 TB.

What is the thing we leverage in this example? 

1. **Spatial redundancy** — within a single frame, large areas are similar (a blue sky). No need to store every pixel independently.
2. **Temporal redundancy** — between frames, most of the image doesn't change. Only the differences need to be stored.

# Whta is FFMPEG?
- it is a CLI tool, that can do the following.
1. Decode any stream from a container using the appropriate codec
2. Re-encode it with a different codec
3. Re-wrap it into a different container
4. Filter/process it in between (resize, trim, merge, etc.)

``` 
General pipeline

[Input File] → Demux → Decode → Filter → Encode → Mux → [Output File]

```

- Demux = unpack streams from the container
- Decode = decompress the raw data
- Filter = optional processing (resize, crop, etc.)
- Encode = recompress with a new codec
- Mux = pack into the new container

## How other services like PornHub, Netflix, YouTube etc use this?

1. FIle gets decoded
2. Re-encode into different version -> Different resolutions 
3. Served adaptively based on the connection speed.

this is called  **ABR** — Adaptive Bitrate Streaming

# Starting the main Course: `ffprobe` 

- Before converting or compressing what you do?
    - Inspecting
    - We need to inspect the file we are working with 

```bash 
ffprobe recording_2026-04-29_23.53.40.mp4

Input #0, mov,mp4,m4a,3gp,3g2,mj2, from 'recording_2026-04-29_23.53.40.mp4':
  Metadata:
    major_brand     : isom
    minor_version   : 512
    compatible_brands: isomiso2avc1mp41
    encoder         : Lavf62.12.100
  Duration: 00:00:53.33, start: 0.000000, bitrate: 13503 kb/s
  Stream #0:0[0x1](und): Video: h264 (High) (avc1 / 0x31637661), yuv420p(progressive), 2560x1600, 13477 kb/s, 39.41 fps, 330 tbr, 90k tbn (default)
    Metadata:
      handler_name    : VideoHandler
  Stream #0:1[0x2](und): Audio: aac (LC) (mp4a / 0x6134706D), 48000 Hz, stereo, fltp, 41 kb/s (default)
    Metadata:
      handler_name    : SoundHandler

``` 

- The actual output will be a bit larger as it will also include the `ffprobe` information like the compilation flags, build, version
- Focus on line `Input #0, mov,mp4,m4a,3gp,3g2,mj2, from 'recording_2026-04-29_23.53.40.mp4':`
    - `#0` this means this is the first input file (it also supports multiple files) shown by `#1 #2 #3`
    - the `mov ....` it is just the container family :- QuickTime/MP4 family.

```bash 
major_brand     : isom
minor_version   : 512
compatible_brands: isomiso2avc1mp41
encoder         : Lavf62.12.100
``` 
- isom — ISO Base Media file format, the spec .mp4 is built on. 
- compatible_brands: isomiso2avc1mp41 — the file declares compatibility with isom, iso2, avc1 (H.264), and mp41 (MP4 version 1)
- encoder: Lavf62.12.100 — written by FFmpeg's libavformat, version 62.12.100

- `Duration: 00:00:53.33, start: 0.000000, bitrate: 13503 kb/s`  
    - Duration :- 53sec,33 milliseconds    
    - bitrate: 13503 kb/s — total bitrate, video + audio combined. ~13.5 Mbps for 53 seconds.

`Stream #0:0[0x1](und): Video: h264 (High) (avc1 / 0x31637661), yuv420p(progressive), 2560x1600, 13477 kb/s, 39.41 fps, 330 tbr, 90k tbn (default)`      
- Stream `#0`: 0 — file 0, stream 0 (first stream)
- `[0x1]` — internal stream ID in the container, hexadecimal
- `(und)` — language tag is undefined (not set).
- `h264 (High)` — H.264 codec, High profile. H.264 has profiles: Baseline → Main → High → High 10 etc. High is standard for good quality encodes
`(avc1 / 0x31637661)` — the FourCC code. Every codec has a 4-character identifier baked into the container. avc1 is H.264's FourCC. The hex is just the same thing in bytes
`yuv420p(progressive)` — color space + scan type. Progressive means full frames, as opposed to interlaced (where frames are split into alternating lines, a relic of old broadcast TV)
`2560x1600` — your exact monitor resolution
`13477 kb/s` — video stream bitrate specifically
`39.41 fps` — fps 
`330 tbr` — timebase rate, the internal clock resolution FFmpeg uses to timestamp frames. You don't need to worry about this
`90k tbn` — ticks per second of the container's internal timestamp unit. MP4 uses 90,000 ticks/second as its standard. Again, internal bookkeeping
`(default)` — this is the default stream that will play if you don't specify otherwise

`Stream #0:1[0x2](und): Audio: aac (LC) (mp4a / 0x6134706D), 48000 Hz, stereo, fltp, 41 kb/s (default)` 
- `Stream #0`:1 — file 0, stream 1 (second stream)
- `aac (LC)` — AAC codec, Low Complexity profile. This is the standard AAC variant used everywhere
- `mp4a / 0x6134706D` — FourCC for AAC audio in MP4
- `48000 Hz` — 48,000 samples per second. Standard for video audio (as opposed to 44,100 Hz which is CD/music standard)
- `stereo` — 2 channels
- `fltp` — float planar — this is the internal sample format FFmpeg uses in memory when decoding. Not a property of the file itself, just how FFmpeg holds it internally
- `41 kb/s` — very low audio bitrate
