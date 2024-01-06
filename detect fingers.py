import cv2
from cvzone.HandTrackingModule import HandDetector
import time
import subprocess



def print_list_as_string(lst):
    print(', '.join(map(str, lst)))


# Set up the hand detector
detector = HandDetector(maxHands=1, detectionCon=0.8)

# Start the webcam
video = cv2.VideoCapture(0)

# Define a mapping from finger numbers to finger names
finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']

# Define a mapping from finger numbers to lists of tuples indicating which fingers are being held up
finger_map = {0: [(0, 0, 0, 0, 0)], 
              1: [(0, 0, 0, 0, 1), (0, 0, 0, 1, 0), (0, 0, 1, 0, 0), (0, 1, 0, 0, 0), (1, 0, 0, 0, 0)], 
              2: [(0, 0, 0, 1, 1), (0, 0, 1, 0, 1), (0, 0, 1, 1, 0), (0, 1, 0, 0, 1), (0, 1, 0, 1, 0), (0, 1, 1, 0, 0), (1, 0, 0, 0, 1), (1, 0, 0, 1, 0), (1, 0, 1, 0, 0), (1, 1, 0, 0, 0)], 
              3: [(0, 0, 1, 1, 1), (0, 1, 0, 1, 1), (0, 1, 1, 0, 1), (0, 1, 1, 1, 0), (1, 0, 0, 1, 1), (1, 0, 1, 0, 1), (1, 0, 1, 1, 0), (1, 1, 0, 0, 1), (1, 1, 0, 1, 0), (1, 1, 1, 0, 0)], 
              4: [(0, 1, 1, 1, 1), (1, 0, 1, 1, 1), (1, 1, 0, 1, 1), (1, 1, 1, 0, 1), (1, 1, 1, 1, 0)], 
              5: [(1, 1, 1, 1, 1)]}

while True:
    # Read the frame
    _, img = video.read()
    
    # Flip the frame horizontally
    img = cv2.flip(img, 1)

    # Detect the hand in the frame
    hand = detector.findHands(img, draw=False)
    
    # If a hand was detected
    if hand:
        # Get the landmarks of the hand
        lmlist = hand[0]
        
        # If the landmarks are valid
        if lmlist:
            # Find which fingers are being held up
            fingerup = detector.fingersUp(lmlist) 
            
            # Write the names of the fingers that are being held up to a text file
            fingers = []
            for i, is_up in enumerate(fingerup):
                if is_up:
                    fingers.append(finger_names[i])
            with open("fingers.txt", "w") as f:
                fingers_string = ','.join(map(str,fingers))
                f.write(fingers_string)
            print(fingers)

        #replace the following variables with they're respective paths, password and IP address
        windows_file_path = "File path of the fingers.txt on your desktop/laptop"
        password = "the password for the ssh file to be sent with automation"
        raspberry_pi_file_path = "File path to store the list of fingers that are held up"
        result = subprocess.run(["scp", windows_file_path, "IP_Address:"+raspberry_pi_file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, input=password.encode())
        

 # Show the frame
    cv2.imshow("Video",img)
    
    # Check for user input
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    time.sleep(0.01)  # Decrease the amount of time spent waiting between frames

