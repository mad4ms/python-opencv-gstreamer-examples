# Python3 examples for the usage of GStreamer in OpenCV
<p align="center"><img src="https://i.imgflip.com/52sun5.jpg" width="400"/></p>

### I give you the light of ~~Eärendil~~ GStreamer, our most beloved ~~star~~ lib. May it be a light for you in dark places, when all other lights go out.

## Short intro
These examples, written in Python, will provide a good starting point for a lot, and the most common, applications of GStreamer and OpenCV. The snippets mainly use OpenCV's VideoWriter and VideoCapture object, and include the following functionalities:
- Grabbing of standard OpenCV videocapture device
 ``` python
 import cv2

# Cam properties
fps = 30.
frame_width = 1920
frame_height = 1080
# Create capture
cap = cv2.VideoCapture(0)
# Set camera properties
cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
cap.set(cv2.CAP_PROP_FPS, fps)
 ```

- Grabbing of v4l2src videocapture device via GStreamer
 ``` python
# The following string usually works on most webcams
webcam2appsink_YUY2_640_480 = "v4l2src device=/dev/video0 ! video/x-raw, format=YUY2, width=640, height=480, pixel-aspect-ratio=1/1, framerate=30/1 ! videoconvert ! appsink"
 ```
- Writing of OpenCV frames to shared memory
 ``` python
gst_str = "appsrc ! videoconvert ! shmsink socket-path=/tmp/foo sync=true wait-for-connection=false shm-size=10000000"
 ```
- Grabbing of shared memory sources
 ``` python
cap = cv2.VideoCapture("shmsrc socket-path=/tmp/foo ! video/x-raw, format=BGR, width=640, height=480, pixel-aspect-ratio=1/1, framerate=30/1 ! decodebin ! videoconvert ! appsink")
 ```
- Writing of OpenCV frames to shared memory, file and RTP
 ``` python
gst_str_rtp = "appsrc ! videoconvert ! x264enc noise-reduction=10000 tune=zerolatency byte-stream=true threads=4 " \
              " ! h264parse ! mpegtsmux ! rtpmp2tpay ! udpsink host=127.0.0.1 port=5000"
 ```
- Usage of hardware acceleration features for encoding and decoding
 ``` python
# mfxh264enc does all the HW encoding on the INTEL HD GPU
appsink2file = "appsrc ! videoconvert ! mfxh264enc ! \
        video/x-h264, profile=baseline ! \
        matroskamux ! filesink location=the_gstreamer_enjoyer.mkv"
 ```
- Portable to CLI usage

Since you are here, you probably know why you want to use GStreamer and OpenCV and I'm not gonna list all the advantages that GStreamer brings to the table. **However, if you find this repo helpful or even remotely funny, consider leaving a star.** Or not. Your choice.

# News
- 2021-03-30 **Updated README; further install instructions; Raspi HW enc pipeline examples incoming**
- 2021-03-23 **Updated README; preparation for nvidia examples**
- 2021-03-01 **Updated for usage with Intel HD GPUs. NVIDIA examples as well as more complex stuff like splitting coming soon**
  




# Prerequisites

- Be a **unix enthusiast**. The **GPU encoding pipelines in GStreamer are extremly powerful, but are hard to install**. 
- **Ubuntu 20.04**
- **Correct drivers for GPU** (CUDA + CUDNN if necessary)
- Install **GStreamer**

  ``` sh
  sudo apt-get install gstreamer1.0* libgstreamer-plugins-bad1.0-0 libgstreamer-plugins-base1.0-0 libgstreamer-plugins-base1.0-dev libgstreamer1.0 libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libgtk-3-dev
  ```

- _optional_ FFMPEG, QT (+ OpenGL)

# Prerequisites for HW accelerated encoding/decoding

