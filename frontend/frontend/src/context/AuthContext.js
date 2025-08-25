// src/context/AuthContext.js
import { createContext, useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import Swal from "sweetalert2";

const AuthContext = createContext();
const BASE_URL = "http://127.0.0.1:8000/schools/";

export const URLS = {
  // Auth
  token: `${BASE_URL}token/`,
  tokenRefresh: `${BASE_URL}token/refresh/`,

  // Accounts
  users: `${BASE_URL}users/`,
  userDetail: (id) => `${BASE_URL}users/${id}/`,
  registerUser: `${BASE_URL}register/`,
  admins: `${BASE_URL}admins/`,
  adminDetail: (id) => `${BASE_URL}admins/${id}/`,
  registerAdmin: `${BASE_URL}admins/create/`,
  changePassword: (id) => `${BASE_URL}admins/${id}/change-password/`,

  // Other resources
  sSchools: `${BASE_URL}secondary-schools/`,
  sGradeEnrollments: `${BASE_URL}sgrade-enrollments/`,
  sTeacherData: `${BASE_URL}steacher/teacher-data/`,
  pSchools: `${BASE_URL}primary-schools/`,
  gradeEnrollments: `${BASE_URL}grade-enrollments/`,
  teacherData: `${BASE_URL}teacher/teacher-data/`,
  userMe: `${BASE_URL}users/me/`,

  // Payments
  updateBalances: `${BASE_URL}update-balance/`,

  // Uploads
  uploadExcel: `${BASE_URL}upload-excel/`,
  sUploadExcel: `${BASE_URL}supload-excel/`,

  // Messages
  messages: `${BASE_URL}messages/`,
  messagesPublic: `${BASE_URL}messages/public/`,
  messageEdit: (id) => `${BASE_URL}messages/${id}/edit/`,
  messageDelete: (id) => `${BASE_URL}messages/${id}/delete/`,
};


// Decode JWT payload
const decodeToken = (token) => {
  try {
    return JSON.parse(atob(token.split(".")[1]));
  } catch {
    return null;
  }
};

// Check token expiry with buffer
const isTokenExpired = (token) => {
  const payload = decodeToken(token);
  if (!payload) return true;
  const expiryTime = payload.exp * 1000;
  const now = Date.now();
  const buffer = 60 * 1000; // refresh 1 min before expiry
  return expiryTime - now < buffer;
};

export const AuthProvider = ({ children }) => {
  const navigate = useNavigate();
  const [authTokens, setAuthTokens] = useState(() =>
    JSON.parse(localStorage.getItem("authTokens") || "null")
  );
  const [user, setUser] = useState(() =>
    JSON.parse(localStorage.getItem("user") || "null")
  );

  // Logout
  const logout = useCallback(() => {
    setAuthTokens(null);
    setUser(null);
    localStorage.removeItem("authTokens");
    localStorage.removeItem("user");
    navigate("/login");
  }, [navigate]);

  // Refresh token (handles rotation)
  const refreshToken = useCallback(async () => {
    if (!authTokens?.refresh) return logout();
    try {
      const res = await fetch(URLS.tokenRefresh, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ refresh: authTokens.refresh }),
      });

      if (res.ok) {
        const data = await res.json();
        const updated = {
          access: data.access,
          refresh: data.refresh || authTokens.refresh, // store rotated refresh if provided
        };
        setAuthTokens(updated);
        localStorage.setItem("authTokens", JSON.stringify(updated));
      } else {
        logout();
      }
    } catch {
      logout();
    }
  }, [authTokens, logout]);

  // Authenticated fetch with 401 safeguard
  const authFetch = useCallback(
    async (url, options = {}) => {
      if (isTokenExpired(authTokens?.access)) {
        await refreshToken();
      }

      const headers = {
        Authorization: `Bearer ${authTokens?.access}`,
        ...options.headers,
      };

      if (!(options.body instanceof FormData)) {
        headers["Content-Type"] = "application/json";
      }

      const response = await fetch(url, { ...options, headers });

      // If still unauthorized after refresh, logout
      if (response.status === 401) {
        logout();
      }

      return response;
    },
    [authTokens, refreshToken, logout]
  );

  // Fetch user profile
