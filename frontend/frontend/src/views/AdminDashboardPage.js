import React, { useContext, useEffect, useState } from "react";
import AuthContext from "../context/AuthContext";
import Swal from "sweetalert2";

const AdminDashboardPage = () => {
  const { authFetch, URLS } = useContext(AuthContext);
  const [users, setUsers] = useState([]);
  const [messages, setMessages] = useState([]);

  const loadData = async () => {
    try {
      const [uRes, mRes] = await Promise.all([
        authFetch(URLS.users),
        authFetch(URLS.messages),
      ]);
      if (!uRes.ok || !mRes.ok) throw new Error();

      const [userData, messageData] = await Promise.all([
        uRes.json(),
        mRes.json(),
      ]);

      setUsers(userData);
      setMessages(messageData);
    } catch {
      Swal.fire("Error", "Could not load dashboard data", "error");
    }
  };

  useEffect(() => {
    loadData();
  }, [authFetch]);

  const updateUser = async (userId, payload, successMsg) => {
    try {
      const res = await authFetch(URLS.userDetail(userId), {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (res.ok) {
        Swal.fire("Success", successMsg, "success");
        loadData();
      } else {
        const err = await res.json();
        Swal.fire("Error", err.detail || "Update failed", "error");
      }
    } catch {
      Swal.fire("Error", "Unexpected error", "error");
    }
  };

  const handlePromote = (id) => updateUser(id, { is_admin: true }, "User promoted to admin");
  const handleDemote = (id) => updateUser(id, { is_admin: false }, "User demoted from admin");

  const handleDeleteUser = async (id) => {
    const confirm = await Swal.fire({
      title: "Delete user?",
      text: "This action cannot be undone.",
      icon: "warning",
      showCancelButton: true,
      confirmButtonText: "Yes, delete",
    });
    if (!confirm.isConfirmed) return;

    try {
      const res = await authFetch(URLS.userDetail(id), { method: "DELETE" });
      if (res.ok) {
        Swal.fire("Deleted", "User removed", "success");
        loadData();
      } else {
        Swal.fire("Error", "Failed to delete user", "error");
      }
    } catch {
      Swal.fire("Error", "Unexpected error", "error");
    }
  };

  const handleChangeDept = async (id) => {
    const { value: dept } = await Swal.fire({
      title: "Change Department",
      input: "select",
      inputOptions: {
        IT: "IT",
        Accounts: "Accounts",
        Administration: "Administration",
        DSI: "DSI",
        Inspectors: "Inspectors",
        Remedial: "Remedial",
        NonFormal: "NonFormal",
        OfficeOrderly: "OfficeOrderly",
        HR: "HR",
        Aid: "Aid",
      },
      inputPlaceholder: "Select department",
      showCancelButton: true,
    });
    if (!dept) return;
    updateUser(id, { department: dept }, "Department updated");
  };

  const handleDeleteMessage = async (id) => {
    const confirm = await Swal.fire({
      title: "Delete message?",
      icon: "warning",
      showCancelButton: true,
      confirmButtonText: "Yes, delete",
    });
    if (!confirm.isConfirmed) return;

    try {
      const res = await authFetch(URLS.messageDelete(id), { method: "DELETE" });
      if (res.ok) {
        Swal.fire("Deleted", "Message removed", "success");
        loadData();
      } else {
        Swal.fire("Error", "Failed to delete message", "error");
      }
    } catch {
      Swal.fire("Error", "Unexpected error", "error");
    }
  };

  const handleEditMessage = async (msg) => {
    const { value: newText } = await Swal.fire({
      title: "Edit Message",
      input: "textarea",
      inputValue: msg.message,
      showCancelButton: true,
    });

    if (!newText || newText === msg.message) return;

    try {
      const res = await authFetch(URLS.messageEdit(msg.id), {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: newText }),
      });
      if (res.ok) {
        Swal.fire("Updated", "Message edited successfully", "success");
        loadData();
      } else {
        Swal.fire("Error", "Failed to edit message", "error");
      }
    } catch {
      Swal.fire("Error", "Unexpected error", "error");
    }
  };

  const getSenderName = (senderId) => {
    const sender = users.find((u) => u.id === senderId);
    return sender ? sender.username : "Unknown";
  };

  return (
    <div className="container mt-4">
      <h2>Unified Admin Dashboard</h2>

      {/* Users Table */}
      <h4 className="mt-4">User Management</h4>
      <table className="table table-bordered table-striped">
        <thead className="table-dark">
          <tr>
            <th>ID</th>
            <th>Username</th>
            <th>Email</th>
            <th>Department</th>
            <th>Phone</th>
            <th>Role</th>
            <th>Bio</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {users.map((row) => (
            <tr key={row.id}>
              <td>{row.id}</td>
              <td>{row.username}</td>
              <td>{row.email}</td>
              <td>{row.department || "—"}</td>
              <td>{row.phone_number || "—"}</td>
              <td>{row.is_admin ? "Admin" : "Staff"}</td>
              <td>{row.bio || "—"}</td>
              <td>
                {row.is_admin ? (
                  <button className="btn btn-sm btn-warning me-1" onClick={() => handleDemote(row.id)}>
                    Demote
                  </button>
                ) : (
                  <button className="btn btn-sm btn-primary me-1" onClick={() => handlePromote(row.id)}>
                    Promote
                  </button>
                )}
                <button className="btn btn-sm btn-info me-1" onClick={() => handleChangeDept(row.id)}>
                  Change Dept
                </button>
                <button className="btn btn-sm btn-danger" onClick={() => handleDeleteUser(row.id)}>
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Messages Table */}
      <h4 className="mt-5">Messages</h4>
      <table className="table table-bordered table-hover">
        <thead className="table-light">
          <tr>
            <th>ID</th>
            <th>Sender</th>
            <th>Message</th>
            <th>Timestamp</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {messages.map((msg) => (
            <tr key={msg.id}>
              <td>{msg.id}</td>
              <td>{getSenderName(msg.sender)}</td>
              <td>{msg.message}</td>
              <td>{new Date(msg.created_at).toLocaleString()}</td>
              <td>
                <button className="btn btn-sm btn-warning me-1" onClick={() => handleEditMessage(msg)}>
                  Edit
                </button>
                <button className="btn btn-sm btn-danger" onClick={() => handleDeleteMessage(msg.id)}>
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default AdminDashboardPage;
