# AI Video Automation Bot 🎬

A local persistent video generation engine that creates 9:16 short-form videos from a text topic. It features two 2D avatars that discuss the topic using script generation, text-to-speech, and dynamic video composition.

### Static Assets, Dynamic Code.

## 🚀 Key Features

- **Automated Scriptwriting**: Uses Google Gemini API to generate engaging dialogue.
- **Natural TTS**: Uses Microsoft Edge TTS for realistic voice generation.
- **Dynamic Visuals**: 
  - **2D Avatar Puppetry**: Text-driven image swapping (Idle vs. Talking states).
  - **Smart Captions**: Sentence-level synced subtitles that appear dynamically above speakers.
  - **Auto-Layout**: Intelligently positions assets for 9:16 vertical video.
- **Highly Configurable**: Control fonts, colors, positions, speeds, and backgrounds via `config.py`.

## 🛠️ Installation

### Prerequisites
1. **Python 3.10+**
2. **FFmpeg**: Required for video processing.
   - Windows: `winget install ffmpeg`
3. **ImageMagick**: Required for text rendering.
   - [Download Installer](https://imagemagick.org/script/download.php#windows)
   - **Important**: During installation, check "Install legacy utilities (e.g. convert)".

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/video-automation-bot.git
   cd video-automation-bot
   ```
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your Environment Variables:
   - Rename `.env.example` to `.env`.
   - Add your Google Gemini API Key: `GEMINI_API_KEY=your_key_here`.

## 🏃 Usage

Generate a video by providing a topic:
```bash
python main.py --topic "The Fermi Paradox"
```
The final video will be saved in the `output/` folder.

## ⚙️ Configuration (`config.py`)

You can fully customize the video style in `config.py`:

| Setting | Description |
| :--- | :--- |
| **Avatars** | |
| `AVATAR_1_POS` / `2_POS` | (x, y) coordinates for the avatars. |
| `AVATAR_WIDTH` | Width of the avatars in pixels. |
| **Captions** | |
| `CAPTION_SETTINGS` | Dictionary for Font, Size, Color, and Position logic. |
| `VOICE_RATE` | Playback speed (e.g., `"+10%"` for faster speech). |
| `SCRIPT_WORD_COUNT` | Target word count (Default: 140). Reduces total time. |
| **Background** | |
| `BACKGROUND_SETTINGS` | Set `"color": "#hex"` for solid color or `None` to use images in `assets/backgrounds`. |

## 📂 Project Structure

```text
video-automation-bot/
├── assets/             # Images and local resources
│   ├── backgrounds/    # Add .png/.jpg files here
│   ├── avatar_1/       # idle.png, talk.png
│   └── avatar_2/       # idle.png, talk.png
├── output/             # Generated videos
├── temp/               # Intermediate audio/script files
├── config.py           # Central configuration file
├── main.py             # Entry point
├── screenwriter.py     # Gemini AI Script Generation
├── voice_synthesizer.py# Edge-TTS Audio Generation
└── video_engine.py     # MoviePy Video Composition
```

## 🧩 Architecture

1.  **Script Generation**: `screenwriter.py` prompts Gemini to create a dialogue script in JSON format.
2.  **Audio Synthesis**: `voice_synthesizer.py` generates audio files for each line using Edge-TTS and captures **sentence-level timestamps**.
3.  **Video Composition**: `video_engine.py` assembles the video:
    - Background layer (Image or Hex Color).
    - Avatar layer (Swaps 'idle' vs 'talk' images based on active speaker).
    - Caption layer (Generates text clips synced to the specific sentence timings).
4.  **Rendering**: The final composition is written to `.mp4` using FFmpeg.
