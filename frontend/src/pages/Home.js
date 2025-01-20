import React, { useContext, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import styled from "styled-components";
import ReactPlayer from "react-player";
import { AuthContext } from "../contexts/AuthContext";
import Header from "../components/shared/Header";
import { getAllSubscriptions } from "../api/subscriptionApi"; // Importing utility function for fetching subscriptions
import { logoutUser } from "../api/authApi";

// Styled Components
const HeroSection = styled.div`
  position: relative;
  height: 100vh;
  width: 100vw;
  background-color: ${({ theme }) => theme.colors.secondary};
  overflow: hidden;

  video,
  .react-player {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    z-index: 1;
  }

  h1 {
    color: #fff;
    font-size: 3rem;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    text-align: center;
    text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.7);
    z-index: 2;
  }
`;

const Section = styled.section`
  padding: ${({ theme }) => theme.spacing(10)} ${({ theme }) => theme.spacing(4)};
  text-align: center;
  background: ${({ theme }) => theme.colors.cardBackground};
  color: ${({ theme }) => theme.colors.textPrimary};

  h2 {
    margin-bottom: ${({ theme }) => theme.spacing(3)};
    font-size: 3rem;
  }

  p {
    font-size: 1.4rem;
    margin: ${({ theme }) => theme.spacing(3)} 0;
    color: ${({ theme }) => theme.colors.textSecondary};
  }
`;

const SubscriptionCards = styled.div`
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: ${({ theme }) => theme.spacing(5)};
`;

const SubscriptionCard = styled.div`
  background: ${({ theme }) => theme.colors.cardBackground};
  padding: ${({ theme }) => theme.spacing(5)};
  border-radius: ${({ theme }) => theme.borderRadius};
  text-align: center;
  box-shadow: ${({ theme }) => theme.shadows.medium};
  flex: 1 1 300px;

  h3 {
    color: ${({ theme }) => theme.colors.primary};
    margin-bottom: ${({ theme }) => theme.spacing(3)};
  }

  ul {
    list-style: none;
    padding: 0;
    color: ${({ theme }) => theme.colors.textSecondary};

    li {
      margin-bottom: ${({ theme }) => theme.spacing(2)};
    }
  }

  p {
    margin-top: ${({ theme }) => theme.spacing(2)};
    color: ${({ theme }) => theme.colors.textSecondary};
  }
`;

const DropdownMenu = styled.div`
  position: relative;
  display: inline-block;

  .dropdown-content {
    display: none;
    position: absolute;
    background-color: ${({ theme }) => theme.colors.cardBackground};
    box-shadow: ${({ theme }) => theme.shadows.medium};
    border-radius: ${({ theme }) => theme.borderRadius};
    min-width: 160px;
    z-index: 10;

    a,
    button {
      color: ${({ theme }) => theme.colors.textPrimary};
      padding: ${({ theme }) => theme.spacing(2)};
      text-decoration: none;
      display: block;
      background: none;
      border: none;
      text-align: left;
      cursor: pointer;
    }

    a:hover,
    button:hover {
      background-color: ${({ theme }) => theme.colors.hoverBackground};
    }
  }

  &:hover .dropdown-content {
    display: block;
  }
`;

const Home = () => {
  const { currentUser, setCurrentUser } = useContext(AuthContext);
  const navigate = useNavigate();
  const [subscriptions, setSubscriptions] = useState([]);

  useEffect(() => {
    const fetchSubscriptions = async () => {
      try {
        const tiers = await getAllSubscriptions();
        const sortedSubscriptions = tiers.sort((a, b) => a.price - b.price);
        setSubscriptions(sortedSubscriptions);
      } catch (error) {
        console.error("Failed to fetch subscriptions:", error);
      }
    };

    fetchSubscriptions();
  }, []);

  const handleLogout = async () => {
    try {
      await logoutUser();
      setCurrentUser(null); // Clear user context
      navigate("/login");
    } catch (error) {
      console.error("Failed to log out:", error.message || error);
    }
  };

  return (
    <>
      <Header>
        {currentUser ? (
          <DropdownMenu>
            <button>{`Ready to dominate, ${currentUser.username}!`}</button>
            <div className="dropdown-content">
              <button onClick={() => navigate("/dashboard")}>Dashboard</button>
              <button onClick={handleLogout}>Logout</button>
            </div>
          </DropdownMenu>
        ) : (
          <>
            <button onClick={() => navigate("/login")}>Login</button>
            <button onClick={() => navigate("/register")}>Register</button>
          </>
        )}
      </Header>

      <HeroSection>
        <ReactPlayer
          url="https://videos.pexels.com/video-files/4761426/4761426-uhd_4096_2160_25fps.mp4"
          className="react-player"
          playing
          loop
          muted
          width="100%"
          height="100%"
        />
        <h1>Renew Your Body and Mind with Yoked</h1>
      </HeroSection>

      {/* About Section */}
      <Section id="about">
        <h2>About Yoked</h2>
        <p>
          Yoked is your ultimate partner in achieving holistic fitness—physically and mentally.
          Our mission is to empower you with tools, resources, and a supportive community
          to unlock your best self. Whether you're a beginner or a fitness enthusiast, Yoked has everything you need.
        </p>
      </Section>

      {/* Subscription Section */}
      <Section id="subscriptions">
        <h2>Subscription Tiers</h2>
        <SubscriptionCards>
          {subscriptions.map((tier) => (
            <SubscriptionCard key={tier.id}>
              <h3>{tier.name}</h3>
              <ul>
                {tier.features.map((feature, index) => (
                  <li key={index}>{feature}</li>
                ))}
              </ul>
              <p>Price: {tier.price === 0 ? "Free" : `$${(tier.price / 100).toFixed(2)}/month`}</p>
            </SubscriptionCard>
          ))}
        </SubscriptionCards>
      </Section>
    </>
  );
};

export default Home;
