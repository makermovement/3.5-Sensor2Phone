import struct
import numpy as np
from scipy import signal as sg

sampling_rate = 44100                    ## Sampling Rate
freq = 440                               ## Frequency (in Hz)
samples = 44100                          ## Number of samples 
x = np.arange(samples)

####### sine wave ###########
y = 100*np.sin(2 * np.pi * freq * x / sampling_rate)

####### square wave ##########
# y = 100* sg.square(2 *np.pi * f *x / Fs )

####### square wave with Duty Cycle ##########
# y = 100* sg.square(2 *np.pi * f *x / Fs , duty = 0.8)

####### Sawtooth wave ########
# y = 100* sg.sawtooth(2 *np.pi * f *x / Fs )


f = open('test.wav','wb')
## Instructions to play test.wav on computer
## 1. Open as Signed 8-bit on Audacity - Watch Video at https://bit.ly/2YwmN9q for instructions
## 2. Or using SoX: play -t raw -r 44.1k -e signed -b 8 -c 1 test.wav

for i in y:
	f.write(struct.pack('b',int(i)))
f.close()

