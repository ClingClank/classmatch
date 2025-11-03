import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import Navigation from "./components/Nav";
import ProtectedRoute from "./components/ProtectedRoute";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Dashboard from "./pages/Dashboard";
import BrowseCourses from "./pages/BrowseCourses";
import Matches from "./pages/Matches";
import CreateGroup from "./pages/CreateGroup";
import "bootstrap/dist/css/bootstrap.min.css";
import "./style.css";

export default function App() {
  return (
    <AuthProvider>
      <div className="app-wrapper">
        <Navigation />
        <main className="main-content">
          <Routes>
            {/* Public routes */}
            <Route path="/" element={<Login />} />
            <Route path="/signup" element={<Signup />} />

            {/* Protected routes */}
            <Route
              path="/dashboard"
              element={
                <ProtectedRoute>
                  <Dashboard />
                </ProtectedRoute>
              }
            />
            <Route
              path="/browse-courses"
              element={
                <ProtectedRoute>
                  <BrowseCourses />
                </ProtectedRoute>
              }
            />
            <Route
              path="/matches"
              element={
                <ProtectedRoute>
                  <Matches />
                </ProtectedRoute>
              }
            />
            <Route
              path="/create-group"
              element={
                <ProtectedRoute>
                  <CreateGroup />
                </ProtectedRoute>
              }
            />

            {/* Catch all */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>
      </div>
    </AuthProvider>
  );
}
