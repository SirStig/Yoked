import React, { createContext, useState } from "react";
import axios from "axios";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [authState, setAuthState] = useState({
        token: localStorage.getItem("token") || null,
        user: null,
    });

    const login = async (email, password) => {
        // Example API call
        const response = await fetch("/api/auth/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password }),
        });

        if (!response.ok) {
            throw new Error("Login failed");
        }

        const data = await response.json();
        localStorage.setItem("token", data.token);
    };

    const [authToken, setAuthToken] = useState(localStorage.getItem("token"));

      const register = async (email, password, username) => {
        const response = await axios.post(`${process.env.REACT_APP_API_URL}/auth/register`, {
          email,
          password,
          username,
        });
        if (response.data) {
          return response.data;
        }
        throw new Error("Registration failed");
      };

    const logout = () => {
        localStorage.removeItem("token");
        setAuthState({ token: null, user: null });
    };

    return (
        <AuthContext.Provider value={{ authState, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
};
