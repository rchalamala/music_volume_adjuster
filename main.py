import numpy as np
import math
import librosa
from librosa import display
import matplotlib.pyplot as plt


def get_onset_times(file_path):
    x, sr = librosa.load(file_path)
    display.waveshow(x, sr=sr)
    plt.show()
    #onset_frames = librosa.onset.onset_detect(x, sr=sr, wait=1, pre_avg=1, post_avg=1, pre_max=1, post_max=1)
    return librosa.onset.onset_detect(x, sr=sr, pre_avg=20, post_avg=20, wait=5, units='time')

def calculate_bpm(onset_times, outlier_percent):
    onset_time_beats = []

    for _ in range(len(onset_times)):
        onset_time_beats.append([])

    for i in range(len(onset_times)):
        for j in range(i + 1, len(onset_times)):
            bpm = (j - i + 1) * 60 / (onset_times[j] - onset_times[i])
            print(i, j, bpm)
            for k in range(i, j + 1):
                onset_time_beats[k].append(bpm)

    bpm = np.empty(len(onset_times), dtype='float32')

    for i in range(len(onset_times)):
        onset_time_beats[i].sort()
        beats = np.array(onset_time_beats[i])
        outlier_length = math.floor(outlier_percent * beats.shape[0])

        bpm[i] = np.mean(beats[outlier_length:beats.shape[0] - outlier_length])
        #bpm[i] = np.median(beats)

    return bpm

if __name__ == "__main__":
    # yt-dlp --extract-audio --audio-format wav "https://www.youtube.com/watch?v=yZqmarGShxg"

    onset_times = get_onset_times("music/start_it_over.wav")

    with open('onset_times.txt', 'w') as f:
        f.write('\n'.join(list(onset_times.astype(str))))

    bpm = calculate_bpm(onset_times, 0.1)

    plt.scatter(onset_times, bpm)
    plt.show()