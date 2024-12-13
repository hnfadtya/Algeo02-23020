# # import pyaudio
# # import numpy as np
# # import mido
# # from mido import MidiFile, MidiTrack, Message
# # import time

# # # Konfigurasi mikrofon
# # RATE = 44100  # Sampel per detik
# # CHANNELS = 1  # Mono
# # FORMAT = pyaudio.paInt16  # Format audio
# # FRAMES_PER_BUFFER = 1024  # Ukuran buffer audio

# # # Fungsi untuk memulai perekaman suara dari mikrofon
# # def record_audio():
# #     p = pyaudio.PyAudio()
# #     stream = p.open(format=FORMAT,
# #                     channels=CHANNELS,
# #                     rate=RATE,
# #                     input=True,
# #                     frames_per_buffer=FRAMES_PER_BUFFER)
# #     print("Mulai merekam...")
# #     frames = []
# #     for _ in range(0, int(RATE / FRAMES_PER_BUFFER * 5)):  # Rekam selama 5 detik
# #         data = stream.read(FRAMES_PER_BUFFER)
# #         frames.append(data)
# #     print("Perekaman selesai.")
# #     stream.stop_stream()
# #     stream.close()
# #     p.terminate()
# #     return np.frombuffer(b''.join(frames), dtype=np.int16)

# # # Fungsi untuk menganalisis frekuensi dari sinyal audio
# # def get_pitch(audio_data):
# #     # Melakukan FFT untuk mendapatkan spektrum frekuensi
# #     fft_data = np.fft.fft(audio_data)
# #     freqs = np.fft.fftfreq(len(audio_data), 1 / RATE)
# #     positive_freqs = freqs[:len(freqs)//2]
# #     positive_fft_data = np.abs(fft_data[:len(fft_data)//2])
    
# #     # Mencari frekuensi dominan (pitch utama)
# #     dominant_freq = positive_freqs[np.argmax(positive_fft_data)]
# #     return dominant_freq

# # # Fungsi untuk mengonversi frekuensi ke nomor MIDI
# # def freq_to_midi(frequency):
# #     if frequency == 0:
# #         return 0
# #     return int(round(69 + 12 * np.log2(frequency / 440.0)))

# # # Fungsi untuk membuat file MIDI
# # def create_midi(pitches):
# #     midi = mido.MidiFile()
# #     track = MidiTrack()
# #     midi.tracks.append(track)
# #     track.append(mido.Message('program_change', program=12))  # Program instrument

# #     for pitch in pitches:
# #         if pitch > 0:
# #             note = freq_to_midi(pitch)
# #             track.append(mido.Message('note_on', note=note, velocity=64, time=0))
# #             track.append(mido.Message('note_off', note=note, velocity=64, time=500))

# #     midi.save('output.mid')

# # # Proses utama
# # if __name__ == "__main__":
# #     audio_data = record_audio()

# #     dominant_freq = get_pitch(audio_data)
# #     print(f"Frekuensi dominan: {dominant_freq} Hz")
    
# #     # Menyusun urutan pitch untuk MIDI
# #     pitches = [dominant_freq]  # Jika lebih dari satu pitch, bisa ditambahkan ke list ini

# #     # Membuat file MIDI
# #     create_midi(pitches)
# #     print("File MIDI telah dibuat: output.mid")
# import pyaudio
# import wave
# import numpy as np
# from pydub import AudioSegment
# from mido import MidiFile, MidiTrack, Message

# # Fungsi untuk merekam audio
# def record_audio(output_filename, chunk=1024, format=pyaudio.paInt16, channels=1, rate=44100):
#     audio = pyaudio.PyAudio()
#     stream = audio.open(format=format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)
#     print("Tekan Enter untuk memulai rekaman...")
#     input()  # Tunggu untuk memulai
#     print("Rekaman dimulai. Tekan Enter lagi untuk berhenti.")
#     frames = []


#     try:
#         while True:
#             data = stream.read(chunk)
#             frames.append(data)
#     except KeyboardInterrupt:
#         pass
#     finally:
#         print("Tekan Enter untuk berhenti.")
#         input()  # Tunggu untuk berhenti

#     print("Rekaman selesai.")
#     stream.stop_stream()
#     stream.close()
#     audio.terminate()

#     with wave.open(output_filename, "wb") as wf:
#         wf.setnchannels(channels)
#         wf.setsampwidth(audio.get_sample_size(format))
#         wf.setframerate(rate)
#         wf.writeframes(b"".join(frames))

