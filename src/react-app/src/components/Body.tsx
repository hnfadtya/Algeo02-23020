import React, { useState, useEffect } from 'react';
import './Body.css';

interface MediaItem {
    id: number;
    pic_name: string;
    audio_file: string;
    url: string;
}

interface BodyProps {
    folders: string[]; // Prop untuk menentukan folder mana yang akan ditampilkan
}

function Body({ folders }: BodyProps) {
    const [mediaData, setMediaData] = useState<MediaItem[]>([]);
    const [currentPage, setCurrentPage] = useState(1);
    const [searchQuery, setSearchQuery] = useState('');
    const itemsPerPage = 12;

    useEffect(() => {
        console.log("Props folders:", folders); // Log 1: Debug nilai folders props

        const fetchData = async () => {
            console.log("Fetching data from Flask..."); // Log 2: Menunjukkan fetching dimulai
            try {
                const response = await fetch('http://127.0.0.1:5000/media');
                if (response.ok) {
                    const data: MediaItem[] = await response.json();
                    console.log("Fetched Data from Flask:", data); // Log 3: Menampilkan data dari Flask

                    // Filter data berdasarkan props folders
                    const filteredData = data.filter(item => {
                        console.log("Checking audio_file:", item.audio_file); // Log 4: Debug tipe data item
                        return folders.some(folder => folder === item.audio_file);
                    });

                    console.log("Filtered Data:", filteredData); // Log 5: Menampilkan hasil filter
                    setMediaData(filteredData);
                } else {
                    console.error("Failed to fetch media. Status:", response.status);
                }
            } catch (error) {
                console.error("Error fetching media data:", error);
            }
        };

        fetchData();
    }, [folders]);

    // Filter data berdasarkan pencarian
    const filteredData = mediaData.filter(item =>
        item.pic_name.toLowerCase().includes(searchQuery.toLowerCase())
    );

    // Pagination
    const totalPages = Math.ceil(filteredData.length / itemsPerPage);
    const currentData = filteredData.slice(
        (currentPage - 1) * itemsPerPage,
        currentPage * itemsPerPage
    );

    console.log("Current Page Data:", currentData); // Log 6: Menampilkan data halaman saat ini

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
                    currentData.map((media) => {
                        console.log("Rendering Media:", media); // Log 7: Menampilkan data yang dirender
                        return (
                            <div key={media.id} className="boxListWrapper">
                                <div className="boxList">
                                    {media.audio_file === 'audio' && (
                                        <audio controls>
                                            <source src={`http://127.0.0.1:5000${media.url}`} type="audio/midi" />
                                            Your browser does not support the audio element.
                                        </audio>
                                    )}
                                    {media.pic_name && (
                                        <img
                                            src={`http://127.0.0.1:5000${media.url}`}
                                            alt={media.pic_name}
                                            style={{ width: '100%', height: 'auto' }}
                                        />
                                    )}
                                    {/* {media.type === 'mapper' && (
                                        <a href={`http://127.0.0.1:5000${media.url}`} target="_blank" rel="noreferrer">
                                            {media.pic_name}
                                        </a>
                                    )} */}
                                </div>
                                <div className="audio-label">{media.pic_name}</div>
                            </div>
                        );
                    })
                ) : (
                    <div>No media files found.</div>
                )}
            </div>

            {/* Pagination */}
            <div className="pagination-container">
                <button onClick={goToPreviousPage} disabled={currentPage === 1}>
                    &laquo; Prev
                </button>
                <span>Page {currentPage} of {totalPages}</span>
                <button onClick={goToNextPage} disabled={currentPage === totalPages}>
                    Next &raquo;
                </button>
            </div>
        </div>
    );
}

export default Body;
