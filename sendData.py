import json
import requests
from datetime import datetime

def process_logs_and_update():
    """
    Citește 'typesLogs.txt', numără datele, salvează în 'update.txt'
    și trimite la API.
    """
    
    input_file = "typesLogs.txt"
    output_file = "update.txt" # Așa cum ai cerut
    api_url = "http://10.206.234.4:5000/api/dashboard"

    category_counts = {}
    total_lines = 0
    today_lines = 0
    
    # Obține data de astăzi în format YYYY-MM-DD
    today_date_str = datetime.now().strftime("%Y-%m-%d")

    # --- 1. Citirea și procesarea fișierului de log ---
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                parts = line.split()
                
                # Verificăm dacă linia are formatul așteptat
                # (cel puțin: NumeCategoria Dată Oră)
                if len(parts) < 3:
                    print(f"Avertisment: Ignor linia malformată: '{line}'")
                    continue
                    
                # Extrage data și categoria
                # Presupunem că data e penultimul element
                line_date_str = parts[-2]
                # Presupunem că tot ce e înainte de dată/oră e categoria
                category_part = " ".join(parts[:-2])

                # --- Numără totalul ---
                total_lines += 1

                # --- Numără pe cel de azi ---
                # Verificăm dacă data de pe linie corespunde cu cea de azi
                if line_date_str == today_date_str:
                    today_lines += 1
                
                # --- Numără pe categorii ---
                category_counts[category_part] = category_counts.get(category_part, 0) + 1

    except FileNotFoundError:
        print(f"❌ Eroare: Fișierul log '{input_file}' nu a fost găsit.")
        return # Oprește execuția dacă nu există fișierul
    except Exception as e:
        print(f"❌ Eroare la citirea fișierului '{input_file}': {e}")
        return

    # --- 2. Construirea structurii de date finale ---
    dashboard_data = {
        "totalPeople": total_lines,
        "todayPeople": today_lines,
        "categories": category_counts
    }

    # Verificare (opțional): 
    # total_lines ar trebui să fie egal cu suma valorilor din category_counts
    # assert total_lines == sum(category_counts.values())

    print("--- Datele procesate ---")
    print(json.dumps(dashboard_data, indent=2))
    print("------------------------")

    # --- 3. Salvarea fișierului local (update.txt) ---
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(dashboard_data, f, indent=4)
        print(f"✅ Succes: Datele au fost salvate (rescris) în '{output_file}'")
    except IOError as e:
        print(f"❌ Eroare la salvarea fișierului '{output_file}': {e}")
        # Continuăm chiar dacă salvarea locală eșuează,
        # poate vrem totuși să trimitem la API

    # --- 4. Transmiterea datelor către endpoint (API) ---
    try:
        response = requests.post(api_url, json=dashboard_data)
        
        if response.status_code >= 200 and response.status_code < 300:
            print(f"✅ Succes: Datele au fost trimise la '{api_url}'")
            print(f"Răspuns server (status {response.status_code}): {response.text}")
        else:
            print(f"⚠️ Eroare: Serverul a răspuns cu codul {response.status_code}")
            print(f"Răspuns: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print(f"❌ Eroare de Conexiune: Nu m-am putut conecta la '{api_url}'.")
        print("   Verifică dacă serverul rulează.")
    except Exception as e:
        print(f"❌ O eroare necunoscută a apărut la trimiterea datelor: {e}")

# --- Pentru a rula funcția ---
if __name__ == "__main__":
    process_logs_and_update()