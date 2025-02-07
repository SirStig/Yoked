import React, { useContext, useState, useEffect, useRef } from "react";
import styled, { css, keyframes } from "styled-components";
import { useNavigate, useLocation } from "react-router-dom";
import { AuthContext } from "../contexts/AuthContext";
import ProfileCompletion from "./Registration/ProfileCompletion";
import SubscriptionSelection from "./Registration/SubscriptionSelection";
import Login from "./Login";
import AccountCreation from "./Registration/AccountCreation";
import Settings from "./Settings/Settings";
import {
  FaHome,
  FaSearch,
  FaBell,
  FaEnvelope,
  FaVideo,
  FaBars,
  FaSignOutAlt,
  FaHeart,
  FaDumbbell,
} from "react-icons/fa";
import {
  MdSettings,
  MdPrivacyTip,
  MdFeedback,
  MdHelpOutline,
  MdOutlinePolicy,
} from "react-icons/md";

// Keyframe Animations
const slideDown = keyframes`
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
`;

const fadeIn = keyframes`
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
`;

// Styled Components
const DashboardContainer = styled.div.withConfig({
  shouldForwardProp: (prop) => !["isBlurred"].includes(prop),
})`
  display: flex;
  height: 100vh;
  background-color: ${({ theme }) => theme.colors.secondary};
  ${({ isBlurred }) =>
    isBlurred &&
    css`
      filter: blur(8px);
      pointer-events: none;
    `}
`;

const Sidebar = styled.div`
  width: 200px;
  background-color: ${({ theme }) => theme.components.sidebar.background};
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 1rem;
  box-shadow: ${({ theme }) => theme.shadows.medium};
  z-index: 10;
  animation: ${fadeIn} 0.5s ease-in-out;
`;

const SidebarItem = styled.div.withConfig({
  shouldForwardProp: (prop) => !["active"].includes(prop),
})`
  display: flex;
  align-items: center;
  gap: 0.9rem;
  padding: 0.9rem;
  cursor: pointer;
  color: ${({ active, theme }) =>
    active
      ? theme.components.sidebar.activeText
      : theme.components.sidebar.text};
  background-color: transparent;
  transition: transform 0.2s ease-in-out;

  &:hover {
    transform: scale(1.05);
  }

  svg {
    font-size: 1.5rem;
  }
`;

const MoreDropdown = styled.div.withConfig({
  shouldForwardProp: (prop) => !["isOpen"].includes(prop),
})`
  position: absolute;
  width: 200px;
  background-color: ${({ theme }) => theme.components.dropdown.background};
  box-shadow: ${({ theme }) => theme.shadows.medium};
  z-index: 11;
  display: ${({ isOpen }) => (isOpen ? "block" : "none")};
  padding: 0.5rem;
  animation: ${slideDown} 0.3s ease-in-out;

  ${SidebarItem} {
    color: ${({ theme }) => theme.components.dropdown.text};
    transition: transform 0.2s ease-in-out;

    &:hover {
      background-color: transparent;
      transform: scale(1.05);
    }
  }
`;

const ProfileButton = styled(SidebarItem)`
  img {
    width: 32px;
    height: 32px;
    object-fit: cover;
  }
`;

const LogoutButton = styled(SidebarItem)``;

const MoreButton = styled(SidebarItem)`
  margin-top: auto;
  svg {
    font-size: 1.8rem;
    transition: ${({ theme }) => theme.transitions.default};
    ${({ isOpen }) => isOpen && "transform: rotate(90deg);"}
  }
`;

const ContentArea = styled.div`
  flex: 1;
  padding: 2rem;
  overflow-y: auto;
`;

const Overlay = styled.div`
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: ${({ theme }) => theme.components.overlay.background};
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
`;

const OverlayContent = styled.div`
  background: ${({ theme }) => theme.colors.secondary};
  padding: 2rem;
  box-shadow: ${({ theme }) => theme.shadows.large};
  width: auto;
  text-align: center;
  border-radius: ${({ theme }) => theme.borderRadius.large};
`;

const OverlayButtons = styled.div`
  position: fixed;
  top: 1rem;
  left: 1rem;
  display: flex;
  gap: 1rem;
  z-index: 1001;
`;

const TransparentButton = styled.button`
  background: none;
  border: none;
  color: ${({ theme }) => theme.colors.primary};
  font-size: 1rem;
  cursor: pointer;
  text-decoration: none;
  transition: ${({ theme }) => theme.transitions.default};

  &:hover {
    color: ${({ theme }) => theme.colors.primaryHover};
    transform: scale(1.1);
  }

  &:active {
    color: ${({ theme }) => theme.colors.accent};
  }
`;

