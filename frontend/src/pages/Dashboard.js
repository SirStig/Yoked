import React, { useContext, useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import styled from "styled-components";
import { AuthContext } from "../contexts/AuthContext";
import { FaVideo, FaDumbbell, FaCalendarAlt, FaAppleAlt, FaUsers, FaUserCircle, FaCog, FaSignOutAlt } from "react-icons/fa";

// Styled Components
const DashboardContainer = styled.div`
  display: flex;
  height: 100vh;
  background-color: ${({ theme }) => theme.colors.background};
`;

const Sidebar = styled.div`
  width: 250px;
  background-color: ${({ theme }) => theme.colors.cardBackground};
  display: flex;
  flex-direction: column;
  padding: 2rem 1rem;
  box-shadow: ${({ theme }) => theme.shadows.medium};
  justify-content: space-between;
`;

const SidebarItem = styled.div`
  display: flex;
  align-items: center;
  padding: 1rem;
  cursor: pointer;
  border-radius: ${({ theme }) => theme.borderRadius};
  color: ${({ active, theme }) =>
    active ? theme.colors.primary : theme.colors.textSecondary};
  background-color: ${({ active, theme }) =>
    active ? theme.colors.cardBackgroundHover : "transparent"};
  transition: background-color 0.3s, color 0.3s;

  &:hover {
    background-color: ${({ theme }) => theme.colors.cardBackgroundHover};
    color: ${({ theme }) => theme.colors.primary};
  }

  svg {
    margin-right: 1rem;
    font-size: 1.5rem;
  }
`;

const LogoutButton = styled(SidebarItem)`
  margin-top: auto;
`;

const ContentArea = styled.div`
  flex: 1;
  padding: 2rem;
  overflow-y: auto;
`;

const ContentHeader = styled.div`
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 1rem;
`;

const Dashboard = () => {
  const { currentUser, logout } = useContext(AuthContext);
  const [activeTab, setActiveTab] = useState("reels");
  const navigate = useNavigate();

  useEffect(() => {
    if (!currentUser) {
      navigate("/login");
    } else if (currentUser.setup_step !== "completed") {
      switch (currentUser.setup_step) {
        case "profile_completion":
          navigate("/profile-setup");
          break;
        case "subscription_selection":
          navigate("/choose-subscription");
          break;
        default:
          navigate("/verify-email");
          break;
      }
    }
  }, [currentUser, navigate]);

  const handleTabChange = (tab) => setActiveTab(tab);

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <DashboardContainer>
      {/* Sidebar */}
      <Sidebar>
        <div>
          <SidebarItem
            active={activeTab === "reels"}
            onClick={() => handleTabChange("reels")}
          >
            <FaVideo />
            Yoked Reels
          </SidebarItem>
          <SidebarItem
            active={activeTab === "workouts"}
            onClick={() => handleTabChange("workouts")}
          >
            <FaDumbbell />
            Workout Library
          </SidebarItem>
          <SidebarItem
            active={activeTab === "weekly"}
            onClick={() => handleTabChange("weekly")}
          >
            <FaCalendarAlt />
            Weekly Programs
          </SidebarItem>
          <SidebarItem
            active={activeTab === "nutrition"}
            onClick={() => handleTabChange("nutrition")}
          >
            <FaAppleAlt />
            Nutrition
          </SidebarItem>
          <SidebarItem
            active={activeTab === "community"}
            onClick={() => handleTabChange("community")}
          >
            <FaUsers />
            Community
          </SidebarItem>
          <SidebarItem
            active={activeTab === "profile"}
            onClick={() => handleTabChange("profile")}
          >
            <FaUserCircle />
            Profile
          </SidebarItem>
          <SidebarItem
            active={activeTab === "settings"}
            onClick={() => handleTabChange("settings")}
          >
            <FaCog />
            Settings
          </SidebarItem>
        </div>
        <LogoutButton onClick={handleLogout}>
          <FaSignOutAlt />
          Logout
        </LogoutButton>
      </Sidebar>

      {/* Content Area */}
      <ContentArea>
        <ContentHeader>
          {activeTab === "reels" && "Yoked Reels"}
          {activeTab === "workouts" && "Workout Library"}
          {activeTab === "weekly" && "Weekly Programs"}
          {activeTab === "nutrition" && "Nutrition"}
          {activeTab === "community" && "Community"}
          {activeTab === "profile" && "Your Profile"}
          {activeTab === "settings" && "Settings"}
        </ContentHeader>

        {/* Placeholder Content */}
        {activeTab === "reels" && <p>Reels Content Goes Here...</p>}
        {activeTab === "workouts" && <p>Workout Library Content Goes Here...</p>}
        {activeTab === "weekly" && <p>Weekly Programs Content Goes Here...</p>}
        {activeTab === "nutrition" && <p>Nutrition Content Goes Here...</p>}
        {activeTab === "community" && <p>Community Content Goes Here...</p>}
        {activeTab === "profile" && <p>Profile Content Goes Here...</p>}
        {activeTab === "settings" && <p>Settings Content Goes Here...</p>}
      </ContentArea>
    </DashboardContainer>
  );
};

export default Dashboard;
