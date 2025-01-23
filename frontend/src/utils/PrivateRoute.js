import React from "react";
import { Navigate } from "react-router-dom";

// Check if admin is authenticated
const isAuthenticated = () => {
  const adminToken = localStorage.getItem("adminToken");
  return !!adminToken; // Return true if token exists
};

const PrivateRoute = ({ children }) => {
  return isAuthenticated() ? children : <Navigate to="/login" />;
};

export default PrivateRoute;
