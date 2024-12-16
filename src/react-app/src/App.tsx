import React, { useState } from 'react';
import Navbar from './components/Navbar';
import Header from './components/Header';
import Body from './components/Body';
import './App.css';

function App() {
    const [selectedFolders, setSelectedFolders] = useState<string[]>(['folder_music', 'folder_image', 'folder_mapper']);
    const [sortedFiles, setSortedFiles] = useState<{ filename: string; similarity: number }[]>([]); // State untuk hasil similarity

    // Logika untuk tombol Album
    const handleShowAlbum = () => {
        console.log("Show Album clicked - Showing all folders");
        setSelectedFolders(['folder_music', 'folder_image', 'folder_mapper']);
    };

    // Logika untuk tombol Music
    const handleShowMusic = () => {
        console.log("Show Music clicked - Showing Music and Mapper folders");
        setSelectedFolders(['folder_music', 'folder_image', 'folder_mapper']);
    };

    return (
        <div className="mainBackground">
            <Navbar onShowAlbum={handleShowAlbum} onShowMusic={handleShowMusic} />
            <Header onUploadComplete={setSortedFiles} /> {/* Kirim fungsi untuk menerima hasil similarity */}
            <Body folders={selectedFolders} sortedFiles={sortedFiles} /> {/* Oper data sortedFiles ke Body */}
        </div>
    );
}

export default App;
