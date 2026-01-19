import pandas as pd

VILLAGE_SPLIT_LANGUAGES = ['Yi', 'Bo']

def filepath(tableLine: pd.core.series.Series) -> str:
    """Given a dataframe row, returns the filepath to the EGG file, as a string."""
    language = tableLine.language

    # These are various catches

    boCatch = ' ' if language == "Bo" else '' # this is because the Bo files end in a random space

    if language in VILLAGE_SPLIT_LANGUAGES: villageSplit = True
    divider = f'/{tableLine.language_variety}/' if villageSplit else '/'
    # TODO more language-specific checks


    return f'egg_melt/{language}{divider}{tableLine.filename}{boCatch}.wav'

def sampleEndpoints(startTime: float, endTime: float, samplerate: int, timepoint: int = 5) -> int:
    """Given the start and end time in ms of the sound in question, as well as the sample rate, \\
    returns a tuple of the samples where we should start and end our slice"""

    targetTimepointStart = startTime + ((endTime - startTime) / 9) * timepoint
    if timepoint >= 9:
        targetTimepointEnd = endTime
    else:
        targetTimepointEnd = startTime + ((endTime - startTime) / 9) * (timepoint + 1)
    return int((samplerate * targetTimepointStart) / 1000), int((samplerate * targetTimepointEnd) / 1000)



# list of anamolies:
# - gujarati "Audio" -> ch1
# - hmong "_Audio" -> ø (also pcxuirer womp)
# - bo (end space!) FIXED
# - yi (village split) FIXED