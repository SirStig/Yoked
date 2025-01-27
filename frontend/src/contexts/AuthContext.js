import React, { createContext, useState, useEffect } from "react";
import { toast } from "react-toastify";
import { registerUser, loginUser, logoutUser } from "../api/authApi";
import { getProfile, getProfileVersion } from "../api/userApi";
import { useNavigate } from "react-router-dom";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  const getCachedProfile = () => {
    const cachedProfile = localStorage.getItem("profile");
    const cachedVersion = localStorage.getItem("profileVersion");
    return {
      profile: cachedProfile ? JSON.parse(cachedProfile) : null,
      version: cachedVersion ? parseInt(cachedVersion, 10) : null,
    };
  };

  const cacheProfile = (profile, version) => {
    localStorage.setItem("profile", JSON.stringify(profile));
    localStorage.setItem("profileVersion", version.toString());
  };

  const register = async (userData) => {
    try {
      const response = await registerUser(userData);
      localStorage.setItem("token", response.access_token);
      await loadUser(true);
    } catch (error) {
      toast.error(error.message || "Registration failed.");
      throw error;
    }
  };

  const login = async (email, password, isMobile = false) => {
    try {
      const response = await loginUser(email, password, isMobile);
      localStorage.setItem("token", response.access_token);
      const user = await loadUser(true);
      toast.success("Login successful!");
      return user;
    } catch (error) {
      toast.error(error.message || "Login failed.");
      throw error;
    }
  };

  const loadUser = async (forceReload = false) => {
    const token = localStorage.getItem("token");
    if (!token) {
      setCurrentUser(null);
      setLoading(false);
      return;
    }

    try {
      const latestVersion = await getProfileVersion();
      const { profile: cachedProfile, version: cachedVersion } = getCachedProfile();

      if (!forceReload && cachedVersion === latestVersion && cachedProfile) {
        setCurrentUser(cachedProfile);
      } else {
        const user = await getProfile();
        cacheProfile(user, latestVersion);
        setCurrentUser(user);
      }

      if (currentUser?.setup_step) {
        switch (currentUser.setup_step) {
          case "verify_email":
            navigate("/verify-email");
            break;
          case "profile_completion":
            navigate("/dashboard", { state: { overlay: "profileCompletion" } });
            break;
          case "subscription_selection":
            navigate("/dashboard", { state: { overlay: "subscriptionSelection" } });
            break;
          case "completed":
            navigate("/dashboard");
            break;
          default:
            navigate("/");
            break;
        }
      }
    } catch (error) {
      toast.error("Failed to load profile. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const logout = async () => {
    try {
      await logoutUser();
      setCurrentUser(null);
      localStorage.clear();
      toast.success("Logged out successfully.");
    } catch (error) {
      toast.error(error.message || "Failed to log out.");
    }
  };

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
