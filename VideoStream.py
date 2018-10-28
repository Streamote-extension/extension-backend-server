import streamlink
import numpy
from threading import Thread
import subprocess as sp
from queue import Queue

class Videostream:
    def __init__(self, twitchUrl, queueSize = 128, resolution = '360p\', n_frame = 10):
        self.stopThread = False
        self. twitchUrl = twitchUrl
        self.res = resolution
        self.n_frame = n_frame

        self.Q = Queue(maxsize = queueSize )
        streamCheckSanity = self.create_pipe()

        if streamCheckSanity:
                self.start_buffer()
        
    def create_pipe (self):
        streamerName = self.twitchUrl.split("/")[3]

        try:
            stream = streamlink.streams(self.twitchUrl)
        except streamlink.exceptions.NoPluginError:
            print("No stream is on for " + streamerName)
            return False
        except:
            print("No stream on at all " + streamerName)
            return False
        
        resolutions = {'360p': {"byte_length": 640, "byte_width": 360}, '480p': {"byte_length": 854, "byte_width": 480}, '720p': {"byte_length": 1280, "byte_width": 720}, '1080p': {"byte_length": 1920, "byte_width": 1080}}

        if self.res in stream:
            finalRes = self.res
        else:
            for key in resolutions:
                if key != self.res and key in stream:
                    print("USED FALL BACK " + key)
                    finalRes = key
                    break
                else: 
                    print("Stream not Found " + streamerName)
                    return False

        self.byte_length = resolutions[finalRes]["byte_length"]
        self.byte_width = resolutions[finalRes]["byte_width"]

        print("FINAL RES " + finalRes + " " + streamerName)

        stream = streams[finalRes]
        self.stream_url = stream.url
                
        self.pipe = sp.Popen(['/home/sd092/ffmpeg-git-20180111-32bit-static/ffmpeg', "-i", self.stream_url,
                         "-loglevel", "quiet",  # no text output
                         "-an",  # disable audio
                         "-f", "image2pipe",
                         "-pix_fmt", "bgr24",
                         "-vcodec", "rawvideo", "-"],
                        stdin=sp.PIPE, stdout=sp.PIPE)
        return True

    def start_buffer(self):
        thr = Thread(target=self.update_buffer,args =())
        thr.daemon = True
        thr.start()
        return self

    def update_buffer(self):
        
        frame_count = 0

        while True:

            if frame_count % self.n_frame == 0:

                raw_image = self.pipe.stdout.read(self.byte_length * self.byte_width * 3)

                frame = numpy.fromstring(raw_image, dtype = 'uint8').reshape((self.byte_width, self.byte_length, 3))

                if not self.Q.full():
                    self.Q.put(frame)
                    count_frame +=1
                else:
                    count_frame += 1 
                    continue

    def read(self):
        return self.Q.get()
    
    def more(self):
        return self.Q.qsize() > 0

    def stop(self):
        self.stopThread = True
        
