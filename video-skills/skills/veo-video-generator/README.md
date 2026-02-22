# Veo Video Generator Skill for OpenClaw

An OpenClaw skill that uses **Google Veo 3.1** to generate cinematic 1080p/4K videos with natively synchronized audio and sound effects.

[![ClawHub Verified](https://img.shields.io/badge/ClawdHub-Verified-brightgreen)](https://clawdhub.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- **Native Audio:** Generates background music and SFX synced to the video.
- **Fast Rendering:** Uses `veo-3.1-fast-generate-preview` for < 60s turnaround.
- **Mobile Ready:** Default 9:16 aspect ratio for social media agents.
- **Standalone:** No complex dependencies; runs on native Node.js.

## Installation

### 1. Local Setup

Clone this into your OpenClaw `skills` directory:

```bash
git clone
cd veo-video-gen
npm install
```

Or ask your agent to [download the skill directly from ClawHub](https://clawhub.ai/kghamilton89/veo-video-generator).

### 2. Configure Credentials

Provide your [Gemini API key](https://aistudio.google.com/api-keys).

## Usage

After installing this skill from [ClawHub](https://clawhub.ai/kghamilton89/veo-video-generator) simply ask your agent: "Generate a video of a calm forest with birds chirping using Veo."

## Metadata (SKILL.md)

This skill defines its requirements in `SKILL.md` using the `metadata.clawdbot` schema:

- Language: Node.js (v20+)
- Environment: GEMINI_API_KEY
- Output: .mp4 (saved to workspace root)

## License

MIT © 2026
