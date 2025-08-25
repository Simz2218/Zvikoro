import React, { useState, useContext } from "react";
import Swal from "sweetalert2";
import withReactContent from "sweetalert2-react-content";
import { motion } from "framer-motion";
import AuthContext from "../context/AuthContext";

const MySwal = withReactContent(Swal);

const DEPARTMENTS = [
  "IT",
  "Accounts",
  "Administration",
  "DSI",
  "Inspectors",
  "Remedial",
  "NonFormal",
  "OfficeOrderly",
  "HR",
  "Aid",
];

const CreateAdminPage = () => {
  const { createAdmin } = useContext(AuthContext);

  const [formData, setFormData] = useState({
    phone_number: "",
    first_name: "",
    surname: "",
    department: "",
  });

  const handleChange = (e) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      await createAdmin(formData);
      setFormData({
        phone_number: "",
        first_name: "",
        surname: "",
        department: "",
      });
      MySwal.fire({
        icon: "success",
        title: "Admin Created",
        text: "New admin profile has been successfully created.",
      });
    } catch {
      MySwal.fire({
        icon: "error",
        title: "Error",
        text: "Unexpected error during admin creation.",
      });
    }
  };

  return (
    <motion.div
      className="container mt-5"
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
    >
      <div className="card shadow-lg p-4">
        <h2 className="text-center mb-4">Create Admin</h2>
        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label className="form-label">Phone Number</label>
            <input
              type="text"
              name="phone_number"
              className="form-control"
              placeholder="e.g. 0781234567"
              value={formData.phone_number}
              onChange={handleChange}
              required
            />
          </div>
          <div className="mb-3">
            <label className="form-label">First Name</label>
            <input
              type="text"
              name="first_name"
              className="form-control"
              placeholder="e.g. Tinashe"
              value={formData.first_name}
              onChange={handleChange}
              required
            />
          </div>
          <div className="mb-3">
            <label className="form-label">Surname</label>
            <input
              type="text"
              name="surname"
              className="form-control"
              placeholder="e.g. Simango"
              value={formData.surname}
              onChange={handleChange}
              required
            />
          </div>
          <div className="mb-3">
            <label className="form-label">Department</label>
            <select
              name="department"
              className="form-select"
              value={formData.department}
              onChange={handleChange}
              required
            >
              <option value="">Select department</option>
              {DEPARTMENTS.map((dept) => (
                <option key={dept} value={dept}>
                  {dept}
                </option>
              ))}
            </select>
          </div>
          <motion.button
            type="submit"
            className="btn btn-primary w-100"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            Create Admin
          </motion.button>
        </form>
      </div>
    </motion.div>
  );
};

export default CreateAdminPage;
