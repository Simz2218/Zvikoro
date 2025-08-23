import React, { useContext } from 'react';
import { Link } from 'react-router-dom';
import AuthContext from '../context/AuthContext';
import backgroundImage from './pictures/Lover of the World.jpg';
import 'bootstrap/dist/css/bootstrap.min.css';

function LoginPage() {
  const { loginUser } = useContext(AuthContext);

  const handleSubmit = (e) => {
    e.preventDefault();
    const username = e.target.username.value;
    const password = e.target.password.value;
    if (username.length > 0) loginUser(username, password);
  };

  return (
    <div
      className="min-vh-100 d-flex align-items-center justify-content-center"
      style={{
        backgroundImage: `url(${backgroundImage})`,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
      }}
    >
      <div className="container shadow-lg rounded bg-white overflow-hidden" style={{ maxWidth: '900px' }}>
        <div className="row g-0">
          {/* Left Image Section */}
          <div className="d-none d-md-flex col-md-6 bg-light align-items-center justify-content-center">
            <img
              src="https://www.iconexperience.com/_img/v_collection_png/512x512/shadow/user_lock.png"
              alt="User Lock Icon"
              className="img-fluid"
              style={{ maxHeight: '250px' }}
            />
          </div>

          {/* Right Form Section */}
          <div className="col-12 col-md-6 p-5">
            <h2 className="fw-bold text-primary mb-3">Welcome back 👋</h2>
            <p className="text-muted mb-4">Sign into your account</p>
            <form onSubmit={handleSubmit}>
              <div className="mb-3">
                <label htmlFor="username" className="form-label text-dark">Username</label>
                <input
                  type="text"
                  name="username"
                  id="username"
                  className="form-control"
                  placeholder="Enter your username"
                  required
                />
              </div>
              <div className="mb-3">
                <label htmlFor="password" className="form-label text-dark">Password</label>
                <input
                  type="password"
                  name="password"
                  id="password"
                  className="form-control"
                  placeholder="Enter your password"
                  required
                />
              </div>
              <button type="submit" className="btn btn-primary w-100">
                Login
              </button>
            </form>

            <div className="mt-3 text-center">
              <Link to="/forgot-password" className="text-decoration-none text-muted">
                Forgot password?
              </Link>
            </div>
            <div className="mt-2 text-center text-muted">
              Don't have an account?{' '}
              <Link to="/register" className="text-primary text-decoration-none">
                Register Now
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default LoginPage;
