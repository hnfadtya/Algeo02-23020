import './Navbar.css';

function Navbar() {
  return (
    <nav className="NavbarCustom">
      {/* Nama Brand di kiri */}
      <h1 className="NavbarBrand">EchoFinder</h1>

      {/* Tombol di kanan */}
      <div className="NavbarButtons">
        <a href="https://www.google.com/search?q=kucing+akmal&sca_esv=4a9e581ba0958f54&rlz=1C1UEAD_enID999ID999&udm=2&biw=960&bih=727&sxsrf=ADLYWILoFQpdq8hfR7UMZPKxXGuXKXpBcg%3A1733139503759&ei=L5xNZ6yGLoqhseMP-NqV2Ak&ved=0ahUKEwjs2d7j_4iKAxWKUGwGHXhtBZsQ4dUDCBA&uact=5&oq=kucing+akmal&gs_lp=EgNpbWciDGt1Y2luZyBha21hbDILEAAYgAQYsQMYgwEyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABDIEEAAYHjIEEAAYHjIEEAAYHjIEEAAYHkj6GlDwBFjhGHACeACQAQCYAcACoAG_F6oBBzAuOC40LjK4AQPIAQD4AQGYAg-gAuUWqAIKwgINEAAYgAQYsQMYQxiKBcICBhAAGAcYHsICChAAGIAEGEMYigXCAgQQIxgnwgIHECMYJxjqAsICCBAAGIAEGLEDwgIHEAAYgAQYCpgDB4gGAZIHBzIuNy4zLjOgB6pL&sclient=img">
          <button className="NavbarButtonAlbum">Album</button>
        </a>
        <a href="https://www.google.com/search?q=kucing+akmal&sca_esv=4a9e581ba0958f54&rlz=1C1UEAD_enID999ID999&udm=2&biw=960&bih=727&sxsrf=ADLYWILoFQpdq8hfR7UMZPKxXGuXKXpBcg%3A1733139503759&ei=L5xNZ6yGLoqhseMP-NqV2Ak&ved=0ahUKEwjs2d7j_4iKAxWKUGwGHXhtBZsQ4dUDCBA&uact=5&oq=kucing+akmal&gs_lp=EgNpbWciDGt1Y2luZyBha21hbDILEAAYgAQYsQMYgwEyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABDIEEAAYHjIEEAAYHjIEEAAYHjIEEAAYHkj6GlDwBFjhGHACeACQAQCYAcACoAG_F6oBBzAuOC40LjK4AQPIAQD4AQGYAg-gAuUWqAIKwgINEAAYgAQYsQMYQxiKBcICBhAAGAcYHsICChAAGIAEGEMYigXCAgQQIxgnwgIHECMYJxjqAsICCBAAGIAEGLEDwgIHEAAYgAQYCpgDB4gGAZIHBzIuNy4zLjOgB6pL&sclient=img">
        <button className="NavbarButtonMusic">Music</button>
        </a>
      </div>
    </nav>
  );
}

export default Navbar;
