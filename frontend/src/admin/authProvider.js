import axios from "axios";
import { toast } from "react-toastify";

const API_URL = process.env.REACT_APP_API_URL || "http://127.0.0.1:8000/api";
const apiClient = axios.create({
  baseURL: `${API_URL}/admin`,
  headers: {
    "Content-Type": "application/json",
    Accept: "application/json",
  },
});

// Attach admin token for authorization if available
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem("adminToken");
  console.log("Authorization header token:", token); // Debug log
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

const authProvider = {
  // Admin login with MFA handling
  login: async ({ username, password }) => {
    console.log("Admin login initiated...");
    try {
      const isMobile = /Mobi|Android/i.test(navigator.userAgent);

      // Send login request
      const response = await apiClient.post("/login", {
        email: username,
        password,
        is_mobile: isMobile,
      });

      console.log("Login response:", response.data); // Debug log

      const { mfa_required, mfa_setup_required, user_id, session_token } = response.data;

      if (mfa_setup_required) {
        console.log("MFA setup required."); // Debug log
        return Promise.resolve({
          mfa_setup_required: true,
          user_id,
          session_token,
        });
      }

      if (mfa_required) {
        console.log("MFA verification required."); // Debug log
        return Promise.resolve({
          mfa_required: true,
          user_id,
          session_token,
        });
      }

      if (!session_token) {
        throw new Error("Login failed: No session token received.");
      }

      // Store token
      localStorage.setItem("adminToken", session_token);
      console.log("Admin token stored:", session_token); // Debug log
      toast.success("Login successful!");
      return Promise.resolve();
    } catch (error) {
      console.error("Login error:", error);
      toast.error(error.response?.data?.detail || "Login failed.");
      return Promise.reject(error);
    }
  },

  // MFA Setup: Expect token upon successful setup
  setupMFA: async ({ user_id, mfa_secret, totp_code }) => {
    console.log("MFA setup initiated..."); // Debug log
    try {
      const response = await apiClient.post("/mfa/setup", {
        user_id,
        mfa_secret,
        totp_code,
      });

      console.log("MFA setup response:", response.data); // Debug log

      const { session_token } = response.data;

      if (!session_token) {
        throw new Error("MFA setup failed: No token returned.");
      }

      // Store the session token
      localStorage.setItem("adminToken", session_token);
      console.log("Admin token stored after MFA setup:", session_token); // Debug log
      toast.success("MFA setup complete!");
      return Promise.resolve();
    } catch (error) {
      console.error("MFA setup error:", error);
      toast.error(error.response?.data?.detail || "MFA setup failed.");
      return Promise.reject(error);
    }
  },

  // MFA Verification: Expect token upon successful verification
    verifyMFA: async ({ user_id, totp_code, session_token }) => {
        console.log("MFA verification initiated..."); // Debug log
        try {
            const response = await apiClient.post("/mfa/verify", {
                user_id,
                totp_code,
                session_token,
            });

            console.log("MFA verify response:", response.data); // Debug log

            const { session_token: newSessionToken } = response.data;

            if (!newSessionToken) {
                throw new Error("MFA verification failed: No token returned.");
            }

            // Store the updated session token
            localStorage.setItem("adminToken", newSessionToken);
            console.log("Admin token stored after MFA verification:", newSessionToken); // Debug log
            toast.success("MFA verified successfully!");
            return Promise.resolve();
        } catch (error) {
            console.error("MFA verification error:", error);
            toast.error(error.response?.data?.detail || "MFA verification failed.");
            return Promise.reject(error);
        }
    },


  // Logout: Clear session and redirect
  logout: () => {
    console.log("Admin logout initiated...");
    localStorage.removeItem("adminToken");
    toast.info("Logged out successfully.");
    return Promise.resolve();
  },

  // Ensure user is authenticated
  checkAuth: () => {
    const token = localStorage.getItem("adminToken");
    console.log("AuthProvider checkAuth: token found?", !!token); // Debug log
    return token ? Promise.resolve() : Promise.reject({ message: "Not authenticated" });
  },

  // Handle unauthorized or forbidden errors
  checkError: (error) => {
    if (error?.response?.status === 401 || error?.response?.status === 403) {
      console.warn("Admin authentication error. Clearing token...");
      localStorage.removeItem("adminToken");
      return Promise.reject();
    }
    return Promise.resolve();
  },

  // Get admin-specific permissions
  getPermissions: async () => {
    console.log("Fetching admin permissions...");
    const token = localStorage.getItem("adminToken");

    if (!token) {
      console.warn("No admin token found.");
      return Promise.reject("Unauthorized");
    }

    try {
      const response = await apiClient.get("/profile", {
        headers: { Authorization: `Bearer ${token}` },
      });

      const { user_type } = response.data;
      console.log("User type fetched:", user_type);

      if (user_type === "admin") {
        console.log("Admin permissions granted.");
        return Promise.resolve("admin");
      } else {
        console.warn("Admin permissions denied.");
        return Promise.reject("Unauthorized");
      }
    } catch (error) {
      console.error("Error fetching permissions:", error.response || error.message);
      if (error.response?.status === 500) {
        console.error("Server error on /profile. Possible backend issue.");
      } else {
        console.warn("Unauthorized session detected. Clearing admin token.");
        localStorage.removeItem("adminToken");
      }
      return Promise.reject("Unauthorized");
    }
  },

};

export default authProvider;
