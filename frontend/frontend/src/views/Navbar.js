import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { FaBars, FaTimes } from 'react-icons/fa';
import 'bootstrap/dist/css/bootstrap.min.css';

const Navbar = () => {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <div>
      {/* Top Navbar */}
      <nav
        className="navbar navbar-dark bg-primary px-4 py-3 d-flex justify-content-between align-items-center shadow"
        style={{ minHeight: '110px' }}
      >
        {/* Sidebar Toggle */}
        <button onClick={() => setMenuOpen(true)} className="btn btn-outline-light">
          <FaBars />
        </button>

        {/* Center Title */}
        <div className="text-center text-light">
          <h1 className="navbar-brand mb-0 fs-3">Better Schools Programme of Zimbabwe</h1>
          <h5 className="mb-0">ZAKA DISTRICT</h5>
        </div>

        {/* Logo and Ministry Text */}
        <div className="text-center">
          <img
            src="https://zimprofiles.com/wp-content/uploads/2023/02/Zimbabwe-Coat-of-Arms-1280px-r.png"
            alt="Zimbabwe Coat of Arms"
            style={{ height: '60px', display: 'block', margin: '0 auto' }}
          />
          <div className="text-light small mt-1">Ministry of Primary and Secondary Education</div>
        </div>
      </nav>

      {/* Sidebar */}
      <div
        className={`position-fixed top-0 start-0 h-100 bg-white shadow-lg p-3 transition ${
          menuOpen ? 'translate-none' : 'translate-start'
        }`}
        style={{
          width: '120px',
          transform: menuOpen ? 'translateX(0)' : 'translateX(-100%)',
          transition: 'transform 0.3s ease-in-out',
          zIndex: 1050,
        }}
      >
        <div className="d-flex justify-content-between align-items-center border-bottom pb-2 mb-3">
          <h5 className="text-primary">Menu</h5>
          <button onClick={() => setMenuOpen(false)} className="btn btn-sm btn-outline-primary">
            <FaTimes />
          </button>
        </div>
        <ul className="nav flex-column">
          <li className="nav-item">
            <Link to="/homepage" className="nav-link text-primary" onClick={() => setMenuOpen(false)}>
              Homepage
            </Link>
          </li>
          <li className="nav-item">
            <Link to="/adddepartment" className="nav-link text-primary" onClick={() => setMenuOpen(false)}>
              Add Department
            </Link>
          </li>
          <li className="nav-item">
            <Link to="/dashboard" className="nav-link text-primary" onClick={() => setMenuOpen(false)}>
              Dashboard
            </Link>
          </li>
        </ul>
      </div>

      {/* Overlay */}
      {menuOpen && (
        <div
          className="position-fixed top-0 start-0 w-100 h-100 bg-dark bg-opacity-50"
          style={{ zIndex: 1040 }}
          onClick={() => setMenuOpen(false)}
        />
      )}
    </div>
  );
};

export default Navbar;
