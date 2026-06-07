import sys
import os
import io
import base64
import pyautogui
from groq import Groq

def capture_and_locate(mode, target_element):
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("ERROR: GROQ_API_KEY environment variable is not set.")
        return

    try:
        width, height = pyautogui.size()
        screenshot = pyautogui.screenshot()
        img_byte_arr = io.BytesIO()
      
        screenshot.convert('RGB').save(img_byte_arr, format='JPEG', quality=70)
        img_bytes = img_byte_arr.getvalue()
        
        base64_image = base64.b64encode(img_bytes).decode('utf-8')
        
        client = Groq(api_key=api_key)
        
        system_prompt = (
            f"You are the visual coordinate locator for a desktop automation pipeline. Screen size: {width}x{height}.\n"
            "Analyze the layout stream and find the target button, text, or region the user specifies.\n"
            "Calculate the exact central X,Y click coordinate for that element.\n"
            "CRITICAL: Output ONLY the raw numbers separated by a comma (e.g., 520,380). Do not include words or markdown text."
        )
        
        user_prompt = f"Target UI Element: {target_element} | Scan Mode: {mode}"
        
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": user_prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            model="llama-3.2-11b-vision-preview",
            temperature=0.0  # Zero randomness for high coordination accuracy
        )
        
        coordinate_output = chat_completion.choices[0].message.content.strip()
        print(coordinate_output)
        
    except Exception as e:
        print(f"ERROR: Perception runtime issue: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("ERROR: Missing arguments. Usage: veronica_perception.py <mode> <target>")
        sys.exit(1)
        
    mode_arg = sys.argv[1].lower().strip()
    target_arg = sys.argv[2]
    
    capture_and_locate(mode_arg, target_arg)