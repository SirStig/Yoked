import React from "react";
import styled from "styled-components";
import { useNavigate } from "react-router-dom";

// Footer container
const FooterContainer = styled.footer`
  background: ${({ theme }) => theme.colors.cardBackground};
  color: ${({ theme }) => theme.colors.textPrimary};
  padding: ${({ theme }) => theme.spacing(6)} ${({ theme }) => theme.spacing(4)};
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: ${({ theme }) => theme.spacing(6)};
  box-shadow: ${({ theme }) => theme.shadows.medium};
  text-align: center;
  width: 100%;

  @media (max-width: ${({ theme }) => theme.breakpoints.sm}) {
    padding: ${({ theme }) => theme.spacing(4)};
  }
`;

// Links section container
const LinksSection = styled.div`
  display: flex;
  gap: ${({ theme }) => theme.spacing(8)};
  justify-content: space-evenly;
  flex-wrap: wrap;
  width: 100%;
  max-width: 1200px;
`;

// Individual category container
const CategoryContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: ${({ theme }) => theme.spacing(1)};
  width: 200px;

  h4 {
    font-size: 1.3rem;
    color: ${({ theme }) => theme.colors.accent};
    margin-bottom: ${({ theme }) => theme.spacing(2)};
    border-bottom: 2px solid ${({ theme }) => theme.colors.accent};
    padding-bottom: ${({ theme }) => theme.spacing(1)};
  }

  a {
    color: ${({ theme }) => theme.colors.textSecondary};
    text-decoration: none;
    font-size: 1rem;
    transition: color ${({ theme }) => theme.transitions.default};

    &:hover {
      color: ${({ theme }) => theme.colors.primary};
    }
  }
`;

// Trademark text
const TrademarkText = styled.div`
  font-size: 0.9rem;
  color: ${({ theme }) => theme.colors.textSecondary};
  margin-top: ${({ theme }) => theme.spacing(4)};
`;

const Divider = styled.div`
  width: 100%;
  height: 2px;
  background: ${({ theme }) => theme.colors.textSecondary};
  margin-top: ${({ theme }) => theme.spacing(4)};
`;

// Footer Component
const Footer = () => {
  const navigate = useNavigate();

  return (
    <FooterContainer>
      {/* Links Section */}
      <LinksSection>
        {/* General Links */}
        <CategoryContainer>
          <h4>General</h4>
          <a onClick={() => navigate("/")}>Home</a>
          <a href="#about">About</a>
          <a href="#features">Features</a>
        </CategoryContainer>

        {/* Account Links */}
        <CategoryContainer>
          <h4>Account</h4>
          <a onClick={() => navigate("/login")}>Login</a>
          <a onClick={() => navigate("/register")}>Register</a>
          <a onClick={() => navigate("/dashboard")}>Dashboard</a>
        </CategoryContainer>

        {/* Legal Links */}
        <CategoryContainer>
          <h4>Legal</h4>
          <a onClick={() => navigate("/legal/privacy")}>Privacy Policy</a>
          <a onClick={() => navigate("/legal/terms")}>Terms & Conditions</a>
        </CategoryContainer>

        {/* Support Links */}
        <CategoryContainer>
          <h4>Support</h4>
          <a onClick={() => navigate("/support")}>Support</a>
          <a href="mailto:support@yoked.com">Contact Us</a>
        </CategoryContainer>
      </LinksSection>

      <Divider />

      {/* Trademark */}
      <TrademarkText>© {new Date().getFullYear()} Yoked. All rights reserved.</TrademarkText>
    </FooterContainer>
  );
};

export default Footer;
