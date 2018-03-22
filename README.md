

# python-opencv-gstreamer-examples
Python examples for grabbing video devices (e.g. webcam, video, ...) and interacting with GStreamer (Shared Memory, RTP Stream).

- Preliminars for Ubuntu 16.04.4 LTS
    - Install GStreamer (`apt-get install gstreamer1.0* libgstreamer-plugins-bad1.0-0 libgstreamer-plugins-base1.0-0 libgstreamer-plugins-base1.0-dev libgstreamer1.0 libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libgtk-3-dev`)
    - *optional* FFMPEG, QT
    - Build OpenCV > 3 without gstreamer 0.10 support: `-D WITH_GSTREAMER=ON -D WITH_GSTREAMER_0_10=OFF`
    
## Usage
- Test if installation was successful: `gst-launch-1.0 v4l2src ! xvimagesink`. You should see your webcam's image.

- [gst_device_to_shm](gst_device_to_shm.py) grabs the `VideoCapture(0)` and puts the raw image in a shared memory. Mind here to define your own webcam properties.
- [gst_shm_to_app](gst_shm_to_app.py) grabs the shared memory frame from [gst_device_to_shm](gst_device_to_shm.py) and pipes it to a VideoCapture.
- [gst_device_to_rtp](gst_device_to_rtp.py) grabs the `VideoCapture(0)`,encodes the frame and streams it to `rtp://localhost:5000`
- [gst_shm_to_rtp](gst_shm_to_rtp.py) grabs the shared memory frame from [gst_device_to_shm](gst_device_to_shm.py) ,encodes the frame and streams it to `rtp://localhost:5000`.
gst_shm_to_rtp.py

## Further informations
Inspired by [https://github.com/tik0/mat2gstreamer]