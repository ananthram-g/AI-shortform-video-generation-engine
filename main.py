import argparse
import sys
import os

# Fix for Winget FFmpeg on Windows not being in global PATH for Python immediately
ffmpeg_path = os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WinGet\Links\ffmpeg.exe")
if os.path.exists(ffmpeg_path):
    os.environ["IMAGEIO_FFMPEG_EXE"] = ffmpeg_path

import config
from screenwriter import generate_script
from voice_synthesizer import run_tts
from video_engine import create_video

def main():
    parser = argparse.ArgumentParser(description="AI Video Automation Bot")
    parser.add_argument("--topic", type=str, required=True, help="The topic for the video conversation.")
    args = parser.parse_args()

    print(f"🎬 Starting processing for topic: {args.topic}")

    # Step 1: Generate Script
    print("📝 Generating Script with Gemini...")
    script_data = generate_script(args.topic)
    if not script_data:
        print("❌ Failed to generate script. Exiting.")
        sys.exit(1)
    
    # Save script for debug
    with open("temp/script.json", "w") as f:
        import json
        json.dump(script_data, f, indent=2)
    print("✅ Script generated.")

    # Step 2: Generate Audio
    print("🗣️ Generating Audio...")
    audio_metadata = run_tts(script_data, output_dir="temp")
    if not audio_metadata:
         print("❌ Failed to generate audio. Exiting.")
         sys.exit(1)
    print(f"✅ Audio generated ({len(audio_metadata)} clips).")

    # Step 3: Create Video
    print("🎥 Rendering Video...")
    try:
        create_video(audio_metadata, output_filename="output/final_video.mp4")
        print("✅ Video rendering complete! Check output/final_video.mp4")
    except Exception as e:
        print(f"❌ Video rendering failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Ensure temp/output dirs exist
    os.makedirs("temp", exist_ok=True)
    os.makedirs("output", exist_ok=True)
    main()
