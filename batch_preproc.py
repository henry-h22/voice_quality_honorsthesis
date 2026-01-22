import pandas as pd
from scipy.io import wavfile
from egg_io import *
from fpca_preprocess import *
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")
all_data = pd.read_csv("voiceSauce.csv")
TIMEPOINT = 4
skips = 0
egg_signals = []
filename_headers = []

for _, savedRow in all_data.iterrows():
    # if savedRow['language'] != 'Zapotec': continue

    try:
        samplerate, data = wavfile.read(filepath(savedRow))
    except FileNotFoundError:
        
        # print(filepath(savedRow))
        continue
    startSample, endSample = sampleEndpoints(savedRow.segment_start, savedRow.segment_end, samplerate, timepoint = TIMEPOINT)
    egg = data[startSample:endSample]
    
    peaks = pitchmark(egg, samplerate, savedRow.strF0)
    threshold = find_threshold(egg, peaks)

    try:
        clipped_egg = clip_egg(egg, threshold, peaks)
        doubleThreshold = False
    except ValueError:
        # skips += 1
        print(f'File {filepath(savedRow)} chose too low of a threshold. Womp!')
        continue
    except Exception:
        # skips += 1
        print(f'idek what {filepath(savedRow)} did wrong :/')
        continue

    final = normalize_egg(clipped_egg)

    if final[92] > 0.5 or final[550] > 0.75:
        skips += 1
        print(f'AHHHHHH {filepath(savedRow)}')
        continue

    egg_signals.append(final)
    filename_headers.append(savedRow['filename'])
    # plt.plot(final)

print(skips)
exportToFDA(egg_signals, filename_headers)
# plt.show()