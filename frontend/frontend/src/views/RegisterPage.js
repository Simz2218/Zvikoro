import React, { useState, useContext } from "react";
import Swal from "sweetalert2";
import AuthContext from "../context/AuthContext";
import bluesky from "../views/pictures/bluesky.png";

function RegisterPage() {
  const { registerUser } = useContext(AuthContext);

  const [form, setForm] = useState({
    admin: "",       // phone number of Admin
    username: "",
    email: "",
    password: "",
    password2: "",
  });

  const handleChange = (field, value) => {
    setForm((prev) => ({ ...prev, [field]: value }));
  };

  const handleSubmit = async () => {
    // Optional: quick client‑side password match check
    if (form.password !== form.password2) {
      Swal.fire("Error", "Passwords do not match", "error");
      return;
    }
    // Call the context method — it handles the fetch and alerts
    await registerUser(form);
    // Reset form after successful registration
    setForm({ admin: "", username: "", email: "", password: "", password2: "" });
  };

  return (
    <div className="container bg-white p-4 rounded shadow-sm" style={{ maxWidth: "500px" }}>
      <h3 className="mb-4">Create Your Account</h3>

      <div className="mb-3">
        <label>Admin Phone Number</label>
        <input
          type="tel"
          className="form-control"
          value={form.admin}
          onChange={(e) => handleChange("admin", e.target.value)}
          placeholder="e.g. 0771234567"
        />
      </div>

      <div className="mb-3">
        <label>Username</label>
        <input
          type="text"
          className="form-control"
          value={form.username}
          onChange={(e) => handleChange("username", e.target.value)}
        />
      </div>

      <div className="mb-3">
        <label>Email</label>
        <input
          type="email"
          className="form-control"
          value={form.email}
          onChange={(e) => handleChange("email", e.target.value)}
        />
      </div>

      <div className="mb-3">
        <label>Password</label>
        <input
          type="password"
          className="form-control"
          value={form.password}
          onChange={(e) => handleChange("password", e.target.value)}
        />
      </div>

      <div className="mb-3">
        <label>Confirm Password</label>
        <input
          type="password"
          className="form-control"
          value={form.password2}
          onChange={(e) => handleChange("password2", e.target.value)}
        />
      </div>

      <button className="btn btn-primary w-100" onClick={handleSubmit}>
        Register
      </button>
    </div>
  );
}

export default RegisterPage;
