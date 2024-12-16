import './Navbar.css';

interface NavbarProps {
    onShowAlbum: () => void;
    onShowMusic: () => void;
}

function Navbar({ onShowAlbum, onShowMusic }: NavbarProps) {
    return (
        <nav className="NavbarCustom">
            <h1 className="NavbarBrand">EchoFinder</h1>
            <div className="NavbarButtons">
                <button
                    onClick={() => {
                        console.log("Album button clicked"); // Debug tombol Album
                        onShowAlbum();
                    }}
                >
                    Album
                </button>
                <button
                    onClick={() => {
                        console.log("Music button clicked"); // Debug tombol Music
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
