import os
import sys
from gtts import gTTS

# --- Configuration ---
TEXT_FILE = "testTTS.txt"
LANGUAGE = 'ro' # 'ro' is the code for Romanian
TEMP_AUDIO_FILE = "temp_speech.mp3"
# --- End Configuration ---

def read_text_from_file(filename):
    """Reads the text content from a file, ensuring UTF-8 encoding."""
    try:    
        # We must use 'utf-8' encoding to correctly read Romanian characters
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"ERROR: File '{filename}' not found.")
        print("Please create a testTTS.txt file in the same directory.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)

def speak_text(text, language):
    """Generates speech using gTTS and plays it with mpg123."""
    if not text or text.isspace():
        print("The text file is empty. Nothing to read.")
        return

    try:
        print("Generating speech... (requires internet)")
        # Create the TTS object
        tts = gTTS(text=text, lang=language, slow=False)
        
        # Save the audio to a temporary file
        tts.save(TEMP_AUDIO_FILE)
        
        print("Playing audio...")
        # Play the audio file using mpg123 (a common Linux audio player)
        # The ' -q' flag makes it "quiet" (suppresses terminal output)
        os.system(f"mpg123 -q {TEMP_AUDIO_FILE}")

    except Exception as e:
        print(f"An error occurred during TTS generation or playback: {e}")
        print("Make sure you have an internet connection.")
        print("Make sure 'mpg123' is installed (sudo apt-get install mpg123)")

    finally:
        # Clean up the temporary file, even if an error occurred
        if os.path.exists(TEMP_AUDIO_FILE):
            os.remove(TEMP_AUDIO_FILE)

# --- Main execution ---
if __name__ == "__main__":
    text_to_read = read_text_from_file(TEXT_FILE)
    speak_text(text_to_read, LANGUAGE)
