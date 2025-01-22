import React, { useContext, useState } from "react";
import styled from "styled-components";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../../contexts/AuthContext";
import { logoutUser } from "../../api/authApi";
import { toast } from "react-toastify";

// Styled button
const StyledButton = styled.button`
  background: ${({ theme }) => theme.colors.primary};
  color: ${({ theme }) => theme.colors.textPrimary};
  border: none;
  padding: ${({ theme }) => theme.spacing(1.5)} ${({ theme }) => theme.spacing(3)};
  border-radius: ${({ theme }) => theme.borderRadius};
  cursor: pointer;
  font-size: 1rem;
  font-weight: ${({ theme }) => theme.font.weightBold};
  transition: background-color ${({ theme }) => theme.transitions.default}, box-shadow ${({ theme }) => theme.transitions.hoverGlow};

  &:hover {
    background: ${({ theme }) => theme.colors.primaryHover};
    box-shadow: ${({ theme }) => theme.shadows.glow};
  }
`;


// Header container styling
const HeaderContainer = styled.header`
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  background: linear-gradient(90deg, ${({ theme }) => theme.colors.secondary}, ${({ theme }) => theme.colors.cardBackground});
  background-size: 200% 200%;
  animation: gradient-animation 6s ease infinite;
  color: ${({ theme }) => theme.colors.textPrimary};
  display: flex;
  align-items: center;
  padding: ${({ theme }) => theme.spacing(2)} ${({ theme }) => theme.spacing(4)};
  z-index: 1000;
  box-shadow: ${({ theme }) => theme.shadows.medium};

  @keyframes gradient-animation {
    0% {
      background-position: 0% 50%;
    }
    50% {
      background-position: 100% 50%;
    }
    100% {
      background-position: 0% 50%;
    }
  }
`;

// Logo styling
const Logo = styled.div`
  font-size: 2rem;
  font-weight: ${({ theme }) => theme.font.weightBold};
  color: ${({ theme }) => theme.colors.accent};
  cursor: pointer;

  &:hover {
    transform: scale(1.05); /* Subtle scaling effect */
  }
`;

// Styled button group (includes navigation and action buttons)
const StyledButtonGroup = styled.div`
  display: flex;
  align-items: center;
  gap: ${({ theme }) => theme.spacing(3)};
  margin-left: auto;
`;

// Styled navigation links
const StyledNavLink = styled.a`
  color: ${({ theme }) => theme.colors.textPrimary};
  text-decoration: none;
  font-weight: ${({ theme }) => theme.font.weightMedium};
  font-size: 1.1rem;
  transition: color ${({ theme }) => theme.transitions.default};

  &:hover {
    color: ${({ theme }) => theme.colors.accent};
  }
`;

// Dropdown menu container
const DropdownContainer = styled.div`
  position: relative;
`;

const DropdownButton = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  background: ${({ theme }) => theme.colors.primary};
  color: ${({ theme }) => theme.colors.textPrimary};
  border: none;
  padding: ${({ theme }) => theme.spacing(1.5)} ${({ theme }) => theme.spacing(3)};
  border-radius: ${({ theme }) => theme.borderRadius};
  cursor: pointer;
  font-size: 1rem;
  font-weight: ${({ theme }) => theme.font.weightBold};
  transition: background-color ${({ theme }) => theme.transitions.default}, box-shadow ${({ theme }) => theme.transitions.hoverGlow};

  &:hover {
    background: ${({ theme }) => theme.colors.primaryHover};
    box-shadow: ${({ theme }) => theme.shadows.glow};
  }
`;

const DropdownMenu = styled.ul`
  position: absolute;
  top: 100%;
  right: 0;
  background: ${({ theme }) => theme.colors.cardBackground};
  border-radius: ${({ theme }) => theme.borderRadius};
  box-shadow: ${({ theme }) => theme.shadows.medium};
  padding: ${({ theme }) => theme.spacing(2)};
  list-style: none;
  margin: 0;
  z-index: 10;
  display: ${({ isOpen }) => (isOpen ? "block" : "none")};
`;

const DropdownMenuItem = styled.li`
  padding: ${({ theme }) => theme.spacing(2)};
  color: ${({ theme }) => theme.colors.textPrimary};
  cursor: pointer;
  transition: background-color ${({ theme }) => theme.transitions.default};

  &:hover {
    background: ${({ theme }) => theme.colors.inputBackground};
  }
`;

// Mobile menu toggle
const MobileMenuToggle = styled.div`
  display: none;

  @media (max-width: ${({ theme }) => theme.breakpoints.sm}) {
    display: block;
    cursor: pointer;
    color: ${({ theme }) => theme.colors.textPrimary};
    font-size: 1.5rem;
  }
`;

const Header = () => {
  const { currentUser } = useContext(AuthContext);
  const navigate = useNavigate();
  const [dropdownOpen, setDropdownOpen] = useState(false);

  const handleLogout = async () => {
    try {
      await logoutUser();
      toast.success("Successfully logged out.");
      window.location.reload(); // Ensure full page refresh after logout
    } catch (error) {
      toast.error(error.message || "Failed to log out.");
    }
  };

  return (
    <HeaderContainer>
      <Logo onClick={() => navigate("/")}>Yoked</Logo>
      <StyledButtonGroup>
        {/* Navigation Links */}
        <StyledNavLink href="#about">About</StyledNavLink>
        <StyledNavLink href="#features">Features</StyledNavLink>
        <StyledNavLink href="#subscriptions">Subscriptions</StyledNavLink>

        {/* Action Buttons */}
        {currentUser ? (
          <DropdownContainer>
            <DropdownButton onClick={() => setDropdownOpen((prev) => !prev)}>
              Let’s Go, {currentUser.username}
            </DropdownButton>
            <DropdownMenu isOpen={dropdownOpen}>
              <DropdownMenuItem onClick={() => navigate("/dashboard")}>Dashboard</DropdownMenuItem>
              <DropdownMenuItem onClick={handleLogout}>Logout</DropdownMenuItem>
            </DropdownMenu>
          </DropdownContainer>
        ) : (
          <>
            <StyledButton onClick={() => navigate("/login")}>Login</StyledButton>
            <StyledButton onClick={() => navigate("/register")}>Register</StyledButton>
          </>
        )}
      </StyledButtonGroup>
      <MobileMenuToggle onClick={() => console.log("Toggle mobile menu")}>☰</MobileMenuToggle>
    </HeaderContainer>
  );
};

export default Header;
