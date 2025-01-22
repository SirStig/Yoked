import React, { useContext, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../contexts/AuthContext";
import Header from "../components/shared/Header";
import Footer from "../components/shared/Footer";
import { getAllSubscriptions } from "../api/subscriptionApi";
import { logoutUser } from "../api/authApi";
import SubscriptionCard from "../components/shared/SubscriptionCard";
import Section from "../components/shared/Section";
import FeatureCard from "../components/shared/FeatureCard";
import styled from "styled-components";

// Hero Section Styling
  const HeroSection = styled.section`
    height: 100vh;
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
    color: ${({ theme }) => theme.colors.textPrimary};
  
    h1 {
      font-size: 3.5rem;
      font-weight: ${({ theme }) => theme.font.weightBold};
      text-shadow: 2px 2px ${({ theme }) => theme.colors.secondary};
      z-index: 2; /* Ensure text is above the overlay */
    }
  
    video {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      object-fit: cover;
      z-index: 0; /* Ensure video is behind the overlay and content */
    }
  
    /* Dark blur overlay */
    &::before {
      content: "";
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0, 0, 0, 0.5); /* Semi-transparent black */
      backdrop-filter: blur(8px); /* Apply blur effect */
      z-index: 1; /* Ensure overlay is above the video but below the text */
    }
  
    @keyframes fade-in {
      from {
        opacity: 0;
      }
      to {
        opacity: 1;
      }
    }
  `;

// Yoked Reels Section
const ReelsSection = styled(Section)`
  background: ${({ theme }) => theme.colors.primary};
  color: ${({ theme }) => theme.colors.textPrimary};
  text-align: center;
  padding: ${({ theme }) => theme.spacing(4)} ${({ theme }) => theme.spacing(2)};
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: ${({ theme }) => theme.spacing(3)};

  img {
    max-width: 100%;
    border-radius: ${({ theme }) => theme.borderRadius};
    box-shadow: ${({ theme }) => theme.shadows.medium};
    transition: transform 0.3s ease;

    &:hover {
      transform: scale(1.05);
    }
  }

  h2 {
    font-size: 2.5rem;
  }

  p {
    font-size: 1.2rem;
    line-height: 1.6;
    max-width: 800px;
  }
`;

// Features Grid Styling
const FeaturesGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: ${({ theme }) => theme.spacing(3)};
`;

// Subscriptions Grid Styling
const SubscriptionsGrid = styled.div`
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: ${({ theme }) => theme.spacing(3)};
`;

// About Section Styling
const AboutSection = styled(Section)`
  background: ${({ theme }) => theme.colors.cardBackground};
  color: ${({ theme }) => theme.colors.textPrimary};
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: ${({ theme }) => theme.spacing(4)};

  img {
    max-width: 600px;
    width: 100%;
    border-radius: ${({ theme }) => theme.borderRadius};
    box-shadow: ${({ theme }) => theme.shadows.medium};
    margin-bottom: ${({ theme }) => theme.spacing(2)};
  }

  p {
    font-size: 1.1rem;
    line-height: 1.8;
    max-width: 900px;
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
      setCurrentUser(null);
      navigate("/login");
    } catch (error) {
      console.error("Failed to log out:", error.message || error);
    }
  };

  return (
    <>
      <Header>
        {currentUser ? (
          <button onClick={handleLogout}>Logout</button>
        ) : (
          <>
            <button onClick={() => navigate("/login")}>Login</button>
            <button onClick={() => navigate("/register")}>Register</button>
          </>
        )}
      </Header>

      {/* Hero Section */}
      <HeroSection id="hero">
        <video autoPlay muted loop>
          <source src="https://videos.pexels.com/video-files/4367547/4367547-hd_1920_1080_30fps.mp4" type="video/mp4"/>
          Your browser does not support the video tag.
        </video>
        <h1>Renew Your Body and Mind with Yoked</h1>
      </HeroSection>

      {/* Yoked Reels Section */}
      <ReelsSection id="reels">
        <h2>Yoked Reels</h2>
        <p>
          Dive into a world of inspiration with Yoked Reels—short-form videos
          created by our community. From workout routines to motivational
          stories, share and discover content to keep you moving and
          motivated. Whether you're posting your progress or finding
          inspiration, Yoked Reels is your go-to space for fitness creativity.
        </p>
        <img src="/path-to-image-for-reels-section.jpg" alt="Yoked Reels in action" />
      </ReelsSection>

      {/* About Section */}
      <AboutSection id="about">
        <h2>About Yoked</h2>
        <img src="/path-to-about-section-image.jpg" alt="Community workout" />
        <p>
          Yoked isn’t just another fitness platform—it’s your personal fitness
          hub. Our mission is simple: provide you with the tools, guidance, and
          community to transform your life. With expert-curated workouts,
          personalized meal plans, and a thriving support network, Yoked makes
          fitness achievable and fun for everyone.
        </p>
        <p>
          We pride ourselves on bringing cutting-edge features like short-form
          reels, live classes, and wearable device integrations. Whether you're
          starting your journey or leveling up, Yoked is here to guide you
          every step of the way.
        </p>
      </AboutSection>

       {/* Features Section */}
      <Section id="features">
        <h2>Features</h2>
        <FeaturesGrid>
          <FeatureCard title="Fitness Tracking" description="Track your progress with detailed analytics and reports." />
          <FeatureCard title="Expert Guidance" description="Access professional trainers and tailored workout plans." />
          <FeatureCard title="Community Support" description="Join a supportive network of fitness enthusiasts." />
          <FeatureCard title="Yoked Reels" description="Share and discover fitness content with our short-form video feature." />
          <FeatureCard title="Live Classes" description="Engage in live sessions with expert trainers in real time." />
          <FeatureCard title="Wearable Integration" description="Connect your fitness devices for seamless tracking." />
        </FeaturesGrid>
      </Section>

      {/* Subscription Section */}
      <Section id="subscriptions">
        <h2>Subscription Tiers</h2>
        <SubscriptionsGrid>
          {subscriptions.map((tier) => (
            <SubscriptionCard
              key={tier.id}
              title={tier.name}
              features={tier.features}
              price={tier.price}
            />
          ))}
        </SubscriptionsGrid>
      </Section>

      {/* Footer */}
      <Footer />
    </>
  );
};

export default Home;
