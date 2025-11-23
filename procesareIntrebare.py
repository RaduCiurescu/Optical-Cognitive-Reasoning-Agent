import sounddevice as sd
import soundfile as sf
import os
from pathlib import Path
from openai import OpenAI

class AudioProcessor:
    def __init__(self):
        # Încarcă cheia API din fișier
        try:
            with open("openaiKEY.txt", "r") as f:
                api_key = f.read().strip()
            self.client = OpenAI(api_key=api_key)
            print("✅ OpenAI client inițializat")
        except FileNotFoundError:
            print("❌ Fișierul openaiKEY.txt nu a fost găsit")
            self.client = None
        except Exception as e:
            print(f"❌ Eroare la inițializarea OpenAI: {e}")
            self.client = None
    
    def transcribe_file(self, file_path: str, language: str = "ro") -> str:
        """
        Trimite un fișier audio (mp3/wav/etc.) la Whisper (OpenAI)
        și întoarce textul transcris.
        """
        if not self.client:
            print("❌ OpenAI client nu este disponibil")
            return None
            
        try:
            print(f"🔤 Trimit către Whisper: {file_path}")
            
            with open(file_path, "rb") as f:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=f,
                    language=language
                )
            
            print("✅ Transcrierea completă")
            return transcript.text

        except Exception as e:
            print(f"❌ Eroare Whisper: {e}")
            return None
    
    def inregistrare_intrebare(self):
        """
        Înregistrează 20 secunde și salvează în folder-ul Intrebari ca intrebareX.wav
        """
        
        # Creează folderul Intrebari dacă nu există
        folder_intrebari = Path("Intrebari")
        folder_intrebari.mkdir(exist_ok=True)
        
        # Găsește următorul număr pentru intrebare
        existing_files = list(folder_intrebari.glob("intrebare*.wav"))
        if existing_files:
            numbers = []
            for file in existing_files:
                try:
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
            duration = 15  # secunde
            sample_rate = 16000  # Hz
            channels = 1  # mono
            
            print(f"🔴 Înregistrare începe în 3 secunde...")
            import time
            for i in range(3, 0, -1):
                print(f"{i}...")
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
    
    def salveaza_raspuns(self, text: str) -> str:
        """
        Salvează textul transcris în folderul raspunsuri ca raspunsX.txt
        """
        
        # Creează folderul raspunsuri dacă nu există
        folder_raspunsuri = Path("raspunsuri")
        folder_raspunsuri.mkdir(exist_ok=True)
        
        # Găsește următorul număr pentru răspuns
        existing_files = list(folder_raspunsuri.glob("raspuns*.txt"))
        if existing_files:
            numbers = []
            for file in existing_files:
                try:
                    name = file.stem  # raspunsX
                    number = int(name.replace("raspuns", ""))
                    numbers.append(number)
                except ValueError:
                    continue
            
            next_number = max(numbers) + 1 if numbers else 1
        else:
            next_number = 1
        
        filename = folder_raspunsuri / f"raspuns{next_number}.txt"
        
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"Transcrierea Răspuns #{next_number}\n")
                f.write("=" * 40 + "\n\n")
                f.write(text)
                f.write(f"\n\n[Salvat automat la {Path().cwd()}]")
            
            print(f"💾 Răspuns salvat: {filename}")
            return str(filename)
            
        except Exception as e:
            print(f"❌ Eroare la salvarea răspunsului: {e}")
            return None
    
    def proceseaza_intrebare_completa(self):
        """
        Funcția principală care face tot workflow-ul:
        1. Înregistrează întrebarea
        2. Transcrie cu OpenAI
        3. Salvează răspunsul
        """
        
        print("🎤 PROCESARE COMPLETĂ ÎNTREBARE")
        print("=" * 40)
        
        # Pasul 1: Înregistrare
        print("\n📝 PASUL 1: Înregistrare audio")
        audio_file = self.inregistrare_intrebare()
        
        if not audio_file:
            print("❌ Înregistrarea a eșuat. Oprire.")
            return None
        
        # Pasul 2: Transcrierea
        print(f"\n🔤 PASUL 2: Transcrierea cu OpenAI")
        transcribed_text = self.transcribe_file(audio_file)
        
        if not transcribed_text:
            print("❌ Transcrierea a eșuat. Oprire.")
            return None
        
        print("\n📄 TEXTUL TRANSCRIS:")
        print("-" * 30)
        print(transcribed_text)
        print("-" * 30)
        
        # Pasul 3: Salvarea răspunsului
        print(f"\n💾 PASUL 3: Salvare răspuns")
        raspuns_file = self.salveaza_raspuns(transcribed_text)
        
        if raspuns_file:
            print(f"\n✅ PROCES COMPLET!")
            print(f"📁 Audio: {audio_file}")
            print(f"📄 Text: {raspuns_file}")
            return {
                'audio_file': audio_file,
                'text_file': raspuns_file,
                'transcription': transcribed_text
            }
        else:
            print("❌ Salvarea răspunsului a eșuat.")
            return None

