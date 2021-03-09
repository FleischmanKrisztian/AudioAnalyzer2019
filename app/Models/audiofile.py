from app import application
from flask import request
from flask_pymongo import PyMongo
import ffmpeg, pymongo, pydub, os, uuid, io, datetime
from pydub import AudioSegment
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import spleeter
import wave
import librosa
import librosa.display
from spleeter.separator import Separator
from scipy import signal
from scipy.io import wavfile
import math
import os
import sys
import wave
import threading
import numpy as np
import matplotlib.ticker as ticker
import subprocess

class Audiofile:
    def __init__(self):
        fileaswhole = request.files["audiofile"]
        self.namewithextension = fileaswhole.filename
        self.numberofchannels = 0
        self.name = os.path.splitext(fileaswhole.filename)[0]
        self.wavormp3 = True
        wronglyformatedpath = os.path.join(application.config['TESTING_PATH'], self.namewithextension)
        self.path = wronglyformatedpath.replace('\\','/')
        doc = fileaswhole
        os.makedirs(application.config['TESTING_PATH'],exist_ok=True)
        doc.save(self.path)

    def generatedata(self):
            t1 = threading.Thread(target=self.spectrogram_audiofile)
            t1.start()
            t2 = threading.Thread(target=self.separate_audiofile,args=[2])
            t2.start()
            t3 = threading.Thread(target=self.channel_audiofile)
            t3.start()
            t1.join()
            t4 = threading.Thread(target=self.librosa_spectrogram)
            t4.start()
            t4.join()
            t5 = threading.Thread(target=self.tempo_graph)
            t5.start()
            t5.join()    
            t6 = threading.Thread(target=self.quality_spectrogram)
            t6.start()
            t7 = threading.Thread(target=self,args=[request.cookies.get('email')])
            t7.start()
            t7.join()
            t6.join()
            t2.join()

            # The spleeter thread leaves behind alien threads which i could not get to delete and after 5-6 audiofiles the application runs out of memory and crashes the whole PC
            # for thread in threading.enumerate():
            #     print(thread.name)

            # for thread in threading.enumerate():
            #     threadstr = str(thread.name)
            #     if threadstr.find('Thread-') != -1:
            #         number = threadstr[7:9]
            #         if int(number) != 1:
            #             # thread.join()
                        
            #             print("Ezt kitorolnem")

            # for thread in threading.enumerate():
            #     print(thread.name)   

    # convert all filetypes to WAV format
    def convert_audiofile(self):
        try:                    
            if not (".wav") in self.path:   
                if not (".mp3") in self.path:
                    self.wavormp3 = False                     
                src = AudioSegment.from_file(self.path)
                dst = application.config['UPLOAD_FOLDER'] + self.name + ".wav"
                os.makedirs(application.config['UPLOAD_FOLDER'],exist_ok=True)
                src.export(dst, format="wav")
                os.remove(self.path)
                self.path = dst
                return "Goodconversion" , 200
            else:
                os.makedirs(application.config['UPLOAD_FOLDER'],exist_ok=True)
                dst = application.config['UPLOAD_FOLDER'] + self.name + ".wav"
                os.rename(self.path, dst)
                self.path = dst
                return "The file was already in wav format!" , 200                
        except:
            "The conversion from your file type to Wav was unsuccessful!", 401

    #NICE SPECTROGRAM
    def spectrogram_audiofile(self):
        file = self.path
        wav_file = wave.open(file,'r')
        signal = wav_file.readframes(-1)
        if wav_file.getsampwidth() == 1:
            signal = np.array(np.frombuffer(signal, dtype='UInt8')-128, dtype=np.int16)
        elif wav_file.getsampwidth() == 2:
            signal = np.frombuffer(signal, dtype=np.int16)
        elif wav_file.getsampwidth() == 4:
            signal = np.frombuffer(signal, dtype=np.int32)
        else:
            raise RuntimeError("Unsupported sample width")
        numberofchannels = wav_file.getnchannels()
        self.numberofchannels = numberofchannels

        # http://schlameel.com/2017/06/09/interleaving-and-de-interleaving-data-with-python/
        deinterleaved = [signal[idx::numberofchannels] for idx in range(numberofchannels)]

        #Get time from indices
        fs = wav_file.getframerate()
        Time=np.linspace(0, round(len(signal)/numberofchannels/fs), round(len(signal)/numberofchannels))
        #Plot
        plt.figure(figsize=(10, 4))
        plt.rcParams['axes.facecolor'] = 'black'
        plt.rcParams['savefig.facecolor'] = 'black'
        plt.rcParams['axes.edgecolor'] = 'white'
        plt.rcParams['lines.color'] = 'white'
        plt.rcParams['text.color'] = 'white'    
        plt.rcParams['xtick.color'] = 'white'    
        plt.rcParams['ytick.color'] = 'white'
        plt.rcParams['axes.labelcolor'] = 'white'
        plt.title('Signal Wave')
        plt.xlabel('Time (s)')
        plt.ylabel('Frequency (Hz)')
        for channel in deinterleaved:
            plt.plot(Time,channel, linewidth=.035)
            os.makedirs(application.config['CLIENT_IMAGES'],exist_ok=True)
            plt.savefig(application.config['CLIENT_IMAGES'] + self.name + "nice.png", dpi=72)
        
    # MEL SPECTROGRAM
    def librosa_spectrogram(self):
        y, sr = librosa.load(self.path, sr=None)
        librosa.feature.melspectrogram(y=y, sr=sr)
        D = np.abs(librosa.stft(y))
        S = librosa.feature.melspectrogram(S=D)
        # Passing through arguments to the Mel filters
        S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128,fmax=32000)
        plt.figure(figsize=(10, 4))
        plt.rcParams['axes.facecolor'] = 'black'
        plt.rcParams['savefig.facecolor'] = 'black'
        plt.rcParams['axes.edgecolor'] = 'white'
        plt.rcParams['lines.color'] = 'white'
        plt.rcParams['text.color'] = 'white'    
        plt.rcParams['xtick.color'] = 'white'    
        plt.rcParams['ytick.color'] = 'white'
        plt.rcParams['axes.labelcolor'] = 'white'
        librosa.display.specshow(librosa.power_to_db(S,ref=np.max),sr=sr,y_axis='mel', fmax=32000,x_axis='time')
        plt.colorbar(format='%+2.0f dB')
        plt.title('Mel spectrogram')
        plt.tight_layout()
        os.makedirs(application.config['CLIENT_IMAGES'],exist_ok=True)
        plt.savefig(application.config['CLIENT_IMAGES'] + self.name + "mel.png", dpi=72)

    # instrumental/vocal Separator
    def separate_audiofile(self,numberOfStems):
        file = self.path
        if numberOfStems == 5:
            separator = Separator('spleeter:5stems')
        elif numberOfStems == 2:
            separator = Separator('spleeter:2stems')
        os.makedirs(application.config['CLIENT_AUDIOFILES'],exist_ok=True)
        separator.separate_to_file(file, application.config['CLIENT_AUDIOFILES'])

    def channel_audiofile(self):
        fs, data = wavfile.read(self.path)
        os.makedirs(application.config['CLIENT_AUDIOFILES'],exist_ok=True)
        wavfile.write(application.config['CLIENT_AUDIOFILES'] + self.name + "L.Wav", fs, data[:, 0])
        wavfile.write(application.config['CLIENT_AUDIOFILES'] + self.name + "R.Wav", fs, data[:, 1])

    def tempo_graph(self):
            
        y, sr = librosa.load(self.path)
        tempo = librosa.beat.beat_track(y=y, sr=sr)
        different = False

        onset_env = librosa.onset.onset_strength(y, sr=sr)
        tempo = librosa.beat.tempo(onset_envelope=onset_env, sr=sr)
        tempo2 = librosa.beat.beat_track(y=y, sr=sr)
        try:
            if int(tempo) < int(tempo2[0])*0.85:
                different = True
            elif int(tempo2[0]) < int(tempo)*0.85:
                different = True
        except:
            return ("An error has occured"), 401
        tempo = np.asscalar(tempo)
        # Compute 2-second windowed autocorrelation
        hop_length = 512
        ac = librosa.autocorrelate(onset_env, 2 * sr // hop_length)
        freqs = librosa.tempo_frequencies(len(ac), sr=sr, hop_length=hop_length)
        # Plot on a BPM axis.  We skip the first (0-lag) bin.
        plt.figure(figsize=(10,4))
        plt.rcParams['axes.facecolor'] = 'black'
        plt.rcParams['savefig.facecolor'] = 'black'
        plt.rcParams['axes.edgecolor'] = 'white'
        plt.rcParams['lines.color'] = 'white'
        plt.rcParams['text.color'] = 'white'    
        plt.rcParams['xtick.color'] = 'white'    
        plt.rcParams['ytick.color'] = 'white'
        plt.rcParams['axes.labelcolor'] = 'white'
        plt.semilogx(freqs[1:], librosa.util.normalize(ac)[1:],
                    label='Onset autocorrelation', base=2)
        plt.axvline(tempo, 0, 1, color='r', alpha=0.75, linestyle='--',label='Tempo: {:.1f} BPM(4/4)'.format(tempo))
        if different:
            tempo2 = np.asscalar(tempo2[0])
            plt.axvline(tempo2, 0, 2, color='cyan', alpha=0.75, linestyle='--', label='Possible Tempo: {:.1f} BPM '.format(tempo2))
        plt.grid()
        plt.title('Static tempo estimation')
        plt.legend(frameon=True)
        plt.axis('tight')
        os.makedirs(application.config['CLIENT_IMAGES'],exist_ok=True)
        plt.savefig(application.config['CLIENT_IMAGES'] + self.name + "tempo.png", dpi=72)

    def quality_spectrogram(self):
        wavname=self.path
        wav = wave.open(wavname, 'r')  
        frames = wav.readframes(-1)
        inttype = 16 * wav.getnchannels()
        if not self.wavormp3:
            inttype = inttype * 2
        sound_info = np.fromstring(frames, 'int' + str(inttype))
        frame_rate = wav.getframerate()
        wav.close()
        plt.rcParams['axes.facecolor'] = 'black'
        plt.rcParams['savefig.facecolor'] = 'black'
        plt.rcParams['axes.edgecolor'] = 'white'
        plt.rcParams['lines.color'] = 'white'
        plt.rcParams['text.color'] = 'white'    
        plt.rcParams['xtick.color'] = 'white'    
        plt.rcParams['ytick.color'] = 'white'
        plt.rcParams['axes.labelcolor'] = 'white'
        fig = plt.figure(num=None, figsize=(10, 4), dpi=72)
        ax = fig.add_subplot(111)
        ax.xaxis.set_major_locator(ticker.MultipleLocator(30))
        ax.xaxis.set_minor_locator(ticker.MultipleLocator(5))
        ax.yaxis.set_major_locator(ticker.MultipleLocator(2000))
        ax.yaxis.set_minor_locator(ticker.MultipleLocator(1000))
        ax.tick_params(axis='both', direction='inout')
        plt.title('Spectrogram of:\n '  + self.name)
        plt.xlabel('time in seconds')
        plt.ylabel('Frequency (Khz)')
        plt.specgram(sound_info, Fs=frame_rate, cmap='gnuplot')
        cbar = plt.colorbar()
        cbar.ax.set_ylabel('dB')
        os.makedirs(application.config['CLIENT_IMAGES'],exist_ok=True)
        plt.savefig(application.config['CLIENT_IMAGES'] + self.name + "quality.png")