const fetchUserProfile = useCallback(async () => {
  if (!authTokens?.access) return;
  try {
    const res = await authFetch(URLS.userMe);
    if (res.ok) {
      const data = await res.json();
      setUser(data);
      localStorage.setItem("user", JSON.stringify(data));
    }
  } catch {
    /* silent */
  }
}, [authFetch, authTokens]);

  // Login
// Login
const loginUser = async (username, password) => {
  try {
    const res = await fetch(URLS.token, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });
    if (res.ok) {
      const data = await res.json();
      setAuthTokens({ access: data.access, refresh: data.refresh });
      localStorage.setItem("authTokens", JSON.stringify({ access: data.access, refresh: data.refresh }));
      setUser(data.user); // Set user state with the entire user object
      localStorage.setItem("user", JSON.stringify(data.user)); // Store user object in local storage
      Swal.fire("Login successful", "", "success");
      navigate("/homepage");
    } else {
      const err = await res.json();
      Swal.fire("Error", err.detail || "Invalid credentials", "error");
    }
  } catch {
    Swal.fire("Error", "Unexpected error during login", "error");
  }
};

  // Create admin
  const createAdmin = async (payload) => {
    try {
      const res = await fetch(URLS.registerAdmin, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (res.status === 201) {
        Swal.fire("Admin created successfully", "", "success");
        navigate("/login");
      } else {
        const err = await res.json();
        Swal.fire("Error", err.detail || "Check your data", "error");
      }
    } catch {
      Swal.fire("Error", "Unexpected error during admin creation", "error");
    }
  };

  // Register user
  const registerUser = async (payload) => {
    if (payload.password !== payload.password2)
      return Swal.fire("Error", "Passwords do not match", "error");
    try {
      const res = await fetch(URLS.registerUser, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (res.status === 201) {
        Swal.fire("User registration successful", "", "success");
        navigate("/login");
      } else {
        const err = await res.json();
        Swal.fire("Error", err.detail || "Check your data", "error");
      }
    } catch {
      Swal.fire("Error", "Unexpected error during registration", "error");
    }
  };

  // Update term balances (POST)
  const updateTermBalances = async () => {
    try {
      const res = await authFetch(URLS.updateBalances, { method: "POST" });
      if (res.ok) {
        Swal.fire("Success", "Term balances updated.", "success");
        return true;
      } else {
        const err = await res.text();
        Swal.fire("Error", err || "Failed to update term balances", "error");
        return false;
      }
    } catch {
      Swal.fire("Error", "Unexpected error while updating balances", "error");
      return false;
    }
  };

  // Update user profile
// Update user profile
const updateUserProfile = async (payload) => {
  try {
    const res = await authFetch(URLS.userMe, {
      method: "PATCH", // partial update
      body: JSON.stringify(payload),
    });
    if (res.ok) {
      Swal.fire("Profile updated", "", "success");
      await fetchUserProfile();
    } else {
      const err = await res.json();
      Swal.fire("Error", JSON.stringify(err), "error");
    }
  } catch {
    Swal.fire("Error", "Unexpected error updating profile", "error");
  }
};


  // Send message
  const sendMessage = async (payload) => {
    try {
      const res = await authFetch(URLS.messages, {
        method: "POST",
        body: JSON.stringify(payload),
      });
      if (res.ok) {
        Swal.fire("Message sent", "", "success");
        return true;
      } else {
        const err = await res.json();
        Swal.fire("Error", err.detail || "Failed to send message", "error");
        return false;
      }
    } catch {
      Swal.fire("Error", "Unexpected error while sending message", "error");
      return false;
    }
  };

  // Fetch public messages
  const fetchPublicMessages = async () => {
    try {
      const res = await fetch(URLS.messagesPublic);
      if (res.ok) {
        return await res.json();
      } else {
        Swal.fire("Error", "Failed to load announcements", "error");
        return [];
      }
    } catch {
      Swal.fire("Error", "Unexpected error loading announcements", "error");
      return [];
    }
  };

  const contextData = {
    user,
    authTokens,
    loginUser,
    logout,
    registerUser,
    createAdmin,
    authFetch,
    URLS,
    updateTermBalances,
    updateUserProfile,
    sendMessage,
    fetchPublicMessages,
    fetchUserProfile,
  };

  return (
    <AuthContext.Provider value={contextData}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext;