#!/usr/bin/env python3
"""
HC-SR04 Ultrasonic Sensor Test with LED Control
Turns on LED when object is within threshold distance
"""

import RPi.GPIO as GPIO
import time
import config

def setup_gpio():
    """Initialize GPIO pins"""
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    # Setup pins
    GPIO.setup(config.PIN_TRIGGER, GPIO.OUT)
    GPIO.setup(config.PIN_ECHO, GPIO.IN)
    GPIO.setup(config.PIN_LED, GPIO.OUT)
    
    # Initialize trigger to LOW
    GPIO.output(config.PIN_TRIGGER, False)
    GPIO.output(config.PIN_LED, False)

def measure_distance():
    """
    Measure distance using HC-SR04 sensor
    Returns distance in meters
    """
    # Send 10us pulse to trigger
    GPIO.output(config.PIN_TRIGGER, True)
    time.sleep(0.00001)  # 10 microseconds
    GPIO.output(config.PIN_TRIGGER, False)
    
    # Wait for echo to start
    pulse_start = time.time()
    timeout_start = pulse_start
    while GPIO.input(config.PIN_ECHO) == 0:
        pulse_start = time.time()
        # Timeout after 1 second to avoid infinite loop
        if pulse_start - timeout_start > 1:
            return -1
    
    # Wait for echo to end
    pulse_end = time.time()
    timeout_start = pulse_end
    while GPIO.input(config.PIN_ECHO) == 1:
        pulse_end = time.time()
        # Timeout after 1 second
        if pulse_end - timeout_start > 1:
            return -1
    
    # Calculate distance
    pulse_duration = pulse_end - pulse_start
    # Speed of sound = 343 m/s, divide by 2 for round trip
    distance = (pulse_duration * 343) / 2
    
    return distance

def control_led(distance):
    """Control LED based on distance threshold"""
    if 0 < distance <= config.DISTANCE_THRESHOLD_METERS:
        GPIO.output(config.PIN_LED, True)
        return True
    else:
        GPIO.output(config.PIN_LED, False)
        return False

def main():
    """Main test loop"""
    try:
        setup_gpio()
        print("HC-SR04 Sonar Test Started")
        print(f"Distance threshold: {config.DISTANCE_THRESHOLD_METERS}m")
        print("Press Ctrl+C to exit")
        print("-" * 40)
        
        while True:
            distance = measure_distance()
            
            if distance == -1:
                print("Measurement timeout - check connections")
                time.sleep(1)
                continue
            
            led_status = control_led(distance)
            status = "ON" if led_status else "OFF"
            
            print(f"Distance: {distance:.2f}m | LED: {status}")
            
            time.sleep(0.5)  # Measurement interval
            
    except KeyboardInterrupt:
        print("\nTest stopped by user")
        
    except Exception as e:
        print(f"Error occurred: {e}")
        
    finally:
        # Cleanup GPIO
        GPIO.output(config.PIN_LED, False)
        GPIO.cleanup()
        print("GPIO cleanup completed")

if __name__ == "__main__":
    main()