const Dashboard = () => {
  const { currentUser, logout } = useContext(AuthContext);
  const [activeTab, setActiveTab] = useState("home");
  const [activeOverlay, setActiveOverlay] = useState(null);
  const [isMoreOpen, setIsMoreOpen] = useState(false);
  const moreRef = useRef(null);
  const dropdownRef = useRef(null);
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    console.log("Dashboard: Checking overlay state...");

    if (location.state?.overlay) {
      console.log("Dashboard: Overlay state received:", location.state.overlay);
      setActiveOverlay(location.state.overlay);
    } else if (currentUser?.setup_step) {
      console.log("Dashboard: Verifying setup_step:", currentUser.setup_step);

      switch (currentUser.setup_step) {
        case "profile_completion":
          setActiveOverlay("profileCompletion");
          break;
        case "subscription_selection":
          setActiveOverlay("subscriptionSelection");
          break;
        default:
          setActiveOverlay(null); // No overlay needed
          break;
      }
    } else {
      setActiveOverlay("login"); // If user is not logged in, default to login overlay
    }
  }, [location.state, currentUser]);



  useEffect(() => {
    const positionDropdown = () => {
      if (isMoreOpen && moreRef.current && dropdownRef.current) {
        const buttonRect = moreRef.current.getBoundingClientRect();
        const dropdownElement = dropdownRef.current;

        dropdownElement.style.top = `${buttonRect.top - dropdownElement.offsetHeight - 8}px`;
        dropdownElement.style.left = `${buttonRect.left}px`;
      }
    };

    positionDropdown();
    window.addEventListener("resize", positionDropdown);

    return () => {
      window.removeEventListener("resize", positionDropdown);
    };
  }, [isMoreOpen]);


  const handleLogout = async () => {
    await logout();
    setActiveOverlay("login");
  };

  const handleMoreItemClick = (action) => {
    action();
    setIsMoreOpen(false);
  };

  return (
    <>
      {activeOverlay && (
        <>
          <Overlay>
            <OverlayContent>
              {activeOverlay === "login" && <Login />}
              {activeOverlay === "register" && <AccountCreation />}
              {activeOverlay === "profileCompletion" && <ProfileCompletion />}
              {activeOverlay === "subscriptionSelection" && <SubscriptionSelection />}
            </OverlayContent>
          </Overlay>
          <OverlayButtons>
            <TransparentButton onClick={() => navigate("/")}>Home</TransparentButton>
            {currentUser && <TransparentButton onClick={handleLogout}>Logout</TransparentButton>}
          </OverlayButtons>
        </>
      )}

      <DashboardContainer isBlurred={!!activeOverlay}>
        <Sidebar>
          <h1>Yoked</h1>
          <SidebarItem active={activeTab === "home" ? "true" : "false"} onClick={() => setActiveTab("home")}>
            <FaHome />
            Home
          </SidebarItem>
          <SidebarItem active={activeTab === "reels" ? "true" : "false"} onClick={() => setActiveTab("reels")}>
            <FaVideo />
            Yoked Reels
          </SidebarItem>
          <SidebarItem active={activeTab === "search" ? "true" : "false"} onClick={() => setActiveTab("search")}>
            <FaSearch />
            Search
          </SidebarItem>
          <SidebarItem active={activeTab === "notifications" ? "true" : "false"} onClick={() => setActiveTab("notifications")}>
            <FaBell />
            Notifications
          </SidebarItem>
          <SidebarItem active={activeTab === "health" ? "true" : "false"} onClick={() => setActiveTab("health")}>
            <FaHeart />
            Health
          </SidebarItem>
          <SidebarItem active={activeTab === "workouts" ? "true" : "false"} onClick={() => setActiveTab("workouts")}>
            <FaDumbbell />
            Workouts
          </SidebarItem>
          <SidebarItem active={activeTab === "messages" ? "true" : "false"} onClick={() => setActiveTab("messages")}>
            <FaEnvelope />
            Messages
          </SidebarItem>
          <ProfileButton active={activeTab === "profile" ? "true" : "false"} onClick={() => setActiveTab("profile")}>
            <img src={currentUser?.avatar || "/assets/default-avatar.png"} alt="User Avatar" />
            Profile
          </ProfileButton>
          <MoreButton
            isOpen={isMoreOpen}
            onClick={() => setIsMoreOpen((prev) => !prev)}
            ref={moreRef}
          >
            <FaBars />
            More
          </MoreButton>
          <MoreDropdown ref={dropdownRef} isOpen={isMoreOpen}>
            <SidebarItem onClick={() => handleMoreItemClick(() => setActiveTab("settings"))}>
              <MdSettings />
              Settings
            </SidebarItem>
            <SidebarItem onClick={() => handleMoreItemClick(() => navigate("/legal/privacy"))}>
              <MdPrivacyTip />
              Privacy Policy
            </SidebarItem>
            <SidebarItem onClick={() => handleMoreItemClick(() => navigate("/legal/terms"))}>
              <MdOutlinePolicy />
              Terms and Conditions
            </SidebarItem>
            <SidebarItem onClick={() => handleMoreItemClick(() => navigate("/support"))}>
              <MdHelpOutline />
              Support
            </SidebarItem>
            <SidebarItem onClick={() => handleMoreItemClick(() => navigate("/feedback"))}>
              <MdFeedback />
              Request a Feature
            </SidebarItem>
          </MoreDropdown>
          <LogoutButton onClick={handleLogout}>
            <FaSignOutAlt />
            Logout
          </LogoutButton>
        </Sidebar>

        <ContentArea>
          {activeTab === "home" && <h2>Home Content</h2>}
          {activeTab === "reels" && <h2>Yoked Reels Content</h2>}
          {activeTab === "search" && <h2>Search Content</h2>}
          {activeTab === "notifications" && <h2>Notifications Content</h2>}
          {activeTab === "health" && <h2>Health Content</h2>}
          {activeTab === "workouts" && <h2>Workouts Content</h2>}
          {activeTab === "messages" && <h2>Messages Content</h2>}
          {activeTab === "profile" && <h2>Profile Content</h2>}
          {activeTab === "settings" && <Settings />}
        </ContentArea>
      </DashboardContainer>
    </>
  );
};

export default Dashboard;
