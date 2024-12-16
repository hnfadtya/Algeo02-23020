import React, { useState } from 'react';
import Navbar from './components/Navbar';
import Header from './components/Header';
import Body from './components/Body';
import './App.css';

function App() {
    const [selectedFolders, setSelectedFolders] = useState<string[]>(['folder_music', 'folder_image', 'folder_mapper']);

    // Logika untuk tombol Album
    const handleShowAlbum = () => {
        console.log("Show Album clicked - Showing all folders");
        setSelectedFolders(['folder_music', 'folder_image', 'folder_mapper']);
    };

    // Logika untuk tombol Music
    const handleShowMusic = () => {
        console.log("Show Music clicked - Showing Music and Mapper folders");
        setSelectedFolders(['folder_music', 'folder_image', 'folder_mapper'])
    };

    return (
        <div className="mainBackground">
            <Navbar onShowAlbum={handleShowAlbum} onShowMusic={handleShowMusic} />
            <Header />
            <Body folders={selectedFolders} />
        </div>
    );
}

export default App;
