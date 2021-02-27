# python-opencv-gstreamer-examples

Python examples for grabbing video devices (e.g. webcam, video, ...) and interacting with GStreamer (Shared Memory, RTP Stream).
**Updated for usage with Intel HD GPUs. NVIDIA examples as well as more complex stuff like splitting coming soon**

- (Updated Feb 2021) Preliminars for Ubuntu 20.04.1 LTS (with correct drivers for GPU)

  - Be a **unix enthusiast**. The **GPU encoding pipelines in GStreamer are extremly powerful, but are hard to install**.
  - Install **GStreamer**
    `sudo apt-get install gstreamer1.0* libgstreamer-plugins-bad1.0-0 libgstreamer-plugins-base1.0-0 libgstreamer-plugins-base1.0-dev libgstreamer1.0 libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libgtk-3-dev`)
  - _optional_ FFMPEG, QT (+ OpenGL)

  - _recommended for **Intel-CPUs** (with Intel HD GPU) (**> Gen7**)_
    - Hardware accelerated x264/hevc encoding and decoding https://github.com/intel/gstreamer-media-SDK
    - _(not easy to setup, especially with parallel CUDA configuration; be warned)_
  - _recommended for **NVIDIA GPUs**_
    - CUDA > 10.1, CuDNN > 7.5
    - NVidia Video Codec SDK (check out [this](https://gist.github.com/corenel/a615b6f7eb5b5425aa49343a7b409200) to enable CUDA acc. H264/H265 enc/dec)
  - _recommended for **AMD GPUs**_
    - get a NVIDIA GPU (or feel free to contribute method; please stop sending [this](https://i.redd.it/iipbbfhi69g61.png)
    - not sponsored by NVIDIA, but by [them](https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstleyVEVO)
  - Build & install **OpenCV 4.x** (4.2 works good for me)
    - Mind that CUDA requires opencv-contrib modules
    - enable deprecated PKG_CONFIG files. Idk why OpenCV thinks they aren't needed anymore.
    - highly recommend **cmake-gui** (`sudo apt-get install cmake-qt-gui`); search and click the features you want to have enabled
    - or enable gstreamer 1.0 support with `-D WITH_GSTREAMER=ON`

## Tests

- Test if **GStreamer installation** was successful: `gst-launch-1.0 v4l2src ! xvimagesink`. You should see your webcam's image.
- Test if **Intel MFX installation** was successful:
  `$ gst-inspect-1.0 | grep mfx`
  `mfx: mfxh264dec: MFX H264 decoder`
  `mfx: mfxhevcdec: MFX HEVC decoder`
  `mfx: mfxh264enc: MFX H.264 encoder`
  `mfx: mfxhevcenc: MFX H.265 encoder`
  `...`
- Test if **NVIDIA NVENC installation** was successful:
  `$ gst-inspect-1.0 | grep nvenc`
  `nvenc: nvh264enc: NVENC H.264 Video Encoder`

## Usage

- [gst_device_to_shm](gst_device_to_shm.py) grabs the `VideoCapture(0)` and puts the raw image in a shared memory. Mind here to define your own webcam properties.
- [gst_shm_to_app](gst_shm_to_app.py) grabs the shared memory frame from [gst_device_to_shm](gst_device_to_shm.py) and pipes it to a VideoCapture.
- [gst_device_to_rtp](gst_device_to_rtp.py) grabs the `VideoCapture(0)`,encodes the frame and streams it to `rtp://localhost:5000`
- [gst_shm_to_rtp](gst_shm_to_rtp.py) grabs the shared memory frame from [gst_device_to_shm](gst_device_to_shm.py) ,encodes the frame and streams it to `rtp://localhost:5000`.
- [gst_intel_device_to_app_to_file](gst_intel_device_to_app_to_file.py) grabs the `v4l2src /dev/video0` (usually webcam) to OpenCV format and writes it as an h264 encoded file.
- [gst_intel_device_to_app_to_rtp](gst_intel_device_to_app_to_rtp.py) grabs the `v4l2src /dev/video0` (usually webcam) to OpenCV format and writes it as an h264 encoded rtp stream. Use the provided `*.sdp` files for VLC viewer.
- [gst_shm_to_rtp](gst_shm_to_rtp.py) grabs the shared memory frame from [gst_device_to_shm](gst_device_to_shm.py) ,encodes the frame and streams it to `rtp://localhost:5000`.

## Further informations

Inspired by https://github.com/tik0/mat2gstreamer

## Disclaimer

- Use at your own risk
- It works on my machine
