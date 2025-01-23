import axios from "axios";
import { toast } from "react-toastify";

// Configure API base URL and headers
const API_URL = process.env.REACT_APP_API_URL || "http://127.0.0.1:8000/api";
const apiClient = axios.create({
  baseURL: `${API_URL}/admin`,
  headers: {
    "Content-Type": "application/json",
    Accept: "application/json",
  },
});

// Log initialization
console.log(`Admin Auth API initialized at: ${apiClient.defaults.baseURL}`);

// Attach admin token for authorization if available
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem("adminToken");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  } else {
    console.warn("No admin token found.");
  }
  return config;
});

// Handle and normalize API errors
const handleError = (error) => {
  console.error("Admin API Error:", error);

  if (error.response) {
    const { status, data } = error.response;
    console.error("Error Details:", data);

    const detail = data?.detail || "An unexpected error occurred.";
    toast.error(detail);

    // Return structured error for further processing
    return Promise.reject({ message: detail, status, data });
  }

  // Handle network or unknown errors
  const networkError = { message: "Network error. Please try again later.", status: 0 };
  toast.error(networkError.message);
  return Promise.reject(networkError);
};

const authProvider = {
  // Login: Authenticate admin users
login: async ({ username, password }) => {
  console.log("Admin login initiated...");
  console.log("Payload received by authProvider:", { username, password });

  try {
    const isMobile = /Mobi|Android/i.test(navigator.userAgent);

    const response = await apiClient.post("/login", {
      email: username,
      password,
      is_mobile: isMobile,
    });

    const { access_token } = response.data;
    localStorage.setItem("adminToken", access_token);

    // Validate admin access
    const userResponse = await apiClient.get("/profile", {
      headers: { Authorization: `Bearer ${access_token}` },
    });

    if (userResponse.data.user_type !== "ADMIN") {
      localStorage.removeItem("adminToken");
      toast.error("You do not have admin access.");
      throw new Error("Insufficient permissions");
    }

    toast.success("Welcome to the Admin Panel!");
    return Promise.resolve();
  } catch (error) {
    console.error("Login error:", error);
    return handleError(error);
  }
},

  // Register: Register a new admin user (requires a secret key)
registerAdmin: async (userData) => {
  try {
    const secretKey = userData.admin_secret_key
    const response = await apiClient.post(
      "/create",
      {
        ...userData,
      },
      {
        headers: {
          "X-Superuser-Secret": secretKey,
        },
      }
    );

    console.log("Headers sent with request:", { "X-Superuser-Secret": secretKey });
    toast.success("Admin account created successfully!");
    return response.data;
  } catch (error) {
    return handleError(error);
  }
},


  // Logout: Clear session and redirect
  logout: () => {
    console.log("Admin logout initiated...");
    try {
      localStorage.removeItem("adminToken");
      toast.info("Logged out successfully.");
      return Promise.resolve();
    } catch (error) {
      console.error("Error during logout:", error);
      return Promise.reject("Logout failed.");
    }
  },

  // Ensure user is authenticated
  checkAuth: () => {
    const token = localStorage.getItem("adminToken");
    if (token) {
      console.log("Admin authentication verified.");
      return Promise.resolve();
    } else {
      console.warn("Admin authentication failed.");
      return Promise.reject({ message: "Not authenticated" });
    }
  },

  // Handle unauthorized or forbidden errors
  checkError: (error) => {
    if (error.status === 401 || error.status === 403) {
      console.warn("Admin authentication error. Clearing token...");
      localStorage.removeItem("adminToken");
      return Promise.reject();
    }
    return Promise.resolve();
  },

  // Get admin-specific permissions
  getPermissions: async () => {
    console.log("Fetching admin permissions...");
    try {
      const token = localStorage.getItem("adminToken");
      if (!token) throw new Error("No admin token found.");

      const response = await apiClient.get("/profile", {
        headers: { Authorization: `Bearer ${token}` },
      });

      const { user_type } = response.data;
      if (user_type === "admin") {
        console.log("Admin permissions granted.");
        return Promise.resolve("admin");
      } else {
        console.warn("Admin permissions denied.");
        return Promise.reject("Unauthorized");
      }
    } catch (error) {
      console.error("Error fetching permissions:", error);
      localStorage.removeItem("adminToken");
      return Promise.reject("Unauthorized");
    }
  },
};

export default authProvider;