- _**Intel-CPUs**_
  - Supported platforms: Intel Haswell / Broadwell / Skylake with Intel HD / Iris Pro graphics / Apollo Lake) (**>= Gen4**)
  - Noticable features:
    - HW H264/H265 encoding and decoding
    - Bitrate control (CBR, VBR, CQP).
    - Selectable profiles up to High Profile.
  - Installation process (Honestly this is pretty frustrating Intel. I got very mad followed by getting drunk and yelling at the PC, but as far as i remember the process went something like this):
    - [LibVA](https://github.com/intel/libva)
    - [GmmLib](https://github.com/intel/gmmlib)
    - [Intel(R) Media Driver for VAAPI](https://github.com/intel/media-driver)
    - [Intel Media SDK](https://github.com/Intel-Media-SDK/MediaSDK#how-to-build)
    - [Gstreamer-Media-SDK](https://github.com/intel/gstreamer-media-SDK)
  
  - Further instructions are [here](https://blogs.igalia.com/vjaquez/2018/11/23/building-gst-msdk-with-mediasdk-opensource/), [here](https://github.com/Intel-Media-SDK/MediaSDK#how-to-build)
  - Detailed examples [here](https://github.com/intel/gstreamer-media-SDK/blob/master/README.USAGE)
  - Achieved speedup for writing a Full-HD frame (1920x1080px) to NVMe SSD:
    - _x264enc (Software encoding)_:  25 ms
    - _mfxh264enc (Hardware encoding)_: 1 ms
- _**NVIDIA GPUs**_
  - Supported platforms: CUDA enabled NVIDIA GPU ([List of CUDA GPUs](https://developer.nvidia.com/cuda-gpus)) (tested on GTX1070, GTX1080Ti and RTX 2070)
  - Noticable features:
    - HW H264/H265 encoding and decoding
    - Bitrate control (CBR, VBR, CQP)
  - Installation process (not so tedious, but still):
  - Get your correct drivers, CUDA and preferably CUDNN ([Link](https://askubuntu.com/questions/1077061/how-do-i-install-nvidia-and-cuda-drivers-into-ubuntu))
  - Follow [this](https://gist.github.com/corenel/a615b6f7eb5b5425aa49343a7b409200) guide (mind here to **checkout the correct branch for your GStreamer version**, for me it was 1.16.2 instead of 1.14.0) and **read the comments**.
  - If you're having problems finding the plugins, check the installation paths of GStreamer plugins. It may be found in `/usr/lib/x86_64-linux-gnu/gstreamer-1.0/`, or in `/usr/local/lib/gstreamer-1.0/` or even in your local path if you don't have `sudo`. Truth is that i copipasta'd the files until it matched. There might be a more elegant way to do this.
  
- _**AMD GPUs**_
  - get a NVIDIA GPU (or feel free to contribute method)
  - not sponsored by NVIDIA, but by [them](https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstleyVEVO)

# Building OpenCV
- Build & install **OpenCV 4.x** (4.2 works good for me; ROS works with it)
  - Mind here that we need to change **a lot** of CMake flags, so I highly recommend **cmake-gui** (`sudo apt-get install cmake-qt-gui`); search and click the features you want to have enabled (even after your exec'd a usual `cmake -D` flag)
  - [Guide](https://medium.com/@sb.jaduniv/how-to-install-opencv-4-2-0-with-cuda-10-1-on-ubuntu-20-04-lts-focal-fossa-bdc034109df3) for building with CUDA support on Ubuntu 20.04 ([18.04 here](https://gist.github.com/raulqf/f42c718a658cddc16f9df07ecc627be7))
  - Mind that CUDA requires opencv-contrib modules (do not forget to check out the correct version here as well)
  - enable deprecated OPENCV_GENERATE_PKGCONFIG files. Idk why OpenCV thinks they aren't needed anymore.
  - or enable gstreamer 1.0 support with `-D WITH_GSTREAMER=ON`

# Tests

- Test if **GStreamer installation** was successful (You should see your webcam's image):

``` sh
 $ gst-launch-1.0 v4l2src ! xvimagesink
 ```

- Test if **Intel MFX installation** was successful:
``` sh
$ gst-inspect-1.0 | grep mfx 
mfx: mfxh264dec: MFX H264 decoder
mfx: mfxhevcdec: MFX HEVC decoder
mfx: mfxh264enc: MFX H.264 encoder
mfx: mfxhevcenc: MFX H.265 encoder
```

- Test if **NVIDIA NVENC installation** was successful:

``` sh
$ gst-inspect-1.0 | grep nvenc 
nvenc: nvh264enc: NVENC H.264 Video Encoder
```

# Usage

- [gst_device_to_shm](gst_device_to_shm.py) grabs the `VideoCapture(0)` and puts the raw image in a shared memory. Mind here to define your own webcam properties.
- [gst_shm_to_app](gst_shm_to_app.py) grabs the shared memory frame from [gst_device_to_shm](gst_device_to_shm.py) and pipes it to a VideoCapture.
- [gst_device_to_rtp](gst_device_to_rtp.py) grabs the `VideoCapture(0)`,encodes the frame and streams it to `rtp://localhost:5000`
- [gst_shm_to_rtp](gst_shm_to_rtp.py) grabs the shared memory frame from [gst_device_to_shm](gst_device_to_shm.py) ,encodes the frame and streams it to `rtp://localhost:5000`.
- [gst_intel_device_to_app_to_file](gst_intel_device_to_app_to_file.py) grabs the `v4l2src /dev/video0` (usually webcam) to OpenCV format and writes it as an h264 encoded file.
- [gst_intel_device_to_app_to_rtp](gst_intel_device_to_app_to_rtp.py) grabs the `v4l2src /dev/video0` (usually webcam) to OpenCV format and writes it as an h264 encoded rtp stream. Use the provided `*.sdp` files for VLC viewer.
- [gst_shm_to_rtp](gst_shm_to_rtp.py) grabs the shared memory frame from [gst_device_to_shm](gst_device_to_shm.py) ,encodes the frame and streams it to `rtp://localhost:5000`.
- [gst_nvidia_device_to_app_to_file] (coming_soon™)
- [gst_nvidia_device_to_app_to_rtp] (coming_soon™)
- [gst_raspberrypi_device_to_app_to_file] (coming_soon™)

# Further informations

Inspired by https://github.com/tik0/mat2gstreamer

# Disclaimer

- Use at your own risk
- It works on my machine
