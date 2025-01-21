import axios from "axios";
import { toast } from "react-toastify";

// Axios instance for centralized configuration
const apiClient = axios.create({
  baseURL: "http://127.0.0.1:8000/api/payments",
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

/**
 * Create a new Stripe payment session
 * @param {string} subscriptionTier - Tier for which the payment session is created (e.g., "Champion", "Olympian")
 * @returns {Object} Stripe session URL to redirect the user
 */
export const createStripePayment = async (subscriptionTier) => {
  try {
    const response = await apiClient.post(`/create?subscription_tier=${subscriptionTier}`);
    return response.data;
  } catch (error) {
    handleError(error);
  }
};

/**
 * Subscribe the user to the free tier
 * @returns {Object} Success message from the server
 */
export const subscribeFreeTier = async () => {
  try {
    const response = await apiClient.post("/subscribe/free");
    return response.data;
  } catch (error) {
    handleError(error);
  }
};

/**
 * Verify a payment status with the platform using session ID
 * @param {string} sessionId - The Stripe session ID to verify
 * @returns {Object} Updated payment record
 */
export const verifyPayment = async (sessionId) => {
  if (!sessionId || typeof sessionId !== "string") {
    throw new Error("Invalid session ID");
  }

  try {
    const response = await apiClient.post(`/verify?session_id=${sessionId}`);
    if (response.data.success) {
      toast.success("Payment successfully verified!");
    } else {
      toast.error("Payment verification failed. Please try again.");
    }
    return response.data;  // Returns the updated payment record
  } catch (error) {
    handleError(error);
  }
};

/**
 * Handle Stripe payment cancelation
 * @returns {Object} Server acknowledgment or status
 */
export const cancelPayment = async () => {
  try {
    const response = await apiClient.post("/cancel");
    return response.data;
  } catch (error) {
    handleError(error);
  }
};

/**
 * Get the current user's payment history
 * @param {number} page - Page number for paginated results
 * @param {number} pageSize - Number of results per page
 * @returns {Object} Paginated list of user payments
 */
export const getPaymentHistory = async (page = 1, pageSize = 10) => {
  try {
    const response = await apiClient.get("/history", {
      params: { page, page_size: pageSize },
    });
    return response.data;
  } catch (error) {
    handleError(error);
  }
};

/**
 * Admin: Get all users' payment history
 * @param {number} page - Page number for paginated results
 * @param {number} pageSize - Number of results per page
 * @returns {Object} Paginated list of all user payments
 */
export const getAdminPaymentHistory = async (page = 1, pageSize = 10) => {
  try {
    const response = await apiClient.get("/admin/history", {
      params: { page, page_size: pageSize },
    });
    return response.data;
  } catch (error) {
    handleError(error);
  }
};

/**
 * Admin: Refund a specific payment
 * @param {string} paymentId - The ID of the payment to refund
 * @returns {Object} Updated payment record after refund
 */
export const refundPayment = async (paymentId) => {
  try {
    const response = await apiClient.post("/refund", { payment_id: paymentId });
    return response.data;
  } catch (error) {
    handleError(error);
  }
};
