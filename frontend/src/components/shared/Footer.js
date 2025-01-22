import React from "react";
import styled from "styled-components";
import { useNavigate } from "react-router-dom";

// Footer container
const FooterContainer = styled.footer`
  background: ${({ theme }) => theme.colors.cardBackground};
  color: ${({ theme }) => theme.colors.textPrimary};
  padding: ${({ theme }) => theme.spacing(4)} ${({ theme }) => theme.spacing(2)};
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: ${({ theme }) => theme.spacing(4)};
  box-shadow: ${({ theme }) => theme.shadows.medium};
  text-align: center;

  @media (max-width: ${({ theme }) => theme.breakpoints.sm}) {
    padding: ${({ theme }) => theme.spacing(2)};
  }
`;

// Links section container
const LinksSection = styled.div`
  display: flex;
  gap: ${({ theme }) => theme.spacing(6)};
  justify-content: center;
  flex-wrap: wrap;
  width: 100%;
`;

// Individual category container
const CategoryContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: ${({ theme }) => theme.spacing(1)};

  h4 {
    font-size: 1.2rem;
    color: ${({ theme }) => theme.colors.textPrimary};
    margin-bottom: ${({ theme }) => theme.spacing(1)};
  }

  a {
    color: ${({ theme }) => theme.colors.textSecondary};
    text-decoration: none;
    font-size: 1rem;
    transition: color ${({ theme }) => theme.transitions.default};

    &:hover {
      color: ${({ theme }) => theme.colors.accent};
    }
  }
`;

// Trademark text
const TrademarkText = styled.div`
  font-size: 0.9rem;
  color: ${({ theme }) => theme.colors.textSecondary};
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
          <a onClick={() => navigate("/privacy-policy")}>Privacy Policy</a>
          <a onClick={() => navigate("/terms-and-conditions")}>Terms & Conditions</a>
        </CategoryContainer>

        {/* Support Links */}
        <CategoryContainer>
          <h4>Support</h4>
          <a onClick={() => navigate("/support")}>Support</a>
          <a href="mailto:support@yoked.com">Contact Us</a>
        </CategoryContainer>
      </LinksSection>

      {/* Trademark */}
      <TrademarkText>© {new Date().getFullYear()} Yoked. All rights reserved.</TrademarkText>
    </FooterContainer>
  );
};

export default Footer;
