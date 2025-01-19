import axios from "axios";

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
    throw error.response.data;
  } else {
    throw new Error("Server error");
  }
};

// API: Register User
export const registerUser = async (userData) => {
  console.log("Calling registerUser with data:", userData); // Debug log
  try {
    const response = await apiClient.post("/register", {
      ...userData,
      accepted_terms: true,
      accepted_privacy_policy: true,
    });
    console.log("Register API Response:", response.data); // Debug log
    return response.data;
  } catch (error) {
    handleError(error);
  }
};

// API: Login User
export const loginUser = async (email, password, isMobile = false) => {
  try {
    const response = await apiClient.post("/login", { email, password, is_mobile: isMobile });
    // Store the session token
    localStorage.setItem("token", response.data.access_token);
    return response.data;
  } catch (error) {
    handleError(error);
  }
};

// API: Logout User
export const logoutUser = async () => {
  try {
    const response = await apiClient.post("/logout");
    // Clear the session token
    localStorage.removeItem("token");
    return response.data;
  } catch (error) {
    handleError(error);
  }
};

// API: Logout All Sessions
export const logoutAllSessions = async () => {
  try {
    const response = await apiClient.post("/logout-all");
    // Clear the session token
    localStorage.removeItem("token");
    return response.data;
  } catch (error) {
    handleError(error);
  }
};

// API: Verify Email
export const verifyEmail = async (token) => {
  try {
    const response = await apiClient.get(`/verify-email?token=${token}`);
    return response.data;
  } catch (error) {
    handleError(error);
  }
};

// API: Password Reset Request
export const requestPasswordReset = async (email) => {
  try {
    const response = await apiClient.post("/password-reset", { email });
    return response.data;
  } catch (error) {
    handleError(error);
  }
};

// API: Reset Password
export const resetPassword = async (token, newPassword) => {
  try {
    const response = await apiClient.post("/reset-password", {
      token,
      new_password: newPassword,
    });
    return response.data;
  } catch (error) {
    handleError(error);
  }
};

// API: Update User Subscription
export const updateUserSubscription = async (subscriptionTier) => {
  try {
    const response = await apiClient.post("/update-subscription", { subscriptionTier });
    return response.data; // Assume the response will return updated user data
  } catch (error) {
    handleError(error);
  }
};