# # Fungsi untuk mengubah audio ke MIDI
# def audio_to_midi(input_audio_file, output_midi_file):
#     # Load audio file
#     audio = AudioSegment.from_file(input_audio_file)
#     samples = np.array(audio.get_array_of_samples())
#     duration = len(samples) / audio.frame_rate

#     # Generate MIDI
#     midi = MidiFile()
#     track = MidiTrack()
#     midi.tracks.append(track)

#     # Konversi sample ke MIDI notes (sederhana)
#     step = int(audio.frame_rate / 10)  # Ambil sampel setiap 0.1 detik
#     for i in range(0, len(samples), step):
#         amplitude = np.abs(samples[i:i+step]).mean()  # Ambil amplitudo rata-rata
#         note = int(60 + 12 * np.log2(amplitude / 1000 + 1)) if amplitude > 0 else 0  # Hitung pitch
#         velocity = min(127, max(0, int(amplitude / 256)))  # Sesuaikan velocity
#         if note > 0:
#             track.append(Message('note_on', note=note, velocity=velocity, time=0))
#             track.append(Message('note_off', note=note, velocity=velocity, time=480))

#     midi.save(output_midi_file)

# if __name__ == "__main__":
#     # Rekam audio
#     audio_filename = "recorded_audio.wav"
#     midi_filename = "output_midi.mid"
#     record_audio(audio_filename)

#     # Konversi ke MIDI
#     print("Mengonversi audio ke MIDI...")
#     audio_to_midi(audio_filename, midi_filename)
#     print(f"MIDI berhasil disimpan di {midi_filename}")
import pyaudio
import numpy as np
import librosa
import mido

def record_audio_to_array(duration=5, rate=44100, chunk=1024, channels=1):
    """
    Rekam audio dari mikrofon dan simpan data ke dalam array numpy.
    """
    p = pyaudio.PyAudio()

    # Konfigurasi stream
    stream = p.open(format=pyaudio.paInt16,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk)

    print("Mulai merekam...")
    frames = []

    for _ in range(0, int(rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(np.frombuffer(data, dtype=np.int16))  # Konversi data ke numpy array
    
    print("Selesai merekam.")
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Gabungkan semua frames menjadi satu array
    audio_data = np.hstack(frames)
    return audio_data.astype(np.float32) / 32768.0  # Normalisasi ke [-1, 1]

def detect_pitch_librosa(audio_array, sr):
    """
    Deteksi pitch menggunakan librosa.
    """
    pitches, magnitudes = librosa.piptrack(y=audio_array, sr=sr)
    detected_pitches = []

    # Iterasi melalui frame untuk mendapatkan pitch dominan di setiap waktu
    for i in range(pitches.shape[1]):
        pitch_values = pitches[:, i]
        if np.max(pitch_values) > 0:  # Jika ada pitch yang terdeteksi
            detected_pitch = np.argmax(pitch_values)  # Indeks pitch dominan
            freq = detected_pitch * sr / (2 * pitches.shape[0])  # Konversi ke frekuensi
            detected_pitches.append(freq)
        else:
            detected_pitches.append(0)
    
    return detected_pitches

def audio_to_midi_from_array(audio_array, output_file, rate=44100):
    """
    Ubah array audio menjadi file MIDI.
    """
    # Deteksi pitch
    pitches = detect_pitch_librosa(audio_array, rate)
    midi = mido.MidiFile()
    track = mido.MidiTrack()
    midi.tracks.append(track)

    time_step = 512 / rate  # Waktu per langkah (hop size 512 default di librosa)
    for i, pitch in enumerate(pitches):
        if pitch > 0:  # Pitch valid
            midi_note = int(librosa.hz_to_midi(pitch))  # Konversi frekuensi ke MIDI note
            # Tambahkan note on dan note off ke track
            track.append(mido.Message('note_on', note=midi_note, velocity=64, time=int(time_step * 1000)))
            track.append(mido.Message('note_off', note=midi_note, velocity=64, time=int(time_step * 1000)))

    midi.save(output_file)
    print(f"MIDI berhasil disimpan ke {output_file}")

def main():
    # Konfigurasi
    midi_file = "output.mid"
    record_duration = 15  # Durasi rekaman (dalam detik)

    # Rekam audio ke array
    audio_array = record_audio_to_array(duration=record_duration)

    # Ubah array audio menjadi file MIDI
    audio_to_midi_from_array(audio_array, midi_file)
    

# if __name__ == "__main__":
#     main()
