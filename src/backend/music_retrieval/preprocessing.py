import librosa
import mido
import numpy as np

def process_audio(audio_path):
    if audio_path.endswith('.wav'):
        y, sr = librosa.load(audio_path, mono=True)
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        y_aligned = librosa.effects.time_stretch(y, rate=tempo/120.0)
    elif audio_path.endswith('.mid'):
        midi = mido.MidiFile(audio_path)
        pitches = [msg.note for msg in midi.play() if msg.type == 'note_on']
        y_aligned = np.array(pitches)
    else:
        raise ValueError("Unsupported file format")
    
    pitches, magnitudes = librosa.piptrack(y=y_aligned, sr=sr)
    return pitches, magnitudes
