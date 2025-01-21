import axios from "axios";
import { toast } from "react-toastify";

// Axios instance for centralized configuration
const apiClient = axios.create({
  baseURL: "http://127.0.0.1:8000/api/auth",
  headers: {
    "Content-Type": "application/json",
  },
});

// Attach Authorization header to requests if token is available
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Normalize errors for consistency
const handleError = (error) => {
  console.error("API Error:", error);
  if (error.response) {
    console.error("Error Details:", error.response.data);
    toast.error(error.response.data?.detail || "An unexpected error occurred.");
    throw new Error(error.response.data?.detail || "An unexpected error occurred.");
  } else {
    toast.error("Network error. Please try again later.");
    throw new Error("Network error. Please try again later.");
  }
};

// Caching layer for profile version
let cachedProfileVersion = localStorage.getItem("profileVersion")
  ? parseInt(localStorage.getItem("profileVersion"), 10)
  : null;

// API: Register User
export const registerUser = async (userData) => {
  console.log("Registering user...");
  try {
    const response = await apiClient.post("/register", {
      ...userData,
      accepted_terms: true,
      accepted_privacy_policy: true,
    });
    console.log("Register API Response:", response.data);
    return response.data;
  } catch (error) {
    handleError(error);
  }
};

// API: Login User
export const loginUser = async (email, password, isMobile = false) => {
  console.log("Logging in user...");
  try {
    const response = await apiClient.post("/login", { email, password, is_mobile: isMobile });

    // Store the session token
    localStorage.setItem("token", response.data.access_token);

    // Fetch and cache the profile version
    const version = await getProfileVersion();
    cachedProfileVersion = version;

    // Cache the profile version in localStorage
    localStorage.setItem("profileVersion", version.toString());

    return response.data;
  } catch (error) {
    handleError(error);
  }
};

// API: Logout User
export const logoutUser = async () => {
  console.log("Logging out user...");
  try {
    const response = await apiClient.post("/logout");

    // Clear the session token and cache
    localStorage.removeItem("token");
    localStorage.removeItem("profileVersion");
    cachedProfileVersion = null;

    return response.data;
  } catch (error) {
    handleError(error);
  }
};

// API: Get Profile Version
export const getProfileVersion = async () => {
  try {
    const response = await apiClient.get("/profile/version");
    const version = response.data.version;

    // Cache the version in localStorage
    cachedProfileVersion = version;
    localStorage.setItem("profileVersion", version.toString());

    return version;
  } catch (error) {
    handleError(error);
  }
};
