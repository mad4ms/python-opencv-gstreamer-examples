import cv2
import gi
import sys
import json
import time
import signal
import numpy as np

gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GstRtspServer, GObject

#cv2.namedWindow('video_realtime_face', cv2.WINDOW_NORMAL)

def to_node(type, message):
    # convert to json and print (node helper will read from stdout)
    try:
        print(json.dumps({type: message}))
    except Exception:
        pass
    # stdout has to be flushed manually to prevent delays in the node helper communication
    sys.stdout.flush()

to_node("status", "Facerecognition started...")

def shutdown(self, signum):
    to_node("status", 'Shutdown: Cleaning up camera...')
    quit()

signal.signal(signal.SIGINT, shutdown)


class SensorFactory(GstRtspServer.RTSPMediaFactory):
    def __init__(self, **properties):
        super(SensorFactory, self).__init__(**properties)
        #self.cap = cv2.VideoCapture(0)
        self.cap = cv2.VideoCapture("shmsrc socket-path=/tmp/foo2 ! video/x-raw, format=BGR ,width=1920,height=1080,framerate=30/1 ! videoconvert ! video/x-raw, format=BGR ! appsink")
        #self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        #self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        self.number_frames = 0
        self.fps = 30.0
        self.duration = 1 / self.fps * Gst.SECOND  # duration of a frame in nanoseconds
        self.launch_string = 'appsrc name=source is-live=true block=true format=GST_FORMAT_TIME ' \
                             'caps=video/x-raw,format=BGR,width=1920,height=1080,framerate=30/1 ' \
                             '! videoconvert ! video/x-raw,format=I420 ' \
                             '! x264enc speed-preset=ultrafast tune=zerolatency threads=4 ' \
                             '! rtph264pay config-interval=1 name=pay0 pt=96'

    def on_need_data(self, src, lenght):
        if self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                #cv2.imshow("video_realtime_face", frame)
                #if cv2.waitKey(1) & 0xFF == ord('q'):
                #    return
                data = frame.tostring()
                buf = Gst.Buffer.new_allocate(None, len(data), None)
                buf.fill(0, data)
                buf.duration = self.duration
                timestamp = self.number_frames * self.duration
                buf.pts = buf.dts = int(timestamp)
                buf.offset = timestamp
                self.number_frames += 1
                retval = src.emit('push-buffer', buf)
                print('pushed buffer, frame {}, duration {} ns, durations {} s'.format(self.number_frames,
                                                                                       self.duration,
                                                                                       self.duration / Gst.SECOND))
                if retval != Gst.FlowReturn.OK:
                    print(retval)

    def do_create_element(self, url):
        return Gst.parse_launch(self.launch_string)

    def do_configure(self, rtsp_media):
        self.number_frames = 0
        appsrc = rtsp_media.get_element().get_child_by_name('source')
        appsrc.connect('need-data', self.on_need_data)


class GstServer(GstRtspServer.RTSPServer):
    def __init__(self, **properties):
        super(GstServer, self).__init__(**properties)
        self.factory = SensorFactory()
        self.factory.set_shared(True)
        self.get_mount_points().add_factory("/test", self.factory)
        self.attach(None)


def run():
    GObject.threads_init()
    Gst.init(None)

    server = GstServer()

    loop = GObject.MainLoop()
    loop.run()


#if __name__ == "__main__":
run()
