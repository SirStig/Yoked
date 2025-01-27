import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import AdminApp from "./admin/AdminApp";
import { AuthProvider } from "./contexts/AuthContext";
import ErrorBoundary from "./components/shared/ErrorBoundary";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import AdminLogin from "./admin/users/AdminLogin";
import AdminRegistration from "./admin/users/AdminRegistration";
import { ThemeProvider } from "styled-components";
import { adminTheme } from "./admin/styles/adminTheme";
import AdminGlobalStyles from "./admin/styles/adminStyles";

const root = ReactDOM.createRoot(document.getElementById("root"));

root.render(
  <React.StrictMode>
    <ErrorBoundary>
      <Router>
        <AuthProvider>
          <Routes>
            {/* Non-protected admin routes */}
            <Route
              path="/admin/login"
              element={
                <ThemeProvider theme={adminTheme}>
                  <AdminGlobalStyles />
                  <AdminLogin />
                </ThemeProvider>
              }
            />
            <Route
              path="/admin/register"
              element={
                <ThemeProvider theme={adminTheme}>
                  <AdminGlobalStyles />
                  <AdminRegistration />
                </ThemeProvider>
              }
            />

            {/* Protected admin routes */}
            <Route path="/admin/*" element={<AdminApp />} />

            {/* Non-admin routes */}
            <Route path="/*" element={<App />} />
          </Routes>
        </AuthProvider>
      </Router>
    </ErrorBoundary>
  </React.StrictMode>
);
