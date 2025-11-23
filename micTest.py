import speech_recognition as sr
import warnings
warnings.filterwarnings("ignore")

r = sr.Recognizer()

# Find your Sennheiser microphone
mics = sr.Microphone.list_microphone_names()
for i, name in enumerate(mics):
    if "sennheiser" in name.lower():
        print(f"Using Sennheiser at index {i}")
        mic = sr.Microphone(device_index=i)
        break
else:
    mic = sr.Microphone()

print("Speak into your headset...")
with mic as source:
    r.adjust_for_ambient_noise(source)
    audio = r.listen(source, timeout=10)

try:
    text = r.recognize_google(audio)
    print(f"You said: {text}")
    with open("mic.txt", "w") as f:
        f.write(text)
    print("✅ Saved to mic.txt")
except Exception as e:
    print(f"Error: {e}")
    with open("mic.txt", "w") as f:
        f.write(f"Error: {e}")