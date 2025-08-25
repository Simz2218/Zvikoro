import React, { useEffect, useState } from "react";
import useAxios from "../utils/useAxios";
import Swal from "sweetalert2";

function AdminCreationTable() {
  const { axiosInstance } = useAxios();
  const [users, setUsers] = useState([]);
  const [newAdmin, setNewAdmin] = useState({ user: "", district: "", role: "admin" });

  useEffect(() => {
    // load existing non-admin users for selection
    axiosInstance.get("users/").then(res => setUsers(res.data));
  }, [axiosInstance]);

  const handleChange = (field, value) => {
    setNewAdmin(prev => ({ ...prev, [field]: value }));
  };

  const handleCreateAdmin = async () => {
    try {
      await axiosInstance.post("admins/", newAdmin);
      Swal.fire("Success", "Admin account created!", "success");
      setNewAdmin({ user: "", is: "", role: "admin" });
    } catch (err) {
      console.error(err);
      Swal.fire("Error", "Failed to create admin", "error");
    }
  };

  return (
    <div className="container bg-white p-4 rounded shadow-sm mt-4">
      <h3>Create Admin Account</h3>
      <table className="table table-bordered">
        <tbody>
          <tr>
            <td>Select User</td>
            <td>
              <select
                className="form-select"
                value={newAdmin.user}
                onChange={(e) => handleChange("user", e.target.value)}
              >
                <option value="">-- Select a User --</option>
                {users
                  .filter(u => !u.is_admin)
                  .map(u => (
                    <option key={u.id} value={u.id}>
                      {u.username} ({u.email})
                    </option>
                  ))}
              </select>
            </td>
          </tr>
          <tr>
            <td>District</td>
            <td>
              <input
                type="text"
                className="form-control"
                value={newAdmin.district}
                onChange={(e) => handleChange("district", e.target.value)}
              />
            </td>
          </tr>
        </tbody>
      </table>
      <button className="btn btn-success" onClick={handleCreateAdmin}>
        Create Admin
      </button>
    </div>
  );
}

export default AdminCreationTable;
