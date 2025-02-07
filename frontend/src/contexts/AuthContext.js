import React, { createContext, useState, useEffect } from "react";
import { toast } from "react-toastify";
import { registerUser, loginUser, logoutUser } from "../api/authApi";
import { getProfile, getProfileVersion } from "../api/userApi";
import { useNavigate } from "react-router-dom";

// Create authentication context
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

  // Function to fetch device details
  const getDeviceDetails = async () => {
    try {
      const device_type = /Mobi|Android/i.test(navigator.userAgent) ? "Mobile" : "Desktop";
      const device_os = navigator.platform || "Unknown";
      const browser = navigator.userAgent || "Unknown";

      // Fetch public IP
      const ipResponse = await fetch("https://api.ipify.org?format=json");
      const { ip } = await ipResponse.json();

      // Fetch location based on IP
      const locationResponse = await fetch(`https://ipapi.co/${ip}/json/`);
      const locationData = await locationResponse.json();

      return {
        device_type,
        device_os,
        browser,
        ip_address: ip || "Unknown",
        location: locationData.city ? `${locationData.city}, ${locationData.region}, ${locationData.country_name}` : "Unknown",
      };
    } catch (error) {
      console.error("Error fetching IP/Location:", error);
      return {
        device_type: /Mobi|Android/i.test(navigator.userAgent) ? "Mobile" : "Desktop",
        device_os: navigator.platform || "Unknown",
        browser: navigator.userAgent || "Unknown",
        ip_address: "Unknown",
        location: "Unknown",
      };
    }
  };

  const register = async (userData) => {
    try {
      const response = await registerUser(userData);
      localStorage.setItem("token", response.access_token);

      // Load the user after successful registration
      const user = await loadUser(true);

      // Navigate based on setup_step
      if (user?.setup_step) {
        console.log("AuthContext: Navigating after registration - setup_step:", user.setup_step);
        switch (user.setup_step) {
          case "profile_completion":
            navigate("/dashboard", { state: { overlay: "profileCompletion" } });
            break;
          case "subscription_selection":
            navigate("/dashboard", { state: { overlay: "subscriptionSelection" } });
            break;
          default:
            navigate("/dashboard");
            break;
        }
      }

      toast.success("Account created successfully!");
    } catch (error) {
      toast.error(error.message || "Registration failed.");
      throw error;
    }
  };


const login = async (email, password, isMobile = false) => {
  try {
    const deviceDetails = await getDeviceDetails();
    const response = await loginUser(email, password, isMobile, deviceDetails);
    localStorage.setItem("token", response.access_token);

    const user = await loadUser(true);

    if (user?.setup_step) {
      switch (user.setup_step) {
        case "profile_completion":
          navigate("/dashboard", { state: { overlay: "profileCompletion" } });
          break;
        case "subscription_selection":
          navigate("/dashboard", { state: { overlay: "subscriptionSelection" } });
          break;
        default:
          navigate("/dashboard");
          break;
      }
    }

    toast.success("Login successful!");
    return user;
  } catch (error) {
    console.error("AuthContext: Login Error:", error);

    let errorMessage = "Login failed. Please try again.";

    if (error.response?.status === 401) {
      errorMessage = "Invalid Email or Password.";
    } else if (error.response?.status === 403) {
      errorMessage = "User account is inactive.";
    } else if (error.response?.data?.detail) {
      errorMessage = error.response.data.detail;
    }

    return Promise.reject({ message: errorMessage }); // Send structured error
  }
};



const loadUser = async (forceReload = false) => {
  console.log("AuthContext: Loading user...");
  const token = localStorage.getItem("token");

  if (!token) {
    console.log("AuthContext: No token found, setting user to null.");
    setCurrentUser(null);
    setLoading(false);
    return;
  }

  try {
    console.log("AuthContext: Checking profile version...");
    const latestVersion = await getProfileVersion();
    const { profile: cachedProfile, version: cachedVersion } = getCachedProfile();

    let user;
    if (!forceReload && cachedVersion === latestVersion && cachedProfile) {
      console.log("AuthContext: Using cached profile.");
      user = cachedProfile;
    } else {
      console.log("AuthContext: Fetching profile from API...");
      user = await getProfile();
      cacheProfile(user, latestVersion);
    }

    // Set the user after fetching the profile
    setCurrentUser(user);

    // 🚨 Prevent redirect if the user is on the payment success page
    if (window.location.pathname === "/payment-success") {
      return;
    } else if (window.location.pathname === "/payment-cancel") {
      return;
    }

    // Use the newly fetched `user`, not `currentUser`
    if (user?.setup_step) {
      console.log("AuthContext: Redirecting user based on setup_step:", user.setup_step);
      switch (user.setup_step) {
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
    console.error("AuthContext: Failed to load profile", error);
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
    navigate("/"); // Ensure user is redirected
    toast.success("Logged out successfully.");
  } catch (error) {
    toast.error(error.message || "Failed to log out.");
  }
};


  useEffect(() => {
      console.log("AuthContext: useEffect triggered, loading user...");
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
