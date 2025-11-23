# stt_openai.py

from openai import OpenAI
import sys

# Încarcă cheia API din fișier
with open("openaiKEY.txt", "r") as f:
    api_key = f.read().strip()

client = OpenAI(api_key=api_key)


def transcribe_file(file_path: str, language: str = "ro") -> str:
    """
    Trimite un fișier audio (mp3/wav/etc.) la Whisper (OpenAI)
    și întoarce textul transcris.ZZ
    Funcțional pentru OpenAI v2.8.0.
    """
    try:
        with open(file_path, "rb") as f:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=f,
                language=language
            )
        return transcript.text

    except Exception as e:
        print(f"Eroare Whisper: {e}")


# ================= MAIN =================
if __name__ == "__main__":


    file_path = "./Intrebare.wav"

    print(f"\n🎤 Trimit fișierul '{file_path}' către Whisper...\n")

    text = transcribe_file(file_path)

    print("\n📄 TRANSCRIERA PRIMITĂ DE LA AI:")
    print("----------------------------------")
    print(text or "[Eroare sau text gol]")
    print("----------------------------------\n")
