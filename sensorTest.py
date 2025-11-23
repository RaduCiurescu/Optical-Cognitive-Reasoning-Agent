	# test_sensor.py
# Script independent pentru testarea senzorului HC-SR04 si a unui LED

import RPi.GPIO as GPIO
import time
import config
import sys

def setup_gpio():
    """Configureaza pinii GPIO pentru senzor si LED."""
    try:
        GPIO.setwarnings(False) # Dezactivam avertismentele
        GPIO.setmode(GPIO.BCM) # Folosim numerotarea BCM
        
        # Setup Senzor
        GPIO.setup(config.PIN_TRIGGER, GPIO.OUT)
        GPIO.setup(config.PIN_ECHO, GPIO.IN)
        
        # Setup LED
        GPIO.setup(config.PIN_LED, GPIO.OUT)
        
        # Initializam pinii
        GPIO.output(config.PIN_TRIGGER, False)
        GPIO.output(config.PIN_LED, False)
        
        print("Asteptam ca senzorul sa se stabilizeze...")
        time.sleep(2) # Asteptam 2 secunde
        print("Senzorul este gata. Se incepe testarea...")
        print("Apasati Ctrl+C pentru a opri.")
        
    except Exception as e:
        print(f"Eroare la initializarea GPIO: {e}")
        print("Asigura-te ca rulezi scriptul cu 'sudo' (sudo python test_sensor.py)")
        sys.exit(1)

def get_distance_meters():
    """Masoara si returneaza distanta in metri. (Copiat din sensor.py)"""
    
    # Trimitem un puls de 10us
    GPIO.output(config.PIN_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(config.PIN_TRIGGER, False)

    start_time = time.time()
    stop_time = time.time()
    
    timeout = time.time() + 0.1 # Timeout de 100ms

    # Asteptam ca ECHO sa devina HIGH
    while GPIO.input(config.PIN_ECHO) == 0:
        start_time = time.time()
        if start_time > timeout:
            # print("Eroare senzor: Timeout ECHO HIGH") # Decomenteaza pt debug
            return None # Eroare de citire

    # Asteptam ca ECHO sa revina la LOW
    timeout = time.time() + 0.1 # Resetam timeout-ul
    while GPIO.input(config.PIN_ECHO) == 1:
        stop_time = time.time()
        if stop_time > timeout:
            # print("Eroare senzor: Timeout ECHO LOW") # Decomenteaza pt debug
            return None # Eroare de citire

    # Calculam distanta
    time_elapsed = stop_time - start_time
    distance_m = (time_elapsed * 343) / 2
    
    return distance_m

def main_loop():
    """Ruleaza bucla de testare."""
    try:
        while True:
            distance = get_distance_meters()
            
            if distance is not None:
                # Afisam distanta in consola
                print(f"Distanta: {distance:.2f} m")
                
                # Verificam pragul
                if distance < config.DISTANCE_THRESHOLD_METERS:
                    # Obiect detectat -> Aprindem LED
                    GPIO.output(config.PIN_LED, True)
                else:
                    # Obiect prea departe -> Stingem LED
                    GPIO.output(config.PIN_LED, False)
            else:
                # Eroare la citire -> Stingem LED
                print("Eroare citire senzor.")
                GPIO.output(config.PIN_LED, False)
            
            # Asteptam putin inainte de urmatoarea citire
            time.sleep(0.2) 

    except KeyboardInterrupt:
        print("\nTest incheiat.")
    finally:
        # Curatam pinii GPIO indiferent de cum se iese
        print("Curatare pini GPIO.")
        GPIO.cleanup()

# --- Punct de Intrare ---
if __name__ == "__main__":
    setup_gpio()
    main_loop()