import sounddevice as sd
import soundfile as sf
import numpy as np

def record_with_sounddevice():
    # List available devices
    print("Available devices:")
    print(sd.query_devices())
    
    # Find Sennheiser device
    devices = sd.query_devices()
    sennheiser_device = None
    
    for i, device in enumerate(devices):
        if "sennheiser" in device['name'].lower():
            sennheiser_device = i
            print(f"Using device {i}: {device['name']}")
            break
    
    # Record 5 seconds
    duration = 5
    sample_rate = 16000
    
    print(f"Recording for {duration} seconds...")
    recording = sd.rec(int(duration * sample_rate), 
                      samplerate=sample_rate, 
                      channels=1,
                      device=sennheiser_device)
    sd.wait()  # Wait until recording is finished
    
    # Save as WAV
    sf.write('sounddevice_recording.wav', recording, sample_rate)
    print("Recording saved!")

# Install: pip install sounddevice soundfile
record_with_sounddevice()