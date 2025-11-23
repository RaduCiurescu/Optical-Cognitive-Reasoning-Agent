import google.generativeai as genai
import os
import PIL.Image

# --- 1. Citeste Cheia API din fisier ---
api_key_file = "apiKey.txt"

try:
    with open(api_key_file, 'r') as f:
        # .strip()
        api_key = f.read().strip()
    
    if not api_key:
        print(f"Eroare: Fisierul {api_key_file} este gol.")
        exit()

except FileNotFoundError:
    print(f"Eroare: Fisierul '{api_key_file}' nu a fost gasit.")
    print("Creeaza fisierul si pune cheia API in el.")
    exit()
except Exception as e:
    print(f"Eroare la citirea fisierului API: {e}")
    exit()

# --- 2. Configureaza API-ul ---
try:
    genai.configure(api_key=api_key)
except Exception as e:
    print(f"Eroare la configurarea API: {e}")
    exit()

# --- 3. Incarca Imaginea ---
nume_imagine = "images/capture_1.jpg"

try:
    img = PIL.Image.open(nume_imagine)
    print(f"Imaginea {nume_imagine} a fost incarcata.")
except FileNotFoundError:
    print(f"Eroare: Nu gasesc imaginea: {nume_imagine}")
    print("Ruleaza intai scriptul de camera pt a face o captura.")
    exit()
except Exception as e:
    print(f"Eroare la incarcarea imaginii: {e}")
    exit()


# --- 4. Initializeaza Modelul ---
try:
    model = genai.GenerativeModel('gemini-2.5-pro')
except Exception as e:
    print(f"Eroare la initializarea modelului: {e}")
    exit()

# --- 5. Trimite Prompt si Imagine ---
print("Trimit imaginea catre Gemini...")

prompt = "Descrie pe scurt ce vezi in aceasta imagine."

try:
    response = model.generate_content([prompt, img])

    # --- 6. Afiseaza Raspunsul ---
    print("\n--- Raspuns de la Gemini ---")
    print(response.text)
    print("--------------------------")

except Exception as e:
    print(f"Eroare la generarea raspunsului: {e}")
    #  eroare de API
    print(f"Detalii: {e}")
