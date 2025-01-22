import React, { useContext, useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import styled from "styled-components";
import { AuthContext } from "../contexts/AuthContext";
import { FaHome, FaDumbbell, FaSeedling, FaUsers, FaUserCircle } from "react-icons/fa";

// Styled Components
const DashboardContainer = styled.div`
  display: flex;
  flex-direction: column;
  height: 100vh;
`;

const Header = styled.header`
  background: ${({ theme }) => theme.colors.primary};
  color: white;
  padding: 1rem;
  text-align: center;
  font-size: 2rem;
`;

const TabsContainer = styled.div`
  display: flex;
  background-color: ${({ theme }) => theme.colors.cardBackground};
  justify-content: space-around;
  padding: 1rem 0;
  border-top: 1px solid ${({ theme }) => theme.colors.border};

  @media (max-width: ${({ theme }) => theme.breakpoints.sm}) {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 1rem;
  }
`;

const Tab = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  color: ${({ active, theme }) =>
    active ? theme.colors.primary : theme.colors.textSecondary};
  transition: color 0.3s ease-in-out;

  &:hover {
    color: ${({ theme }) => theme.colors.primary};
  }

  svg {
    font-size: 2rem;
  }

  p {
    font-size: 0.8rem;
    margin-top: 0.5rem;
  }
`;

const ContentContainer = styled.div`
  flex-grow: 1;
  padding: 2rem;
  background-color: ${({ theme }) => theme.colors.background};
`;

const Dashboard = () => {
  const { currentUser } = useContext(AuthContext);
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

  // Handle tab changes
  const handleTabChange = (tab) => {
    setActiveTab(tab);
  };

  return (
    <DashboardContainer>
      <Header>Let's Workout {currentUser?.username}!</Header>

      {/* Tabs */}
      <TabsContainer>
        <Tab active={activeTab === "reels"} onClick={() => handleTabChange("reels")}>
          <FaHome />
          <p>Reels</p>
        </Tab>
        <Tab active={activeTab === "workouts"} onClick={() => handleTabChange("workouts")}>
          <FaDumbbell />
          <p>Workouts</p>
        </Tab>
        <Tab active={activeTab === "nutrition"} onClick={() => handleTabChange("nutrition")}>
          <FaSeedling />
          <p>Nutrition</p>
        </Tab>
        <Tab active={activeTab === "community"} onClick={() => handleTabChange("community")}>
          <FaUsers />
          <p>Community</p>
        </Tab>
        <Tab active={activeTab === "profile"} onClick={() => handleTabChange("profile")}>
          <FaUserCircle />
          <p>Profile</p>
        </Tab>
      </TabsContainer>

      {/* Content Area */}
      <ContentContainer>
        {activeTab === "reels" && <h2>Reels Page</h2>}
        {activeTab === "workouts" && <h2>Workouts Library</h2>}
        {activeTab === "nutrition" && <h2>Nutrition</h2>}
        {activeTab === "community" && <h2>Community</h2>}
        {activeTab === "profile" && <h2>User Profile</h2>}
      </ContentContainer>
    </DashboardContainer>
  );
};

export default Dashboard;
