import os
from MIR import *



# Masukkan database 
# DATABASE pertama kali jika database dan query belum dimasukkan
path_database_folder = input("Masukkan path folder: ")
hasil_database =  proses_database (path_database_folder)
output_path = "C:/codingTingkat 2/backup algeo2/vektor_database.json"
save_json_in_batches(hasil_database,output_path,batch_size=100)
# print("database berhasil disimpan")


# Update database
update_midi_path = input("Masukkan Path ")
update_midi_database("vektor_database.json",update_midi_path)



# INPUT TESTER
# --------------1-----------------
#Masukkan query

path_file = input("Masukkan path: ")
hasil_midi = process_midi (path_file)

#-------------2------------------
wav_mic_file = "output_from_mic.wav"
record_duration = 20  # Durasi rekaman (dalam detik)
midi_mic_file = "output_from_mic.mid"
rekam_audio(record_duration,wav_mic_file,channels=1)
wav_to_midi(wav_mic_file,midi_mic_file)
hasil_midi = process_midi (midi_mic_file)


#query by humming
hasil_database = load_json("vektor_database.json")
result = query_by_humming (hasil_midi, hasil_database)
sorted_songs = olah_score_song(result)
print_score_song(sorted_songs)



