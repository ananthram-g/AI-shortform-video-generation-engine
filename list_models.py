import google.generativeai as genai
import config
import os

genai.configure(api_key=config.GEMINI_API_KEY)

try:
    with open("available_models.txt", "w") as f:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                f.write(f"{m.name}\n")
    print("Models written to available_models.txt")
except Exception as e:
    print(f"Error: {e}")
