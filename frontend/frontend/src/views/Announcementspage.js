import React, { useEffect, useState, useContext } from "react";
import AuthContext from "../context/AuthContext";
import bluesky from "../views/pictures/bluesky.png";
import "./Announcement.css";

function AnnouncementsPage() {
  const { fetchPublicMessages } = useContext(AuthContext);
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    const loadMessages = async () => {
      const data = await fetchPublicMessages();
      setMessages(data);
    };
    loadMessages();
  }, [fetchPublicMessages]);

  return (
    <div
      className="announcements-container"
      style={{
        backgroundImage: `linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.4)), url(${bluesky})`,
        backgroundSize: "cover",
        backgroundPosition: "center",
        backgroundAttachment: "fixed",
        minHeight: "100vh",
        padding: "2rem 1rem",
      }}
    >
      <h1 className="page-title">📢 Announcements</h1>

      {messages.length === 0 ? (
        <p className="no-messages">No announcements yet.</p>
      ) : (
        messages.map((msg) => (
          <div key={msg.id} className="announcement-card">
            <div className="announcement-header">
              <img
                src={msg.profile_picture || "/default-avatar.png"}
                alt={msg.username}
                className="profile-pic"
                onError={(e) => (e.target.src = "/default-avatar.png")}
              />
              <div className="user-info">
                <h3 className="username">{msg.username}</h3>
                <span
                  className="department-badge"
                  title={`Department: ${msg.department}`}
                >
                  {msg.department || "—"}
                </span>
              </div>
            </div>
            <div className="announcement-body">
              <p>{msg.message}</p>
            </div>
          </div>
        ))
      )}
    </div>
  );
}

export default AnnouncementsPage;
