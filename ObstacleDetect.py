from gpiozero import LED, Button  # <-- Changed LineSensor to Button
from time import sleep

# --- Configuration ---

# Set up the GPIO pin for your LED.
led = LED(18)

# Set up the GPIO pin for your IR Proximity Sensor (e.g., FC-51).
# We are using the Button class because the sensor's 'OUT' pin
# goes LOW when it detects an obstacle, just like a button press.
#
# --- IR Sensor Wiring ---
# VCC pin -> 3.3V pin on Pi
# GND pin -> GND pin on Pi
# OUT pin -> GPIO 17 on Pi
sensor = Button(17)  # <-- Changed LineSensor to Button

# --- Main Program ---

print("Obstacle Detector is running...")
print("Press CTRL+C to stop.")

try:
    while True:
        
        # sensor.is_pressed will be True when the sensor's
        # OUT pin goes LOW (which is when it detects an obstacle).
        if sensor.is_pressed:  # <-- Changed .is_line to .is_pressed
            # Obstacle is close! Turn the LED on.
            led.on()
            print("LED ON - Obstacle detected!   ")
        else:
            # Obstacle is far away. Turn the LED off.
            led.off()
            # We use \r to print on the same line without scrolling
            print("LED OFF - All clear.          ", end="\r")

        # Wait for a short time before taking the next reading
        sleep(0.1)

except KeyboardInterrupt:
    # This part runs when you press CTRL+C to stop the script
    print("\nStopping program...")
    led.off() # Turn the LED off
    sensor.close() # Clean up sensor resources
    print("Goodbye!")
