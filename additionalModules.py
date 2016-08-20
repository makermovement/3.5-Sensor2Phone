def oneButtonGames(frqY):
    '''play games with one button as controller'''
    try:
        if frqY >204 and frqY <205 :  # Between 204 and 205 for rate = 15000 and chunksize = 1024, but varies
            print "spacebar detected"
            kbd = xaut.keyboard()
            kbd.click(65)  # 65 is the code for Space Bar..
    except:
        pass

def clap(x): # amplitude based
    '''When clap is heard, play Einaudi's I-gouri'''
    if(int(x)>=30000):
        print "clap sound heard"
        os.system("xdg-open test.mp3") # can exclusively specify vlc but xdg-open opens up the default app
        sys.exit()

def linearSlider(frqY):
    '''Move the slider based on the frequency'''
    mouse.move(frqY/10,300)# maybe we can include another circuit to control y-axis

def dataTX(source):
  ''' Data Transmission using the TRRS/TRS'''
  with open(source,"rb") as File:
      s = str((File.read()))
      data =[]
      for i in s:
          data.append(ord(i)*100) # You don't necessarily need to multiply by 100, you can multiply by any number. But 100 worked
      print np.int16(data)    # converts the data into 16-bit
      scipy.io.wavfile.write("t.wav",44100,np.int16(data))  # converts the data into wave file

      #Take this and store it as a wav file... PLay it at 44100 fps or if it permits even at higher frame rates 

def dataRX():
  ''' Data Reception using the TRRS/TRS'''
  inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,alsaaudio.PCM_NONBLOCK)
  z = ""
  # Set attributes: Mono, 8000 Hz, 16 bit little endian samples
  inp.setchannels(1)
  inp.setrate(44100)
  inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
  inp.setperiodsize(160)
  while True:
      l,data = inp.read()
      if l:
          x= audioop.max(data, 2)
          z = z + str(chr(x/100))  # since the data at the TX is multiplied by 100, we have to divide the data by 100

  f = open("hello"  , "wb")   
  f.write(str.decode('base64'))
  f.close()

def volumeControl(y):
    ''' Controls the volume of computer based on variation of resistance'''
    e = sum(y)/10.0   #average out the values for consistency       
    z= ((e/17000.0))*100 ##17000 was the maximum value obtained for mobile- pc transfer
                        ## Tweak z value as necessary
    if (z<=100 and z>90):
        print "Voluem set to 100%"
        k = 'amixer -D pulse sset Master '+str(100)+'%'
    elif(z<=90 and z>70):
        print "Volume set to 75%"
        k = 'amixer -D pulse sset Master '+str(75)+'%'
    elif(k<=70 and z >10):
        print "Volume set to 50%"
        k = 'amixer -D pulse sset Master '+str(50)+'%'
    elif(k<=10):
        print "Volume set to 25%"
        k = 'amixer -D pulse sset Master '+str(25)+'%'
    else:
        print "Volume set to 0%"
        k = 'amixer -D pulse sset Master '+str(0)+'%'
    os.system(str(k))

def ir_sensor():
  '''Digital IR sensor integration using the TRRS'''
    if frqY >8983 :
        print "No human nearby " + str(max(np.abs(fft_frame)))
    else:
        print "Human detected " + str(max(np.abs(fft_frame)))
