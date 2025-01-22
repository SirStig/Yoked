import React from "react";
import styled from "styled-components";
import { Outlet } from "react-router-dom";

// Header with dark theme and centered text
const Header = styled.header`
  background-color: ${({ theme }) => theme.colors.primary}; /* Dark background */
  padding: ${({ theme }) => theme.spacing(3)};
  text-align: center;
  font-size: 2rem;
  color: ${({ theme }) => theme.colors.textPrimary};
  font-weight: bold;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);

  @media (max-width: ${({ theme }) => theme.breakpoints.sm}) {
    font-size: 1.5rem; /* Adjust font size for mobile */
  }
`;

// Footer with dark theme and aligned text
const Footer = styled.footer`
  background-color: ${({ theme }) => theme.colors.primary}; /* Dark background */
  padding: ${({ theme }) => theme.spacing(2)};
  text-align: center;
  font-size: 0.9em;
  color: ${({ theme }) => theme.colors.textSecondary};
  box-shadow: 0 -2px 8px rgba(0, 0, 0, 0.1);

  @media (max-width: ${({ theme }) => theme.breakpoints.sm}) {
    font-size: 0.8em; /* Adjust font size for mobile */
  }
`;

// Main content area with padding and minimum height adjustment
const MainContent = styled.main`
  padding: ${({ theme }) => theme.spacing(3)};
  min-height: calc(100vh - 160px); /* Ensure the content area fills the screen */
  background-color: ${({ theme }) => theme.colors.background}; /* Dark background */
  color: ${({ theme }) => theme.colors.textPrimary};
  
  @media (max-width: ${({ theme }) => theme.breakpoints.md}) {
    padding: ${({ theme }) => theme.spacing(2)}; /* Adjust padding for tablets */
  }

  @media (max-width: ${({ theme }) => theme.breakpoints.sm}) {
    padding: ${({ theme }) => theme.spacing(1)}; /* Adjust padding for mobile */
  }
`;

const MainLayout = () => (
  <div>
    <Header>Yoked</Header>
    <MainContent>
      <Outlet />
    </MainContent>
    <Footer>© 2025 Yoked. All rights reserved.</Footer>
  </div>
);

export default MainLayout;
