import React, { useState } from 'react';
import './Body.css';

function Body() {
    // Data dummy
    const audioData = Array.from({ length: 100 }, (_, index) => ({
        id: index + 1,
        name: `audio_${index + 1}.wax`
    }));

    // State
    const [currentPage, setCurrentPage] = useState(1);
    const [searchQuery, setSearchQuery] = useState(''); // State untuk search bar
    const itemsPerPage = 12; // Jumlah item per halaman

    // Filter data berdasarkan search query
    const filteredData = audioData.filter(audio =>
        audio.name.toLowerCase().includes(searchQuery.toLowerCase())
    );

    // Hitung jumlah halaman berdasarkan hasil filter
    const totalPages = Math.ceil(filteredData.length / itemsPerPage);

    // Data untuk halaman saat ini
    const currentData = filteredData.slice(
        (currentPage - 1) * itemsPerPage,
        currentPage * itemsPerPage
    );

    // Fungsi untuk navigasi halaman
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

    // Fungsi untuk menangani perubahan input search
    const handleSearchChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setSearchQuery(event.target.value);
        setCurrentPage(1); // Reset ke halaman 1 saat melakukan pencarian
    };
    

    return (
        <div className="BodyContainer">
            {/* Search Bar and Pagination */}
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

            {/* Grid Audio */}
            <div className="audio-grid">
                {currentData.map((audio) => (
                    <div key={audio.id} className="boxListWrapper">
                        <div className="boxList">
                            <button className="play-button">
                                <i className="fas fa-play"></i>
                            </button>
                        </div>
                        <div className="audio-label">{audio.name}</div>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default Body;
