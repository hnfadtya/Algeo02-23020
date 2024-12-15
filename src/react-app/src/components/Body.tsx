import React, { useState, useEffect } from 'react';
import './Body.css';

interface MediaItem {
    id: number;
    name: string;
    type: string;
    url: string;
}

function Body() {
    const [mediaData, setMediaData] = useState<MediaItem[]>([]);
    const [currentPage, setCurrentPage] = useState(1);
    const [searchQuery, setSearchQuery] = useState('');
    const itemsPerPage = 12;

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch('http://127.0.0.1:5000/media');

                if (response.ok) {
                    const data = await response.json();
                    console.log("Data fetched from Flask:", data); // Debug: Cetak data
                    setMediaData(data);
                } else {
                    throw new Error('Failed to fetch media');
                }
            } catch (error) {
                console.error('Error fetching media data:', error);
            }
        };
        fetchData();
    }, []);

    const filteredData = mediaData.filter(item =>
        item.name.toLowerCase().includes(searchQuery.toLowerCase())
    );

    const totalPages = Math.ceil(filteredData.length / itemsPerPage);
    const currentData = filteredData.slice(
        (currentPage - 1) * itemsPerPage,
        currentPage * itemsPerPage
    );

    const goToNextPage = () => {
        if (currentPage < totalPages) setCurrentPage(currentPage + 1);
    };

    const goToPreviousPage = () => {
        if (currentPage > 1) setCurrentPage(currentPage - 1);
    };

    const handleSearchChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setSearchQuery(event.target.value);
        setCurrentPage(1);
    };

    return (
        <div className="BodyContainer">
            <div className="top-bar">
                <div className="search-bar">
                    <input
                        type="text"
                        placeholder="Search files..."
                        value={searchQuery}
                        onChange={handleSearchChange}
                    />
                </div>
                <div className="pagination-container">
                    <button className="nav-button" onClick={goToPreviousPage} disabled={currentPage === 1}>
                        &laquo; Prev
                    </button>
                    <div className="page-display">
                        Page {currentPage} of {totalPages}
                    </div>
                    <button className="nav-button" onClick={goToNextPage} disabled={currentPage === totalPages}>
                        Next &raquo;
                    </button>
                </div>
            </div>

            <div className="audio-grid">
                {currentData.map((media) => (
                    <div key={media.id} className="boxListWrapper">
                        <div className="boxList">
                            {media.type === 'audio' && (
                                <audio controls>
                                    <source src={`http://127.0.0.1:5000${media.url}`} type="audio/mpeg" />
                                    Your browser does not support the audio element.
                                </audio>
                            )}
                            {media.type === 'image' && (
                                <img
                                    src={`http://127.0.0.1:5000${media.url}`}
                                    alt={media.name}
                                    style={{ width: '100%', height: 'auto' }}
                                />
                            )}
                            {media.type === 'mapper' && (
                                <a href={`http://127.0.0.1:5000${media.url}`} target="_blank" rel="noreferrer">
                                    {media.name}
                                </a>
                            )}
                        </div>
                        <div className="audio-label">{media.name}</div>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default Body;
