import React, { useContext, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import styled from "styled-components";
import ReactPlayer from "react-player";
import { AuthContext } from "../contexts/AuthContext";
import Header from "../components/shared/Header";

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

const FeaturesGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: ${({ theme }) => theme.spacing(5)};
`;

const FeatureCard = styled.div`
  background: ${({ theme }) => theme.colors.cardBackground};
  padding: ${({ theme }) => theme.spacing(5)};
  border-radius: ${({ theme }) => theme.borderRadius};
  box-shadow: ${({ theme }) => theme.shadows.medium};
  animation: scale-up ${({ theme }) => theme.transitions.default};

  h3 {
    margin-bottom: ${({ theme }) => theme.spacing(3)};
    color: ${({ theme }) => theme.colors.primary};
  }

  p {
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

const Home = () => {
  const { currentUser } = useContext(AuthContext);
  const navigate = useNavigate();

  useEffect(() => {
    if (currentUser) {
      // Redirect to the appropriate setup page based on the user's setup step
      if (currentUser.setup_step === "completed") {
        navigate("/dashboard");
      } else {
        navigate(`/${currentUser.setup_step}`);
      }
    }
  }, [currentUser, navigate]);

  return (
    <>
      <Header />
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
        <FeaturesGrid>
          <FeatureCard>
            <h3>Community</h3>
            <p>
              Engage with like-minded individuals in forums, direct messaging, and exclusive challenges.
            </p>
          </FeatureCard>
          <FeatureCard>
            <h3>Progress Tracking</h3>
            <p>
              Monitor your weight, body measurements, and progress photos with advanced analytics.
            </p>
          </FeatureCard>
          <FeatureCard>
            <h3>Gamification</h3>
            <p>
              Earn badges, achievements, and rewards to stay motivated on your fitness journey.
            </p>
          </FeatureCard>
          <FeatureCard>
            <h3>Nutrition Guidance</h3>
            <p>
              Access personalized meal plans, recipes, and advanced calorie tracking tools.
            </p>
          </FeatureCard>
          <FeatureCard>
            <h3>Workout Library</h3>
            <p>
              Explore expert-designed workouts for every fitness level and goal.
            </p>
          </FeatureCard>
          <FeatureCard>
            <h3>Yoked Reels</h3>
            <p>
              Discover high-quality, short-form fitness videos for tips, motivation, and guidance.
            </p>
          </FeatureCard>
        </FeaturesGrid>
      </Section>

      {/* Subscription Section */}
      <Section id="subscriptions">
        <h2>Subscription Tiers</h2>
        <SubscriptionCards>
          <SubscriptionCard>
            <h3>Basic (Free)</h3>
            <ul>
              <li>Limited access to "Yoked Reels" with ads.</li>
              <li>Basic workout routines with ads.</li>
              <li>Read-only access to community forums.</li>
              <li>Basic progress tracking tools.</li>
            </ul>
            <p>Price: Free forever</p>
          </SubscriptionCard>
          <SubscriptionCard>
            <h3>Pro ($9.99/month)</h3>
            <ul>
              <li>Ad-free access to "Yoked Reels" and workout videos.</li>
              <li>Expanded workout library with goal-specific filters.</li>
              <li>General nutrition articles and healthy recipes.</li>
              <li>Full access to community forums with posting privileges.</li>
              <li>Direct messaging with other members.</li>
              <li>Enhanced progress tracking tools.</li>
            </ul>
            <p>Price: $9.99/month</p>
          </SubscriptionCard>
          <SubscriptionCard>
            <h3>Elite ($19.99/month)</h3>
            <ul>
              <li>Everything in Pro.</li>
              <li>Personalized workout plans tailored to your goals.</li>
              <li>Live fitness classes and one-on-one coaching.</li>
              <li>Advanced nutrition guidance with calorie tracking tools.</li>
              <li>Priority support from the Yoked team.</li>
              <li>Exclusive access to private community challenges.</li>
              <li>Comprehensive progress analytics and visualizations.</li>
            </ul>
            <p>Price: $19.99/month</p>
          </SubscriptionCard>
        </SubscriptionCards>
      </Section>
    </>
  );
};

export default Home;
