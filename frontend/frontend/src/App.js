import React, { useContext } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import PrivateRoute from "./utils/PrivateRoute";
import { AuthProvider } from "./context/AuthContext";
import 'react-data-grid/lib/styles.css';
import 'bootstrap/dist/css/bootstrap.min.css';

// Layout
import Navbar from "./views/Navbar";

// Pages
import Homepage from "./views/Homepage";
import LoginPage from "./views/LoginPage";
import Profilepage from "./views/Profilepage";
import Paymentspage from "./views/Paymentspage";
import HRpage from "./views/HRpage";
import EmployeePage from "./views/EmployeePage";
import PryPaymentsPage from "./views/PryPaymentsPage";
import SecPaymentsPage from "./views/SecPaymentsPage";
import PaymentsTable from "./views/PaymentsTable";
import AdminDashboardPage from "./views/AdminDashboardPage";
import RegisterPage from "./views/RegisterPage";
import AdminCreationTable from "./views/AdminCreationTable";
import Announcementspage from "./views/Announcementspage";
import CreateAdminPage from "./views/CreateAdminPage"; // ✅ New page

import AuthContext from "./context/AuthContext";

function AppRoutes() {
  const { user } = useContext(AuthContext);

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
    <Routes>
      {/* Public */}
      <Route path="/homepage" element={<Homepage />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route path="/announcements" element={<Announcementspage />} />

      {/* Authenticated */}
      <Route element={<PrivateRoute />}>
        <Route path="/dashboard" element={<Profilepage />} />
        <Route path="/profile/edit" element={<Profilepage />} />

        {canSeeSchools && (
          <Route path="/schools" element={<HRpage />} />
        )}

        {canSeeEmployees && (
          <Route path="/employees" element={<EmployeePage />} />
        )}

        {canSeePayments && (
          <>
            <Route path="/payments" element={<Paymentspage />} />
            <Route path="/payments/primary" element={<PryPaymentsPage />} />
            <Route path="/payments/secondary" element={<SecPaymentsPage />} />
            <Route path="/payments/secondary-table" element={<PaymentsTable />} />
          </>
        )}

        {isAdmin && (
          <>
            <Route path="/admin-dashboard" element={<AdminDashboardPage />} />
            <Route path="/admin-creation-table" element={<AdminCreationTable />} />
            <Route path="/admin-create" element={<CreateAdminPage />} /> {/* ✅ New route */}
          </>
        )}
      </Route>
    </Routes>
  );
}

function App() {
  return (
    <Router>
      <AuthProvider>
        <Navbar />
        <AppRoutes />
      </AuthProvider>
    </Router>
  );
}

export default App;
