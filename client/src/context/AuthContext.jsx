import React, { createContext, useContext, useState, useEffect } from "react";
import { sampleUsers } from "../data/sampleData";

const AuthContext = createContext(null);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check for existing session on mount
    const sessionData = localStorage.getItem("classmatch_session");
    if (sessionData) {
      try {
        const session = JSON.parse(sessionData);
        const foundUser = sampleUsers.find((u) => u.email === session.email);
        if (foundUser) {
          setUser(foundUser);
        }
      } catch (error) {
        console.error("Error loading session:", error);
        localStorage.removeItem("classmatch_session");
      }
    }
    setLoading(false);
  }, []);

  const login = (email, password) => {
    // Find user in sample data
    const foundUser = sampleUsers.find(
      (u) => u.email === email && u.password === password
    );

    if (!foundUser) {
      throw new Error("Invalid email or password");
    }

    // Create session
    const session = { email: foundUser.email, timestamp: Date.now() };
    localStorage.setItem("classmatch_session", JSON.stringify(session));

    setUser(foundUser);
    return foundUser;
  };

  const signup = (userData) => {
    // In real app, this would call API
    // For now, just add to localStorage
    const users = JSON.parse(localStorage.getItem("classmatch_users") || "[]");

    // Check if email exists
    if (
      users.find((u) => u.email === userData.email) ||
      sampleUsers.find((u) => u.email === userData.email)
    ) {
      throw new Error("Email already exists");
    }

    const newUser = {
      id: Date.now(),
      ...userData,
      avatar: userData.name
        .split(" ")
        .map((n) => n[0])
        .join("")
        .toUpperCase(),
      enrolledCourses: [],
      studyPreferences: {
        times: [],
        location: [],
        style: "",
      },
    };

    users.push(newUser);
    localStorage.setItem("classmatch_users", JSON.stringify(users));

    // Auto login after signup
    const session = { email: newUser.email, timestamp: Date.now() };
    localStorage.setItem("classmatch_session", JSON.stringify(session));
    setUser(newUser);

    return newUser;
  };

  const logout = () => {
    localStorage.removeItem("classmatch_session");
    setUser(null);
  };

  const updateProfile = (updates) => {
    const updatedUser = { ...user, ...updates };
    setUser(updatedUser);

    // Update in localStorage for persistence
    const users = JSON.parse(localStorage.getItem("classmatch_users") || "[]");
    const index = users.findIndex((u) => u.email === user.email);
    if (index !== -1) {
      users[index] = updatedUser;
      localStorage.setItem("classmatch_users", JSON.stringify(users));
    }
  };

  const value = {
    user,
    login,
    signup,
    logout,
    updateProfile,
    isAuthenticated: !!user,
    loading,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
