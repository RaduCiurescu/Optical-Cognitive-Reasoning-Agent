import sounddevice as sd
import soundfile as sf
import os
from pathlib import Path

def inregistrare_intrebare():
    """
    Înregistrează 20 secunde și salvează în folder-ul Intrebari ca intrebareX.wav
    """
    
    # Creează folderul Intrebari dacă nu există
    folder_intrebari = Path("Intrebari")
    folder_intrebari.mkdir(exist_ok=True)
    
    # Găsește următorul număr pentru intrebare
    existing_files = list(folder_intrebari.glob("intrebare*.wav"))
    if existing_files:
        # Extrage numerele din numele fișierelor existente
        numbers = []
        for file in existing_files:
            try:
                # Extrage numărul din "intrebareX.wav"
                name = file.stem  # intrebareX
                number = int(name.replace("intrebare", ""))
                numbers.append(number)
            except ValueError:
                continue
        
        next_number = max(numbers) + 1 if numbers else 1
    else:
        next_number = 1
    
    filename = folder_intrebari / f"intrebare{next_number}.wav"
    
    try:
        # Găsește microfonul Sennheiser
        devices = sd.query_devices()
        sennheiser_device = None
        
        print("🔍 Căutare microfon Sennheiser...")
        for i, device in enumerate(devices):
            if "sennheiser" in device['name'].lower():
                sennheiser_device = i
                print(f"✅ Găsit: {device['name']}")
                break
        
        if sennheiser_device is None:
            print("⚠️ Nu s-a găsit microfonul Sennheiser. Se folosește microfonul implicit.")
        
        # Setări înregistrare
        duration = 20  # secunde
        sample_rate = 16000  # Hz
        channels = 1  # mono
        
        print(f"🔴 Înregistrare începe în 3 secunde...")
        print("3...")
        import time
        time.sleep(1)
        print("2...")
        time.sleep(1)
        print("1...")
        time.sleep(1)
        print(f"🎤 ÎNREGISTRARE - {duration} secunde!")
        
        # Înregistrează audio
        recording = sd.rec(
            int(duration * sample_rate),
            samplerate=sample_rate,
            channels=channels,
            device=sennheiser_device,
            dtype='int16'
        )
        
        # Așteaptă să se termine înregistrarea
        sd.wait()
        
        # Salvează ca WAV
        sf.write(filename, recording, sample_rate)
        
        print(f"✅ Înregistrarea salvată: {filename}")
        print(f"📊 Mărime fișier: {os.path.getsize(filename)} bytes")
        
        return str(filename)
        
    except Exception as e:
        print(f"❌ Eroare la înregistrare: {e}")
        return None

# Funcție cu opțiuni avansate
def inregistrare_intrebare_avansata(duration=20, sample_rate=16000):
    """
    Versiune avansată cu parametri personalizabili
    """
    
    folder_intrebari = Path("Intrebari")
    folder_intrebari.mkdir(exist_ok=True)
    
    # Găsește următorul număr
    existing_files = list(folder_intrebari.glob("intrebare*.wav"))
    next_number = 1
    
    if existing_files:
        numbers = []
        for file in existing_files:
            try:
                name = file.stem
                if name.startswith("intrebare"):
                    number_str = name[9:]  # după "intrebare"
                    if number_str.isdigit():
                        numbers.append(int(number_str))
            except:
                continue
        
        if numbers:
            next_number = max(numbers) + 1
    
    filename = folder_intrebari / f"intrebare{next_number}.wav"
    
    print(f"🎤 Pregătire înregistrare: {filename}")
    print(f"⏱️ Durată: {duration} secunde")
    print(f"🔊 Sample rate: {sample_rate} Hz")
    
    try:
        # Găsește device-ul audio
        devices = sd.query_devices()
        device_index = None
        
        for i, device in enumerate(devices):
            if "sennheiser" in device['name'].lower():
                device_index = i
                print(f"🎧 Microfon: {device['name']}")
                break
        
        # Countdown
        for i in range(3, 0, -1):
            print(f"{i}...")
            import time
            time.sleep(1)
        
        print("🔴 ÎNREGISTRARE ACTIVĂ!")
        
        # Înregistrare
        recording = sd.rec(
            int(duration * sample_rate),
            samplerate=sample_rate,
            channels=1,
            device=device_index,
            dtype='float32'
        )
        
        sd.wait()
        
        # Salvare
        sf.write(filename, recording, sample_rate)
        
        file_size = os.path.getsize(filename)
        print(f"✅ Succes! Salvat: {filename}")
        print(f"📁 Mărime: {file_size:,} bytes ({file_size/1024:.1f} KB)")
        
        return str(filename)
        
    except Exception as e:
        print(f"❌ Eroare: {e}")
        return None

# Funcție de test cu meniu
def test_inregistrare():
    """
    Funcție de test cu meniu interactiv
    """
    
    print("🎤 Test Înregistrare Întrebări")
    print("=" * 30)
    
    while True:
        print(f"\n📋 Opțiuni:")
        print("  1 - Înregistrare normală (20s)")
        print("  2 - Înregistrare personalizată")
        print("  3 - Listează înregistrările")
        print("  4 - Șterge toate înregistrările")
        print("  q - Ieșire")
        
        choice = input("Alege opțiunea: ").strip()
        
        if choice == "1":
            filename = inregistrare_intrebare()
            if filename:
                print(f"📝 Fișier creat: {filename}")
                
        elif choice == "2":
            try:
                duration = int(input("Durată (secunde): ") or "20")
                sample_rate = int(input("Sample rate (Hz): ") or "16000")
                filename = inregistrare_intrebare_avansata(duration, sample_rate)
                if filename:
                    print(f"📝 Fișier creat: {filename}")
            except ValueError:
                print("❌ Valori invalide!")
                
        elif choice == "3":
            folder = Path("Intrebari")
            if folder.exists():
                files = list(folder.glob("intrebare*.wav"))
                if files:
                    print(f"\n📂 Înregistrări găsite ({len(files)}):")
                    for file in sorted(files):
                        size = os.path.getsize(file)
                        print(f"  📄 {file.name} ({size:,} bytes)")
                else:
                    print("📭 Nu există înregistrări")
            else:
                print("📁 Folderul Intrebari nu există")
                
        elif choice == "4":
            confirm = input("⚠️ Ștergi toate înregistrările? (da/nu): ").lower()
            if confirm == "da":
                folder = Path("Intrebari")
                if folder.exists():
                    files = list(folder.glob("intrebare*.wav"))
                    for file in files:
                        file.unlink()
                    print(f"🗑️ {len(files)} fișiere șterse")
                else:
                    print("📁 Nu există fișiere de șters")
            else:
                print("❌ Anulat")
                
        elif choice == "q":
            print("👋 La revedere!")
            break
        else:
            print("❌ Opțiune invalidă")

if __name__ == "__main__":
    # Test rapid
    print("🎤 Apel funcție înregistrare...")
    filename = inregistrare_intrebare()
    
    if filename:
        print(f"✅ Înregistrare completă: {filename}")
    else:
        print("❌ Înregistrarea a eșuat")