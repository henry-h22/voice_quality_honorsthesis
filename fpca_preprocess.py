import numpy as np
from scipy.signal import find_peaks

def sampleEndpoints(startTime: float, endTime: float, samplerate: int, timepoint: int = 5, full_vowel_override = False) -> int:
    """Given the start and end time in ms of the sound in question, as well as the sample rate, \\
    returns a tuple of the samples where we should start and end our slice"""

    targetTimepointStart = startTime + ((endTime - startTime) / 9) * timepoint
    if timepoint >= 9:
        targetTimepointEnd = endTime
    else:
        targetTimepointEnd = startTime + ((endTime - startTime) / 9) * (timepoint + 3)
    if full_vowel_override:
        targetTimepointStart = startTime
        targetTimepointEnd = endTime
    return int((samplerate * targetTimepointStart) / 1000), int((samplerate * targetTimepointEnd) / 1000)


def pitchmark(egg: np.array, samplerate: int, F0: float) -> np.array:
    """This function is used to find the peaks in the egg signal. We need sample rate and F0 to make sure we don't double count!"""
    distance = int(0.7 * samplerate / F0)
    peaks, _ = find_peaks(egg, distance = distance)
    return peaks


def find_threshold(egg: np.array, peaks) -> float:
    """Given the signal, and the peak locations (in samples), this function returns the 25% threshold that will be used."""
    if len(peaks) < 3:
        if len(peaks) > 1:
            target_area = egg[peaks[0]:peaks[1]]
        else:
            target_area = egg
    else:
        target_area = egg[peaks[1]:peaks[2]]
    target_max = float(np.max(target_area))
    target_min = float(np.min(target_area))
    return target_min + ((target_max - target_min) / 4)


def clip_egg(egg: np.array, threshold: float, peaks: list[int]) -> np.array:
    """This function uses the threshold to give us JUST the portion of the signal we need for further analysis. Needs the sample location of the peaks just to be safe."""
    crosses = get_crosses(egg, threshold)
    if len(peaks) == 2:
        return egg[crosses[0]:crosses[-1]]
    
    # Find first cross following first peak:
    following_first_peak = [sample for sample in crosses if (sample > peaks[0] and sample < peaks[1])]
    beginning = min(following_first_peak)

    # Find the first cross following the third peak:
    following_third_peak = [sample for sample in crosses if (sample > peaks[2])]
    end = min(following_third_peak)

    return egg[beginning:end]


def get_crosses(egg: np.array, threshold: float) -> list[int]:
    samples_above_threshold = set(np.argwhere(egg >= threshold).flatten())
    crosses = []
    for i in range(1, len(egg)):
        if (i - 1 in samples_above_threshold) != (i in samples_above_threshold):
            crosses.append(i)
    return crosses

def clip_2_peaks_catch(egg: np.array, peaks: list[int], crosses: list[int]) -> np.array:
    return 


def clip_egg_old(egg: np.array, threshold: float, first_peak: int) -> np.array:
    """DEPRECATED! Use clip_egg!! \\
    This function uses the threshold to give us JUST the portion of the signal we need for further analysis. Needs the sample location of the first peak (peaks[0]) just to be safe."""
    rounded_off = egg[first_peak:]
    above_threshold = set(np.argwhere(rounded_off >= threshold).flatten())

    crosses = []
    for i in range(1, len(rounded_off)):
        if (i - 1 in above_threshold) != (i in above_threshold):
            crosses.append(i)
    
    return rounded_off[crosses[0]:crosses[4]]


def amp_normalize(egg: np.array) -> np.array:
    return (egg - float(np.min(egg))) / (float(np.max(egg)) - float(np.min(egg)))


def time_normalize(egg: np.array, length = 1000) -> np.array:
    original_length = len(egg)
    xp = np.arange(original_length)
    x = np.linspace(0, original_length - 1, num = length)
    return np.interp(x, xp, egg)


def normalize_egg(egg: np.array) -> np.array:
    """This function performs the amplitude- and time- normalization steps."""
    return time_normalize(amp_normalize(egg))

