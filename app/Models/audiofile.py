from app import application
from flask import request
from flask_pymongo import PyMongo
import pyAudioAnalysis , ffmpeg, pymongo, pydub, os, uuid, io, datetime
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
import numpy as np
import matplotlib.ticker as ticker
import subprocess

class Audiofile:
    def __init__(self):
        fileaswhole = request.files["audiofile"]
        self.namewithextension = fileaswhole.filename
        self.name = os.path.splitext(fileaswhole.filename)[0]
        self.length = "NOTYETANALYSED"
        self.tempo_from_spotify = 0
        self.wavormp3 = True
        self.spotifyID = "NONE"
        self.bitrate = "NOTYETANALYSED"
        self.size = request.cookies.get("filesize")
        now = datetime.datetime.now()
        self.uploadtime = str(now.hour) + "-" + str(now.minute) + "-" + str(now.second)
        wronglyformatedpath = os.path.join(application.config['UPLOAD_FOLDER'], self.namewithextension)
        self.path = wronglyformatedpath.replace('\\','/')
        doc = fileaswhole
        doc.save(self.path)

    # convert all filetypes to WAV format 
    def convert_audiofile(self):
        try:                    
            if not (".wav") in self.path:   
                if not (".mp3") in self.path:
                    self.wavormp3 = False                     
                src = AudioSegment.from_file(self.path)
                dst = application.config['UPLOAD_FOLDER'] + self.name + ".wav"
                src.export(dst, format="wav")
                os.remove(self.path)
                self.path = dst
                return "Goodconversion" , 200
            else:
                dst = application.config['UPLOAD_FOLDER'] + self.name + ".wav"
                os.rename(self.path, dst)
                self.path = dst
                return "The file was already in wav format!"                
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
        else:
            raise RuntimeError("Unsupported sample width")

        # http://schlameel.com/2017/06/09/interleaving-and-de-interleaving-data-with-python/
        deinterleaved = [signal[idx::wav_file.getnchannels()] for idx in range(wav_file.getnchannels())]

        #Get time from indices
        fs = wav_file.getframerate()
        Time=np.linspace(0, round(len(signal)/wav_file.getnchannels()/fs), round(len(signal)/wav_file.getnchannels()))
        #Plot
        plt.figure(figsize=(10, 4))
        plt.title('Signal Wave')
        plt.xlabel('Time (s)')
        plt.ylabel('Frequency (Hz)')
        for channel in deinterleaved:
            plt.plot(Time,channel, linewidth=.035)
            plt.savefig(application.config['SPEC_FOLDER'] + self.name + ".png", dpi=72)
        print("Thread 1 finished")
        
    # MEL SPECTROGRAM
    def librosa_spectrogram(self):
        y, sr = librosa.load(self.path, sr=None)
        librosa.feature.melspectrogram(y=y, sr=sr)
        D = np.abs(librosa.stft(y))
        S = librosa.feature.melspectrogram(S=D)
        # Passing through arguments to the Mel filters
        S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128,fmax=32000)
        plt.figure(figsize=(10, 4))
        librosa.display.specshow(librosa.power_to_db(S,ref=np.max),sr=sr,y_axis='mel', fmax=32000,x_axis='time')
        plt.colorbar(format='%+2.0f dB')
        plt.title('Mel spectrogram')
        plt.tight_layout()
        plt.savefig(application.config['MEL_FOLDER'] + self.name + ".png", dpi=72)
        print("Thread 4 finished")

    # instrumental/vocal Separator
    def separate_audiofile(self,numberOfStems):
        file = self.path
        if numberOfStems == 5:
            separator = Separator('spleeter:5stems')
        elif numberOfStems == 2:
            separator = Separator('spleeter:2stems')

        separator.separate_to_file(file, application.config['SEPARATED_FOLDER'])

        print("Thread 2 finished")

    def channel_audiofile(self):
        # file = self.path
        fs, data = wavfile.read(self.path)

        wavfile.write(application.config['CHANNEL_FOLDER'] + self.name + "L.Wav", fs, data[:, 0])
        wavfile.write(application.config['CHANNEL_FOLDER'] + self.name + "R.Wav", fs, data[:, 1])

        print("Thread 3 finished")

    def tempo_graph(self):
       # Estimate a static tempo
            
        y, sr = librosa.load(self.path)
        tempo = librosa.beat.beat_track(y=y, sr=sr)
        self.tempo = tempo
        different = False

        onset_env = librosa.onset.onset_strength(y, sr=sr)
        tempo = librosa.beat.tempo(onset_envelope=onset_env, sr=sr)
        tempo2 = librosa.beat.beat_track(y=y, sr=sr)
        try:
            if int(tempo) > int(tempo2)*0.80:
                different = True
            elif int(tempo2) > int(tempo)*0.80:
                different = True
        except:
            print("An error has occured"), 401
        tempo = np.asscalar(tempo)
        # Compute 2-second windowed autocorrelation
        hop_length = 512
        ac = librosa.autocorrelate(onset_env, 2 * sr // hop_length)
        freqs = librosa.tempo_frequencies(len(ac), sr=sr, hop_length=hop_length)
        # Plot on a BPM axis.  We skip the first (0-lag) bin.
        plt.figure(figsize=(8,5))
        plt.semilogx(freqs[1:], librosa.util.normalize(ac)[1:],
                    label='Onset autocorrelation', basex=2)
        plt.axvline(tempo, 0, 1, color='r', alpha=0.75, linestyle='--',
                label='Tempo: {:.1f} BPM(4/4)'.format(tempo))
        if different:
            tempo2 = np.asscalar(tempo2)
            plt.axvline(tempo2, 0, 2, color='y', alpha=0.75, linestyle='--', label='Possible Tempo: {:.1f} BPM '.format(tempo2))
        plt.xlabel('Tempo (BPM)')
        plt.grid()
        plt.title('Static tempo estimation')
        plt.legend(frameon=True)
        plt.axis('tight')
        plt.savefig(application.config['TEMPO_FOLDER'] + self.name + ".png", dpi=72)
        print("Thread 5 finished")


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
        fig = plt.figure(num=None, figsize=(12, 7.5), dpi=72)
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
        plt.savefig(application.config['QUALITY_FOLDER'] + self.name + ".png")
        print("Thread 6 finished")
    