def sampleEndpoints(startTime: float, endTime: float, samplerate: int, timepoint: int = 5) -> int:
    """Given the start and end time in ms of the sound in question, as well as the sample rate, \\
    returns a tuple of the samples where we should start and end our slice"""

    targetTimepointStart = startTime + ((endTime - startTime) / 9) * timepoint
    if timepoint >= 9:
        targetTimepointEnd = endTime
    else:
        targetTimepointEnd = startTime + ((endTime - startTime) / 9) * (timepoint + 1)
    return int((samplerate * targetTimepointStart) / 1000), int((samplerate * targetTimepointEnd) / 1000)
