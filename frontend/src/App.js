import React, { useContext } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import { ThemeProvider } from "styled-components";
import GlobalStyles from "./styles/globalStyles";
import { theme } from "./styles/theme";
import { AuthContext } from "./contexts/AuthContext";
import Home from "./pages/Home";
import Login from "./pages/Login";
import AccountCreation from "./pages/Registration/AccountCreation";
import Verification from "./pages/Verification";
import ProfileCompletion from "./pages/Registration/ProfileCompletion";
import SubscriptionSelection from "./pages/Registration/SubscriptionSelection";
import Dashboard from "./pages/Dashboard";

// Route Wrappers
const ProtectedRoute = ({ children }) => {
  const { currentUser, loading } = useContext(AuthContext);

  if (loading) {
    return (
      <div style={{ textAlign: "center", marginTop: "20%" }}>
        <h2>Loading...</h2>
      </div>
    );
  }

  if (!currentUser) {
    return <Navigate to="/login" replace />;
  }

  const excludedPaths = ["/", "/privacy-policy", "/terms-and-conditions", "/login", "/register"];
  const nextStepPath = `/${currentUser.setup_step}`;

  // Ensure no redirection happens on excluded paths
  if (
    currentUser.setup_step !== "completed" &&
    !excludedPaths.includes(window.location.pathname) &&
    window.location.pathname !== nextStepPath
  ) {
    return <Navigate to={nextStepPath} replace />;
  }

  return children;
};

const GuestRoute = ({ children, allowLoggedInHome = false }) => {
  const { currentUser, loading } = useContext(AuthContext);

  if (loading) return <div>Loading...</div>;

  if (currentUser) {
    // Allow logged-in users to access the home page if specified
    return allowLoggedInHome ? children : <Navigate to="/dashboard" replace />;
  }

  return children;
};

const App = () => {
  return (
    <ThemeProvider theme={theme}>
      <GlobalStyles />
      <Router>
        <Routes>
          {/* Guest Routes */}
          <Route
            path="/"
            element={
              <GuestRoute allowLoggedInHome>
                <Home />
              </GuestRoute>
            }
          />
          <Route
            path="/login"
            element={
              <GuestRoute>
                <Login />
              </GuestRoute>
            }
          />
          <Route
            path="/register"
            element={
              <GuestRoute>
                <AccountCreation />
              </GuestRoute>
            }
          />

          {/* Setup Steps */}
          <Route
            path="/verify_email"
            element={
              <ProtectedRoute>
                <Verification />
              </ProtectedRoute>
            }
          />
          <Route
            path="/profile_completion"
            element={
              <ProtectedRoute>
                <ProfileCompletion />
              </ProtectedRoute>
            }
          />
          <Route
            path="/subscription_selection"
            element={
              <ProtectedRoute>
                <SubscriptionSelection />
              </ProtectedRoute>
            }
          />

          {/* Main Application */}
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            }
          />
        </Routes>
      </Router>
    </ThemeProvider>
  );
};

export default App;
