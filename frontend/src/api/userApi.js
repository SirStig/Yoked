import axios from "axios";

// Axios instance for centralized configuration
const apiClient = axios.create({
  baseURL: "http://127.0.0.1:8000/api/users",
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
  if (error.response) {
    throw new Error(error.response.data?.detail || "An error occurred.");
  } else if (error.request) {
    throw new Error("No response from the server. Please try again later.");
  } else {
    throw new Error("An unexpected error occurred.");
  }
};

// API: Update Profile
export const updateProfile = async (profileData) => {
  try {
    const response = await apiClient.put("/profile", profileData);
    return response.data;
  } catch (error) {
    handleError(error);
  }
};

// API: Get Profile
export const getProfile = async () => {
  try {
    const response = await apiClient.get("/profile");
    return response.data;
  } catch (error) {
    handleError(error);
  }
};

// API: Delete Account
export const deleteAccount = async () => {
  try {
    const response = await apiClient.put("/deactivate"); // Updated to match `/deactivate` route
    return response.data;
  } catch (error) {
    handleError(error);
  }
};

// API: Reactivate Account
export const reactivateAccount = async (userId) => {
  try {
    const response = await apiClient.put("/reactivate", { user_id: userId }); // Match `reactivate` route
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

// API: Specific Session Logout (for mobile or specific sessions)
export const logoutSession = async (token) => {
  try {
    const response = await apiClient.post("/logout", { token });
    return response.data;
  } catch (error) {
    handleError(error);
  }
};

// API: Update User Setup Step
export const updateUserSetupStep = async (setupStep) => {
  try {
    const response = await apiClient.put("/profile", { setup_step: setupStep }); // Adjust if backend requires a separate endpoint
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
