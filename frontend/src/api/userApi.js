import axios from "axios";

// Axios instance for centralized configuration
const apiClient = axios.create({
  baseURL: "http://127.0.0.1:8000/api/users",  // Make sure this matches your backend URL
  headers: {
    "Content-Type": "application/json",
  },
});

// Attach token automatically for authenticated requests
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Centralized error handling
const handleError = (error) => {
  console.error("API Error:", error);
  if (error.response) {
    console.error("Error Details:", error.response.data);
    throw new Error(error.response.data?.detail || "An error occurred.");
  } else if (error.request) {
    throw new Error("No response from the server. Please try again later.");
  } else {
    throw new Error("An unexpected error occurred.");
  }
};

// Caching layer for profile data
let cachedProfile = localStorage.getItem("profile")
  ? JSON.parse(localStorage.getItem("profile"))
  : null;

let cachedProfileVersion = localStorage.getItem("profileVersion")
  ? parseInt(localStorage.getItem("profileVersion"), 10)
  : null;

const cacheProfile = (profile, version) => {
  cachedProfile = profile;
  cachedProfileVersion = version;
  localStorage.setItem("profile", JSON.stringify(profile));
  localStorage.setItem("profileVersion", version.toString());
};

const clearCache = () => {
  cachedProfile = null;
  cachedProfileVersion = null;
  localStorage.removeItem("profile");
  localStorage.removeItem("profileVersion");
};

// API: Get Profile
export const getProfile = async () => {
  try {
    const response = await apiClient.get("/profile");
    cacheProfile(response.data, response.data.profile_version);
    return response.data;
  } catch (error) {
    handleError(error);
  }
};

// API: Get Profile Version with Caching
export const getProfileVersion = async () => {
  try {
    const response = await apiClient.get("/profile");
    return response.data.profile_version;  // Use profile_version from the response
  } catch (error) {
    handleError(error);
  }
};

// API: Update Profile
export const updateProfile = async (profileData) => {
  try {
    const response = await apiClient.put("/profile", profileData);

    // Invalidate cache on update
    clearCache();

    return response.data;
  } catch (error) {
    handleError(error);
  }
};

// API: Delete Account
export const deleteAccount = async () => {
  try {
    const response = await apiClient.put("/deactivate");
    return response.data;
  } catch (error) {
    handleError(error);
  }
};

// API: Reactivate Account
export const reactivateAccount = async (userId) => {
  try {
    const response = await apiClient.put("/reactivate", { user_id: userId });

    // Invalidate cache on reactivation
    clearCache();

    return response.data;
  } catch (error) {
    handleError(error);
  }
};

// API: Invalidate All Sessions
export const logoutAllSessions = async () => {
  try {
    const response = await apiClient.post("/logout-all");
    return response.data;
  } catch (error) {
    handleError(error);
  }
};

// API: Update User Setup Step
export const updateUserSetupStep = async (setupStep) => {
  try {
    const response = await apiClient.put("/profile", { setup_step: setupStep });

    // Invalidate cache on setup step update
    clearCache();

    return response.data;
  } catch (error) {
    handleError(error);
  }
};

// API: Check Active Status
export const checkActiveStatus = async () => {
  try {
    const response = await apiClient.get("/active-status");
    return response.data;
  } catch (error) {
    handleError(error);
  }
};
