# Algeo02-23020
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
