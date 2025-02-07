import axios from "axios";
import { toast } from "react-toastify";

// Axios instance for settings API
const apiClient = axios.create({
  baseURL: "http://127.0.0.1:8000/api/settings",
  headers: {
    "Content-Type": "application/json",
  },
});

// Attach Authorization token to requests
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Centralized error handler
const handleError = (error) => {
  console.error("API Error:", error);
  if (error.response?.data?.detail) {
    toast.error(error.response.data.detail);
    throw new Error(error.response.data.detail);
  } else {
    toast.error("An unexpected error occurred.");
    throw new Error("An unexpected error occurred.");
  }
};

/**
 * Update user profile settings
 * @param {Object} profileData - User's updated profile information
 */
export const updateProfileSettings = async (profileData) => {
  try {
    const response = await apiClient.put("/profile", profileData);
    toast.success("Profile updated successfully!");
    return response.data;
  } catch (error) {
    handleError(error);
  }
};

/**
 * Update user security settings (MFA, password change, account deactivation)
 * @param {Object} securityData - User's security preferences
 */
export const updateSecuritySettings = async (securityData) => {
  try {
    const response = await apiClient.put("/security", securityData);
    toast.success("Security settings updated!");
    return response.data;
  } catch (error) {
    handleError(error);
  }
};

/**
 * Update notification preferences
 * @param {Object} notificationData - User's notification settings
 */
export const updateNotificationPreferences = async (notificationData) => {
  try {
    const response = await apiClient.put("/notifications", notificationData);
    toast.success("Notification preferences updated!");
    return response.data;
  } catch (error) {
    handleError(error);
  }
};

/**
 * Cancel user's subscription
 */
export const cancelSubscription = async () => {
  try {
    const response = await apiClient.post("/subscription/cancel");
    toast.success("Subscription canceled successfully!");
    return response.data;
  } catch (error) {
    handleError(error);
  }
};

/**
 * Update user's subscription tier
 * @param {string} newTierId - ID of the new subscription tier
 */
export const updateSubscription = async (newTierId) => {
  try {
    const response = await apiClient.put("/subscription/update", {
      new_tier_id: newTierId,
    });
    toast.success("Subscription updated successfully!");
    return response.data;
  } catch (error) {
    handleError(error);
  }
};

/**
 * Request email verification before updating email
 * @param {string} newEmail - The new email address
 */
export const requestEmailUpdate = async (newEmail) => {
  try {
    const response = await apiClient.post("/email/update-request", {
      new_email: newEmail,
    });
    toast.info("Verification code sent to your new email.");
    return response.data;
  } catch (error) {
    handleError(error);
  }
};

/**
 * Verify email update with the received code
 * @param {string} verificationCode - Code received via email
 */
export const verifyEmailUpdate = async (verificationCode) => {
  try {
    const response = await apiClient.post("/email/verify", {
      verification_code: verificationCode,
    });
    toast.success("Email updated successfully!");
    return response.data;
  } catch (error) {
    handleError(error);
  }
};

/**
 * Change user password (Requires old password & new password)
 * @param {Object} passwordData - Old and new password fields
 */
export const changePassword = async (passwordData) => {
  try {
    const response = await apiClient.put("/password/update", passwordData);
    toast.success("Password changed successfully!");
    return response.data;
  } catch (error) {
    handleError(error);
  }
};

/**
 * Fetch all active user sessions
 * @returns {Array} List of user sessions
 */
export const getUserSessions = async () => {
  try {
    const response = await apiClient.get("/sessions");
    return response.data;
  } catch (error) {
    handleError(error);
  }
};

/**
 * Log out a specific session by ID
 * @param {string} sessionId - ID of the session to revoke
 */
export const revokeSession = async (sessionId) => {
  try {
    await apiClient.delete(`/sessions/${sessionId}`);
    toast.success("Session logged out successfully.");
  } catch (error) {
    handleError(error);
  }
};

/**
 * Fetch the user's current subscription details
 * @returns {Object} Subscription details
 */
export const getSubscriptionDetails = async () => {
  try {
    const response = await apiClient.get("/subscription");
    return response.data;
  } catch (error) {
    handleError(error);
  }
};

/**
 * Fetch user's notification preferences
 * @returns {Object} Notification settings
 */
export const getNotificationPreferences = async () => {
  try {
    const response = await apiClient.get("/notifications");
    return response.data;
  } catch (error) {
    handleError(error);
  }
};

/**
 * Fetch user's Reels & Community settings
 * @returns {Object} Reels & Community settings
 */
export const getReelsCommunitySettings = async () => {
  try {
    const response = await apiClient.get("/reels");
    return response.data;
  } catch (error) {
    handleError(error);
  }
};

/**
 * Update user's Reels & Community settings
 * @param {Object} settings - Updated settings
 */
export const updateReelsCommunitySettings = async (settings) => {
  try {
    await apiClient.put("/reels", settings);
    toast.success("Reels & Community settings updated successfully.");
  } catch (error) {
    handleError(error);
  }
};

/**
 * Fetch user's Fitness settings
 * @returns {Object} Fitness settings
 */
export const getFitnessSettings = async () => {
  try {
    const response = await apiClient.get("/nutrition");
    return response.data;
  } catch (error) {
    handleError(error);
  }
};

/**
 * Update user's Fitness settings
 * @param {Object} settings - Updated settings
 */
export const updateFitnessSettings = async (settings) => {
  try {
    await apiClient.put("/nutrition", settings);
    toast.success("Fitness settings updated successfully.");
  } catch (error) {
    handleError(error);
  }
};
