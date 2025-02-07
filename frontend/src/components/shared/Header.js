import React, { useContext, useState, useEffect } from "react";
import styled from "styled-components";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../../contexts/AuthContext";
import { logoutUser } from "../../api/authApi";
import { toast } from "react-toastify";
import { Link as ScrollLink } from "react-scroll";

// Styled components for the header
const HeaderContainer = styled.header`
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  color: ${({ theme }) => theme.colors.textPrimary};
  display: flex;
  align-items: center;
  padding: ${({ theme }) => theme.spacing(2)} ${({ theme }) => theme.spacing(4)};
  z-index: 1000;
  transition: background 0.3s ease, box-shadow 0.3s ease;
  backdrop-filter: ${({ isScrolled }) => (isScrolled ? "blur(10px)" : "none")};
  background: ${({ isScrolled, theme }) =>
    isScrolled ? "rgba(0, 0, 0, 0.7)" : "transparent"};
  box-shadow: ${({ isScrolled, theme }) =>
    isScrolled ? theme.shadows.medium : "none"};

  @media (max-width: ${({ theme }) => theme.breakpoints.sm}) {
    padding: ${({ theme }) => theme.spacing(2)};
  }
`;

const Logo = styled.div`
  font-size: 1.8rem;
  font-weight: ${({ theme }) => theme.font.weightBold};
  color: ${({ theme }) => theme.colors.accent};
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: ${({ theme }) => theme.spacing(2)};
  flex: 1;

  img {
    width: 40px;
    height: 40px; 
    object-fit:
  }
`;

const NavLinks = styled.div`
  display: flex;
  flex: 2;
  justify-content: center;
  gap: ${({ theme }) => theme.spacing(4)};
  align-items: center;

  a {
    color: #ffffff;
    text-decoration: none;
    font-size: 1rem;
    font-weight: ${({ theme }) => theme.font.weightMedium};
    transition: color ${({ theme }) => theme.transitions.default};
    display: flex;
    align-items: center;
    cursor: pointer;

    &:hover {
      color: ${({ theme }) => theme.colors.accent};
    }
  }

  @media (max-width: ${({ theme }) => theme.breakpoints.sm}) {
    display: none;
  }
`;

const ButtonGroup = styled.div`
  display: flex;
  align-items: center;
  gap: ${({ theme }) => theme.spacing(2)};
  flex: 1;
  justify-content: flex-end;
`;

const RoundedButton = styled.button`
  background: #ffffff;
  color: #000000;
  border: none;
  padding: ${({ theme }) => theme.spacing(1.5)} ${({ theme }) => theme.spacing(3)};
  border-radius: 50px;
  font-size: 1rem;
  font-weight: ${({ theme }) => theme.font.weightMedium};
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;

  &:hover {
    transform: scale(1.05);
    box-shadow: ${({ theme }) => theme.shadows.light};
  }
`;

const DropdownContainer = styled.div`
  position: relative;
  display: inline-block;
  width: auto;
`;

const DropdownButton = styled.div`
  background: #ffffff;
  color: #000000;
  border: none;
  padding: ${({ theme }) => theme.spacing(1.5)} ${({ theme }) => theme.spacing(3)};
  border-radius: 50px;
  font-size: 1rem;
  font-weight: ${({ theme }) => theme.font.weightMedium};
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: ${({ theme }) => theme.spacing(1)};
  transition: transform 0.3s ease, box-shadow 0.3s ease;

  &:hover {
    transform: scale(1.05);
    box-shadow: ${({ theme }) => theme.shadows.light};
  }
`;

const DropdownMenu = styled.ul`
  position: absolute;
  top: calc(100% + 4px);
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
  text-align: center;

  &:hover {
    background: ${({ theme }) => theme.colors.inputBackground};
  }
`;

const Header = () => {
  const { currentUser } = useContext(AuthContext);
  const navigate = useNavigate();
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const [isScrolled, setIsScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 50); // Activate after 50px of scrolling
    };

    window.addEventListener("scroll", handleScroll);
    return () => {
      window.removeEventListener("scroll", handleScroll);
    };
  }, []);

  const handleLogout = async () => {
    try {
      await logoutUser();
      toast.success("Successfully logged out.");
      window.location.reload();
    } catch (error) {
      toast.error(error.message || "Failed to log out.");
    }
  };

  const handleDashboardNavigation = () => {
    if (!currentUser) {
      navigate("/dashboard", { state: { overlay: "login" } });
      return;
    }

    console.log("Header: Navigating to dashboard with setup_step:", currentUser?.setup_step);

    switch (currentUser?.setup_step) {
      case "profile_completion":
        navigate("/dashboard", { state: { overlay: "profileCompletion" } });
        break;
      case "subscription_selection":
        navigate("/dashboard", { state: { overlay: "subscriptionSelection" } });
        break;
      default:
        navigate("/dashboard");
        break;
    }
  };

  const handleSettingsNavigation = () => {
    if (!currentUser) {
      navigate("/dashboard", { state: { overlay: "login" } });
    } else {
      navigate("/dashboard", { state: { overlay: "settings" } });
    }
  };


  return (
    <HeaderContainer isScrolled={isScrolled}>
      <Logo onClick={() => navigate("/")}>
        <img src="/assets/yoked-logo-1.svg" alt="Yoked Logo"/>
        Yoked
      </Logo>
      <NavLinks>
        <ScrollLink to="home" smooth={true} duration={500} offset={-80}>
          Home
        </ScrollLink>
        <ScrollLink to="features" smooth={true} duration={500} offset={-80}>
          Features
        </ScrollLink>
        <ScrollLink to="subscriptions" smooth={true} duration={500} offset={-80}>
          Subscriptions
        </ScrollLink>
      </NavLinks>
      <ButtonGroup>
        {currentUser ? (
          <DropdownContainer>
            <DropdownButton onClick={() => setDropdownOpen((prev) => !prev)}>
              Welcome, {currentUser.username}
            </DropdownButton>
            <DropdownMenu isOpen={dropdownOpen}>
              <DropdownMenuItem onClick={() => handleDashboardNavigation(null)}>
                Dashboard
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => handleDashboardNavigation("settings")}>Settings</DropdownMenuItem>
              <DropdownMenuItem onClick={handleLogout}>Logout</DropdownMenuItem>
            </DropdownMenu>
          </DropdownContainer>
        ) : (
          <>
            <RoundedButton onClick={() => handleDashboardNavigation("login")}>Login</RoundedButton>
            <RoundedButton onClick={() => handleDashboardNavigation("register")}>Register</RoundedButton>
          </>
        )}
      </ButtonGroup>
    </HeaderContainer>
  );
};

export default Header;
