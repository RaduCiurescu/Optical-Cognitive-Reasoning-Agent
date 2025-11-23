    # utils.py
# ... (celelalte importuri raman la fel)
from datetime import datetime # Asigura-te ca ai acest import

# ... (toate celelalte functii raman la fel) ...

def log_document_type(doc_type):
    """
    MODIFICAT: Adauga tipul documentului si data in fisierul typesLogs.txt.
    Format: YYYY-MM-DD,Categorie
    """
    today_str = datetime.now().strftime("%Y-%m-%d")
    log_entry = f"{today_str},{doc_type}\n" # Noul format
    
    try:
        with open(config.LOG_TYPE_FILE, "a", encoding="utf-8") as f:
            f.write(log_entry)
        # Am actualizat mesajul de log
        print(f"Statistica '{log_entry.strip()}' salvata in {config.LOG_TYPE_FILE}")
    except Exception as e:
        print(f"Eroare la scrierea in {config.LOG_TYPE_FILE}: {e}")

# ... (restul functiilor, ex: log_document_content, raman neschimbate) ...