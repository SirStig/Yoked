import axios from "axios";
import { toast } from "react-toastify";
import { getProfileVersion } from "./userApi";

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

// Function to get device details including IP and location
const getDeviceDetails = async () => {
  try {
    const device_type = /Mobi|Android/i.test(navigator.userAgent) ? "Mobile" : "Desktop";
    const device_os = navigator.platform || "Unknown";
    const browser = navigator.userAgent || "Unknown";

    // Fetch the user's public IP address
    const ipResponse = await fetch("https://api.ipify.org?format=json");
    const { ip } = await ipResponse.json();

    // Fetch location data based on IP
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

// Handle errors and display appropriate messages
const handleError = (error) => {
  console.error("API Error:", error);

  if (error.response) {
    const { status, data } = error.response;
    console.error("Error Details:", data);

    let errorMessage = "An unexpected error occurred.";

    if (data?.detail) {
      errorMessage = data.detail;
    } else if (status === 400) {
      errorMessage = "Bad request. Please check your input.";
    } else if (status === 401) {
      errorMessage = "Incorrect email or password.";
    } else if (status === 403) {
      errorMessage = "You do not have permission to perform this action.";
    } else if (status === 404) {
      errorMessage = "Resource not found.";
    } else if (status === 409) {
      errorMessage = "A conflict occurred. Possible duplicate entry.";
    }

    // Handle specific backend messages
    if (data?.detail?.includes("Username already registered")) {
      errorMessage = "Username already exists.";
    } else if (data?.detail?.includes("Email already registered")) {
      errorMessage = "Email already exists.";
    } else if (data?.detail?.includes("Invalid credentials")) {
      errorMessage = "Incorrect email or password.";
    }

    toast.error(errorMessage);
    return Promise.reject({ message: errorMessage, status, data });
  }

  const networkError = { message: "Network error. Please try again later.", status: 0 };
  toast.error(networkError.message);
  return Promise.reject(networkError);
};

// API: Register User
export const registerUser = async (userData) => {
  console.log("Registering user...");
  try {
    const response = await apiClient.post("/register", {
      ...userData,
      accepted_terms: true,
      accepted_privacy_policy: true,
    });
    return response.data;
  } catch (error) {
    return handleError(error);
  }
};

// API: Login User
export const loginUser = async (email, password) => {
  console.log("Logging in user...");

  try {
    // Fetch device details including IP and location
    const deviceDetails = await getDeviceDetails();

    const response = await apiClient.post("/login", {
      email,
      password,
      is_mobile: deviceDetails.device_type === "Mobile",
      ...deviceDetails, // Send all device info
    });

    // Store the session token
    localStorage.setItem("token", response.data.access_token);

    // Fetch and cache the profile version
    const version = await getProfileVersion();
    localStorage.setItem("profileVersion", version.toString());

    toast.success("Login successful!");
    return response.data;
  } catch (error) {
    return handleError(error);
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

    toast.success("Logged out successfully.");
    return response.data;
  } catch (error) {
    return handleError(error);
  }
};

// API: Logout All Sessions
export const logoutAllSessions = async () => {
  console.log("Logging out from all sessions...");
  try {
    const response = await apiClient.post("/logout-all");

    // Clear the session token and cache
    localStorage.removeItem("token");
    localStorage.removeItem("profileVersion");

    toast.success("Logged out from all devices.");
    return response.data;
  } catch (error) {
    return handleError(error);
  }
};
