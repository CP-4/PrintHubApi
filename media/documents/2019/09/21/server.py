import sys
import socket
import struct
# import binascii
import time, logging
from datetime import datetime
import threading, collections, queue, os, os.path
# from deepspeech import Model
import wavTranscriber
import numpy as np
# import wave
import argparse
import scipy.io.wavfile as wav
from threading import Semaphore

audio_queue = queue.Queue()
_fetch_audio_sema = Semaphore(1)

gbl_audio, sample_rate, audio_length = wavTranscriber.read_wave('audio.wav')
gbl_audio = np.frombuffer(gbl_audio, dtype=np.int16)

def main2(ARGS):
    if os.path.isdir(ARGS.model):
        model_dir = ARGS.model
        ARGS.model = os.path.join(model_dir, 'output_graph.pb')
        ARGS.alphabet = os.path.join(model_dir, ARGS.alphabet if ARGS.alphabet else 'alphabet.txt')
        ARGS.lm = os.path.join(model_dir, ARGS.lm)
        ARGS.trie = os.path.join(model_dir, ARGS.trie)
    threadName = threading.currentThread().name
    print(threadName + ':' + 'Initializing model...')
    logging.info("ARGS.model: %s", ARGS.model)
    logging.info("ARGS.alphabet: %s", ARGS.alphabet)
    print(threadName + ':' + 'ARGS.model: %s', ARGS.model)
    print(threadName + ':' + 'ARGS.alphabet: %s', ARGS.alphabet)

    model = deepspeech.Model(ARGS.model, ARGS.n_features, ARGS.n_context, ARGS.alphabet, ARGS.beam_width)


    if ARGS.lm and ARGS.trie:
        logging.info("ARGS.lm: %s", ARGS.lm)
        logging.info("ARGS.trie: %s", ARGS.trie)
        print('ARGS.lm: %s', ARGS.lm)
        print('ARGS.trie: %s', ARGS.trie)
        model.enableDecoderWithLM(ARGS.alphabet, ARGS.lm, ARGS.trie, ARGS.lm_alpha, ARGS.lm_beta)

    print(threadName + ':' + 'Model loded...')

    while (True):
        # print('.')
        if not audio_queue.empty():
            print(threadName + ':' + 'Inferencing')
            # fs, audio = wav.read(audio_queue.get())
            # text = model.stt(audio_queue.get(), 16000)
            # print(text)
            text = audio_queue.get()

def main(args):
    parser = argparse.ArgumentParser(description='Running multiple instances of DS on same port')
    parser.add_argument('--aggressive', type=int, choices=range(4), required=False,
                        help='Determines how aggressive filtering out non-speech is. (Interger between 0-3)')
    parser.add_argument('--audio', required=False,
                        help='Path to the audio file to run (WAV format)')
    parser.add_argument('--model', required=True,
                        help='Path to directory that contains all model files (output_graph, lm, trie and alphabet)')
    parser.add_argument('--stream', required=False, action='store_true',
                        help='To use deepspeech streaming interface')
    args = parser.parse_args()

    threadName = threading.currentThread().name

    # Point to a path containing the pre-trained models & resolve ~ if used
    dirName = os.path.expanduser(args.model)
    print(dirName)

    # Resolve all the paths of model files
    output_graph, alphabet, lm, trie = wavTranscriber.resolve_models(dirName)
    print(output_graph, alphabet, lm, trie)

    # Load output_graph, alpahbet, lm and trie
    model_retval = wavTranscriber.load_model(output_graph, alphabet, lm, trie)
    print(threadName + ':' + 'Model loded . . . ')



    while  True:
        # audio, sample_rate, audio_length = wavTranscriber.read_wave('audio.wav')

        with _fetch_audio_sema:
            audio = fetch_audio()

        print(threadName + ':' + 'audio_queue_after_get:' + str(audio_queue.qsize()))
        sample_rate = 16000
        audio = np.frombuffer(audio, dtype=np.int16)
        output = wavTranscriber.stt(model_retval[0], audio, sample_rate)
        print(threadName + ':' + output[0])

def fetch_audio():

    threadName = threading.currentThread().name

    while True:
        if not audio_queue.empty():
            print(threadName + ':' + 'audio_queue_before_get:' + str(audio_queue.qsize()))

            audio = audio_queue.get()
            if gbl_audio == audio:
                print('data conccr')
            else:
                print('data NOT conccr')

            return audio

if __name__ == '__main__':

    audio = bytearray()

    ARGS = sys.argv[1:]

    ds1 = threading.Thread(target=main, args=(ARGS, ), name='DS1')
    ds2 = threading.Thread(target=main, args=(ARGS, ), name='DS2')
    ds1.start()
    ds2.start()

    HOST = 'localhost'
    PORT = 8070

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.bind((HOST, PORT))
    except socket.error as msg:
        s.close()
        print('Bind Fail Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
        sys.exit()

    s.listen(1)
    # print('listening...')
    while True:
        c, addr = s.accept()
        # print ('Got connection from', addr)
        # send a thank you message to the client.
        c.send(str.encode('connected'))

        while True:
            l = c.recv(1024)
            if not l: break
            audio.extend(l)

        with open('output.wav','wb') as f:
            f.write(audio)

        gbl_audio = np.frombuffer(audio, dtype=np.int16)
        audio_queue.put(audio)
        # print(audio_queue.qsize())

        # Close the connection with the client
        c.close()
        pass
