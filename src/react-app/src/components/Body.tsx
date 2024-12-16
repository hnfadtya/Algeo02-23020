import React, { useState, useEffect } from 'react';
import './Body.css';

interface MediaItem {
    id: number;
    name: string;
    type: string;
    url: string;
}

interface SortedFile {
    filename: string;
    similarity: number;
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
                    const filteredData = data.filter(item => folders.includes(item.type));
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
              name: item.filename,
              type: 'folder_image',
              url: `/media/picture/${item.filename}`,
          }))
        : mediaData;

    // Filter data berdasarkan pencarian
    const filteredData = displayData.filter(item =>
        item.name.toLowerCase().includes(searchQuery.toLowerCase())
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
                                {/* Render berdasarkan tipe file */}
                                {media.type === 'folder_music' && (
                                    <audio controls>
                                        <source src={`http://127.0.0.1:5000${media.url}`} type="audio/mpeg" />
                                        Your browser does not support the audio element.
                                    </audio>
                                )}
                                {media.type === 'folder_image' && (
                                    <img
                                        src={`http://127.0.0.1:5000${media.url}`}
                                        alt={media.name}
                                        className="media-image"
                                    />
                                )}
                                {media.type === 'folder_mapper' && (
                                    <a href={`http://127.0.0.1:5000${media.url}`} target="_blank" rel="noreferrer">
                                        {media.name}
                                    </a>
                                )}
                            </div>
                            <div className="audio-label">{media.name}</div>
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
