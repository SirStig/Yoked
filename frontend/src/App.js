import React, { useContext, useEffect } from "react";
import { Routes, Route, Navigate, useLocation } from "react-router-dom";
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
import PaymentSuccess from "./pages/PaymentSuccess";
import PaymentCancel from "./pages/PaymentCancel";

const ProtectedRoute = ({ children }) => {
  const { currentUser, loading, loadUser } = useContext(AuthContext);
  const location = useLocation();

  useEffect(() => {
    const fetchUserData = async () => {
      if (!loading && !currentUser) {
        await loadUser(); // Ensure user data is loaded
      }
    };
    fetchUserData();
  }, [loading, currentUser, loadUser]);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (!currentUser) {
    return <Navigate to="/login" replace />;
  }

  const currentPath = location.pathname;

  // Mapping setup_step to the corresponding paths
  const setupStepToPath = {
    "verify_email": "/verify_email",
    "profile_completion": "/profile-setup",
    "subscription_selection": "/choose-subscription",
    "completed": "/dashboard"
  };

  const nextStepPath = setupStepToPath[currentUser.setup_step] || "/dashboard";

  // Redirect to the appropriate setup page based on setup_step
  if (currentUser.setup_step !== "completed" && currentPath !== nextStepPath) {
    return <Navigate to={nextStepPath} replace />;
  }

  return children;
};

const GuestRoute = ({ children, allowLoggedInHome = false }) => {
  const { currentUser, loading } = useContext(AuthContext);

  if (loading) return <div>Loading...</div>;

  if (currentUser) {
    return allowLoggedInHome ? children : <Navigate to="/dashboard" replace />;
  }

  return children;
};

const App = () => {
  return (
    <ThemeProvider theme={theme}>
      <GlobalStyles />
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
        <Route
          path="/payment-cancel"
          element={
            <GuestRoute>
              <PaymentCancel />
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
          path="/profile-setup"
          element={
            <ProtectedRoute>
              <ProfileCompletion />
            </ProtectedRoute>
          }
        />
        <Route
          path="/choose-subscription"
          element={
            <ProtectedRoute>
              <SubscriptionSelection />
            </ProtectedRoute>
          }
        />

        {/* Payment Success Route */}
        <Route
          path="/payment-success"
          element={
            <ProtectedRoute>
              <PaymentSuccess />
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
    </ThemeProvider>
  );
};

export default App;
