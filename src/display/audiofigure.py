from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
import matplotlib.pyplot as plt
import numpy as np

from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtCore import QTimer

from audio.microphonerecorder import MicrophoneRecorder


# matplotlib figure showing audio signals and FFT
class AudioFigure(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.figure = plt.figure(figsize=(width, height),
                                 dpi=dpi,
                                 tight_layout=True)
        self.top_axes = self.figure.add_subplot(211)
        self.bot_axes = self.figure.add_subplot(212)

        FigureCanvasQTAgg.__init__(self, self.figure)
        self.setParent(parent)

        FigureCanvasQTAgg.setSizePolicy(self,
                                        QSizePolicy.Expanding,
                                        QSizePolicy.Expanding)
        FigureCanvasQTAgg.updateGeometry(self)

        # Create a timer for updating the plot
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(100)

        self.init_data()
        self.init_plot()

    # Initialise the x data and microphone recorder
    def init_data(self):
        # Start recording the microphone
        self.mic = MicrophoneRecorder()
        self.mic.start()

        # X for amplitude v time plot
        self.time = (np.arange(self.mic.chunksize, dtype=np.float32)
                     / self.mic.rate * 1000)
        # X for amplitude v frequency plot
        self.freq = np.fft.rfftfreq(self.mic.chunksize,
                                    1./self.mic.rate)

    # Initialise the plots
    def init_plot(self):
        # Top plot for amplitude v time
        self.top_axes.set_ylim(-32768, 32768)
        self.top_axes.set_xlim(0, self.time.max())
        self.top_axes.set_xlabel('time [ms]')
        self.top_axes.grid()
        # Fill with nothing
        self.top_line, = self.top_axes.plot(self.time,
                                            np.ones_like(self.time))

        # Bottom plot for amplitude v frequency
        self.bot_axes.set_ylim(0, 1)
        self.bot_axes.set_xlim(0, self.freq.max())
        self.bot_axes.set_xlabel('frequency [Hz]')
        # Fill with nothing
        self.bot_line, = self.bot_axes.plot(self.freq,
                                            np.ones_like(self.freq))

    # Function to handle new data from microphone
    def update_plot(self):
        # Return the frames from the microphone buffer
        frames = self.mic.get_frames()

        if len(frames) > 0:
            # Plot the last frame
            time_frame = frames[-1]
            # Set the time data
            self.top_line.set_data(self.time, time_frame)

            # Do a FFT on the data, get only the real component
            fft_frame = np.fft.rfft(time_frame)
            # Normalise the FFT amplitude to 1
            max_val = np.abs(fft_frame).max()
            if max_val == 0:
                max_val == 1
            fft_frame /= max_val
            # Set the frequency data
            self.bot_line.set_data(self.freq, np.abs(fft_frame))

            # Update the plot
            self.draw()
