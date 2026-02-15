import google.generativeai as genai
import json
import config

def generate_script(topic):
    """
    Generates a dialogue script between two avatars based on the given topic using Gemini.
    """
    if not config.GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not set in config.py or environment variables.")

    genai.configure(api_key=config.GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-flash-latest') # Using standard flash model

    prompt = f"""
    You are a screenwriter for a short-form vertical video.
    Create a dialogue script between two characters discussing the topic: "{topic}".
    
    Roles:
    - avatar_1: The Host (Expert, authoritative).
    - avatar_2: The Guest/Skeptic (Curious, skeptical, or novice).

    Constraints:
    - Total word count must be approx {config.SCRIPT_WORD_COUNT} words.
    - The dialogue should be engaging and punchy.
    - Output MUST be a valid JSON array.

    Output Schema:
    [
      {{
        "id": "avatar_1" or "avatar_2",
        "text": "The spoken dialogue line here.",
        "mood": "neutral" | "excited" | "skeptical" | "happy" (optional context)
      }},
      ...
    ]
    
    Return ONLY the JSON. No markdown formatting.
    """

    try:
        response = model.generate_content(prompt)
        text_response = response.text.strip()
        
        # Cleanup if model adds markdown code blocks
        if text_response.startswith("```json"):
            text_response = text_response[7:]
        if text_response.startswith("```"):
             text_response = text_response[3:]
        if text_response.endswith("```"):
            text_response = text_response[:-3]
            
        script_data = json.loads(text_response)
        return script_data

    except Exception as e:
        print(f"Error generating script: {e}")
        # if hasattr(e, 'response'):
        #     print(e.response)
        return None

if __name__ == "__main__":
    # Test
    print(generate_script("Why is the sky blue?"))