# Funcții independente pentru uz rapid
def inregistrare_si_transcriere():
    """Funcție simplă pentru apel rapid"""
    processor = AudioProcessor()
    return processor.proceseaza_intrebare_completa()

def test_doar_transcriere(file_path: str):
    """Testează doar transcrierea unui fișier existent"""
    processor = AudioProcessor()
    
    if not os.path.exists(file_path):
        print(f"❌ Fișierul nu există: {file_path}")
        return
    
    text = processor.transcribe_file(file_path)
    if text:
        print(f"\n📄 TRANSCRIERE:")
        print(text)
        
        raspuns_file = processor.salveaza_raspuns(text)
        if raspuns_file:
            print(f"💾 Salvat în: {raspuns_file}")

# Meniu interactiv
def meniu_principal():
    """Meniu interactiv pentru testare"""
    
    processor = AudioProcessor()
    
    print("🎤 SISTEM ÎNREGISTRARE + TRANSCRIERE")
    print("=" * 40)
    
    while True:
        print(f"\n📋 Opțiuni:")
        print("  1 - Înregistrare + Transcriere completă")
        print("  2 - Doar transcriere fișier existent")
        print("  3 - Listează înregistrările")
        print("  4 - Listează răspunsurile")
        print("  q - Ieșire")
        
        choice = input("Alege opțiunea: ").strip()
        
        if choice == "1":
            result = processor.proceseaza_intrebare_completa()
            if result:
                print(f"\n🎉 Succes complet!")
                
        elif choice == "2":
            file_path = input("Calea către fișier: ").strip()
            test_doar_transcriere(file_path)
            
        elif choice == "3":
            folder = Path("Intrebari")
            if folder.exists():
                files = list(folder.glob("intrebare*.wav"))
                if files:
                    print(f"\n📂 Înregistrări ({len(files)}):")
                    for file in sorted(files):
                        size = os.path.getsize(file)
                        print(f"  🎵 {file.name} ({size:,} bytes)")
                else:
                    print("📭 Nu există înregistrări")
            else:
                print("📁 Folderul Intrebari nu există")
                
        elif choice == "4":
            folder = Path("raspunsuri")
            if folder.exists():
                files = list(folder.glob("raspuns*.txt"))
                if files:
                    print(f"\n📂 Răspunsuri ({len(files)}):")
                    for file in sorted(files):
                        size = os.path.getsize(file)
                        print(f"  📄 {file.name} ({size:,} bytes)")
                else:
                    print("📭 Nu există răspunsuri")
            else:
                print("📁 Folderul raspunsuri nu există")
                
        elif choice == "q":
            print("👋 La revedere!")
            break
        else:
            print("❌ Opțiune invalidă")

if __name__ == "__main__":
    # Rulare rapidă
    print("🚀 Apel funcție completă...")
    result = inregistrare_si_transcriere()
    
    if result:
        print(f"\n🎉 REZULTAT FINAL:")
        print(f"Audio: {result['audio_file']}")
        print(f"Text:  {result['text_file']}")