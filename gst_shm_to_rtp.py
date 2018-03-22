import cv2

# WORKING: cap = cv2.VideoCapture("shmsrc socket-path=/tmp/foo ! video/x-raw, format=BGR ,width=1920,height=1080,framerate=30/1 ! videoconvert ! video/x-raw, format=BGR ! appsink")

# Define the source as shared memory (shmsrc) and point to the socket. !
# Set the caps (raw (not encoded) frame video/x-raw, format as BGR or RGB (opencv format of grabbed cameras)) and define the properties of the camera !
# And sink the grabbed data to the appsink
cap = cv2.VideoCapture("shmsrc socket-path=/tmp/foo ! video/x-raw, format=BGR ,width=1920,height=1080,framerate=30/1 ! appsink")

if not cap.isOpened():
    print("Cannot capture from camera. Exiting.")
    quit()


gst_str_rtp = "appsrc ! videoconvert ! x264enc noise-reduction=10000 tune=zerolatency byte-stream=true threads=4 " \
              " ! h264parse ! mpegtsmux ! rtpmp2tpay ! udpsink host=127.0.0.1 port=5000"

# Create videowriter as a RTP sink
out = cv2.VideoWriter(gst_str_rtp, 0, 30, (1920, 1080), True)

while True:

    ret, frame = cap.read()
    #
    if ret == False:
        break

    out.write(frame)


    cv2.imshow("SHM frame",frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# gst-launch-1.0 v4l2src ! x264enc ! shmsink socket-path=/tmp/foo sync=true wait-for-connection=false shm-size=10000000

# gst-launch-1.0 shmsrc socket-path=/tmp/foo ! h264parse ! avdec_h264 ! videoconvert ! ximagesink

# gst-launch-1.0 shmsrc socket-path=/tmp/foo ! video/x-raw, format=BGR ,width=1920,height=1080,framerate=30/1 ! videoconvert ! ximagesink
