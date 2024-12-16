Algeo02-23020/
├── doc/                     # Dokumentasi terkait proyek
├── test/                    # Berisi file untuk testing
├── src/                     # Berisi source code utama
│   ├── frontend/            # Folder untuk pengembangan frontend
│   │   ├── react-app/       # Folder untuk aplikasi React
│   │   │   ├── node_modules/ # Library dependensi React
│   │   │   ├── public/      # File publik React seperti index.html
│   │   │   ├── src/         # Source code React
│   │   │   │   ├── app.py
│   │   │   │   ├── App.css
│   │   │   │   ├── App.tsx
│   │   │   │   ├── index.css
│   │   │   │   ├── backend/ # Bagian backend yang terintegrasi
│   │   │   │   │   ├── __pycache__/
│   │   │   │   │   ├── image_retrieval/
│   │   │   │   │   │   ├── __pycache__/
│   │   │   │   │   │   └── retrieval.py
│   │   │   │   │   ├── music_retrieval/
│   │   │   │   │   │   ├── __pycache__/
│   │   │   │   │   │   ├── MIR.py
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── config.py
│   │   │   │   │   │   └── routes.py
│   │   │   │   ├── __pycache__/
│   │   │   │   ├── components/ # Komponen React
│   │   │   │   │   ├── Body.css
│   │   │   │   │   ├── Body.tsx
│   │   │   │   │   ├── Header.css
│   │   │   │   │   ├── Header.tsx
│   │   │   │   │   ├── ListGroup.tsx
│   │   │   │   │   ├── Navbar.css
│   │   │   │   │   └── Navbar.tsx
│   │   │   │   ├── media/    # Folder untuk file media
│   │   │   │   │   ├── mapper/
│   │   │   │   │   ├── music/
│   │   │   │   │   ├── picture/
│   │   │   │   │   └── uploads/
│   │   │       ├── datamusic/ # Folder data tambahan
├── main.py                  # Entry point aplikasi
└── requirements.txt         # Dependensi Python
             

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
1. Clone Repository ini.
2. Jalankan run.bat untuk menginstal 
3. Jalankan run2.bat dan buka link  http://localhost:5173/ tersebut



