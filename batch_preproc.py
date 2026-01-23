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
VERBOSE = False

for _, savedRow in all_data.iterrows():
    if savedRow['language'] != 'Zapotec': continue

    try:
        samplerate, data = wavfile.read(filepath(savedRow))
    except FileNotFoundError:
        
        # print(filepath(savedRow))
        continue
    startSample, endSample = sampleEndpoints(savedRow.segment_start, savedRow.segment_end, samplerate, timepoint = TIMEPOINT)
    egg = data[startSample:endSample]
    egg = lowpass(egg, samplerate, 422)
    
    peaks = pitchmark(egg, samplerate, savedRow.strF0)
    threshold = find_threshold(egg, peaks)

    try:
        clipped_egg = clip_egg(egg, threshold, peaks)
        doubleThreshold = False
    except ValueError:
        skips += 1
        if VERBOSE: print(f'File {filepath(savedRow)} chose too low of a threshold. Womp!')
        continue
    except Exception:
        skips -= 1000
        if VERBOSE: print(f'idek what {filepath(savedRow)} did wrong :/')
        continue

    final = normalize_egg(clipped_egg)

    if final[92] > 0.5 or final[550] > 0.75:
        skips += 1
        if VERBOSE: print(f'AHHHHHH {filepath(savedRow)}')
        continue

    # egg_signals.append(final)
    # filename_headers.append(savedRow['filename'])
    plt.plot(final)

print(skips)
# exportToFDA(egg_signals, filename_headers)
plt.show()



# notes:
# What we want to know is whether certain languages benefit more from low-pass than others
# we're also still working on the cutoff freq
# Bo: 27 with 722, 64 with 522, 14 without, but the ones that are there are rough tbh. I'd say keep it. 722 best here
# Gujarati: 106 with 722, 177 with 522, 69 without, lots of visual craziness without, those extra 40 can go i fear
# Luchun: 21 with 722, 31 with 522, 16 without but its messy, why are we even doing this, the lowpass should so stay
# Mandarin: 2 with 722, 522 is crazy, looks terrible without it. 2 for everything. 222. we're keeping it
# Miao: we lose 1 with the addition of 722 cutoff lowpass-- small price to pay for much smoother lines. slay
# Yi: Looks much better with the 722 cutoff lowpass, and we only lose one, which looked bad anyway.
# Zapotec: 8 with 722, 10 with 522, 18 without. we're just doing 722 on all of them, final answer