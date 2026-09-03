import cv2
import serial
import time

ser = serial.Serial('COM7', 9600, timeout=1, write_timeout=1)        # Sends servo angle values to Arduino over a serial connection with 9600 speed

capture = cv2.VideoCapture(0)                       # Opens a connection to the default webcam so we can pull frames from it

if not capture.isOpened():                          # Checks if live feed came through
    # print("Error: Couldn't open video device.")
    exit()

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')      # Opens connection to read xml classifier file data

width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))          # Converts float to int for frame width
print(width)
height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))        # Converts float to int for frame height
print(height)

frame_center_x = width // 2                 # Calculates frame center width
frame_center_y = height // 2                # Calculates frame center height

smooth_offset_face_x = 0                    # Initial value for offset x
smooth_offset_face_y = 0                    # Initial value for offset y
alpha = 0.3

while True:                         
    ret, frame = capture.read()

    if not ret:                                     # Checks if frame comes back as None, if so, error is imminent and we break
        print("Error: Can't receive frame")
        break

    grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)         # Opens connection to set default color as gray

    face_detections = face_cascade.detectMultiScale(grayscale, scaleFactor=1.1, minNeighbors=8, minSize=(30, 30))   # Opens connection to establish scale factors of facial detection
    # print(face_detections)         # grayscale is brightness detection, scaleFactor is shrinking data to account for distance, minNeighbors needs 5 minimum matches on a location to make box, minSize is box size

    if len(face_detections) != 0:
        max_box = max(face_detections, key=lambda box: box[2] * box[3])     # Finds largest detected area from w * h indices
        x, y, w, h = max_box            # Assigns variables to position and size of area

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)        # Arguments of frame, top left corner, bottom right corner, color, thickness
        face_center_x = x + w // 2      # Detects center from left-top corner width-wise
        face_center_y = y + h // 2      # Detects center from left-top corner height-wise

        offset_face_x = face_center_x - frame_center_x          # Calculates offset face center from frame center (accounts for movement)
        offset_face_y = face_center_y - frame_center_y
        # print(offset_face_x, offset_face_y)

        smooth_value_x = (alpha * offset_face_x) + ((1 - alpha) * smooth_offset_face_x)     # Calculates new smooth value for x (EMA)
        smooth_offset_face_x = smooth_value_x
        smooth_value_y = (alpha * offset_face_y) + ((1 - alpha) * smooth_offset_face_y)     # Calculates new smooth value for y (EMA)
        smooth_offset_face_y = smooth_value_y

        # print(smooth_offset_face_x, smooth_offset_face_y)

        servo_angle_x = ((smooth_offset_face_x - (-frame_center_x)) / (frame_center_x - (-frame_center_x))) * 180      # Calculates servo x angle by value - min / max - min * 180 (degrees)
        # print(servo_angle_x)

        servo_angle_y = ((smooth_offset_face_y - (-frame_center_y)) / (frame_center_y - (-frame_center_y))) * 180      # Calculates servo y angle by value - min / max - min * 180 (degrees)
        # print(servo_angle_y)

        send_data_x = int(servo_angle_x)            # Converts float to int
        send_data_y = int(servo_angle_y)
        send_data_str = str(send_data_x) + ',' + str(send_data_y) + '\n'       # Converts and concats both x and y values from int to str
        send_data_bytes = send_data_str.encode()    # Converts str to bytes
        ser.write(send_data_bytes)                  # Writes bytes to serial
        
        time.sleep(0.02)

    cv2.imshow('Live Feed', frame)

    if cv2.waitKey(1) == ord('q'):      # 'Q' ends live feed
        break

capture.release()
cv2.destroyAllWindows()