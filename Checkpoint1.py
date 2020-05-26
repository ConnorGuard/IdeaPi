#Speech recognition module
import speech_recognition as sr
#Audio recording modules
import pyaudio
import wave
#Emailing modules
import sendgrid
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
#Other Modules needed
import sys
import os

form_1 = pyaudio.paInt16 # 16-bit resolution
chans = 1 # 1 channel
samp_rate = 44100 # 44.1kHz sampling rate
chunk = 4096 # 2^12 samples for buffer
record_secs = 10 # seconds to record
dev_index = 2 # device index found through raspberry pi
wav_output_filename = 'recording.wav' # name of .wav file
audio = pyaudio.PyAudio() # create pyaudio instantiation
# create pyaudio stream
stream = audio.open(format = form_1,rate = samp_rate,channels = chans, \
                    input_device_index = dev_index,input = True, \
                    frames_per_buffer=chunk)
print("recording for 10 seconds...")
frames = []
# loop through stream and append audio chunks to frame array
for ii in range(0,int((samp_rate/chunk)*record_secs)):
    data = stream.read(chunk)
    frames.append(data)

print("finished recording")
# stop the stream, close it, and terminate the pyaudio instantiation
stream.stop_stream()
stream.close()
audio.terminate()

# save the audio frames as .wav file
wavefile = wave.open(wav_output_filename,'wb')
wavefile.setnchannels(chans)
wavefile.setsampwidth(audio.get_sample_size(form_1))
wavefile.setframerate(samp_rate)
wavefile.writeframes(b''.join(frames))
wavefile.close()

# speech Recognition instantiation
r=sr.Recognizer()
#Get file recorded
file='recording.wav'
with sr.AudioFile(file) as source:
        #open audio file and listen to it
        audio=r.listen(source)
try:    
        #use google API to get Speech to Text
        Text=r.recognize_google(audio)
        #print text to terminal
        print('you said:' + Text)
        #save text to textfile
        textfile = open('newidea', 'w')
        textfile.write(Text)
        textfile.close()
        #send email with text
        print('Sending Email..')
        #email details
        message = Mail(from_email='Example.Example@gmail.com',
        to_emails ='Example.Example@gmail.com',
        subject='New Idea!',
        html_content='<strong>'+Text+'</strong>')
        #I should save the API key in an environment variable, but for this project I wont.
        #This is NOT my actual API key I used, for security to my personal Email I changed it.
        api = SendGridAPIClient('SG.HibevbcvNQlesdfgdfgdfvbdfvdfZMzLtSESFJICQ')
        #sends email
        response = api.send(message)
        #checks email status
        print(response.status_code, response.body, response.headers)
        print('Sent')
except Exception as e:
        #if no words were spoken in the audio, then it stop the program
        print(e)





