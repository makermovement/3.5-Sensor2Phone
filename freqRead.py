# -*- coding: utf-8 -*-

### THIS CODE PRINTS OUT THE FIRST MAXIMUM FREQUENCY AND ITS AMPLITUDE OF THE FFT
# Additional modules to be installed :
#  numpy       ----  www.numpy.org
#  matplotlib  ----  www.matplotlib.org
#  PyQt4       ----  www.riverbankcomputing.com/software/pyqt/download
#  pyAudio     ----  www.people.csail.mit.edu/hubert/pyaudio/

### TO TERMINATE PRESS CTRL + Z
import sys,os,time
import threading,operator
import atexit 
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from PyQt4 import QtGui, QtCore
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar

# class taken from the SciPy 2015 Vispy talk opening example 
# see https://github.com/vispy/vispy/pull/928

class MicrophoneRecorder(object):
    # Set the rate and chunksize here if you need it 
    def __init__(self, rate=44100 , chunksize=160):
        self.rate = rate    
        self.chunksize = chunksize
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16,
                                  channels=1,
                                  rate=self.rate,
                                  input=True,
                                  frames_per_buffer=self.chunksize,
                                  stream_callback=self.new_frame)
        self.lock = threading.Lock()
        self.stop = False
        self.frames = []
        atexit.register(self.close)

    def new_frame(self, data, frame_count, time_info, status):
        data = np.fromstring(data, 'int16')
        with self.lock:
            self.frames.append(data)
            if self.stop:
                return None, pyaudio.paComplete
        return None, pyaudio.paContinue
    
    def get_frames(self):
        with self.lock:
            frames = self.frames
            self.frames = []
            return frames
    
    def start(self):
        self.stream.start_stream()

    def close(self):
        with self.lock:
            self.stop = True
        self.stream.close()
        self.p.terminate()


class MplFigure(object):
    def __init__(self, parent):
        self.figure = plt.figure(facecolor='white')
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, parent)

class LiveFFTWidget(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.initUI()
        self.initData()       
        
    def initUI(self):
        # timer for calls, taken from:
        # http://ralsina.me/weblog/posts/BB974.html
        timer = QtCore.QTimer()
        timer.timeout.connect(self.freqRead)  #This is where the handleNewData is called from
        timer.start(50)
        # keep reference to timer        
        self.timer = timer
        
     
    def initData(self):
        mic = MicrophoneRecorder()
        mic.start()  

        # keeps reference to mic        
        self.mic = mic
        
        # computes the parameters that will be used during plotting
        self.freq_vect = np.fft.rfftfreq(mic.chunksize, 
                                         1./mic.rate)
        self.time_vect = np.arange(mic.chunksize, dtype=np.float32) / mic.rate * 1000
                                
    def freqRead(self):
        """ read the chunks and computes the fft """            
        frames = self.mic.get_frames()
        if len(frames) > 0:
            current_frame = frames[-1]
            fft_frame = np.fft.rfft(current_frame)   # absolute value of fft_frame will give the amplitude information
            frq = np.fft.rfftfreq(len(fft_frame))
            mY = np.abs(fft_frame)      # Find magnitude
            peakY = np.max(mY)          # Find max peak
            locY = np.argmax(mY)        # Find its location
            try:    
                frqY = frq[locY]*44100       # This 4000 comes from the rate 
                if frqY> 200 or frqY1>200:              # It makes no sense to print out values below 200 hz 
                    if frqY > 4500 :        # Above 4500 Hz, overtones are present, therefore eliminating them for now
                        frqY = frqY/2
                    else:
                        frqY = frqY
                    
                    if frqY >8983 :
                        print "No human nearby " + str(max(np.abs(fft_frame)))
                    else:
                        print "Human detected " + str(max(np.abs(fft_frame)))
                    # print frqY, max(np.abs(fft_frame))  # Print the frequency and its associated Amplitude value
            except:
                pass
