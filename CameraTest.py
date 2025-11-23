import cv2
import time
import os

# --- 1. Setup ---

folder_name = "images"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)
    print(f"Created directory: {folder_name}")

# Camera and feed setup
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

print("Live feed started. Press 'q' to quit.")
print("Capture sequence will begin in 5 seconds...")

# --- 2. Timing and State Setup ---

# Total pictures to take
total_captures = 5
# Counter for pictures taken
captures_taken = 0

# Time delays (in seconds)
first_capture_delay = 5.0
capture_interval = 2.0

# Get the start time
start_time = time.time()

# Calculate the time for the *first* capture
next_capture_time = start_time + first_capture_delay

# --- 3. Main Loop (Feed + Capture) ---

while True:
    # Always read the frame for the live feed
    ret, frame = cap.read()
    if not ret:
        print("Error: Can't receive frame (stream end?). Exiting ...")
        break

    # Get the current time
    current_time = time.time()

    # --- Capture Logic ---
    # Check if we still need to take pictures AND if it's time for the next one
    if (captures_taken < total_captures) and (current_time >= next_capture_time):
        
        # Increment capture count
        captures_taken += 1
        
        # Create filename and save the *current* frame
        filename = os.path.join(folder_name, f"capture_{captures_taken}.jpg")
        cv2.imwrite(filename, frame)
        
        print(f"Captured: {filename}")
        
        # Schedule the *next* capture
        next_capture_time += capture_interval

        # Notify when done
        if captures_taken == total_captures:
            print("Capture sequence complete. Live feed remains active.")

    # --- Live Feed Display Logic ---
    # This runs on every single loop, regardless of capture state
    cv2.imshow('Live Feed', frame)

    # --- Quit Logic ---
    if cv2.waitKey(1) == ord('q'):
        break

# --- 4. Cleanup ---
cap.release()
cv2.destroyAllWindows()
print("Camera feed stopped.")
