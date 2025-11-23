import google.generativeai as genai
import os
import PIL.Image
import re
from datetime import datetime

# --- 1. Functie de Logare Profesionala ---
def scrie_log(domeniu, descriere):
    """
    Salveaza raspunsul in 'textLog.txt' cu un format profesional
    si un timestamp.
    """
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S") 
    
    log_entry = f"""
===================================================
Data/Ora: {timestamp}
Domeniu: {domeniu}
---------------------------------------------------
Descriere:
{descriere}
===================================================
"""
    try:
        with open("textLog.txt", "a", encoding="utf-8") as f:
            f.write(log_entry)
        print(f"Raspuns adaugat in textLog.txt")
    except Exception as e:
        print(f"Eroare la scrierea log-ului: {e}")

# --- 2. Functia de Redactare (Plasa de Siguranta) ---
def redacteaza_date_personale(text):
    """
    Inlocuieste datele personale comune cu termeni generici.
    Acesta este Stratul 2 (Plasa de Siguranta).
    """
    print("Se verifica datele personale (plasa de siguranta)...")
    
    # Inlocuieste email-urile
    text = re.sub(r'\S+@\S+\.\S+', '(emailul dumneavoastra)', text)
    
    # Inlocuieste numerele de telefon
    text = re.sub(r'(\+4|0)[ -]?(\d{3}[ -]?\d{3}[ -]?\d{3}|\d{2}[ -]?\d{3}[ -]?\d{4})', '(nr. de telefon al dvs.)', text)
    
    # Inlocuieste CNP-urile
    text = re.sub(r'\b[125678]\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{6}\b', '(CNP-ul dumneavoastra)', text)
    
    # Putem adauga si o regula simpla pentru adrese
    text = re.sub(r'\b(Str|B-dul|Aleea|Piata|Nr|Bl|Sc|Ap)\b[\. ]*[\w\d]+', '(adresa dvs.)', text, flags=re.IGNORECASE)

    return text

# --- 3. Citeste Cheia API din fisier ---
api_key_file = "apiKey.txt"
try:
    with open(api_key_file, 'r') as f:
        api_key = f.read().strip()
    if not api_key:
        print(f"Eroare: Fisierul {api_key_file} este gol.")
        exit()
except FileNotFoundError:
    print(f"Eroare: Fisierul '{api_key_file}' nu a fost gasit.")
    exit()

# --- 4. Configureaza API-ul ---
try:
    genai.configure(api_key=api_key)
except Exception as e:
    print(f"Eroare la configurarea API: {e}")
    exit()

# --- 5. Incarca Imaginea ---
nume_imagine = "images/capture_1.jpg"
try:
    img = PIL.Image.open(nume_imagine)
    print(f"Imaginea {nume_imagine} a fost incarcata.")
except FileNotFoundError:
    print(f"Eroare: Nu gasesc imaginea: {nume_imagine}")
    print("Ruleaza intai scriptul de camera pt a face o captura.")
    exit()

# --- 6. Initializeaza Modelul ---
try:
    model = genai.GenerativeModel('gemini-pro-vision')
except Exception as e:
    print(f"Eroare la initializarea modelului: {e}")
    exit()

# --- 7. MODIFICAT: Trimite Prompt cu Instructiuni de Redactare ---
print("Trimit imaginea catre Gemini...")

lista_domenii = ["Facturi",]

# Acesta este noul prompt
prompt = f"""
Analizeaza aceasta imagine. Raspunsul tau trebuie sa urmeze STRICT acest format:
LINIA 1: Doar numele domeniului, ales din aceasta lista: {', '.join(lista_domenii)}
LINIA 2: Descrierea detaliata a imaginii.

INSTRUCTIUNE IMPORTANTA: In descrierea de pe LINIA 2, evită cu strictețe dezvaluirea oricaror date personale, cum ar fi adrese poștale complete sau CNP-uri. Menționează doar existența lor generic (de ex. "se observă o adresă").
"""

try:
    response = model.generate_content([prompt, img])
    
    # --- 8. Proceseaza Raspunsul ---
    domeniu = "Eroare"
    descriere = "Eroare"

    try:
        raspuns_text = response.text.strip()
        parti = raspuns_text.split('\n', 1) 
        
        if len(parti) == 2:
            domeniu = parti[0].strip()
            descriere = parti[1].strip()
            
            if domeniu not in lista_domenii:
                print(f"Avertisment: Modelul a returnat un domeniu neasteptat: '{domeniu}'")
        else:
            print("EROARE: Modelul nu a returnat formatul cerut (Domeniu pe Linia 1, Descriere pe Linia 2).")
            domeniu = "Eroare Format"
            descriere = raspuns_text 
        
        print(f"\n--- Raspuns Primit de la Gemini ---")
        print(f"Domeniu Identificat: {domeniu}")
        print(f"Descriere (inainte de redactare): {descriere}")
        print("---------------------------------")

        # Aici actioneaza plasa noastra de siguranta (Stratul 2)
        descriere_redactata = redacteaza_date_personale(descriere)
        
        if descriere != descriere_redactata:
            print("Status: Date personale (neomise de AI) au fost prinse si inlocuite pentru log.")

        scrie_log(domeniu, descriere_redactata)

    except Exception as e:
        print(f"\nEroare la procesarea raspunsului: {e}")
        scrie_log("Eroare Procesare", str(e))

except Exception as e:
    print(f"\nEroare la generarea raspunsului de la Gemini: {e}")