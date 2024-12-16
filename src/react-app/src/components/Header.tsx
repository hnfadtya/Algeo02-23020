import './Header.css';
import React, { useState } from 'react';

// Interface untuk hasil similarity
interface SortedFile {
    filename: string;
    similarity?: number;
    score?: number; // Untuk hasil MIDI similarity
}

interface HeaderProps {
    onUploadComplete: (files: SortedFile[]) => void;
}

function Header({ onUploadComplete }: HeaderProps) {
    const [file, setFile] = useState<File | null>(null); // State untuk file yang dipilih
    const [fileUrl, setFileUrl] = useState<string | null>(null); // URL pratinjau file
    const [sortedFiles, setSortedFiles] = useState<SortedFile[]>([]); // Hasil ranking similarity
    const [currentPage, setCurrentPage] = useState(1); // Halaman pagination
    const itemsPerPage = 5; // Jumlah item per halaman

    // Fungsi untuk menangkap file yang dipilih
    const handleFileSelection = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            const selectedFile = e.target.files[0];
            setFile(selectedFile);
            if (selectedFile.type.startsWith('image/')) {
                setFileUrl(URL.createObjectURL(selectedFile)); // Pratinjau gambar jika image
            } else {
                setFileUrl(null);
            }
        }
    };

    // Fungsi untuk mengunggah file (gambar atau MIDI) dan mendapatkan hasil similarity
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

            const result = await response.json();
            if (response.ok) {
                // Periksa apakah hasil adalah image atau MIDI similarity
                if (result.sorted_files) {
                    setSortedFiles(result.sorted_files); // Image similarity results
                    onUploadComplete(result.sorted_files);
                } else if (result.sorted_songs) {
                    setSortedFiles(
                        result.sorted_songs.map((song: any) => ({
                            filename: song[0],
                            score: song[1],
                        }))
                    ); // MIDI similarity results
                    onUploadComplete(
                        result.sorted_songs.map((song: any) => ({
                            filename: song[0],
                            score: song[1],
                        }))
                    );
                }
                setCurrentPage(1); // Reset ke halaman pertama
                alert('File uploaded and processed successfully!');
            } else {
                alert(`Error: ${result.message}`);
            }
        } catch (error) {
            console.error('Error uploading file:', error);
            alert('An error occurred while uploading the file.');
        }
    };

    // Fungsi untuk upload file ZIP ke folder kategori tertentu
    const handleCategoryUpload = async (category: string) => {
        const fileInput = document.createElement('input');
        fileInput.type = 'file';
        fileInput.accept = '.zip';
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

                    const result = await response.json();
                    if (response.ok) {
                        alert('ZIP file uploaded and extracted successfully!');
                    } else {
                        alert(`Error: ${result.message}`);
                    }
                } catch (error) {
                    console.error('Error uploading ZIP file:', error);
                }
            }
        };
        fileInput.click();
    };

    // Fungsi untuk mereset semua media
    const handleResetMedia = async () => {
        const confirmation = window.confirm('Are you sure you want to reset all media files?');
        if (!confirmation) return;

        try {
            const response = await fetch('http://127.0.0.1:5000/reset_media', { method: 'POST' });
            const result = await response.json();

            if (response.ok) {
                alert('Media folders have been reset.');
                setSortedFiles([]);
                setFile(null);
                setFileUrl(null);
                setCurrentPage(1);
            } else {
                alert(`Error: ${result.message}`);
            }
        } catch (error) {
            console.error('Error resetting media folders:', error);
        }
    };

    // Pagination: Data untuk halaman saat ini
    const currentPageData = sortedFiles.slice(
        (currentPage - 1) * itemsPerPage,
        currentPage * itemsPerPage
    );

    const handleNextPage = () => {
        if (currentPage < Math.ceil(sortedFiles.length / itemsPerPage)) {
            setCurrentPage(currentPage + 1);
        }
    };

    const handlePreviousPage = () => {
        if (currentPage > 1) {
            setCurrentPage(currentPage - 1);
        }
    };

    return (
        <div className="container">
            <div className="left">
                <h1 className="Text1">Hello, Welcome to EchoFinder.</h1>
                <h1 className="Text2">Sound Search, Simplified.</h1>
                <div className="ButtonCustom">
                    <button className="NavbarButtonAudios" onClick={() => handleCategoryUpload('music')}>
                        Audios
                    </button>
                    <button className="NavbarButtonPicture" onClick={() => handleCategoryUpload('picture')}>
                        Picture
                    </button>
                    <button className="NavbarButtonMapper" onClick={() => handleCategoryUpload('mapper')}>
                        Mapper
                    </button>
                    <button
                        className="NavbarButtonReset"
                        onClick={handleResetMedia}
                        style={{ marginLeft: '10px', backgroundColor: 'red', color: 'white' }}
                    >
                        Reset
                    </button>
                </div>
            </div>

            <div className="right">
                <div className="">
                    <input
                        type="file"
                        onChange={handleFileSelection}
                        style={{ display: 'block', marginBottom: '10px' }}
                    />
                    <button onClick={handleUploadToUploads} style={{ marginTop: '10px' }}>
                        Upload
                    </button>
                </div>

                {/* Pratinjau Gambar */}
                {fileUrl && (
                    <div className="uploaded-image-box">
                        <h3>Uploaded Image</h3>
                        <img src={fileUrl} alt="Uploaded file" style={{ maxWidth: '100%', height: 'auto' }} />
                    </div>
                )}

                {/* Hasil Similarity */}
                {sortedFiles.length > 0 && (
                    <div className="result-box">
                        <h3>Similarity Results</h3>
                        {currentPageData.map((file, index) => (
                            <div key={index} className="result-item">
                                <p>
                                    <strong>{file.filename}</strong> -{' '}
                                    {file.similarity
                                        ? `Similarity: ${file.similarity}%`
                                        : `Score: ${file.score?.toFixed(2)}`}
                                </p>
                            </div>
                        ))}

                        {/* Pagination */}
                        <div className="pagination">
                            <button onClick={handlePreviousPage} disabled={currentPage === 1}>
                                Previous
                            </button>
                            <span>
                                Page {currentPage} of {Math.ceil(sortedFiles.length / itemsPerPage)}
                            </span>
                            <button
                                onClick={handleNextPage}
                                disabled={currentPage === Math.ceil(sortedFiles.length / itemsPerPage)}
                            >
                                Next
                            </button>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}

export default Header;
