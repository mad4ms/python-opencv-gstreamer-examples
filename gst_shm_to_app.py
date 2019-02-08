import cv2

# WORKING: cap = cv2.VideoCapture("shmsrc socket-path=/tmp/foo ! video/x-raw, format=BGR ,width=1920,height=1080,framerate=30/1 ! videoconvert ! video/x-raw, format=BGR ! appsink")

# Define the source as shared memory (shmsrc) and point to the socket. !
# Set the caps (raw (not encoded) frame video/x-raw, format as BGR or RGB (opencv format of grabbed cameras)) and define the properties of the camera !
# And sink the grabbed data to the appsink
# cap = cv2.VideoCapture("shmsrc socket-path=/tmp/foo ! video/x-raw, format=BGR ,width=1920,height=1080,framerate=30/1 ! appsink")

## Update
cap = cv2.VideoCapture("shmsrc socket-path=/tmp/foo ! video/x-raw, format=BGR, width=640, height=480, pixel-aspect-ratio=1/1, framerate=30/1 ! \
     decodebin ! videoconvert ! appsink")

if not cap.isOpened():
    print("Cannot capture from camera. Exiting.")
    quit()


while True:

    ret, frame = cap.read()
    #
    if ret == False:
        break


    cv2.imshow("FrameREAD",frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# gst-launch-1.0 v4l2src ! x264enc ! shmsink socket-path=/tmp/foo sync=true wait-for-connection=false shm-size=10000000

# gst-launch-1.0 shmsrc socket-path=/tmp/foo ! h264parse ! avdec_h264 ! videoconvert ! ximagesink

# gst-launch-1.0 shmsrc socket-path=/tmp/foo ! video/x-raw, format=BGR ,width=1920,height=1080,framerate=30/1 ! videoconvert ! ximagesink
