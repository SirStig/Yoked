import React, { createContext, useState, useEffect } from "react";
import { toast } from "react-toastify";
import { registerUser, loginUser, logoutUser } from "../api/authApi"; // Import auth APIs
import { getProfile } from "../api/userApi"; // Import user profile API

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState(null);
  const [loading, setLoading] = useState(true); // To handle loading states

  // Register a new user
  const register = async (userData) => {
    try {
      const response = await registerUser(userData);
      toast.success("Account created! Verify your email to continue.");
      localStorage.setItem("token", response.access_token); // Save token

      // Load user profile after registration
      await loadUser();
    } catch (error) {
      toast.error(error.message || "Registration failed.");
    }
  };

  // Login user
  const login = async (email, password, isMobile = false) => {
    try {
      const response = await loginUser(email, password, isMobile);
      setCurrentUser(response.user); // Update current user state
      toast.success("Login successful!");

      // Navigate to setup step or dashboard
      if (response.user?.setup_step && response.user.setup_step !== "completed") {
        window.location.href = `/${response.user.setup_step}`;
      }
    } catch (error) {
      toast.error(error.message || "Login failed.");
    }
  };

  // Load the current user profile
  const loadUser = async () => {
    const token = localStorage.getItem("token");
    if (!token) {
      setLoading(false);
      setCurrentUser(null);
      return;
    }

    try {
      const user = await getProfile();
      setCurrentUser(user); // Set user data in state
    } catch (error) {
      toast.error(error.message || "Session expired. Please log in again.");
      localStorage.removeItem("token");
      setCurrentUser(null);
    } finally {
      setLoading(false);
    }
  };

  // Logout user
  const logout = async () => {
    try {
      await logoutUser();
      setCurrentUser(null);
      toast.success("Logged out successfully.");
    } catch (error) {
      toast.error(error.message || "Failed to log out.");
    } finally {
      localStorage.removeItem("token");
    }
  };

  // Initialize user data on app load
  useEffect(() => {
    loadUser();
  }, []);

  return (
    <AuthContext.Provider
      value={{
        currentUser,
        register,
        login,
        logout,
        loadUser,
        loading,
      }}
    >
      {loading ? (
        <div className="loading-spinner">
          <div className="spinner"></div>
        </div>
      ) : (
        children
      )}
    </AuthContext.Provider>
  );
};
