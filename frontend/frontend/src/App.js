import React from 'react'
import { BrowserRouter as Router, Routes, Route } from "react-router-dom"
import PrivateRoute from "./utils/PrivateRoute"
import { AuthProvider } from "./context/AuthContext"
import Homepage from "./views/Homepage"
import UserCreationPage from "./views/UserCreationPage"
import LoginPage from "./views/LoginPage"
import Profilepage from "./views/Profilepage"
import Navbar from "./views/Navbar"
import Paymentspage from "./views/Paymentspage"
import HRpage from './views/HRpage';
import EmployeePage from './views/EmployeePage';

function App() {
  return (
    <Router>
      <AuthProvider>
        <Navbar/>
        <Routes>
          <Route path="/homepage" element={<Homepage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/employees" element={<EmployeePage />} />
          <Route element={<PrivateRoute />}>
            <Route path="/dashboard" element={<Profilepage />} />
            <Route path="/schools" element={<HRpage />} />
            <Route path="/payments" element={<Paymentspage />} />
            <Route path="/addUser" element={<UserCreationPage />} />
          </Route>
        </Routes>
      </AuthProvider>
    </Router>
  )
}

export default App;