# Python3 examples for the usage of GStreamer in OpenCV
<div style="text-align:center"><img src="https://i.imgflip.com/52sun5.jpg" width="400"/></div>

## I give you the light of ~~Eärendil~~ GStreamer, our most beloved ~~star~~ lib. May it be a light for you in dark places, when all other lights go out.

These examples, written in Python, will provide a good starting point for a lot, and the most common, applications of GStreamer and OpenCV. The snippets include following functionalities:
- Grabbing of standard OpenCV videocapture device
- Grabbing of v4l2src videocapture device via GStreamer
- Grabbing of shared memory sources
- Writing of OpenCV frames to shared memory, file and RTP
- Usage of hardware acceleration features for encoding and decoding
- Portable to CLI usage

As you are here, you probably know why you want to use GStreamer and OpenCV and I'm not gonna list all the advantages that GStreamer brings to the table.
**However, if you find this repo helpful or even remotely funny, consider leaving a star.**

# News
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

- _**Intel-CPUs** (Intel Haswell / Broadwell / Skylake with Intel HD / Iris Pro graphics / Apollo Lake) (**>= Gen4**)_
  - HW H264/H265 encoding and decoding
  - Bitrate control (CBR, VBR, CQP).
  - Selectable profiles up to High Profile.
  - Follow https://github.com/intel/gstreamer-media-SDK to install MSDK and gst-msdk
  - Detailed examples [here](https://github.com/intel/gstreamer-media-SDK/blob/master/README.USAGE)
  - _(not easy to setup, especially with parallel CUDA configuration; be warned)_
  - _x264enc: 25 ms (Software) ; mfxh264enc: 1 ms (HW enc)_: Achieved speedup on 1920x1080 px 
- _**NVIDIA GPUs**_
  - CUDA > 10.1, CuDNN > 7.5
  - CUDA accelerated H264/H265 encoding and decoding
  - Nvidia Video Codec SDK (check out [this](https://gist.github.com/corenel/a615b6f7eb5b5425aa49343a7b409200) to enable CUDA acc. H264/H265 enc/dec)
- _Recommended for **AMD GPUs**_
  - get a NVIDIA GPU (or feel free to contribute method)
  - not sponsored by NVIDIA, but by [them](https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstleyVEVO)
- Build & install **OpenCV 4.x** (4.2 works good for me)
  - Mind that CUDA requires opencv-contrib modules
  - enable deprecated PKG_CONFIG files. Idk why OpenCV thinks they aren't needed anymore.
  - highly recommend **cmake-gui** (`sudo apt-get install cmake-qt-gui`); search and click the features you want to have enabled
  - or enable gstreamer 1.0 support with `-D WITH_GSTREAMER=ON`

## Tests

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
