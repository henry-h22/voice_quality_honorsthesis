import pandas as pd
import os.path

VILLAGE_SPLIT_LANGUAGES = ['Yi', 'Bo']

def filepath(tableLine: pd.core.series.Series) -> str:
    """Given a dataframe row, returns the filepath to the EGG file, as a string."""
    language = tableLine['language']
    variety = tableLine['language_variety']
    filename = tableLine['filename']

    # These are various catches!
    if language == 'Gujarati': 
        filename = filename.replace("_Audio", "_ch1")
    if language == 'Yi' and '_tone_' in filename:
        filename = filename.replace("_tone_", '')

    boCatch = ' ' if (language == 'Bo' and variety == 'Village 1') else '' # this is because the Bo Village 1 files end in a random space
    villageSplit = language in VILLAGE_SPLIT_LANGUAGES
    divider = f'/{variety}/' if villageSplit else '/'

    return f'egg_melt/{language}{divider}{filename}{boCatch}.wav'


def random_test_file(df: pd.DataFrame) -> pd.core.series.Series:
    """Grabs a random filepath that we definitely have as both a wav and in the csv. \\
    Returns the dataframe row, as we need that!"""
    attempts = 0
    while True:
        candidateRow = df.sample(1)
        for _, row in candidateRow.iterrows():
            filepath_ = filepath(row)
            if os.path.isfile(filepath_):
                print(f'Found file after {attempts} attempts.')
                return candidateRow
            attempts += 1


# TODO: GET A SENSE OF HOW MANY WAV FILES WE HAVE THAT DONT EXIST IN THE CSV, AND VICE VERSA
# TODO: get hmong files to wav

# list of anamolies:
# - gujarati "Audio" -> ch1 (fixed!)
# - also: gujarati M1 data is not here, the M1 folder just has M10 data but again. :(
# - hmong "_Audio" -> ø (also pcxuirer womp)
# - i dont remember if luchun has anything up (it doesn't)
# - mandarin F5 is in '.egg' format. boooooo
# - bo (end space!) FIXED
# - yi (village split) FIXED