
from TTS.utils.synthesizer import Synthesizer
from TTS.utils.manage import ModelManager

import pyaudio
import wave

import os

MODEL = 'tts_models/en/ljspeech/speedy-speech-wn'

class MozillaTTS():

    def __init__(self):

        manager = ModelManager()
        model_path, config_path, model_item = manager.download_model(MODEL)
            
        vocoder_path, vocoder_config_path, _ = manager.download_model(model_item['default_vocoder'])

        # last arg is use kuda,
        self.synth = Synthesizer(model_path, config_path, vocoder_path, vocoder_config_path, False) 

    def say(self, text):

        # generate wav
        wav = self.synth.tts(text)
        # output TODO would be nice to play this without having to do file I/O...
        out_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'output.wav')
        self.synth.save_wav(wav, out_file,)

        # Open the sound file 
        chunk = 1024
        wf = wave.open(out_file, 'rb')

        # play wav
        p = pyaudio.PyAudio()

        # Open a .Stream object to write the WAV file to
        # 'output = True' indicates that the sound will be played rather than recorded
        stream = p.open(format = p.get_format_from_width(wf.getsampwidth()),
                        channels = wf.getnchannels(),
                        rate = wf.getframerate(),
                        output = True)

        # Play the sound by writing the audio data to the stream
        data = wf.readframes(chunk)
        while data != '':
            stream.write(data)
            data = wf.readframes(chunk)

        # Close and terminate the stream
        stream.close()
        p.terminate()

    