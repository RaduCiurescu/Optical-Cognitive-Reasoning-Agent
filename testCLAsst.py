import speech_recognition as sr
import wave
import time
import os
from datetime import datetime

def record_5_seconds():
    print("🎤 5-Second Audio Recorder")
    print("=" * 30)
    
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    
    # Find and configure your Sennheiser microphone
    mic_list = sr.Microphone.list_microphone_names()
    sennheiser_index = None
    
    for i, name in enumerate(mic_list):
        if "sennheiser" in name.lower():
            sennheiser_index = i
            microphone = sr.Microphone(device_index=i)
            print(f"✅ Using Sennheiser microphone at index {i}")
            break
    
    if sennheiser_index is None:
        print("🎧 Using default microphone")
    
    while True:
        print(f"\n📋 Options:")
        print("  1 - Record 5 seconds")
        print("  q - Quit")
        
        choice = input("Enter choice: ").strip().lower()
        
        if choice == "1":
            try:
                print("\n🔴 Recording in 3 seconds...")
                time.sleep(1)
                print("2...")
                time.sleep(1) 
                print("1...")
                time.sleep(1)
                print("🎙️ RECORDING NOW - Speak for 5 seconds!")
                
                with microphone as source:
                    # Quick noise adjustment
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    
                    # Record for exactly 5 seconds
                    audio = recognizer.listen(source, phrase_time_limit=15)
                
                # Create filename with timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"recording_{timestamp}.wav"
                
                # Save audio to WAV file
                with open(filename, "wb") as f:
                    f.write(audio.get_wav_data())
                
                print(f"✅ Recording saved as: {filename}")
                print(f"📁 File size: {os.path.getsize(filename)} bytes")
                
                # Optional: Try to transcribe it
                try:
                    text = recognizer.recognize_google(audio, language='ro-RO')
                    print(f"📝 Transcription (Romanian): {text}")
                    
                    # Save transcription too
                    text_filename = f"transcription_{timestamp}.txt"
                    with open(text_filename, "w", encoding="utf-8") as f:
                        f.write(f"Recording: {filename}\n")
                        f.write(f"Transcription: {text}\n")
                    
                    print(f"💾 Transcription saved as: {text_filename}")
                    
                except sr.UnknownValueError:
                    print("🤷 Could not transcribe audio")
                except Exception as e:
                    print(f"⚠️ Transcription error: {e}")
                
            except Exception as e:
                print(f"❌ Recording failed: {e}")
                
        elif choice == "q":
            print("👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid choice. Press 1 to record or q to quit.")

if __name__ == "__main__":
    record_5_seconds()