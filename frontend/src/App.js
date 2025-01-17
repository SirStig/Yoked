import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { ThemeProvider } from "styled-components";
import GlobalStyles from "./styles/globalStyles";
import darkTheme from "./styles/theme";
import MainLayout from "./layouts/MainLayout";
import Home from "./pages/Home";
import Workouts from "./pages/Workouts";
import Nutrition from "./pages/Nutrition";
import Community from "./pages/Community";
import Profile from "./pages/Profile";
import Login from "./pages/Login";
import Register from "./pages/Register";
import NotFound from "./pages/NotFound";
import { AuthProvider } from "./contexts/AuthContext";

const App = () => {
  return (
    <AuthProvider>
      <ThemeProvider theme={darkTheme}>
        <GlobalStyles />
        <Router>
          <Routes>
            <Route path="/" element={<MainLayout />}>
              <Route index element={<Home />} />
              <Route path="workouts" element={<Workouts />} />
              <Route path="nutrition" element={<Nutrition />} />
              <Route path="community" element={<Community />} />
              <Route path="profile" element={<Profile />} />
            </Route>
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </Router>
      </ThemeProvider>
    </AuthProvider>
  );
};

export default App;
