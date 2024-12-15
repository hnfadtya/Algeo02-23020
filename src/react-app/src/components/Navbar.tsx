import './Navbar.css';

interface NavbarProps {
    onShowAlbum: () => void; // Fungsi untuk tombol Album
    onShowMusic: () => void; // Fungsi untuk tombol Music
}

function Navbar({ onShowAlbum, onShowMusic }: NavbarProps) {
    return (
        <nav className="NavbarCustom">
            <h1 className="NavbarBrand">EchoFinder</h1>
            <div className="NavbarButtons">
                <button
                    onClick={() => {
                        console.log("Album button clicked"); // Debug
                        onShowAlbum();
                    }}
                >
                    Album
                </button>
                <button
                    onClick={() => {
                        console.log("Music button clicked"); // Debug
                        onShowMusic();
                    }}
                >
                    Music
                </button>
            </div>
        </nav>
    );
}

export default Navbar;
