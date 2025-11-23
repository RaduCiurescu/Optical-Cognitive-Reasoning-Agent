# sensorTest.py
# Script de testare pentru fazele DETECTING, VERIFYING, PLAYING

import RPi.GPIO as GPIO
import time
import config
import sys

def setup_gpio():
    """Configureaza pinii GPIO pentru senzor, LED/Tranzistor si Buton Reset."""
    try:
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        
        GPIO.setup(config.PIN_TRIGGER, GPIO.OUT)
        GPIO.setup(config.PIN_ECHO, GPIO.IN)
        GPIO.setup(config.PIN_LED, GPIO.OUT)
        GPIO.setup(config.BUTTON_RESET, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        GPIO.output(config.PIN_TRIGGER, False)
        GPIO.output(config.PIN_LED, False)
        
        print("Asteptam ca senzorul sa se stabilizeze...")
        time.sleep(2)
        print("Sistemul este gata. Se incepe testarea.")
        print("Apasati Ctrl+C pentru a opri.")
        
    except Exception as e:
        print(f"Eroare la initializarea GPIO: {e}")
        sys.exit(1)

def get_distance_meters():
    """Masoara si returneaza distanta in metri. (Neschimbat)"""
    
    GPIO.output(config.PIN_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(config.PIN_TRIGGER, False)

    start_time = time.time()
    stop_time = time.time()
    
    timeout = time.time() + 0.1 

    while GPIO.input(config.PIN_ECHO) == 0:
        start_time = time.time()
        if start_time > timeout:
            return None 

    timeout = time.time() + 0.1
    while GPIO.input(config.PIN_ECHO) == 1:
        stop_time = time.time()
        if stop_time > timeout:
            return None

    time_elapsed = stop_time - start_time
    distance_m = (time_elapsed * 343) / 2
    
    return distance_m

def main_loop():
    """Ruleaza bucla de testare conform diagramei UniHack."""
    
    # Stari bazate pe diagrama UniHack_Diagram.drawio
    STATE_DETECTING = "DETECTING"   #  Asteapta obiect (echivalent IDLE in codul vechi)
    STATE_VERIFYING = "VERIFYING"   #  Obiect detectat, se aplica tolerantele
    STATE_PLAYING = "PLAYING"       #  Redare MP3 blocata
    STATE_COOLDOWN = "COOLDOWN"     # Stare de test: asteapta reset manual
    
    # Variabile de stare
    current_state = STATE_DETECTING
    detection_start_time = 0.0 # Cand a inceput starea VERIFYING
    last_seen_time = 0.0       # Cand a fost vazut ultima oara obiectul (pentru spike)
    play_start_time = 0.0      # Cand a inceput starea PLAYING

    try:
        print(f"Sistem in starea {current_state}. Se asteapta...")
        while True:
            # 1. Citim intrarile (senzor si buton)
            distance = get_distance_meters()
            is_object_detected = (distance is not None and distance < config.DISTANCE_THRESHOLD_METERS)
            is_reset_pressed = (GPIO.input(config.BUTTON_RESET) == GPIO.LOW)

            # --- Logica State Machine ---

            if current_state == STATE_DETECTING:
                #  Asteptam ca o persoana sa fie detectata
                if is_object_detected:
                    # Obiect detectat! Trecem la VERIFYING [cite: 9]
                    current_state = STATE_VERIFYING
                    detection_start_time = time.time()
                    last_seen_time = time.time()
                    GPIO.output(config.PIN_LED, False) # Pornim semnalul MP3
                    print(f"DETECTAT! Se intra in starea {current_state}. (Se porneste semnalul)")

            elif current_state == STATE_VERIFYING:
                #  Suntem in "Tolerance accepted to a desired window" [cite: 14]
                if is_object_detected:
                    # Obiectul e inca acolo, resetam timer-ul de "spike"
                    last_seen_time = time.time()
                    
                    # Verificam daca a trecut timpul de activare
                    time_in_detection = time.time() - detection_start_time
                    if time_in_detection > config.ACTIVATION_TIME_SECONDS:
                        # DA! (Path "Yes" [cite: 19]) Trecem la PLAYING [cite: 11]
                        current_state = STATE_PLAYING
                        play_start_time = time.time()
                        print(f"VERIFICARE completa. Se BLOCheaza in {current_state} pentru {config.PLAY_DURATION_SECONDS} secunde.")
                    else:
                        # Inca nu, mai asteptam
                        print(f"VERIFICARE in curs... {time_in_detection:.1f}s / {config.ACTIVATION_TIME_SECONDS}s")
                
                else:
                    # Obiectul a disparut (sau eroare senzor)
                    time_since_last_seen = time.time() - last_seen_time
                    
                    # Verificam daca a trecut timpul de toleranta (SPIKE)
                    if time_since_last_seen > config.SPIKE_TOLERANCE_SECONDS:
                        # A fost plecat prea mult. (Path "No" [cite: 18]) Anulam si revenim la DETECTING
                        current_state = STATE_DETECTING
                        time_in_detection = 0
                        GPIO.output(config.PIN_LED, False) # Oprim semnalul MP3
                        print(f"Obiect pierdut. Anulare. Revenire la {current_state}. (Se opreste semnalul)")

            elif current_state == STATE_PLAYING:
                #  Suntem in redare blocata. Semnalul e ON.
                # Ignoram complet senzorul.
                
                time_playing = time.time() - play_start_time
                if time_playing > config.PLAY_DURATION_SECONDS:
                    # Timpul de redare s-a terminat [cite: 24]
                    # In loc sa trecem la chatbot, intram in COOLDOWN de test
                    current_state = STATE_COOLDOWN
                    time_start_cooldown = time.time()
                    #GPIO.output(config.PIN_LED, True) # Pronire semnalul
                    print(f"Redare terminata. Se intra in {current_state}. (Se opreste semnalul)")
                    print("Apasati butonul de RESET pentru a relua testul.")
                else:
                    # Redare in curs
                    GPIO.output(config.PIN_LED, True) # Pronire semnalul
                    print(f"Redare blocata. Timp ramas: {config.PLAY_DURATION_SECONDS - time_playing:.1f}s")
            
            elif current_state == STATE_COOLDOWN:
                GPIO.output(config.PIN_LED, False) # Oprire semnalul
                # Stare de test. Asteptam reset manual.
                time_cooldown = time.time() - time_start_cooldown
                if time_cooldown > 15 or GPIO.input(config.BUTTON_RESET) == GPIO.HIGH: #adaugam button click pt exits
                    current_state = STATE_DETECTING
                    print(f"Buton RESET apasat! Sistemul revine in {current_state}.")
                    time.sleep(0.5) 
                    GPIO.cleanup()
                    sys.exit()
                else:
                    print(f"Cooldown activat de: {time_cooldown}s")
            
            time.sleep(0.1) 

    except KeyboardInterrupt:
        print("\nTest incheiat.")
    finally:
        print("Curatare pini GPIO.")
        GPIO.cleanup()

# --- Punct de Intrare ---
if __name__ == "__main__":
    setup_gpio()
    main_loop()