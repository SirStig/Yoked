import React, { useState } from "react";
import styled from "styled-components";
import { FaDumbbell, FaUtensils, FaVideo, FaChartLine, FaUsers } from "react-icons/fa";

const SectionContainer = styled.section`
  background: ${({ theme }) => theme.colors.sectionBackground};
  padding: ${({ theme }) => theme.spacing(6)} 0;
  text-align: center;
`;

const SectionTitle = styled.h2`
  font-size: 2.5rem;
  font-weight: ${({ theme }) => theme.font.weightBold};
  color: ${({ theme }) => theme.colors.textPrimary};
  margin-bottom: ${({ theme }) => theme.spacing(5)};

  @media (max-width: ${({ theme }) => theme.breakpoints.sm}) {
    font-size: 2rem;
  }
`;

const UnifiedBox = styled.div`
  display: grid;
  grid-template-rows: auto 1fr;
  grid-template-columns: repeat(3, 1fr);
  gap: 0;
  max-width: 1200px;
  margin: 0 auto;
  overflow: hidden;
  box-shadow: ${({ theme }) => theme.shadows.medium};
`;

const IconBox = styled.div`
  grid-column: span 3;
  display: flex;
  justify-content: center;
  background: ${({ theme }) => theme.colors.cardBackground};
`;

const IconButtonContainer = styled.div`
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  background: ${({ isSelected, theme }) =>
    isSelected ? theme.colors.primary : theme.colors.sectionBackground};
  color: ${({ isSelected, theme }) =>
    isSelected ? theme.colors.textPrimary : theme.colors.textSecondary};
  transition: background 0.3s ease, color 0.3s ease;
  padding: ${({ theme }) => theme.spacing(4)};
  width: 100%;
  height: 100%;

  &:hover {
    background: ${({ theme }) => theme.colors.primaryHover};
    color: ${({ theme }) => theme.colors.textPrimary};
  }
`;

const IconLabel = styled.span`
  margin-top: ${({ theme }) => theme.spacing(2)};
  font-size: 1rem;
  font-weight: ${({ theme }) => theme.font.weightMedium};
  text-align: center;
`;

const GradientCard = styled.div`
  background: ${({ gradient }) => gradient};
  padding: ${({ theme }) => theme.spacing(4)};
  color: ${({ theme }) => theme.colors.textPrimary};
  text-align: center;
  font-size: 1rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100%;
`;

const FeaturesSection = () => {
  const featureData = {
    Workouts: [
      {
        title: "Strength Training",
        description:
          "Discover a comprehensive library of strength training programs designed to suit all fitness levels. Learn proper techniques with guided videos, target specific muscle groups, and track your progress to maximize results. Whether you are a beginner or an advanced athlete, our programs are tailored to help you achieve your strength goals.",
      },
      {
        title: "HIIT",
        description:
          "Explore High-Intensity Interval Training (HIIT) workouts that burn calories efficiently and boost endurance. These quick and effective routines are perfect for busy individuals looking to improve cardiovascular health and shed fat fast.",
      },
      {
        title: "Yoga & Flexibility",
        description:
          "Improve your flexibility, balance, and overall well-being with yoga routines crafted by experts. Access guided sessions that help you de-stress, increase mobility, and build a stronger mind-body connection.",
      },
    ],
    Nutrition: [
      {
        title: "Personalized Meal Plans",
        description:
          "Receive meal plans tailored to your dietary preferences, goals, and nutritional needs. Our meal plans include diverse recipes, grocery lists, and calorie/macro breakdowns to keep you on track.",
      },
      {
        title: "Calorie Tracking",
        description:
          "Track your daily caloric intake and macros effortlessly with our intuitive tools. Stay informed about your eating habits and make adjustments to reach your goals more effectively.",
      },
      {
        title: "Healthy Recipes",
        description:
          "Access a curated library of healthy recipes for every meal. Enjoy easy-to-follow instructions, nutritional details, and options for various dietary needs, from vegan to keto.",
      },
    ],
    "Yoked Reels": [
      {
        title: "Create Videos",
        description:
          "Share your fitness journey with the community by creating short, engaging videos. Showcase your progress, tips, and achievements to inspire others.",
      },
      {
        title: "Engage & Discover",
        description:
          "Interact with a vibrant fitness community by liking, commenting, and following other creators. Discover trending reels for motivation and new ideas.",
      },
      {
        title: "Motivation at Your Fingertips",
        description:
          "Stay inspired with a feed tailored to your interests. Explore content that aligns with your fitness goals and learn from others' experiences.",
      },
    ],
    Progress: [
      {
        title: "Weight Tracking",
        description:
          "Monitor your weight changes over time with visual graphs and detailed records. Stay motivated by seeing how far you’ve come on your journey.",
      },
      {
        title: "Photo Comparisons",
        description:
          "Upload photos to visually track your transformation. Create side-by-side comparisons to celebrate milestones and achievements.",
      },
      {
        title: "Goal Achievements",
        description:
          "Set personalized fitness goals and earn badges for reaching them. Stay motivated with gamified achievements and rewards.",
      },
    ],
    Community: [
      {
        title: "Forums & Messaging",
        description:
          "Connect with like-minded fitness enthusiasts through our community forums and messaging features. Share tips, ask questions, and stay accountable.",
      },
      {
        title: "Interactive Engagement",
        description:
          "Engage with posts, reels, and other content by liking, commenting, and sharing. Build meaningful connections with others on similar journeys.",
      },
      {
        title: "Supportive Environment",
        description:
          "Find motivation and encouragement from a community that shares your goals. Be part of a supportive network dedicated to helping everyone succeed.",
      },
    ],
  };

  const [selectedFeature, setSelectedFeature] = useState("Yoked Reels");

  const features = [
    { icon: FaDumbbell, title: "Workouts" },
    { icon: FaUtensils, title: "Nutrition" },
    { icon: FaVideo, title: "Yoked Reels" },
    { icon: FaChartLine, title: "Progress" },
    { icon: FaUsers, title: "Community" },
  ];

  const gradients = [
    "linear-gradient(135deg, #6a5acd, #4a90e2)", // Purple to blue
    "linear-gradient(135deg, #4a4a4a, #606060)", // Dark gray
    "linear-gradient(135deg, #ff4500, #ff7043)", // Orange
  ];

  return (
    <SectionContainer>
      <SectionTitle>Explore Yoked's Features</SectionTitle>
      <UnifiedBox>
        <IconBox>
          {features.map((feature) => (
            <IconButtonContainer
              key={feature.title}
              isSelected={selectedFeature === feature.title}
              onClick={() => setSelectedFeature(feature.title)}
            >
              <feature.icon size={48} />
              <IconLabel>{feature.title}</IconLabel>
            </IconButtonContainer>
          ))}
        </IconBox>
        {featureData[selectedFeature].map((detail, index) => (
          <GradientCard key={index} gradient={gradients[index % gradients.length]}>
            <h3>{detail.title}</h3>
            <p>{detail.description}</p>
          </GradientCard>
        ))}
      </UnifiedBox>
    </SectionContainer>
  );
};

export default FeaturesSection;
