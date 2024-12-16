import './Header.css';
import React, { useState } from 'react';

function Header() {
    const [file, setFile] = useState<File | null>(null); // State untuk file

    // Fungsi untuk menangani file umum (Tombol Upload)
    const handleFileSelection = (e: React.ChangeEvent<HTMLInputElement>) => {
        const fileInput = e.target;
        if (fileInput.files && fileInput.files[0]) {
            setFile(fileInput.files[0]); // Simpan file
        }
    };

    const handleUploadToUploads = async () => {
        if (!file) {
            alert('Please select a file before uploading.');
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('http://127.0.0.1:5000/upload', {
                method: 'POST',
                body: formData,
            });

            // Periksa status HTTP
            if (!response.ok) {
                const errorData = await response.json();
                // alert(`Error: ${errorData.message}`);
                return;
            }

            const result = await response.json();
            alert(result.message);
        } catch (error) {
            console.error('Error uploading file:', error);
        }
    };

    // Fungsi untuk menangani unggahan ZIP berdasarkan kategori
    const handleCategoryUpload = async (category: string) => {
        const fileInput = document.createElement('input');
        fileInput.type = 'file';
        fileInput.accept = '.zip'; // Hanya file ZIP
        fileInput.onchange = async (e) => {
            const target = e.target as HTMLInputElement;
            if (target.files && target.files[0]) {
                const file = target.files[0];

                const formData = new FormData();
                formData.append('file', file);
                formData.append('category', category);

                try {
                    const response = await fetch('http://127.0.0.1:5000/upload_zip', {
                        method: 'POST',
                        body: formData,
                    });

                    // Periksa status HTTP
                    if (!response.ok) {
                        const errorData = await response.json();
                        // alert(`Error: ${errorData.message}`);
                        return;
                    }

                    const result = await response.json();
                    alert(result.message);
                } catch (error) {
                    console.error('Error uploading file:', error);
                }
            }
        };
        fileInput.click();
    };

    const handleResetMedia = async () => {
        const confirmation = window.confirm("Are you sure you want to reset all media files?");
        if (!confirmation) return;
    
        try {
            const response = await fetch('http://127.0.0.1:5000/reset_media', {
                method: 'POST',
            });
    
            const result = await response.json();
            if (response.ok) {
                alert(result.message);
                window.location.reload(); // Refresh data di aplikasi
            } else {
                alert(`Error: ${result.message}`);
            }
        } catch (error) {
            console.error('Error resetting media folders:', error);
            alert('Failed to reset media folders.');
        }
    };

    return (
        <div className="container">
            <div className="left">
                <h1 className="Text1">Hello, Welcome to EchoFinder.</h1>
                <h1 className="Text2">Sound Search, Simplified.</h1>
                <div className="ButtonCustom">
                    {/* Tombol untuk kategori ZIP */}
                    <button
                        className="NavbarButtonAudios"
                        onClick={() => handleCategoryUpload('music')}
                    >
                        Audios
                    </button>
                    <button
                        className="NavbarButtonPicture"
                        onClick={() => handleCategoryUpload('picture')}
                    >
                        Picture
                    </button>
                    <button
                        className="NavbarButtonMapper"
                        onClick={() => handleCategoryUpload('mapper')}
                    >
                        Mapper
                    </button>
                    {/* Tombol Reset */}
                    <button
                        className="NavbarButtonReset"
                        onClick={handleResetMedia}
                        style={{ marginLeft: '10px', backgroundColor: 'red', color: 'white' }}
                    >
                        Reset
                    </button>
                </div>
                <div className="leftBottom">
                    <h1 className="Text3">Dataset : Audios.zip</h1>
                    <h1 className="Text4">Mapper : mapper.txt</h1>
                </div>
            </div>
            <div className="right">
                <div className="box">
                    <input
                        type="file"
                        onChange={handleFileSelection} // Fungsi untuk Tombol Upload
                        style={{ display: 'block', marginBottom: '10px' }}
                    />
                    <button onClick={handleUploadToUploads} style={{ marginTop: '10px' }}>
                        Upload
                    </button>
                </div>
            </div>
        </div>
    );
}

export default Header;