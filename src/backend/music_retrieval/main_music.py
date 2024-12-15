import os
from MIR import *
import numpy as np
from midi_json import *
from mic_to_wav import *
from convert_to_midi import *

# TEST_MIDI_PATH = "C:/coding/Tingkat 2/Tubes Algeo 2/Algeo02-23020/src/backend/music_retrieval/database/Remember_the_Time.mid"
# DATABASE_FOLDER = "C:/coding/Tingkat 2/Tubes Algeo 2/Algeo02-23020/src/backend/music_retrieval/database/midi"

menu = 0 
hasil_midi=0
hasil_database=0
hasil_database_json = 0
while ( menu != 7):
    print("============================================")
    print ("NGOLAH MUSIK NIHH BROOO !!!!")
    print("============================================")
    print()
    print("MENU: ")
    print ("1. Proses 1 file")
    print ("2. Proses database file")
    print ("3. Record audio")
    print ("4. Proses query")
    print ("5. Baca json file")
    print ("6. Update file")
    print ("7. Exit")
    menu = int (input ("Masukkan Menu: "))
    print()


    if (menu ==1 ):
        path_file = input("Masukkan path: ")
        hasil_midi = process_midi (path_file)
        print("print ga??")
        print("1. print")
        pilih = int (input())
        
        if pilih == 1:
            print (hasil_midi)
            print()
        
    elif (menu ==2 ):
        path_database_folder = input("Masukkan path folder: ")
        hasil_database =  proses_database (path_database_folder)
        output_path = "vektor_database.json"
        save_json_in_batches(hasil_database,output_path,batch_size=100)
        print("berhasil disimpan")
        print()
        print()
        
        choose =0
        while choose != 3: 
            print()
            print(" APAKAH MAU DIMASUKKAN KE FILE")
            print( "1. TIDAK!!.  TAMPILKAN SAJA VEKTORNYA")
            print ("2. MAU DONG SAYANG :))")
            print("3. exit")
            print()

            choose = int (input ("pilih print ga(3. exit): "))
            if (choose == 1):
                print (hasil_database)
                print()

            elif(choose ==2):
                output_path = "vektor_database.json"
                save_json_in_batches(hasil_database,output_path,batch_size = 5)
                print("berhasil disimpan")
                print()
                print()
            else:
                continue
    elif(menu ==3):
        wav_mic_file = "output_from_mic.wav"
        record_duration = 20  # Durasi rekaman (dalam detik)
        midi_mic_file = "output_from_mic.mid"
        # # Rekam audio ke array
        # audio_array = record_audio_to_array(duration=record_duration)

        # # Ubah array audio menjadi file MIDI
        # audio_to_midi_from_array(audio_array, midi_mic_file)
        rekam_audio(record_duration,wav_mic_file,channels=1)
        wav_to_midi(wav_mic_file,midi_mic_file)

        hasil_midi = process_midi (midi_mic_file)
        print("print ga??")
        print("1. print")
        pilih = int (input())
        
        if pilih == 1:
            print (hasil_midi)
            print()

    elif (menu ==4):
        if hasil_midi ==0 :
            print("harap masukkan query atau tester")

        elif hasil_database == 0:
            print("harap masukkan database")
        else:
            print("sedang loading pemrosesan")
            result = query_by_humming (hasil_midi, hasil_database)
            sorted_songs = olah_score_song(result)
            
            option = 0



            while option!= 4:
                print()
                print ("PILIH: ")
                print ("1.urutan vektor")
                print ("2. top n = ")
                print("3. judul yang paling mungkin")
                print("4. Exit")
                print()
                option = int (input("pilih(4 exit): "))
                if (option ==1 ):
                    print_score_song(sorted_songs)
                elif (option ==2):
                    n= int (input ("mau top berapa nih: "))
                    print_top_similar_song(sorted_songs, n)
                elif(option ==3):
                    print_most_similar_song(sorted_songs)
                else:
                    continue

    elif (menu ==5):
        hasil_database_json = load_json("vektor_database.json")
        print("berhasil load json! ")
        if(hasil_database_json ==0):
            hasil_database = hasil_database
        else:
            hasil_database = hasil_database_json
    if (menu == 6):
        update_midi_path = input("Masukkan Path ")
        update_midi_database("vektor_database.json",update_midi_path)
        hasil_database_json = load_json("vektor_database.json")
        print("berhasil load json yang baru! ")
        if(hasil_database_json ==0):
            hasil_database = hasil_database
        else:
            hasil_database = hasil_database_json
    else:
        continue