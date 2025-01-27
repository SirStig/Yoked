import React, { useContext } from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import { ThemeProvider } from "styled-components";
import GlobalStyles from "./styles/globalStyles";
import { theme } from "./styles/theme";
import { AuthContext } from "./contexts/AuthContext";
import Home from "./pages/Home";
import Dashboard from "./pages/Dashboard";
import Verification from "./pages/Verification";
import PaymentSuccess from "./pages/PaymentSuccess";
import PaymentCancel from "./pages/PaymentCancel";
import NotFound from "./pages/NotFound";
import Privacy from "./pages/legal/privacy";
import TermsConditions from "./pages/legal/terms_and_conditions";

// ProtectedRoute for pages that require specific setup steps
const ProtectedRoute = ({ children, requiredSetupStep }) => {
  const { currentUser } = useContext(AuthContext);

  if (!currentUser) {
    return <Navigate to="/" replace />;
  }

  if (currentUser.setup_step !== requiredSetupStep && requiredSetupStep) {
    return <Navigate to="/dashboard" replace />;
  }

  return children;
};

const App = () => {
  return (
    <ThemeProvider theme={theme}>
      <GlobalStyles />
      <Routes>
        {/* Public Route */}
        <Route path="/" element={<Home />} />
        <Route path="/legal/privacy" element={<Privacy />} />
        <Route path="/legal/terms" element={<TermsConditions />} />

        {/* Dashboard Route */}
        <Route
          path="/dashboard"
          element={<Dashboard />}
        />

        {/* Email Verification */}
        <Route
          path="/verify-email"
          element={
            <ProtectedRoute requiredSetupStep="verify_email">
              <Verification />
            </ProtectedRoute>
          }
        />

        {/* Payment Routes */}
        <Route path="/payment-success" element={<PaymentSuccess />} />
        <Route path="/payment-cancel" element={<PaymentCancel />} />

        {/* Fallback Route */}
        <Route path="*" element={<NotFound />} />
      </Routes>
    </ThemeProvider>
  );
};

export default App;
