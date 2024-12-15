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
                const data = await response.json();
                setMediaData(data);
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
        if (currentPage < totalPages) {
            setCurrentPage(currentPage + 1);
        }
    };

    const goToPreviousPage = () => {
        if (currentPage > 1) {
            setCurrentPage(currentPage - 1);
        }
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
                    <button
                        className="nav-button"
                        onClick={goToPreviousPage}
                        disabled={currentPage === 1}
                    >
                        &laquo; Prev
                    </button>
                    <div className="page-display">Page {currentPage} of {totalPages}</div>
                    <button
                        className="nav-button"
                        onClick={goToNextPage}
                        disabled={currentPage === totalPages}
                    >
                        Next &raquo;
                    </button>
                </div>
            </div>

            {/* Grid Display */}
            <div className="audio-grid">
                {currentData.map((media) => (
                    <div key={media.id} className="boxListWrapper">
                        <div className="boxList">
                            {media.type === 'audio' && (
                                <button className="play-button">
                                    <i className="fas fa-play"></i>
                                </button>
                            )}
                            {media.type === 'image' && (
                                <img
                                    src={`http://127.0.0.1:5000${media.url}`}  // Pastikan menggunakan URL lengkap
                                    alt={media.name}
                                    style={{ width: '100%', height: 'auto' }}
                                />
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
