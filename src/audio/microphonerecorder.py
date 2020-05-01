import sys
import pyaudio
import threading
import atexit
import numpy as np


# Record waveforms from the microphone
class MicrophoneRecorder(object):

    def __init__(self, rate=4000, chunksize=1024):
        # rate = number of frames per second
        self.rate = rate
        # chunk = number of frames signal is split into
        self.chunksize = chunksize
        self.p = pyaudio.PyAudio()
        # Get correct audio channel for mac or pi
        dev_index = 0
        self.amp = 1.
        if sys.platform=='linux':
            dev_index = 2
            self.amp = 20.

        # Open the audio stream
        self.stream = self.p.open(format=pyaudio.paInt16,
                                  channels=1,
                                  rate=self.rate,
                                  input_device_index=dev_index,
                                  input=True,
                                  frames_per_buffer=self.chunksize,
                                  stream_callback=self.new_frame)

        # Thread the data to prevent gui freezing (maybe?)
        self.lock = threading.Lock()
        self.stop = False
        self.frames = []
        atexit.register(self.close)

    # Get frames from the stream
    def new_frame(self, data, frame_count, time_info, status):
        # Convert bytes to a numpy arrya
        data = self.amp*np.frombuffer(data, dtype=np.int16)
        # Append array to internal buffet
        with self.lock:
            self.frames.append(data)
            if self.stop:
                return None, pyaudio.paComplete
        return None, pyaudio.paContinue

    # Return frames from the internal buffer
    def get_frames(self):
        with self.lock:
            # Get the frames and clear the buffer
            frames = self.frames
            self.frames = []
            return frames

    # Start the stream
    def start(self):
        self.stream.start_stream()

    # Clean up stream on close
    def close(self):
        with self.lock:
            self.stop = True
        self.stream.close()
        self.p.terminate()
