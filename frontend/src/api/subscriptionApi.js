import axios from "axios";
import { toast } from "react-toastify";

// Axios instance for centralized configuration
const apiClient = axios.create({
  baseURL: "http://127.0.0.1:8000/api/subscriptions", // Ensure this is the correct endpoint
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

// Centralized error handling
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

// Helper functions to handle localStorage caching
const getCachedSubscriptions = () => {
  const subscriptions = localStorage.getItem("cachedSubscriptions");
  const version = localStorage.getItem("cachedSubscriptionVersion");
  return {
    subscriptions: subscriptions ? JSON.parse(subscriptions) : null,
    version: version ? parseInt(version, 10) : null,
  };
};

const setCachedSubscriptions = (subscriptions, version) => {
  localStorage.setItem("cachedSubscriptions", JSON.stringify(subscriptions));
  localStorage.setItem("cachedSubscriptionVersion", version.toString());
};

/**
 * Fetch the current subscription version
 * @returns {number} Version number of the subscription data
 */
export const getSubscriptionVersion = async () => {
  try {
    const response = await apiClient.get("/version");
    return response.data.version; // Assuming the API returns { version: <number> }
  } catch (error) {
    handleError(error);
  }
};

/**
 * Fetch all subscription tiers
 * @returns {Array} List of all subscription tiers
 */
export const getAllSubscriptions = async () => {
  try {
    const { subscriptions, version: cachedVersion } = getCachedSubscriptions();
    const currentVersion = await getSubscriptionVersion();

    // Return cached data if version matches
    if (subscriptions && cachedVersion === currentVersion) {
      console.log("Using cached subscription data.");
      return subscriptions;
    }

    // Fetch fresh data if version mismatch
    const response = await apiClient.get("/");
    const freshSubscriptions = response.data;
    setCachedSubscriptions(freshSubscriptions, currentVersion); // Update cache
    console.log("Subscription data fetched and cached.");
    return freshSubscriptions;
  } catch (error) {
    handleError(error);
  }
};

/**
 * Fetch subscription tier by ID
 * @param {string} tierId - The ID of the subscription tier
 * @returns {Object} Subscription tier details
 */
export const getSubscriptionById = async (tierId) => {
  try {
    const response = await apiClient.get(`/${tierId}`);
    return response.data;
  } catch (error) {
    handleError(error);
  }
};

/**
 * Activate a subscription tier (Admin-only)
 * @param {string} tierId - The ID of the subscription tier
 * @returns {Object} Updated subscription tier
 */
export const activateSubscription = async (tierId) => {
  try {
    const response = await apiClient.put(`/${tierId}/activate`);
    toast.success("Subscription tier activated successfully!");

    // Invalidate cache
    localStorage.removeItem("cachedSubscriptions");
    localStorage.removeItem("cachedSubscriptionVersion");

    return response.data;
  } catch (error) {
    handleError(error);
  }
};

/**
 * Deactivate a subscription tier (Admin-only)
 * @param {string} tierId - The ID of the subscription tier
 * @returns {Object} Updated subscription tier
 */
export const deactivateSubscription = async (tierId) => {
  try {
    const response = await apiClient.put(`/${tierId}/deactivate`);
    toast.success("Subscription tier deactivated successfully!");

    // Invalidate cache
    localStorage.removeItem("cachedSubscriptions");
    localStorage.removeItem("cachedSubscriptionVersion");

    return response.data;
  } catch (error) {
    handleError(error);
  }
};

/**
 * Create a new subscription tier (Admin-only)
 * @param {Object} tierData - Details of the subscription tier
 * @returns {Object} Created subscription tier
 */
export const createSubscription = async (tierData) => {
  try {
    const response = await apiClient.post("/", tierData);
    toast.success("Subscription tier created successfully!");

    // Invalidate cache
    localStorage.removeItem("cachedSubscriptions");
    localStorage.removeItem("cachedSubscriptionVersion");

    return response.data;
  } catch (error) {
    handleError(error);
  }
};

/**
 * Update a subscription tier (Admin-only)
 * @param {string} tierId - The ID of the subscription tier
 * @param {Object} tierData - Updated details of the subscription tier
 * @returns {Object} Updated subscription tier
 */
export const updateSubscription = async (tierId, tierData) => {
  try {
    const response = await apiClient.put(`/${tierId}`, tierData);
    toast.success("Subscription tier updated successfully!");

    // Invalidate cache
    localStorage.removeItem("cachedSubscriptions");
    localStorage.removeItem("cachedSubscriptionVersion");

    return response.data;
  } catch (error) {
    handleError(error);
  }
};

/**
 * Delete a subscription tier (Admin-only)
 * @param {string} tierId - The ID of the subscription tier
 * @returns {Object} Confirmation of deletion
 */
export const deleteSubscription = async (tierId) => {
  try {
    const response = await apiClient.delete(`/${tierId}`);
    toast.success("Subscription tier deleted successfully!");

    // Invalidate cache
    localStorage.removeItem("cachedSubscriptions");
    localStorage.removeItem("cachedSubscriptionVersion");

    return response.data;
  } catch (error) {
    handleError(error);
  }
};
