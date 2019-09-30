import glob
# import webrtcvad
import logging
# import wavSplit
from deepspeech import Model
from timeit import default_timer as timer
import contextlib
import wave


'''
Load the pre-trained model into the memory
@param models: Output Grapgh Protocol Buffer file
@param alphabet: Alphabet.txt file
@param lm: Language model file
@param trie: Trie file

@Retval
Returns a list [DeepSpeech Object, Model Load Time, LM Load Time]
'''
def load_model(models, alphabet, lm, trie):
    N_FEATURES = 26
    N_CONTEXT = 9
    BEAM_WIDTH = 500
    LM_ALPHA = 0.75
    LM_BETA = 1.85
    # print('loading model')
    model_load_start = timer()
    ds = Model(models, N_FEATURES, N_CONTEXT, alphabet, BEAM_WIDTH)
    model_load_end = timer() - model_load_start
    # print("Loaded model in %0.3fs." % (model_load_end))
    logging.debug("Loaded model in %0.3fs." % (model_load_end))

    lm_load_start = timer()
    ds.enableDecoderWithLM(alphabet, lm, trie, LM_ALPHA, LM_BETA)
    lm_load_end = timer() - lm_load_start
    logging.debug('Loaded language model in %0.3fs.' % (lm_load_end))
    # print('Loaded language model in %0.3fs.' % (lm_load_end))

    return [ds, model_load_end, lm_load_end]

'''
Run Inference on input audio file
@param ds: Deepspeech object
@param audio: Input audio for running inference on
@param fs: Sample rate of the input audio file

@Retval:
Returns a list [Inference, Inference Time, Audio Length]

'''
def stt(ds, audio, fs):
    inference_time = 0.0
    audio_length = len(audio) * (1 / 16000)

    # Run Deepspeech
    logging.debug('Running inference...')
    inference_start = timer()
    output = ds.stt(audio, fs)
    inference_end = timer() - inference_start
    inference_time += inference_end
    logging.debug('Inference took %0.3fs for %0.3fs audio file.' % (inference_end, audio_length))

    return [output, inference_time]

'''
Resolve directory path for the models and fetch each of them.
@param dirName: Path to the directory containing pre-trained models

@Retval:
Retunns a tuple containing each of the model files (pb, alphabet, lm and trie)
'''
def resolve_models(dirName):
    pb = glob.glob(dirName + "/*.pbmm")[0]
    logging.debug("Found Model: %s" % pb)

    alphabet = glob.glob(dirName + "/alphabet.txt")[0]
    logging.debug("Found Alphabet: %s" % alphabet)

    lm = glob.glob(dirName + "/lm.binary")[0]
    trie = glob.glob(dirName + "/trie")[0]
    logging.debug("Found Language Model: %s" % lm)
    logging.debug("Found Trie: %s" % trie)

    return pb, alphabet, lm, trie

def read_wave(path):
    """Reads a .wav file.

    Takes the path, and returns (PCM audio data, sample rate).
    """
    with contextlib.closing(wave.open(path, 'rb')) as wf:
        num_channels = wf.getnchannels()
        assert num_channels == 1
        sample_width = wf.getsampwidth()
        assert sample_width == 2
        sample_rate = wf.getframerate()
        assert sample_rate in (8000, 16000, 32000)
        frames = wf.getnframes()
        pcm_data = wf.readframes(frames)
        duration = frames / sample_rate
        return pcm_data, sample_rate, duration
