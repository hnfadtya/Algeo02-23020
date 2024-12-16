import React, { useState, useEffect } from 'react';
import './Body.css';

interface MediaItem {
    id: number;
    audio_file: string;
    pic_name: string;
    url: string;
}

interface SortedFile {
    id: number;
    audio_file: string;
    pic_name: string;
    similarity: number;
    url: string;
}

interface BodyProps {
    folders: string[]; // Prop untuk menentukan folder mana yang akan ditampilkan
    sortedFiles?: SortedFile[]; // Prop opsional untuk menampilkan hasil ranking similarity
}

function Body({ folders, sortedFiles }: BodyProps) {
    const [mediaData, setMediaData] = useState<MediaItem[]>([]);
    const [currentPage, setCurrentPage] = useState(1);
    const [searchQuery, setSearchQuery] = useState('');
    const itemsPerPage = 12;

    // Fetch data dari Flask API jika sortedFiles tidak ada
    useEffect(() => {
        if (sortedFiles && sortedFiles.length > 0) {
            console.log('Using sortedFiles for ranking display.');
            return; // Skip fetching jika sortedFiles tersedia
        }

        const fetchData = async () => {
            try {
                const response = await fetch('http://127.0.0.1:5000/media');
                if (response.ok) {
                    const data: MediaItem[] = await response.json();

                    // Filter data berdasarkan folder yang dipilih
                    const filteredData = data.filter(item => folders.includes('folder_image'));
                    setMediaData(filteredData);
                } else {
                    console.error('Failed to fetch media. Status:', response.status);
                }
            } catch (error) {
                console.error('Error fetching media data:', error);
            }
        };

        fetchData();
    }, [folders, sortedFiles]);

    // Data yang akan ditampilkan (menggunakan sortedFiles jika tersedia)
    const displayData = sortedFiles
        ? sortedFiles.map((item, index) => ({
              id: index + 1,
              audio_file: item.audio_file,
              pic_name: item.pic_name,
              url: `/media/picture/${item.pic_name}`,
          }))
        : mediaData;

    // Filter data berdasarkan pencarian
    const filteredData = displayData.filter(item =>
        item.pic_name.toLowerCase().includes(searchQuery.toLowerCase())
    );

    // Pagination logic
    const totalPages = Math.ceil(filteredData.length / itemsPerPage);
    const currentData = filteredData.slice(
        (currentPage - 1) * itemsPerPage,
        currentPage * itemsPerPage
    );

    // Navigasi halaman
    const goToPreviousPage = () => {
        if (currentPage > 1) setCurrentPage(currentPage - 1);
    };

    const goToNextPage = () => {
        if (currentPage < totalPages) setCurrentPage(currentPage + 1);
    };

    return (
        <div className="BodyContainer">
            {/* Search Bar */}
            <div className="top-bar">
                <div className="search-bar">
                    <input
                        type="text"
                        placeholder="Search files..."
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                    />
                </div>
            </div>

            {/* Media Grid */}
            <div className="audio-grid">
                {currentData.length > 0 ? (
                    currentData.map((media) => (
                        <div key={media.id} className="boxListWrapper">
                            <div className="boxList">
                                {/* Render gambar */}
                                <img
                                    src={`http://127.0.0.1:5000${media.url}`}
                                    alt={media.pic_name}
                                    className="media-image"
                                />
                            </div>
                            <div className="audio-label">{media.audio_file}</div>
                        </div>
                    ))
                ) : (
                    <div>No media files found.</div>
                )}
            </div>

            {/* Pagination */}
            <div className="pagination-container">
                <button onClick={goToPreviousPage} disabled={currentPage === 1}>
                    &laquo; Prev
                </button>
                <span>
                    Page {currentPage} of {totalPages}
                </span>
                <button onClick={goToNextPage} disabled={currentPage === totalPages}>
                    Next &raquo;
                </button>
            </div>
        </div>
    );
}

export default Body;
