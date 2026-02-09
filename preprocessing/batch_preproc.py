import pandas as pd
from scipy.io import wavfile
from egg_io import *
from fpca_preprocess import *
import matplotlib.pyplot as plt
import warnings
from soundfile import LibsndfileError
warnings.filterwarnings("ignore")
all_data = pd.read_csv("voiceSauce.csv")
TIMEPOINT = 5 # hey Hmong wants 5 but some languages may be better off with 4? unsure

skips = 0
egg_signals = []
egg_ids = []
newVoiceSauceDataFrame = []
VERBOSE = True
language = 'Hmong'

for _, row in all_data.iterrows():
    if row['language'] != 'Hmong': continue

    try:
        egg, samplerate = loadFile(row, TIMEPOINT)
    except FileNotFoundError:
        # print(filepath(savedRow))
        continue
    except LibsndfileError:
        print(filepath(row))
        continue

    if len(egg) < 1000:
        skips += 10000
        continue

    egg = lowpass(egg, samplerate, 722)
    peaks = pitchmark(egg, samplerate, row.strF0)
    threshold = find_threshold(egg, peaks)

    try:
        clipped_egg = clip_egg(egg, threshold, peaks)
        doubleThreshold = False
    except ValueError:
        skips += 1
        if VERBOSE: print(f'File {filepath(row)} chose too low of a threshold. Womp!')
        continue
    except Exception:
        skips -= 1000 # this case hasn't been happening (hooray!)
        if VERBOSE: print(f'idek what {filepath(row)} did wrong :/')
        continue

    final = normalize_egg(clipped_egg)

    if final[92] > 0.5 or final[550] > 0.75:
        skips += 1
        if VERBOSE: print(f'AHHHHHH {filepath(row)}')
        continue

    egg_signals.append(final)
    token_id = hash(row['speaker_id'] + str(row['CPP']))
    egg_ids.append(token_id)
    row['token_id'] = token_id
    newVoiceSauceDataFrame.append(row)
    # plt.plot(final)

print(skips)
exportToFDA(egg_signals, egg_ids, newVoiceSauceDataFrame, language = language)
# plt.show()


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

# TODO: Hmong fixes:
# We have Hmong stuff now! Exciting! Apparently 88 of the Hmong files have skips, turn Verbose on to check
# also 96 of them end up too short?? unsure what thats about, could look into it