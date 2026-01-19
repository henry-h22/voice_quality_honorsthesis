import pandas as pd
import os.path

VILLAGE_SPLIT_LANGUAGES = ['Yi', 'Bo']

def filepath(tableLine: pd.core.series.Series) -> str:
    """Given a dataframe row, returns the filepath to the EGG file, as a string."""
    language = tableLine.language.item()

    # These are various catches!
    boCatch = ' ' if language == "Bo" else '' # this is because the Bo files end in a random space
    villageSplit = language in VILLAGE_SPLIT_LANGUAGES
    divider = f'/{tableLine.language_variety.item()}/' if villageSplit else '/'

    return f'egg_melt/{language}{divider}{tableLine.filename.item()}{boCatch}.wav'


def random_test_file(df: pd.DataFrame) -> pd.core.series.Series:
    """Grabs a random filepath that we definitely have as both a wav and in the csv. \\
    Returns the dataframe row, as we need that!"""
    attempts = 0
    while True:
        candidateRow = df.sample(1)
        filepath_ = filepath(candidateRow)
        if os.path.isfile(filepath_):
            print(f'Found file after {attempts} attempts.')
            return candidateRow
        attempts += 1


# TODO: GET A SENSE OF HOW MANY WAV FILES WE HAVE THAT DONT EXIST IN THE CSV, AND VICE VERSA
# TODO: get hmong files to wav

# list of anamolies:
# - gujarati "Audio" -> ch1
# - hmong "_Audio" -> ø (also pcxuirer womp)
# - i dont remember if luchun has anything up
# - ^ same w mandarin
# - bo (end space!) FIXED
# - yi (village split) FIXED