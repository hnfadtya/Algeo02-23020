## Structure
test/
doc/
src/
│
├── backend/                
│   ├── __init__.py         
│   ├── routes.py           
│   ├── config.py           
│   ├── image_retrieval/    
│   │   ├── preprocessing.py
│   │   ├── standardization.py
│   │   ├── pca.py          
│   │   ├── similarity.py   
│   │   └── retrieval.py    
│   ├── music_retrieval/    
│   │   ├── preprocessing.py
│   │   ├── feature_extraction.py
│   │   ├── similarity.py   
│   │   └── humming.py      
│
├── frontend/               
│   ├── index.html          
│   ├── static/             
│   │   ├── css/            
│   │   │   └── styles.css  
│   │   ├── js/             
│   │   │   └── script.js   
│   │   └── images/         
│
├── dataset/                
│   ├── query/              
│   ├── images/             
│   └── audio/              
│
├── results/                
├── requirements.txt        
└── main.py

## Branch Name Convention
```
<BE/FE> /<deskripsi>
```

Contoh : `BE/ImageProcessingandloading`

## Aturan Semantic Commit

1. Format Umum :
```
<tipe>: <deskripsi>
```

2. Tipe Commit :
- `feat`: Menambahkan fitur baru.
- `fix`: Memperbaiki bug.
- `docs`: Mengubah dokumentasi.
- `style`: Perubahan yang tidak mempengaruhi logika (formatting, spasi, dll).
- `refactor`: Perubahan kode yang tidak menambah fitur atau memperbaiki bug.
- `test`: Menambahkan atau memperbaiki pengujian.
- `chore`: Tugas rutin yang tidak termasuk dalam kategori di atas (pengaturan build, perubahan dependensi, dll).

Contoh : `fix: memperbaiki bug PCA`

## Penamaan Component atau Actions

1. Komponen (Components) :
- Format : `PascalCase`
- Contoh : `UserProfile`, `NavBar`, `Button`

2. Actions : 
- Format : `camelCase`
- Contoh : `fetchUserData`, `updateProfile`, `handleSubmit`

3. Folder dan File :
- Format : `kebab-case`
- Contoh : `user-profile.tsx`, `nav-bar.tsx`, `api-enpoint.ts`

 # Algeo02-23020
Tugas Besar 2 IF2123 - Kelompok 30
| NIM | Nama |
| :---: | :---: |
| 13523020 | Stefan Mattew Susanto |
| 13523038 | Abrar Abhirama Widyadhana |
| 13523041 | Hanif Kalyana Aditya |

## Nama Program
Image Retrieval dan Music Information Retrieval Menggunakan PCA dan Vektor

## Deskripsi
Program ini melakukan <i>image and audio recognition</i> berupa sebuah lagu beserta album covernya menggunakan metode <i>PCA dan Query by Humming</i>. Program ini dibuat menggunakan bahasa pemrograman Python.

## Cara Menjalankan
Berikut adalah cara menjalankan program ini,

## Project Status
| Fitur | Status |
| :---: | :---: |
