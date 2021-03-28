import os, os.path
import time, logging
from datetime import datetime

import deepspeech

import numpy as np

from stt.vadaudio import VADAudio
logging.basicConfig(level=20)

def main():
    # Load DeepSpeech model
    model_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'stt', 'models')
    model = deepspeech.Model(os.path.join(model_dir, 'deepspeech-0.9.3-models.pbmm'))
    model.enableExternalScorer(os.path.join(model_dir, 'deepspeech-0.9.3-models.scorer'))

    # Start session when seeing me

    # Start audio with VAD
    # agressiveness is 0-3 and affects how much it will try to filter speech
    vad_audio = VADAudio(aggressiveness=0,
                         device=None,
                         input_rate=16000,
                         file=None)
    print("Listening (ctrl-C to exit)...")
    frames = vad_audio.vad_collector()

    # Deepspeech model
    stream_context = model.createStream()
    wav_data = bytearray()
    for frame in frames:
        if frame is not None:
            logging.debug("streaming frame")
            stream_context.feedAudioContent(np.frombuffer(frame, np.int16))

        else:
            logging.debug("end utterence")
            text = stream_context.finishStream()
            vad_audio.stream.stop_stream()
            
            print("Recognized: %s" % text)
            if text != "":

                print(text)
            
            # Listen from microphone
            vad_audio.stream.start_stream()
            stream_context = model.createStream()

if __name__ == '__main__':
    main()
