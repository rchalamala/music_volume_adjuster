import librosa
import os
import IPython.display as ipd 

# https://github.com/openmusic-project/openmusic/blob/master/OPENMUSIC/resources/lib/m1/libsndfile.dylib

def main1(file_path):
    x, sr = librosa.load(file_path)
    onset_frames = librosa.onset.onset_detect(x, sr=sr, wait=1, pre_avg=1, post_avg=1, pre_max=1, post_max=1)
    onset_times = librosa.frames_to_time(onset_frames)
    # remove extension, .mp3, .wav etc.
    file_name_no_extension, _ = os.path.splitext(file_path)
    output_name = file_name_no_extension + '.beatmap.txt'
    with open(output_name, 'wt') as f:
        f.write('\n'.join(['%.4f' % onset_time for onset_time in onset_times]))

def main2(file_path):
    x, sr = librosa.load(file_path) 
    ipd.Audio(x, rate=sr)
    tempo, beat_times = librosa.beat.beat_track(x, sr=sr, units='time')
    clicks = librosa.clicks(beat_times, sr=sr, length=len(x))
    ipd.Audio(x + clicks, rate=sr)

if __name__ == "__main__":
    main1('somebody_else.wav')