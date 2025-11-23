# test_stt.py
# Script pentru a testa separat functionalitatea de recunoastere vocala (STT)
# si raspuns la intrebari (Q&A) din voice_handler.py

import os
import sys
import time
import google.generativeai as genai

# Importam modulele noastre
import voice_handler
import utils
import config

def main_test():
    """Functia principala de testare a modulului voice_handler."""
    
    # --- 1. Initializare API (necesara pentru voice_handler.setup_voice_input) ---
    print("Se configureaza API-ul Google...")
    api_key = utils.read_api_key()
    if not api_key:
        print("EROARE: Nu gasesc fisierul apiKey.txt. Opresc testul.")
        sys.exit(1)
    try:
        genai.configure(api_key=api_key)
        print("API-ul Google a fost configurat cu succes.")
    except Exception as e:
        print(f"EROARE la configurarea API: {e}")
        sys.exit(1)

    # --- 2. Initializare Voice Handler (Functia pe care o testam) ---
    print("\nSe initializeaza modulul de voce (microfon si model text)...")
    if not voice_handler.setup_voice_input():
        print("EROARE: Initializarea modulului de voce a esuat.")
        print("Verifica daca ai instalat 'SpeechRecognition', 'PyAudio' si 'portaudio19-dev'.")
        sys.exit(1)
    
    print("\n--- Initializare STT finalizata cu succes ---")

    # --- 3. Creare Context Fals (Mock) ---
    mock_log_path = "temp_context_for_test.txt"
    mock_context_content = """
    Acesta este un document de test. 
    Este o factura pentru un laptop model 'SuperBook'.
    Pretul total este 5000 RON. 
    Clientul se numeste Ana Popescu.
    Adresa de livrare este Strada Libertatii, Numarul 10, Bucuresti.
    """
    try:
        with open(mock_log_path, 'w', encoding='utf-8') as f:
            f.write(mock_context_content)
        print(f"Am creat un fisier de context fals: {mock_log_path}")
    except Exception as e:
        print(f"EROARE la crearea fisierului de context fals: {e}")
        sys.exit(1)

    # --- 4. Bucla de Testare ---
    print("\n--- INCEPEM BUCLA DE TESTARE (va rula de 3 ori) ---")
    print("Poti testa Cazul #1 (intrebare), Cazul #2 ('nu') sau Cazul #3 (timeout).")
    print("Apasati Ctrl+C pentru a opri mai devreme.")
    
    try:
        for i in range(3):
            print(f"\n--- TESTUL #{i+1} / 3 ---")
            
            # Acesta este apelul principal, folosind contextul fals
            voice_handler.handle_follow_up_question(mock_log_path)
            
            print(f"--- TESTUL #{i+1} incheiat ---")
            time.sleep(1) # O mica pauza intre teste
            
    except KeyboardInterrupt:
        print("\nTest oprit manual.")
    
    finally:
        # --- 5. Curatare ---
        if os.path.exists(mock_log_path):
            os.remove(mock_log_path)
            print(f"\nAm sters fisierul de context fals: {mock_log_path}")
        print("Test STT incheiat.")

# --- Punct de Intrare ---
if __name__ == "__main__":
    main_test()