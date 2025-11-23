from gpiozero import Button
from time import sleep

# --- MODIFICAREA ESTE AICI ---
# pull_up=False îi spune bibliotecii să NU activeze rezistorul intern.
# Acum, .is_pressed va fi adevărat când pinul citește HIGH (3.3V).
buton = Button(17, pull_up=False)

print("Scriptul a pornit (cu rezistor PULL-DOWN extern).")
print("Apasă butonul...")

while True:
    if buton.is_pressed:
        print("Butonul este APĂSAT! (Citește HIGH)")
    else:
        # Când e eliberat, rezistorul extern îl trage la LOW (GND)
        print("Butonul este eliberat. (Citește LOW)")
    
    sleep(0.5)