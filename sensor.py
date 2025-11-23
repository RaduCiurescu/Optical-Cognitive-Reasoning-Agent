# sensor.py
# Rescris pentru a folosi 'gpiod' in loc de 'RPi.GPIO' (compatibil RPi 5)

import gpiod
import time
import config
import sys
import subprocess

# Pe Raspberry Pi 5, cipul principal GPIO este 'gpiochip4'
CHIP_NAME = 'gpiochip4'
chip = None
trigger_line = None
echo_line = None
led_line = None

def setup_sensor():
    """Configureaza pinii GPIO folosind gpiod."""
    global chip, trigger_line, echo_line, led_line
    try:
        # Deschidem cipul GPIO
        chip = gpiod.Chip(CHIP_NAME)
        
        # Cerem acces la liniile (pinii) GPIO de care avem nevoie
        trigger_line = chip.get_line(config.PIN_TRIGGER)
        echo_line = chip.get_line(config.PIN_ECHO)
        led_line = chip.get_line(config.PIN_LED)

        # Configuram liniile
        # 'consumer' este un nume descriptiv pentru 'cine' foloseste pinul
        trigger_line.request(consumer="sensor_trigger", type=gpiod.line.Request.DIRECTION_OUTPUT, default_val=0)
        led_line.request(consumer="sensor_led", type=gpiod.line.Request.DIRECTION_OUTPUT, default_val=0)
        echo_line.request(consumer="sensor_echo", type=gpiod.line.Request.DIRECTION_INPUT)
        
        print("Asteptam ca senzorul sa se stabilizeze (gpiod)...")
        time.sleep(2) # Asteptam 2 secunde
        print("Senzorul este gata.")
        return True
        
    except Exception as e:
        print(f"Eroare la initializarea GPIO (gpiod): {e}")
        print("Asigura-te ca rulezi scriptul cu 'sudo' si 'libgpiod-dev' e instalat.")
        return False

def get_distance_meters():
    """Masoara si returneaza distanta in metri."""
    try:
        # Trimitem un puls de 10us
        trigger_line.set_value(1)
        time.sleep(0.00001)
        trigger_line.set_value(0)

        start_time = time.time()
        stop_time = time.time()
        timeout = time.time() + 0.1 # Timeout de 100ms

        # Asteptam ca ECHO sa devina HIGH
        while echo_line.get_value() == 0:
            start_time = time.time()
            if start_time > timeout:
                print("Eroare senzor: Timeout la asteptare ECHO HIGH")
                return None # Eroare de citire

        # Asteptam ca ECHO sa revina la LOW
        timeout = time.time() + 0.1 # Resetam timeout-ul
        while echo_line.get_value() == 1:
            stop_time = time.time()
            if stop_time > timeout:
                print("Eroare senzor: Timeout la asteptare ECHO LOW")
                return None # Eroare de citire

        # Calculam distanta
        time_elapsed = stop_time - start_time
        distance_m = (time_elapsed * 343) / 2
        
        return distance_m
    except Exception as e:
        print(f"Eroare in get_distance_meters (gpiod): {e}")
        return None

def check_object_presence():
    """
    Functia principala ceruta.
    Returneaza 1 daca un obiect e mai aproape decat pragul, altfel 0.
    """
    distance = get_distance_meters()
    
    if distance is not None:
        if distance < config.DISTANCE_THRESHOLD_METERS:
            return 1 # Obiect detectat
            
    return 0 # Niciun obiect sau eroare senzor

def control_led(is_present):
    """Aprinde sau stinge LED-ul in functie de starea 'is_present' (1 sau 0)."""
    try:
        if is_present == 1:
            led_line.set_value(1) # Aprinde LED
        else:
            led_line.set_value(0) # Stinge LED
    except Exception as e:
        # Nu oprim programul principal pentru o eroare de LED
        print(f"Eroare la controlul LED-ului (gpiod): {e}")

def cleanup_sensor():
    """Curata (elibereaza) liniile GPIO la iesire."""
    print("Curatare pini GPIO (gpiod).")
    try:
        # Eliberam fiecare linie pentru ca alte programe sa le poata folosi
        if trigger_line:
            trigger_line.release()
        if echo_line:
            echo_line.release()
        if led_line:
            led_line.release()
        # Inchidem conexiunea la cipul GPIO
        if chip:
            chip.close()
    except Exception as e:
        print(f"Eroare minora la cleanup gpiod: {e}")