

import librosa
import pretty_midi
import numpy as np

# def wav_to_midi(wav_file, midi_file, sr=22050):
#     # Load file WAV
#     audio, sr = librosa.load(wav_file, sr=sr)
    
#     # Deteksi pitch menggunakan fungsi librosa
#     pitches, magnitudes = librosa.piptrack(y=audio, sr=sr)
    
#     # Buat objek PrettyMIDI
#     midi = pretty_midi.PrettyMIDI()
#     instrument = pretty_midi.Instrument(program=0)  # Piano
    
#     # Iterasi setiap frame untuk mendeteksi pitch
#     for time_idx in range(pitches.shape[1]):
#         pitch_col = pitches[:, time_idx]
#         if np.max(pitch_col) > 0:  # Ada pitch yang terdeteksi
#             pitch_idx = np.argmax(pitch_col)
#             pitch = librosa.hz_to_midi(librosa.midi_to_hz(pitch_idx))
            
#             # Tambahkan note ke MIDI
#             note = pretty_midi.Note(
#                 velocity=100, 
#                 pitch=int(pitch), 
#                 start=time_idx * librosa.frames_to_time(1, sr=sr),
#                 end=(time_idx + 1) * librosa.frames_to_time(1, sr=sr)
#             )
#             instrument.notes.append(note)
    
#     midi.instruments.append(instrument)
#     midi.write(midi_file)
#     print(f"MIDI file saved to {midi_file}")


# Jalankan fungsi
# wav_file = "input.wav"
# midi_file = "output.mid"
# wav_to_midi(wav_file, midi_file)

#==============

import librosa
import pretty_midi
import numpy as np

def wav_to_midi(wav_file, midi_file, sr=22050):
    """
    Mengonversi file WAV menjadi file MIDI.

    Args:
        wav_file (str): Path ke file WAV input.
        midi_file (str): Path ke file MIDI output.
        sr (int): Sample rate untuk file WAV (default: 22050).
    """
    # Load file WAV
    audio, sr = librosa.load(wav_file, sr=sr)
    
    # Deteksi pitch menggunakan fungsi librosa
    pitches, magnitudes = librosa.piptrack(y=audio, sr=sr)
    
    # Buat objek PrettyMIDI
    midi = pretty_midi.PrettyMIDI()
    instrument = pretty_midi.Instrument(program=0)  # Piano
    
    # Iterasi setiap frame untuk mendeteksi pitch
    for time_idx in range(pitches.shape[1]):
        pitch_col = pitches[:, time_idx]
        if np.max(pitch_col) > 0:  # Ada pitch yang terdeteksi
            pitch_idx = np.argmax(pitch_col)
            # Konversi pitch ke MIDI note
            pitch_hz = librosa.midi_to_hz(pitch_idx)  # Dari index ke Hz
            pitch_midi = librosa.hz_to_midi(pitch_hz)  # Dari Hz ke MIDI
            
            # Pastikan pitch berada dalam rentang MIDI (0..127)
            if 0 <= pitch_midi <= 127:
                note = pretty_midi.Note(
                    velocity=100, 
                    pitch=int(pitch_midi), 
                    start=time_idx * librosa.frames_to_time(1, sr=sr),
                    end=(time_idx + 1) * librosa.frames_to_time(1, sr=sr)
                )
                instrument.notes.append(note)
    
    midi.instruments.append(instrument)
    midi.write(midi_file)
    print(f"MIDI file saved to {midi_file}")


#==============





# Fungsi untuk mengubah WAV menjadi MIDI
# def wav_to_midi(wav_file_path):
#     # Membaca file WAV
#     audio, sample_rate = sf.read(wav_file_path)

#     # Prediksi dengan model default
#     model_output, midi_data, _ = predict(audio, ICASSP_2022_MODEL, sample_rate)

#     # Mengembalikan data MIDI
#     return midi_data

# # Contoh penggunaan
# wav_file_path = "C:/coding/Tingkat 2/Tubes Algeo 2/Algeo02-23020/src/backend/music_retrieval/database/wav/blues.00001.wav"
# midi_data = wav_to_midi(wav_file_path)

# print(midi_data)


# Contoh penggunaan
# wav_file_path = "path/to/your/file.wav"
# midi_data = wav_to_midi(wav_file_path)

# print(midi_data)

# Contoh penggunaan
# wav_file_path = "path/to/your/file.wav"
# midi_data = wav_to_midi(wav_file_path)
# print(midi_data)

# # Contoh penggunaan
# wav_file_path = ".wav"
# midi_data = wav_to_midi(wav_file_path)

# # midi_data sekarang adalah file MIDI dalam format bytearray
# print(midi_data)
