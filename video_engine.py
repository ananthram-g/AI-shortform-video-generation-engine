

from moviepy.editor import *
from moviepy.config import change_settings
import config
import os

# Try to find ImageMagick if not in path (Common issue on Windows)
if os.path.exists(config.IMAGEMAGICK_BINARY):
    change_settings({"IMAGEMAGICK_BINARY": config.IMAGEMAGICK_BINARY})
else:
    print(f"Warning: ImageMagick not found at {config.IMAGEMAGICK_BINARY}. Subtitles might fail.")

def create_video(audio_metadata, output_filename="output/final_video.mp4"):
    """
    Composites the video based on audio metadata.
    """
    
    # Load Assets
    assets_dir = os.path.join(os.path.dirname(__file__), "assets")
    
    # Check if assets exist, else use placeholders or error
    avatar1_idle_path = os.path.join(assets_dir, "avatar_1", "idle.png")
    avatar1_talk_path = os.path.join(assets_dir, "avatar_1", "talk.png")
    avatar2_idle_path = os.path.join(assets_dir, "avatar_2", "idle.png")
    avatar2_talk_path = os.path.join(assets_dir, "avatar_2", "talk.png")
    
    # Validate assets existence (Optional: create dummy if missing for testing)
    for p in [avatar1_idle_path, avatar1_talk_path, avatar2_idle_path, avatar2_talk_path]:
        if not os.path.exists(p):
            print(f"Warning: Asset not found: {p}. Using color clip placeholders if possible or failing.")

    clips = []
    current_time = 0.0
    
    # Audio Clips List to concatenate later for the master track
    audio_clips = []

    # Iterate through generated audio segments
    for item in audio_metadata:
        file_path = item["file_path"]
        speaker = item["speaker"]
        text = item["text"]
        
        audio_clip = AudioFileClip(file_path)
        duration = audio_clip.duration
        audio_clips.append(audio_clip)

        # Create Video Segment for this duration
        # Background (can be static image or color for now)
        # 9:16 aspect ratio (1080x1920)
        
        # We process the scene for the duration of this audio clip
        # Speaker is talking, other is idle
        
        # Define Avatars
        # Format: (x, y)
        pos_1 = config.AVATAR_1_POS
        pos_2 = config.AVATAR_2_POS
        width = config.AVATAR_WIDTH
        
        # Determine images
        if speaker == "avatar_1":
            img1 = avatar1_talk_path if os.path.exists(avatar1_talk_path) else None
            img2 = avatar2_idle_path if os.path.exists(avatar2_idle_path) else None
        else:
            img1 = avatar1_idle_path if os.path.exists(avatar1_idle_path) else None
            img2 = avatar2_talk_path if os.path.exists(avatar2_talk_path) else None

        # Create ImageClips
        if img1 and os.path.exists(img1):
             clip_1 = ImageClip(img1).set_duration(duration).resize(width=width).set_position(pos_1)
        else:
             clip_1 = ColorClip(size=(300, 300), color=(255, 0, 0)).set_duration(duration).set_position(pos_1)

        if img2 and os.path.exists(img2):
             clip_2 = ImageClip(img2).set_duration(duration).resize(width=width).set_position(pos_2)
        else:
             clip_2 = ColorClip(size=(300, 300), color=(0, 0, 255)).set_duration(duration).set_position(pos_2)
        
        # Background
        bg_settings = config.BACKGROUND_SETTINGS
        bg_color_hex = bg_settings.get("color")
        
        def hex_to_rgb(hex_str):
            hex_str = hex_str.lstrip('#')
            return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))
        
        if bg_color_hex:
            # User specified a solid color
            try:
                rgb_color = hex_to_rgb(bg_color_hex)
                bg_clip = ColorClip(size=(config.VIDEO_WIDTH, config.VIDEO_HEIGHT), color=rgb_color).set_duration(duration)
            except Exception as e:
                print(f"Error parsing hex color {bg_color_hex}: {e}. using default.")
                bg_clip = ColorClip(size=(config.VIDEO_WIDTH, config.VIDEO_HEIGHT), color=(50,50,50)).set_duration(duration)
        else:
            # Attempt to load image from assets
            bg_dir = os.path.join(assets_dir, "backgrounds")
            bg_files = [f for f in os.listdir(bg_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))] if os.path.exists(bg_dir) else []
            
            if bg_files:
                bg_path = os.path.join(bg_dir, bg_files[0])
                bg_clip = ImageClip(bg_path).set_duration(duration)
                if bg_clip.w / bg_clip.h < config.VIDEO_WIDTH / config.VIDEO_HEIGHT:
                    bg_clip = bg_clip.resize(width=config.VIDEO_WIDTH)
                else:
                    bg_clip = bg_clip.resize(height=config.VIDEO_HEIGHT)
                bg_clip = bg_clip.set_position("center")
            else:
                # Fallback default color
                bg_clip = ColorClip(size=(config.VIDEO_WIDTH, config.VIDEO_HEIGHT), color=bg_settings.get("default_color", (50,50,50))).set_duration(duration)

        # Subtitles (Dynamic Positioning & Split Chunks with Sentence Sync)
        try:
            # Determine position
            cap_conf = config.CAPTION_SETTINGS
            if speaker == "avatar_1":
                txt_pos = cap_conf.get("pos_avatar_1", (50, 385))
            else:
                txt_pos = cap_conf.get("pos_avatar_2", (530, 435))

            text_clips = []
            
            # Check if we have sentence-level timing
            sentences = item.get("sentences", [])
            
            # Fallback if no sentences found (single block)
            if not sentences:
                sentences = [{"text": text, "start": 0.0, "end": duration}]

            for sent in sentences:
                sent_text = sent["text"]
                sent_start = sent["start"]
                sent_end = sent["end"]
                sent_duration = sent_end - sent_start
                
                # Split sentence into chunks
                words = sent_text.split()
                if not words: continue

                chunks = []
                chunk_size = cap_conf.get("chunk_size", 4)
                for i in range(0, len(words), chunk_size):
                    chunks.append(" ".join(words[i:i+chunk_size]))
                
                total_chars = len(sent_text.replace(" ", "")) if sent_text.strip() else 1
                current_chunk_time = sent_start
                
                for chunk in chunks:
                    chunk_chars = len(chunk.replace(" ", ""))
                    # Proportional duration within the sentence
                    chunk_duration = sent_duration * (chunk_chars / total_chars)
                    
                    txt_clip = TextClip(
                        chunk, 
                        fontsize=cap_conf.get("fontsize", 70), 
                        color=cap_conf.get("color", "white"), 
                        font=cap_conf.get("font", "Arial"), 
                        method='caption', 
                        size=cap_conf.get("size", (500, None)), 
                        align='center'
                    )
                    txt_clip = txt_clip.set_position(txt_pos).set_start(current_chunk_time).set_duration(chunk_duration)
                    text_clips.append(txt_clip)
                    current_chunk_time += chunk_duration
            
            combined = CompositeVideoClip([bg_clip, clip_1, clip_2] + text_clips)
        except Exception as e:
            print(f"Subtitle error: {e}")
            combined = CompositeVideoClip([bg_clip, clip_1, clip_2])

        combined = combined.set_start(current_time)
        clips.append(combined)
        
        current_time += duration

    # Background Music (Optional loop)
    # music_path = os.path.join(assets_dir, "music", "background.mp3")
    # ... logic to add background music ...

    # Final Composite
    final_video = CompositeVideoClip(clips)
    
    # Concatenate Audio
    final_audio = concatenate_audioclips(audio_clips)
    final_video = final_video.set_audio(final_audio)
    
    # Write File
    final_video.write_videofile(output_filename, fps=config.FPS, codec="libx264", audio_codec="aac")
    print(f"Video saved to {output_filename}")

if __name__ == "__main__":
    # Test stub
    pass
