import React, { createContext, useState, useEffect } from "react";
import { toast } from "react-toastify";
import { registerUser, loginUser, logoutUser } from "../api/authApi"; // Import auth APIs
import { getProfile, getProfileVersion } from "../api/userApi"; // Import user profile APIs
import { useNavigate } from "react-router-dom";  // Import navigate

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState(null);
  const [loading, setLoading] = useState(true); // To handle loading states
  const navigate = useNavigate();  // Initialize navigate for programmatic navigation

  // Fetch cached profile and version from localStorage
  const getCachedProfile = () => {
    const cachedProfile = localStorage.getItem("profile");
    const cachedVersion = localStorage.getItem("profileVersion");
    return {
      profile: cachedProfile ? JSON.parse(cachedProfile) : null,
      version: cachedVersion ? parseInt(cachedVersion, 10) : null,
    };
  };

  // Cache profile and version in localStorage
  const cacheProfile = (profile, version) => {
    localStorage.setItem("profile", JSON.stringify(profile));
    localStorage.setItem("profileVersion", version.toString());
  };

  // Register a new user
  const register = async (userData) => {
    try {
      console.log("Registering user...");
      const response = await registerUser(userData);
      console.log("Registration response:", response);
      localStorage.setItem("token", response.access_token);
      console.log("Token stored in localStorage:", response.access_token);
      await loadUser(true); // Force reload profile after registration
    } catch (error) {
      console.error("Registration error:", error);
    }
  };

  // Login user
  const login = async (email, password, isMobile = false) => {
    try {
      const response = await loginUser(email, password, isMobile);

      // Save token to localStorage
      localStorage.setItem("token", response.access_token);
      console.log("Token stored in localStorage:", response.access_token);

      // Load user profile
      const user = await loadUser(true); // Force reload profile after login
      toast.success("Login successful!");
      return user; // Return the user object for navigation logic
    } catch (error) {
      toast.error(error.message || "Login failed.");
      throw error;
    }
  };

  // Load the current user profile with optional force reload
  const loadUser = async (forceReload = false) => {
    const token = localStorage.getItem("token");
    if (!token) {
      setCurrentUser(null);
      setLoading(false);
      return;
    }

    try {
      const latestVersion = await getProfileVersion(); // Fetch profile version from /profile endpoint
      const { profile: cachedProfile, version: cachedVersion } = getCachedProfile();

      // If version matches, use the cached profile
      if (!forceReload && cachedVersion === latestVersion && cachedProfile) {
        setCurrentUser(cachedProfile);
      } else {
        // Fetch fresh profile data
        const user = await getProfile();
        cacheProfile(user, latestVersion);  // Cache the fresh profile data
        setCurrentUser(user);
      }

      // Redirect based on setup_step (ensure we use the updated route names)
      if (currentUser?.setup_step) {
        const step = currentUser.setup_step;
        const setupRoutes = {
          "verify_email": "/verify_email",
          "profile_completion": "/profile-setup",
          "subscription_selection": "/choose-subscription",
        };

        if (step !== "completed" && setupRoutes[step]) {
          navigate(setupRoutes[step]);
        }
      }
    } catch (error) {
      console.error("Error loading user profile:", error);
      toast.error("Failed to load profile. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  // Logout user
  const logout = async () => {
    try {
      await logoutUser();
      setCurrentUser(null);
      localStorage.clear(); // Clear all cached data
      toast.success("Logged out successfully.");
    } catch (error) {
      toast.error(error.message || "Failed to log out.");
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
        setCurrentUser,
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
