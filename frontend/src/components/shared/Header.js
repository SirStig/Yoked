import React, { useContext, useState, useRef, useEffect } from "react";
import styled from "styled-components";
import { Link as ScrollLink } from "react-scroll";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../../contexts/AuthContext";
import {logoutUser} from "../../api/authApi";
import {toast} from "react-toastify";

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
  font-size: 1.8rem;
  font-weight: ${({ theme }) => theme.font.weightBold};
  color: ${({ theme }) => theme.colors.accent};
  cursor: pointer;
  transition: transform 0.3s ease;

  &:hover {
    transform: scale(1.1);
  }
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
  font-weight: ${({ theme }) => theme.font.weightMedium};
  transition: color ${({ theme }) => theme.transitions.default};

  &:hover {
    color: ${({ theme }) => theme.colors.accent};
  }
`;

const UserMenuWrapper = styled.div`
  position: relative;
  display: inline-block;
`;

const UserMenuButton = styled.button`
  background: linear-gradient(90deg, ${({ theme }) => theme.colors.accent}, ${({ theme }) => theme.colors.primary});
  color: ${({ theme }) => theme.colors.textPrimary};
  font-size: 1.1rem;
  font-weight: ${({ theme }) => theme.font.weightBold};
  border: none;
  border-radius: ${({ theme }) => theme.borderRadius};
  padding: ${({ theme }) => theme.spacing(1.5)} ${({ theme }) => theme.spacing(3)};
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: ${({ theme }) => theme.spacing(1)};

  &::after {
    content: "▼";
    font-size: 0.8rem;
    color: ${({ theme }) => theme.colors.textPrimary};
    margin-left: ${({ theme }) => theme.spacing(1)};
  }

  &:hover {
    background: linear-gradient(90deg, ${({ theme }) => theme.colors.accentHover}, ${({ theme }) => theme.colors.primaryHover});
  }
`;

const DropdownMenu = styled.div`
  position: absolute;
  top: 100%;
  right: 0;
  background: ${({ theme }) => theme.colors.cardBackground};
  border-radius: ${({ theme }) => theme.borderRadius};
  box-shadow: ${({ theme }) => theme.shadows.medium};
  margin-top: ${({ theme }) => theme.spacing(1)};
  overflow: hidden;
  z-index: 1000;
  width: 100%; /* Match button width */

  button {
    display: block;
    width: 100%; /* Match dropdown menu width */
    padding: ${({ theme }) => theme.spacing(2)};
    color: ${({ theme }) => theme.colors.textPrimary};
    background: none;
    border: none;
    text-align: left;
    font-size: 1rem;
    cursor: pointer;
    transition: background 0.3s ease;

    &:hover {
      background: ${({ theme }) => theme.colors.hoverBackground};
    }
  }
`;

const Button = styled.button`
  background: ${({ theme }) => theme.colors.primary};
  color: ${({ theme }) => theme.colors.textPrimary};
  border: none;
  padding: ${({ theme }) => theme.spacing(1.5)} ${({ theme }) => theme.spacing(3)};
  border-radius: ${({ theme }) => theme.borderRadius};
  cursor: pointer;
  font-size: 1rem;
  font-weight: ${({ theme }) => theme.font.weightMedium};
  transition: background ${({ theme }) => theme.transitions.default};

  &:hover {
    background: ${({ theme }) => theme.colors.primaryHover};
  }
`;

const Header = () => {
  const { currentUser, setCurrentUser } = useContext(AuthContext);
  const navigate = useNavigate();
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const dropdownRef = useRef(null);

  const handleLogout = async () => {
    try {
      await logoutUser();
      toast.success("Successfully logged out.");
      window.location.reload();
    } catch (error) {
      toast.error(error.message || "Failed to log out.");
    }
  };
  // Close dropdown when clicking outside
  useEffect(() => {
    const handleOutsideClick = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setDropdownOpen(false);
      }
    };

    document.addEventListener("mousedown", handleOutsideClick);
    return () => {
      document.removeEventListener("mousedown", handleOutsideClick);
    };
  }, []);

  return (
    <HeaderContainer>
      <Logo onClick={() => navigate("/")}>Yoked</Logo>
      <NavLinks>
        <StyledScrollLink to="about" smooth={true} duration={500}>
          About
        </StyledScrollLink>
        <StyledScrollLink to="subscriptions" smooth={true} duration={500}>
          Subscriptions
        </StyledScrollLink>
        {currentUser ? (
          <UserMenuWrapper ref={dropdownRef}>
            <UserMenuButton onClick={() => setDropdownOpen((prev) => !prev)}>
              {`Let’s Go, ${currentUser.username}`}
            </UserMenuButton>
            {dropdownOpen && (
              <DropdownMenu>
                <button onClick={() => navigate("/dashboard")}>Dashboard</button>
                <button onClick={handleLogout}>Logout</button>
              </DropdownMenu>
            )}
          </UserMenuWrapper>
        ) : (
          <>
            <Button onClick={() => navigate("/login")}>Login</Button>
            <Button onClick={() => navigate("/register")}>Register</Button>
          </>
        )}
      </NavLinks>
    </HeaderContainer>
  );
};

export default Header;
