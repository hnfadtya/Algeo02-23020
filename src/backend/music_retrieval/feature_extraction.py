import numpy as np

def extract_features(pitches, magnitudes):
    atb = np.histogram(pitches, bins=128, range=(0, 127))[0]
    intervals = np.diff(pitches, axis=1)
    rtb = np.histogram(intervals, bins=255, range=(-127, 127))[0]
    first_tone_diffs = pitches - pitches[0]
    ftb = np.histogram(first_tone_diffs, bins=255, range=(-127, 127))[0]
    atb_norm = atb / np.sum(atb)
    rtb_norm = rtb / np.sum(rtb)
    ftb_norm = ftb / np.sum(ftb)
    return atb_norm, rtb_norm, ftb_norm
