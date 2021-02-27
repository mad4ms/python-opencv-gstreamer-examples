import cv2

# Funny note. If you exec "export GST_DEBUG=4" and then try something like displaying your webcam on the autovideosink
# like this "gst-launch-1.0 v4l2src ! videoconvert ! autovideosink", the debug spits out all possible caps that you
# can actually copy and paste. (caps are the preferences for the cam .. the video/x-raw , format, res and stuff.

# The following string usually works on most webcams
webcam2appsink_YUY2_640_480 = "v4l2src device=/dev/video0 ! video/x-raw, format=YUY2, width=640, height=480, pixel-aspect-ratio=1/1, framerate=30/1 ! videoconvert ! appsink"

# mfxh264enc does all the HW encoding
appsink2file = "appsrc ! videoconvert ! mfxh264enc ! \
        video/x-h264, profile=baseline ! \
        matroskamux ! filesink location=the_gstreamer_enjoyer.mkv"

# Open the capture string
cap = cv2.VideoCapture(webcam2appsink_YUY2_640_480)

# Hardcoded image properties. Mind here to change them to your needs.
frame_width = 640
frame_height = 480
fps = 30.
show = True
# Create videowriter
out = cv2.VideoWriter(appsink2file, 0, fps, (frame_width, frame_height), True)

if not cap.isOpened():
    print("Cannot capture from camera. Exiting.")
    quit()

if not out:
    print("Cannot write. Exiting.")
    quit()

while True:
    ret, frame = cap.read()
    #
    if ret == False:
        break

    out.write(frame)
    if show:
        cv2.imshow("the_gstreamer_enjoyer", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
