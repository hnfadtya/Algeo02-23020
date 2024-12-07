import './Header.css';
import React, { useState } from 'react';


function Header() {
    const [file, setFile] = useState<File | null>(null);

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const fileInput = e.target as HTMLInputElement; // Pastikan TypeScript tahu bahwa ini adalah input file
        if (fileInput.files && fileInput.files[0]) {
            setFile(fileInput.files[0]);
        }
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!file) {
            alert('Please select a file before uploading.');
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('http://127.0.0.1:5000/upload', {
                method: 'POST',
                body: formData,
            });
            const result = await response.json();
            alert(result.message);
        } catch (error) {
            console.error('Error uploading file:', error);
        }
    };

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
                <div className="leftBottom">
                    <h1 className="Text3">Dataset : Audios.zip</h1>
                    <h1 className="Text4">Mapper : mapper.txt</h1>
                </div>
            </div>
            <div className="right">
                <div className="box">ssss</div>
                {/* Input file hidden dengan id */}
                {/* <input
                    id="file-upload"
                    type="file"
                    className="file-input"
                    accept=".zip,.png,.jpg,.jpeg,.mp3,.wav,.midi"
                    onChange={handleFileUpload}
                    multiple
                    style={{ display: 'none' }} // Sembunyikan input file
                /> */}
                {/* <button className="NavbarButtonUpload" onClick={triggerFileUpload}>
                    Upload
                </button> */}
                
                {/* <form action="http://127.0.0.1:5000/upload" method="post" encType="multipart/form-data">
                    <input type="file" name="file" />
                    <input type="submit" value="Upload" />
                </form> */}

                <form onSubmit={handleSubmit}>
                            <input type="file" onChange={handleFileChange} />
                            <button type="submit">Upload</button>
                </form>
                                
            </div>
        </div>
    );
}

export default Header;
