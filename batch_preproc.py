import pandas as pd
from scipy.io import wavfile
from egg_io import *
from fpca_preprocess import *
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")
all_data = pd.read_csv("voiceSauce.csv")
TIMEPOINT = 4

for _, savedRow in all_data.iterrows():
    if savedRow['language'] != 'Yi': continue

    try:
        samplerate, data = wavfile.read(filepath(savedRow))
    except FileNotFoundError:
        # skips += 1
        # print(filepath(savedRow))
        continue
    startSample, endSample = sampleEndpoints(savedRow.segment_start, savedRow.segment_end, samplerate, timepoint = TIMEPOINT)
    egg = data[startSample:endSample]
    
    peaks = pitchmark(egg, samplerate, savedRow.strF0)

    try:
        threshold = find_threshold(egg, peaks)
    except IndexError:
        print(f'file {filepath(savedRow)} fucked up')
        continue

    try:
        clipped_egg = clip_egg(egg, threshold, peaks[0])
    except IndexError:
        print(f'file {filepath(savedRow)} fucked up')
        continue

    final = normalize_egg(clipped_egg)

    plt.plot(final)

plt.show()