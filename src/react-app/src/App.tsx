import React, { useState } from 'react';
import Navbar from './components/Navbar';
import Header from './components/Header';
import Body from './components/Body';
import './App.css';

function App() {
    const [selectedFolders, setSelectedFolders] = useState<string[]>(['audio', 'image', 'mapper']);

    const handleShowAlbum = () => {
        console.log("Show Album clicked");
        setSelectedFolders(['audio', 'image', 'mapper']);
    };

    const handleShowMusic = () => {
        console.log("Show Music clicked");
        setSelectedFolders(['audio', 'mapper']);
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
