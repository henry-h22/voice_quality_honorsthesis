import pandas as pd
import numpy as np
import os.path
from scipy.io import wavfile
import soundfile as sf
from fpca_preprocess import sampleEndpoints

VILLAGE_SPLIT_LANGUAGES = ['Yi', 'Bo']

def loadFile(tableLine: pd.core.series.Series, timepoint: int) -> tuple[np.array, int]:
    """This function takes in a dataframe row, and returns the key area of the signal."""
    filepath_string = filepath(tableLine)
    if filepath_string[-3:] == 'pmf':
        # the Hmong files are stored as .pmf files, which take a bit of extra wrangling
        samplerate = 20000
        raw_data, _ = sf.read(
            filepath_string, channels = 1, samplerate = samplerate, dtype = 'float32', 
            format = 'RAW', subtype = 'FLOAT', endian = 'LITTLE'
        )
        egg_start_sample = max(np.argmax(raw_data[1000:]), np.argmin(raw_data[1000:])) + 1000
        data = raw_data[egg_start_sample:]
    else:
        samplerate, data = wavfile.read(filepath_string)
    
    startSample, endSample = sampleEndpoints(tableLine['segment_start'], tableLine['segment_end'], samplerate, timepoint = timepoint)
    
    return data[startSample:endSample], samplerate


def filepath(tableLine: pd.core.series.Series) -> str:
    """Given a dataframe row, returns the filepath to the EGG file, as a string."""
    language = tableLine['language']
    variety = tableLine['language_variety']
    filename = tableLine['filename']
    filetype = 'wav'

    # These are various catches!
    if language == 'Gujarati': 
        filename = filename.replace("_Audio", "_ch1")
    if language == 'Yi' and variety == 'Village 1' and (filename[:3] in ['f1_', 'F2_', 'M1_']):
        filename = filename[:3] + 'tone_' + filename[3:]
    if language == 'Luchun':
        filename = filename.replace("x005F_", '')
    if language == 'Hmong':
        filename = filename.replace("_Audio", '')
        filetype = 'pmf'

    boCatch = ''
    if language == 'Bo': # this is because most of the Bo Village 1 files end in a random space
        if variety == 'Village 1':
            if tableLine['speaker_id'] != 'Bo_M2':
                boCatch = ' '
            
    
    villageSplit = language in VILLAGE_SPLIT_LANGUAGES
    divider = f'/{variety}/' if villageSplit else '/'

    return f'egg_melt/{language}{divider}{filename}{boCatch}.{filetype}'


def random_test_file(df: pd.DataFrame, filterLanguage: str = '/') -> pd.core.series.Series:
    """Grabs a random filepath that we definitely have as both a wav and in the csv. \\
    Returns the dataframe row, as we need that!"""
    attempts = 0
    while True:
        candidateRow = df.sample(1)
        for _, row in candidateRow.iterrows():
            filepath_ = filepath(row)
            if os.path.isfile(filepath_) and filterLanguage in filepath_:
                print(f'Found file after {attempts} attempts.')
                return row
            attempts += 1


def grabSpecificFile(df: pd.DataFrame, file: str) -> pd.core.series.Series:
    for _, row in df.iterrows():
        if filepath(row) == file:
            return row


def exportToFDA(egg_signals: list[np.array], filename_headers: list[str], dfList: list[pd.core.series.Series], language: str = 'none'):
    data_matrix = np.vstack(egg_signals).T
    path_addon = '' if language == 'none' else f'by_lang/{language}_'
    pd.DataFrame(data_matrix, columns = filename_headers).to_csv(f"{path_addon}egg_pulses.csv", index = False)
    pd.DataFrame(dfList).to_csv(f'{path_addon}voiceSauce_idd.csv', index = False)


# list of anamolies (important for filepath function)
# - gujarati "Audio" -> ch1 (fixed!)
# - also: gujarati M1 data is not here, the M1 folder just has M10 data but again. :(
# - hmong "_Audio" -> ø (also pcquirer womp) (I THINK THERES A PCQUIRER WORKAROUND!!!)
# - i dont remember if luchun has anything up (it doesn't) (well okay one minor thing)
# - mandarin F5 is in '.egg' format. boooooo (they account for 6 datapoints, so dont worry)
# - mandarin F42 is missing, but thats 4 rows so don't fret
# - bo (end space!) FIXED
# - yi (village split) FIXED