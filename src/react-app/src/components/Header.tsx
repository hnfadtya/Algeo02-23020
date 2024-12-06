import './Header.css';

function Header(){
    return (
        <div className="container">
            <div className="left">
                <h1 className="Text1">Hello, Welcome to EchoFinder.</h1>
                <h1 className="Text2">Sound Search, Simplified.</h1>
                <div className="ButtonCustom">
                <a href="#">
                    <button className="NavbarButtonAudios">Audios</button>
                </a>
                <a href="#">
                    <button className="NavbarButtonPicture">Picture</button>
                </a>
                <a href="#">
                    <button className="NavbarButtonMapper">Mapper</button>
                </a>
                </div>
                <div className='leftBottom'>
                <h1 className="Text3">Dataset : Audios.zip</h1>
                <h1 className="Text4">Mapper : mapper.txt</h1>
                </div>
            </div>
            <div className="right">
                <div className="box">ssss</div>
                <a href="#">
                    <button className="NavbarButtonUpload">Upload</button>
                </a>
            </div>
            
        </div>

    )
}

export default Header;