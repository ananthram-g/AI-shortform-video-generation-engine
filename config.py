import os

# API Keys
# SECURITY WARNING: Do not hardcode your API key here. Use environment variables.
# You can set this in your terminal or use a .env file (recommended).
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") 

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not found. Please set it before running.")

# Voice Settings
# Avatar 1: Host (Deep, authoritative)
AVATAR_1_VOICE = "en-US-ChristopherNeural"

# Avatar 2: Guest/Skeptic (Higher pitch, fast)
AVATAR_2_VOICE = "en-US-AnaNeural"

# Voice Speed (e.g., "+0%", "+10%", "-5%")
VOICE_RATE = "+25%"#"+0%"

# Script Generation
# Target word count for the dialogue. 
# ~140 words is approx 60 seconds at normal speed.
SCRIPT_WORD_COUNT = 240

# Video Settings
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
FPS = 24

# ImageMagick Path (Required for subtitles)
# Update this path if ImageMagick is installed elsewhere on your system.
IMAGEMAGICK_BINARY = r"C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe"

# ---------------------------------------------------------
# VISUAL CONFIGURATION
# ---------------------------------------------------------

# Avatars
AVATAR_WIDTH = 500
# Format: (x, y)
AVATAR_1_POS = (50, 600)
AVATAR_2_POS = (530, 650)

# Captions
CAPTION_SETTINGS = {
    "font": "Comic-Sans-MS",
    "fontsize": 70,
    "color": "#191970", # Navy Blue
    "stroke_color": None,
    "stroke_width": 0,
    "highlight_color": None,
    "size": (500, None), # Width limit
    "chunk_size": 4, # Words per chunk
    # Positions (Above heads)
    "pos_avatar_1": (50, 355),
    "pos_avatar_2": (530, 405)
}

# Background
# If "color" is set (e.g., "#000000"), it overrides any image found in assets/backgrounds.
# Set to None to use images from assets/backgrounds.
BACKGROUND_SETTINGS = {
    "color": None, # e.g. "#FF0000" for Red. None = Use Image.
    "default_color": (50, 50, 50) # Fallback if no image and no color set
}
