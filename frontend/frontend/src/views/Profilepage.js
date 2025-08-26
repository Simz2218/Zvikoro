import React, { useState, useEffect, useContext } from "react";
import AuthContext, { URLS } from "../context/AuthContext";
import Swal from "sweetalert2";
import bluesky from "../views/pictures/bluesky.png";

const Profilepage = () => {
  const {
    authFetch,
    updateUserProfile,
    sendMessage,
    fetchUserProfile,
  } = useContext(AuthContext);

  const [formData, setFormData] = useState({
    username: "",
    email: "",
    bio: "",
    phone_number: "",
    department: "",
  });
  const [profilePreview, setProfilePreview] = useState(null);
  const [profileFile, setProfileFile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const res = await authFetch(URLS.userMe);
        if (res.ok) {
          const data = await res.json();
          setFormData({
            username: data.username || "",
            email: data.email || "",
            bio: data.bio || "",
            phone_number: data.admin?.phone_number || "",
            department: data.admin?.department || "",
          });
          setProfilePreview(data.profile_url || null);
        } else {
          Swal.fire("Error", "Failed to fetch profile", "error");
        }
      } catch {
        Swal.fire("Error", "Unexpected error fetching profile", "error");
      } finally {
        setLoading(false);
      }
    };
    fetchProfile();
  }, [authFetch]);

  const handleChange = (e) =>
    setFormData((prev) => ({ ...prev, [e.target.name]: e.target.value }));

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setProfileFile(file);
      setProfilePreview(URL.createObjectURL(file));
    }
  };

  const handleImageUpload = async (e) => {
    e.preventDefault();
    if (!profileFile)
      return Swal.fire("Error", "No image selected", "error");

    const formDataImg = new FormData();
    formDataImg.append("profile", profileFile);

    try {
      const res = await authFetch(URLS.userMe, {
        method: "PATCH",
        body: formDataImg,
      });
      if (res.ok) {
        Swal.fire({
          toast: true,
          position: "top-end",
          icon: "success",
          title: "Profile image updated",
          showConfirmButton: false,
          timer: 2000,
        });
        setProfileFile(null);
        await fetchUserProfile();
      } else {
        Swal.fire("Error", "Failed to upload image", "error");
      }
    } catch {
      Swal.fire("Error", "Unexpected error uploading image", "error");
    }
  };

  const handleImageRemove = async () => {
    await updateUserProfile({ profile: null });
    setProfilePreview(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await authFetch(URLS.userMe, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          username: formData.username,
          email: formData.email,
          bio: formData.bio,
          admin: { phone_number: formData.phone_number },
        }),
      });
      if (res.ok) {
        Swal.fire({
          toast: true,
          position: "top-end",
          icon: "success",
          title: "Profile updated",
          showConfirmButton: false,
          timer: 2000,
        });
        await fetchUserProfile();
      } else {
        const err = await res.json();
        Swal.fire("Error", err.detail || "Failed to update profile", "error");
      }
    } catch {
      Swal.fire("Error", "Unexpected error updating profile", "error");
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!message.trim())
      return Swal.fire("Error", "Message cannot be empty", "error");
    await sendMessage({ message });
    setMessage("");
  };

  if (loading) {
    return (
      <div className="container mt-4">
        <p>Loading profile…</p>
      </div>
    );
  }

  return (
    <div className="container mt-4">
      <h2>My Profile</h2>

      {/* Profile Image */}
      <div className="mb-4 text-center">
        <h5>Profile Image</h5>
        {profilePreview ? (
          <img
            src={profilePreview}
            alt="Profile"
            className="img-thumbnail"
            style={{ width: "120px", height: "120px", objectFit: "cover" }}
            onError={(e) => (e.target.src = "/default-avatar.png")}
          />
        ) : (
          <p>No image uploaded</p>
        )}
        <div className="mt-2">
          <input type="file" accept="image/*" onChange={handleImageChange} />
          <button
            className="btn btn-primary btn-sm ms-2"
            onClick={handleImageUpload}
          >
            Upload
          </button>
          <button
            className="btn btn-danger btn-sm ms-2"
            onClick={handleImageRemove}
          >
            Remove
          </button>
        </div>
      </div>

      {/* Profile Form */}
      <form onSubmit={handleSubmit} className="mt-3">
        <div className="mb-3">
          <label>Username</label>
          <input
            type="text"
            name="username"
            className="form-control"
            value={formData.username}
            onChange={handleChange}
            autoFocus
          />
        </div>

        <div className="mb-3">
          <label>Email</label>
          <input
            type="email"
            name="email"
            className="form-control"
            value={formData.email}
            onChange={handleChange}
          />
        </div>

        <div className="mb-3">
          <label>Phone Number</label>
          <input
            type="text"
            name="phone_number"
            className="form-control"
            value={formData.phone_number}
            onChange={handleChange}
          />
        </div>

        <div className="mb-3">
          <label>Department</label>
          <input
            type="text"
            className="form-control"
            value={formData.department || "—"}
            disabled
          />
        </div>

        <div className="mb-3">
          <label>Bio</label>
          <textarea
            name="bio"
            className="form-control"
            rows="3"
            value={formData.bio}
            onChange={handleChange}
          />
        </div>

        <button className="btn btn-success" type="submit" disabled={loading}>
          {loading ? "Saving…" : "Save Profile"}
        </button>
      </form>

      <hr className="my-4" />

      {/* Send Message */}
      <form onSubmit={handleSendMessage}>
        <h4>Send a Message</h4>
        <div className="mb-3">
          <textarea
            className="form-control"
            rows="3"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Type your message here..."
          />
        </div>
        <button className="btn btn-info" type="submit">
          Send Message
        </button>
      </form>
    </div>
  );
};

export default Profilepage;
