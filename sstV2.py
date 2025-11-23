import pyaudio
import wave
import time

def record_with_pyaudio(duration=5):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    
    p = pyaudio.PyAudio()
    
    # Find your Sennheiser microphone
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        if "sennheiser" in info['name'].lower():
            device_index = i
            print(f"Using: {info['name']}")
            break
    else:
        device_index = None  # Use default
    
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    input_device_index=device_index,
                    frames_per_buffer=CHUNK)
    
    print(f"Recording for {duration} seconds...")
    frames = []
    
    for i in range(0, int(RATE / CHUNK * duration)):
        data = stream.read(CHUNK)
        frames.append(data)
    
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    # Save as WAV
    wf = wave.open('pyaudio_recording.wav', 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    
    print("Recording saved!")

# Install: pip install pyaudio
record_with_pyaudio(5)