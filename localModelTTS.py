import os
import sys
import subprocess
from piper import PiperVoice

# --- Configuration ---
TEXT_FILE = "testTTS.txt"
# Vom salva direct ca .mp3
SAVED_AUDIO_FILE = "saved_speech_piper.mp3" 
# Vom folosi un fisier .wav temporar
TEMP_WAV_FILE = "temp_speech.wav" 

# --- IMPORTANT ---
# This script assumes you have ALREADY downloaded the model files
# and placed them in the same directory as this script.
MODEL_PATH = './ro_RO-mihai-medium.onnx'
MODEL_CONFIG_PATH = './ro_RO-mihai-medium.onnx.json'
# --- End Configuration ---

def check_dependencies():
    """Checks if ffmpeg and mpg123 are installed."""
    print("Checking dependencies (ffmpeg, mpg123)...")
    try:
        # Verificam ffmpeg
        subprocess.run(["ffmpeg", "-version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("ERROR: 'ffmpeg' is not installed or not in PATH.")
        print("Please run: sudo apt-get install ffmpeg")
        sys.exit(1)
    
    print("Dependencies OK.")

def check_model_files():
    """Checks if the required model files exist."""
    if not os.path.exists(MODEL_PATH) or not os.path.exists(MODEL_CONFIG_PATH):
        print("ERROR: Piper model files not found.")
        print(f"Make sure '{MODEL_PATH}' and '{MODEL_CONFIG_PATH}'")
        print("are in the same directory as this script.")
        print("You can download them from:")
        print("https://huggingface.co/rhasspy/piper-voices/tree/main/ro/ro-RO/mihai/medium")
        sys.exit(1)
    else:
        # Files are found, we can proceed.
        print("Piper model files found. Proceeding...")

def read_text_from_file(filename):
    """Reads the text content from a file, ensuring UTF-8 encoding."""
    try:    
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"ERROR: File '{filename}' not found.")
        print("Please create a testTTS.txt file in the same directory.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)

def speak_text_piper(text, voice):
    """Generates speech, converts to MP3, and plays it."""
    if not text or text.isspace():
        print("The text file is empty. Nothing to read.")
        return

    try:
        print("Initializing Piper voice... (this may take a moment)")
        
        print("Generating speech (offline) to WAV...")
        with open(TEMP_WAV_FILE, "wb") as wav_file:
            # Synthesize speech and write to the temporary WAV file
            voice.synthesize(text, wav_file)
        
        # --- DEBUGGING ---
        # Verificam daca fisierul .wav a fost creat corect
        if not os.path.exists(TEMP_WAV_FILE) or os.path.getsize(TEMP_WAV_FILE) == 0:
            print(f"CRITICAL ERROR: Failed to create {TEMP_WAV_FILE}. File is missing or 0 bytes.")
            print("This indicates a problem with voice.synthesize().")
            sys.exit(1)
        else:
            print(f"DEBUG: {TEMP_WAV_FILE} created, size: {os.path.getsize(TEMP_WAV_FILE)} bytes.")
        # --- END DEBUGGING ---

        print(f"Converting WAV to MP3: {SAVED_AUDIO_FILE}...")
        # Folosim ffmpeg pentru a converti WAV in MP3
        # Am scos '-loglevel quiet' pentru a vedea erorile!
        subprocess.run([
            "ffmpeg", 
            "-i", TEMP_WAV_FILE, 
            "-q:a", "4", 
            SAVED_AUDIO_FILE, 
            "-y"
        ])
        
        # --- DEBUGGING ---
        # Verificam fisierul final .mp3
        if not os.path.exists(SAVED_AUDIO_FILE) or os.path.getsize(SAVED_AUDIO_FILE) < 100: # 100 bytes e o limita de siguranta
            print(f"CRITICAL ERROR: Failed to convert to {SAVED_AUDIO_FILE}. File is missing or 0 bytes.")
            print("Please check the 'ffmpeg' output above for errors.")
            sys.exit(1)
        # --- END DEBUGGING ---

        print("Playing audio (MP3)...")
        # Folosim 'mpg123' pentru a reda fisierul MP3
        subprocess.run(["mpg123", "-q", SAVED_AUDIO_FILE])

        print(f"\nSuccess! Audio saved to {SAVED_AUDIO_FILE}")

    except FileNotFoundError as e:
        if "ffmpeg" in str(e) or "mpg123" in str(e):
            print(f"ERROR: '{e.filename}' not found.")
            print("You must install 'ffmpeg' and 'mpg123' to convert and play MP3s.")
            print("Run: sudo apt-get install ffmpeg mpg123")
        else:
            print(f"An error occurred: {e}")
    except Exception as e:
        print(f"An error occurred during TTS synthesis or playback: {e}")
    # finally:
    #     # Am comentat stergerea pentru a putea depana
    #     print(f"DEBUG: Keeping {TEMP_WAV_FILE} for inspection.")
    #     # if os.path.exists(TEMP_WAV_FILE):
    #     #     os.remove(TEMP_WAV_FILE)

# --- Main execution ---
if __name__ == "__main__":
    # 1. Check if the files exist
    check_model_files()
    
    # 1b. Check dependencies
    check_dependencies()

    # 2. Read the text
    text_to_read = read_text_from_file(TEXT_FILE)
    
    # 3. Load the Piper voice model
    print("Loading voice model...")
    voice = PiperVoice.load(MODEL_PATH, config_path=MODEL_CONFIG_PATH)
    
    # 4. Speak the text
    speak_text_piper(text_to_read, voice)
