import React, { useState, useContext } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { FaBars, FaTimes, FaUserCircle } from 'react-icons/fa';
import 'bootstrap/dist/css/bootstrap.min.css';
import AuthContext from "../context/AuthContext";
import './NavBar.css';

const Navbar = ({ districtName = "ZAKA DISTRICT" }) => {
  const [menuOpen, setMenuOpen] = useState(false);
  const { user, logout } = useContext(AuthContext);
  const navigate = useNavigate();
  const location = useLocation();

  const toggleMenu = () => setMenuOpen(!menuOpen);
  const closeMenu = () => setMenuOpen(false);
  const isActive = (path) => (location.pathname === path ? "fw-bold text-decoration-underline" : "");

  const rawDept = (user?.department ?? user?.dept ?? "").toString().trim().toLowerCase();
  const isAdmin = Boolean(
    user?.is_admin ??
    user?.isAdmin ??
    (Array.isArray(user?.roles) && user.roles.includes("admin")) ??
    false
  );
  const isAccounts = !isAdmin && rawDept === "accounts";
  const isHR = !isAdmin && (rawDept === "hr" || rawDept === "human resources");

  const canSeePayments = isAdmin || isAccounts;
  const canSeeSchools = isAdmin || isHR;
  const canSeeEmployees = isAdmin;

  return (
    <div className="d-flex flex-column min-vh-10">
      {/* Top Navbar */}
      <nav
        className="navbar navbar-dark bg-primary px-4 py-3 d-flex justify-content-between align-items-center shadow"
        style={{ minHeight: '110px' }}
      >
        <button
          onClick={toggleMenu}
          className="btn btn-outline-light"
          aria-label="Open menu"
        >
          <FaBars />
        </button>

        <div className="text-center text-light">
          <h1 className="navbar-brand mb-0 fs-3">
            Better Schools Programme of Zimbabwe
          </h1>
          <h5 className="mb-0">{districtName}</h5>
        </div>

        <div className="text-center">
          <img
            src="https://zimprofiles.com/wp-content/uploads/2023/02/Zimbabwe-Coat-of-Arms-1280px-r.png"
            alt="Zimbabwe Coat of Arms"
            style={{ height: '60px', display: 'block', margin: '0 auto' }}
          />
          <div className="text-light small mt-1">
            Ministry of Primary and Secondary Education
          </div>
        </div>
      </nav>

      {/* Sidebar */}
      <div
        className={`position-fixed top-0 start-0 bg-white shadow-lg p-3 ${menuOpen ? 'open' : ''}`}
        style={{
          width: '260px',
          height: '100vh',
          zIndex: 1050,
          overflowY: 'auto',
          transform: menuOpen ? 'translateX(0)' : 'translateX(-100%)',
          transition: 'transform 0.3s ease-in-out',
        }}
        aria-hidden={!menuOpen}
      >
        {user && (
          <div className="d-flex align-items-center mb-3 border-bottom pb-2">
            <FaUserCircle size={44} className="text-primary me-2" />
            <div className="overflow-hidden">
              <div className="fw-bold text-truncate" title={user?.username || ""}>
                {user?.username}
              </div>
              {user?.email && (
                <div className="small text-muted text-truncate" title={user.email}>
                  {user.email}
                </div>
              )}
              {(user?.department || user?.dept) && (
                <div className="small text-secondary text-truncate" title={user?.department || user?.dept}>
                  {(user?.department || user?.dept)}
                </div>
              )}
              {isAdmin && <span className="badge bg-success mt-1">Admin</span>}
            </div>
          </div>
        )}

        <div className="d-flex justify-content-between align-items-center border-bottom pb-2 mb-3">
          <h5 className="text-primary mb-0">Menu</h5>
          <button
            onClick={closeMenu}
            className="btn btn-sm btn-outline-primary"
            aria-label="Close menu"
          >
            <FaTimes />
          </button>
        </div>

        <ul className="nav flex-column">
          <li className="nav-item">
            <Link to="/homepage" className={`nav-link text-primary ${isActive("/homepage")}`} onClick={closeMenu}>
              Homepage
            </Link>
          </li>
          <li className="nav-item">
            <Link to="/announcements" className={`nav-link text-primary ${isActive("/announcements")}`} onClick={closeMenu}>
              Announcements
            </Link>
          </li>

          {!user && (
            <>
              <li className="nav-item">
                <Link to="/login" className={`nav-link text-primary ${isActive("/login")}`} onClick={closeMenu}>
                  Login
                </Link>
              </li>
              <li className="nav-item">
                <Link to="/register" className={`nav-link text-primary ${isActive("/register")}`} onClick={closeMenu}>
                  Register
                </Link>
              </li>
            </>
          )}

          {user && (
            <>
              <li className="nav-item">
                <Link to="/dashboard" className={`nav-link text-primary ${isActive("/dashboard")}`} onClick={closeMenu}>
                  Dashboard
                </Link>
              </li>

              {canSeeSchools && (
                <li className="nav-item">
                  <Link to="/schools" className={`nav-link text-primary ${isActive("/schools")}`} onClick={closeMenu}>
                    Schools
                  </Link>
                </li>
              )}

              {canSeeEmployees && (
                <li className="nav-item">
                  <Link to="/employees" className={`nav-link text-primary ${isActive("/employees")}`} onClick={closeMenu}>
                    Employees
                  </Link>
                </li>
              )}

              {canSeePayments && (
                <>
                  <li className="nav-item">
                    <Link to="/payments" className={`nav-link text-primary ${isActive("/payments")}`} onClick={closeMenu}>
                      Payments Hub
                    </Link>
                  </li>
                  <li className="nav-item mt-3">
                    <strong className="text-secondary px-2">Payments</strong>
                  </li>
                  <li className="nav-item">
                    <Link to="/payments/primary" className={`nav-link text-primary ${isActive("/payments/primary")}`} onClick={closeMenu}>
                      Primary Schools
                    </Link>
                  </li>
                  <li className="nav-item">
                    <Link to="/payments/secondary" className={`nav-link text-primary ${isActive("/payments/secondary")}`} onClick={closeMenu}>
                      Secondary Schools
                    </Link>
                  </li>
                  <li className="nav-item">
                    <Link to="/payments/secondary-table" className={`nav-link text-primary ${isActive("/payments/secondary-table")}`} onClick={closeMenu}>
                      Sec. Payments Table
                    </Link>
                  </li>
                </>
              )}

              {isAdmin && (
                <>
                  <li className="nav-item mt-3">
                    <strong className="text-secondary px-2">Admin</strong>
                  </li>
                  <li className="nav-item">
                    <Link to="/admin-dashboard" className={`nav-link text-primary ${isActive("/admin-dashboard")}`} onClick={closeMenu}>
                      Admin Dashboard
                    </Link>
                  </li>
                  <li className="nav-item">
                    <Link to="/admin-creation-table" className={`nav-link text-primary ${isActive("/admin-creation-table")}`} onClick={closeMenu}>
                      Admin Creation Table
                    </Link>
                  </li>
                  <li className="nav-item">
                    <Link to="/admin-create" className={`nav-link text-primary ${isActive("/admin-create")}`} onClick={closeMenu}>
                      Create Admin
                    </Link>
                  </li>
                </>
              )}

              <li className="nav-item">
                <Link to="/profile/edit" className={`nav-link text-primary ${isActive("/profile/edit")}`} onClick={closeMenu}>
                  Edit My Profile
                </Link>
              </li>

              <li className="nav-item mt-4">
                <button
                  className="btn btn-danger w-100"
                  onClick={() => {
                    logout();
                    closeMenu();
                    navigate("/login");
                  }}
                >
                  Logout
                </button>
              </li>
            </>
          )}
        </ul>
      </div>

      {/* Overlay */}
      {menuOpen && (
        <div
          className="position-fixed top-0 start-0 w-100 h-100 bg-dark bg-opacity-50"
          style={{ zIndex: 100 }}
          onClick={closeMenu}
          aria-label="Close menu overlay"
        />
      )}
    </div>
  );
};

export default Navbar;