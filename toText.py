import speech_recognition as sr
import os
import glob
from datetime import datetime

def transcribe_wav_to_text():
    print("🎵 WAV to Text Transcriber")
    print("=" * 30)
    
    # Find all WAV files in current directory
    wav_files = glob.glob("*.wav")
    recording_files = [f for f in wav_files if f.startswith("recording_") or f.startswith("audio_")]
    
    if not wav_files:
        print("❌ No WAV files found in current directory")
        return
    
    print("📁 Available WAV files:")
    for i, file in enumerate(wav_files, 1):
        size = os.path.getsize(file)
        print(f"  {i}. {file} ({size} bytes)")
    
    # Auto-select if there's a recent recording, or ask user to choose
    if recording_files:
        # Use the most recent recording file
        latest_file = max(recording_files, key=os.path.getctime)
        print(f"\n🎯 Auto-selected latest recording: {latest_file}")
        selected_file = latest_file
    else:
        try:
            choice = int(input(f"\nSelect file (1-{len(wav_files)}): "))
            selected_file = wav_files[choice - 1]
        except (ValueError, IndexError):
            print("❌ Invalid selection")
            return
    
    # Transcribe the selected file
    transcribe_file(selected_file)

def transcribe_file(wav_filename):
    try:
        print(f"\n🔤 Transcribing: {wav_filename}")
        
        recognizer = sr.Recognizer()
        
        with sr.AudioFile(wav_filename) as source:
            print("📁 Loading audio file...")
            audio = recognizer.record(source)
            print(f"✅ Audio loaded successfully")
        
        # Try Romanian first, then English as fallback
        languages = [('ro-RO', 'Romanian'), ('en-US', 'English')]
        
        for lang_code, lang_name in languages:
            try:
                print(f"🌐 Trying {lang_name} transcription...")
                text = recognizer.recognize_google(audio, language=lang_code)
                
                if text.strip():  # If we got some text
                    print(f"✅ {lang_name} transcription successful!")
                    print(f"📝 Text: {text}")
                    
                    # Create output filename
                    base_name = os.path.splitext(wav_filename)[0]
                    text_filename = f"{base_name}_transcription.txt"
                    
                    # Save transcription
                    with open(text_filename, "w", encoding="utf-8") as f:
                        f.write(f"Audio Transcription\n")
                        f.write(f"=" * 20 + "\n\n")
                        f.write(f"Source file: {wav_filename}\n")
                        f.write(f"Language: {lang_name} ({lang_code})\n")
                        f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                        f.write(f"\nTranscription:\n")
                        f.write(f"{text}\n")
                    
                    print(f"💾 Transcription saved to: {text_filename}")
                    return
                    
            except sr.UnknownValueError:
                print(f"⚠️ Could not understand {lang_name} audio")
                continue
            except sr.RequestError as e:
                print(f"❌ {lang_name} recognition service error: {e}")
                continue
        
        # If all languages failed
        print("❌ Could not transcribe audio in any language")
        
        # Save error message
        base_name = os.path.splitext(wav_filename)[0]
        text_filename = f"{base_name}_transcription.txt"
        
        with open(text_filename, "w", encoding="utf-8") as f:
            f.write(f"Audio Transcription - FAILED\n")
            f.write(f"=" * 30 + "\n\n")
            f.write(f"Source file: {wav_filename}\n")
            f.write(f"Error: Could not transcribe audio content\n")
            f.write(f"Possible reasons:\n")
            f.write(f"- Audio quality too low\n")
            f.write(f"- Speech not clear enough\n")
            f.write(f"- Language not supported\n")
        
        print(f"📝 Error log saved to: {text_filename}")
        
    except FileNotFoundError:
        print(f"❌ File not found: {wav_filename}")
    except Exception as e:
        print(f"❌ Error processing file: {e}")

def transcribe_specific_file():
    """Quick function to transcribe a specific file"""
    filename = input("Enter WAV filename: ").strip()
    
    if not filename.endswith('.wav'):
        filename += '.wav'
    
    if os.path.exists(filename):
        transcribe_file(filename)
    else:
        print(f"❌ File not found: {filename}")

if __name__ == "__main__":
    print("🎤 Choose transcription mode:")
    print("1. Auto-detect and transcribe WAV files")
    print("2. Specify a WAV file to transcribe")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        transcribe_wav_to_text()
    elif choice == "2":
        transcribe_specific_file()
    else:
        print("❌ Invalid choice")