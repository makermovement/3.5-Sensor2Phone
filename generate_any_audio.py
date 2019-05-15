import struct
import numpy as np
from scipy import signal as sg

Fs = 44100                    ## Sampling Rate
f = 440                       ## Frequency (in Hz)
sample = 44100                ## Number of samples 
x = np.arange(sample)

####### sine wave ###########
y = 100*np.sin(2 * np.pi * f * x / Fs)

####### square wave ##########
# y = 100* sg.square(2 *np.pi * f *x / Fs )

####### square wave with Duty Cycle ##########
# y = 100* sg.square(2 *np.pi * f *x / Fs , duty = 0.8)

####### Sawtooth wave ########
# y = 100* sg.sawtooth(2 *np.pi * f *x / Fs )


f = open('test.wav','wb')
## Open as Signed 8-bit on Audacity - Watch Video for instructions

for i in y:
	f.write(struct.pack('b',int(i)))
f.close()

