import struct
import numpy as np
from scipy import signal as sg
import wave 

Fs = 44100                    ## Sampling Rate
f = 440                       ## Frequency (in Hz)
sample = 441000                ## Number of samples 
x = np.arange(sample)

####### sine wave ###########
y = 1000*np.sin(2 * np.pi * f * x / Fs)

####### square wave ##########
# y = 100* sg.square(2 *np.pi * f *x / Fs )

####### square wave with Duty Cycle ##########
# y = 100* sg.square(2 *np.pi * f *x / Fs , duty = 0.8)

####### Sawtooth wave ########
# y = 100* sg.sawtooth(2 *np.pi * f *x / Fs )


f = wave.open('test.wav','w')
f.setparams((2, 2, 44100, 0, 'NONE', 'not compressed'))

for i in y:
        print(i)
        f.writeframes(struct.pack('h',int(i)))
f.close()


