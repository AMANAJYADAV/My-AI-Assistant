import sys
import time
import subprocess
import webbrowser
import pyautogui

def veronica_advanced_autopilot(action, payload):
    pyautogui.FAILSAFE = True
    clean_payload = payload.strip()

    #ACTION 1: Pipeline and Chat Authentication
    if action == "chat":
        print(f"SYSTEM_CHECK: [Listening: ONLINE] -> [Perception/Eyes: ONLINE] -> [Autopilot/Hands: READY].")
        print(f"VERONICA: Test sequence accepted. Transmission payload: '{clean_payload}'")

    #ACTION 2: Smart Opener
    elif action in ["site", "app", "open"]:
        known_apps = ["notepad", "calc", "calculator", "mspaint", "paint", "cmd", "powershell", "explorer", "taskmgr"]
        payload_lower = clean_payload.lower().strip()
        
        is_app = False
        if action == "app":
            is_app = True
        elif action == "site":
            is_app = False
        else: 
            if payload_lower in known_apps or ":" in payload_lower or "\\" in payload_lower:
                is_app = True
            else:
                is_app = False

        if is_app:
            try:
                subprocess.Popen(f'start "" "{clean_payload}"', shell=True)
                print(f"DONE: Dynamically launched system program: {clean_payload}")
            except Exception as e:
                print(f"ERROR: System could not resolve or launch '{clean_payload}': {e}")
        else:
            if "." not in clean_payload:
                url = f"https://www.{payload_lower.replace(' ', '')}.com"
            else:
                url = clean_payload if payload_lower.startswith("http") else f"https://{clean_payload}"
            
            try:
                subprocess.Popen(f'start chrome "{url}"', shell=True)
                print(f"DONE: Forced Google Chrome to open link -> {url}")
            except Exception as e:
                webbrowser.open(url)
                print(f"DONE: Opened generic browser link -> {url}")

    #ACTION 4: Text Typing
    elif action == "type":
        print("Veronica: You have 2 seconds to click the active window...")
        time.sleep(2) 
        pyautogui.write(clean_payload, interval=0.05)
        print("DONE: Text payload has been typed successfully.")
        print("STATUS: Application kept open. System entering IDLE state, waiting for next voice trigger...")

    #ACTION 5: Mouse Controller
    elif action == "click":
        try:
            if clean_payload and "," in clean_payload:
                x, y = map(int, clean_payload.split(","))
                pyautogui.click(x, y)
                print(f"DONE: Clicked at coordinates {x}, {y}")
            else:
                pyautogui.click()
                print("DONE: Clicked current cursor position")
        except Exception as e:
            print(f"ERROR: Click operation failed: {e}")

    #ACTION 6: Mouse Movement
    elif action == "move":
        try:
            x, y = map(int, clean_payload.split(","))
            pyautogui.moveTo(x, y, duration=0.3)
            print(f"DONE: Moved mouse cursor to {x}, {y}")
        except Exception as e:
            print(f"ERROR: Mouse movement failed: {e}")
            
    else:
        print(f"ERROR: Action '{action}' unrecognized by Veronica Autopilot.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("ERROR: Missing arguments. Usage: autopilot.py <action> <payload>")
        sys.exit(1)
        
    action_arg = sys.argv[1].lower().strip()
 
    payload_arguments = sys.argv[2:]
    if payload_arguments and payload_arguments[-1] == "ALLOWED":
        payload_arguments = payload_arguments[:-1]
        
    final_payload = " ".join(payload_arguments).strip()
    
    if final_payload.startswith('"') and final_payload.endswith('"'):
        final_payload = final_payload[1:-1]
        
    veronica_advanced_autopilot(action_arg, final_payload)