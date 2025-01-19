import React from "react";
import styled from "styled-components"; // Import styled
import { Link as ScrollLink } from "react-scroll"; // Import Link from react-scroll
import { useNavigate } from "react-router-dom"; // Import useNavigate

const HeaderContainer = styled.header`
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  background: ${({ theme }) => theme.colors.secondary};
  color: ${({ theme }) => theme.colors.textPrimary};
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: ${({ theme }) => theme.spacing(2)} ${({ theme }) => theme.spacing(3)};
  z-index: 1000;
  box-shadow: ${({ theme }) => theme.shadows.medium};
`;

const Logo = styled.div`
  font-size: 1.5rem;
  font-weight: ${({ theme }) => theme.font.weightBold};
  cursor: pointer;
`;

const NavLinks = styled.div`
  display: flex;
  align-items: center;
  gap: ${({ theme }) => theme.spacing(4)};
`;

const StyledScrollLink = styled(ScrollLink)`
  color: ${({ theme }) => theme.colors.textPrimary};
  cursor: pointer;
  text-decoration: none;
  transition: color ${({ theme }) => theme.transitions.default};

  &:hover {
    color: ${({ theme }) => theme.colors.accent};
  }
`;

const Button = styled.button`
  background: ${({ theme }) => theme.colors.primary};
  color: ${({ theme }) => theme.colors.textPrimary};
  border: none;
  padding: ${({ theme }) => theme.spacing(1)} ${({ theme }) => theme.spacing(2)};
  border-radius: ${({ theme }) => theme.borderRadius};
  cursor: pointer;
  transition: background ${({ theme }) => theme.transitions.default};
  font-size: 1rem;
  width: 120px; /* Ensure equal width */
  text-align: center;

  &:hover {
    background: ${({ theme }) => theme.colors.primaryHover};
  }
`;

const Header = () => {
  const navigate = useNavigate();

  return (
    <HeaderContainer>
      <Logo onClick={() => navigate("/")}>Project Yoked</Logo>
      <NavLinks>
        <StyledScrollLink to="about" smooth={true} duration={500}>
          About
        </StyledScrollLink>
        <StyledScrollLink to="subscriptions" smooth={true} duration={500}>
          Subscriptions
        </StyledScrollLink>
        <Button onClick={() => navigate("/login")}>Login</Button>
        <Button onClick={() => navigate("/register")}>Register</Button>
      </NavLinks>
    </HeaderContainer>
  );
};

export default Header;
