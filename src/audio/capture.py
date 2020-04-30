import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


RATE = 44100
CHUNK = 4096


class AudioSignal(object):

    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16,
                                  channels=1,
                                  input_device_index=2,
                                  rate=RATE,
                                  input=True,
                                  frames_per_buffer=CHUNK)

    def __call__(self):
        try:
            ydata = np.frombuffer(
                self.stream.read(CHUNK, exception_on_overflow=False),
                dtype=np.int16)
            xdata = np.linspace(0, len(ydata), len(ydata))
            return xdata, ydata
        except Exception:
            raise RuntimeError

    def __del__(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        

if __name__=='__main__':

    audio = AudioSignal()

    def frames():
        while True:
            yield audio()

    fig, ax = plt.subplots()
    xdata = []
    ydata = []
    ln, = plt.plot([], [])
    
    def init():
        ax.set_xlim(0, 4096)
        ax.set_ylim(-2**16/2, 2**16/2)
        return ln,

    def animate(args):
        xdata = args[0]
        ydata = 20*args[1]
        ln.set_data(xdata, ydata)
        return ln,

    ani = FuncAnimation(fig, animate, frames=frames,
                        init_func=init, blit=True)

    plt.grid()
    plt.show()

    del audio
