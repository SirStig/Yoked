import React from "react";
import styled from "styled-components";

const HeroSectionContainer = styled.div`
  position: relative;
  height: 100vh;
  width: 100%;
  background: url("/assets/hero-background.png") no-repeat center center/cover;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
  padding: ${({ theme }) => theme.spacing(4)};
  color: ${({ theme }) => theme.colors.textPrimary};

  &::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.6); /* Dark overlay for readability */
    z-index: 1;
  }

  > * {
    z-index: 2; /* Ensure content is above the overlay */
  }

  @media (max-width: ${({ theme }) => theme.breakpoints.sm}) {
    align-items: center;
    text-align: center;
    padding: ${({ theme }) => theme.spacing(2)};
  }
`;

const HeroHeading = styled.h1`
  font-size: 2.8rem;
  font-weight: ${({ theme }) => theme.font.weightBold};
  text-shadow: 2px 2px 10px rgba(0, 0, 0, 0.7);
  margin-bottom: ${({ theme }) => theme.spacing(2)};
  max-width: 600px;

  @media (max-width: ${({ theme }) => theme.breakpoints.sm}) {
    font-size: 2rem;
    max-width: 90%;
    text-align: center;
  }
`;

const HeroContent = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;

  @media (max-width: ${({ theme }) => theme.breakpoints.sm}) {
    align-items: center;
  }
`;

const HeroSubheading = styled.p`
  font-size: 1.1rem;
  font-weight: ${({ theme }) => theme.font.weightRegular};
  line-height: 1.6;
  color: ${({ theme }) => theme.colors.textPrimary};
  margin-bottom: ${({ theme }) => theme.spacing(3)};
  max-width: 500px;
  text-align: left;

  @media (max-width: ${({ theme }) => theme.breakpoints.sm}) {
    font-size: 0.9rem;
    max-width: 90%;
    text-align: center;
  }
`;

const ButtonGroup = styled.div`
  display: flex;
  gap: ${({ theme }) => theme.spacing(3)};

  @media (max-width: ${({ theme }) => theme.breakpoints.sm}) {
    flex-direction: column;
    gap: ${({ theme }) => theme.spacing(2)};
    align-self: center;
  }
`;

const StyledButton = styled.button`
  background: ${({ theme }) => theme.colors.primary};
  color: ${({ theme }) => theme.colors.textButton};
  border: none;
  padding: ${({ theme }) => theme.spacing(2)} ${({ theme }) => theme.spacing(4)};
  border-radius: ${({ theme }) => theme.borderRadius};
  font-size: 1rem;
  font-weight: ${({ theme }) => theme.font.weightMedium};
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;

  &:hover {
    transform: scale(1.05);
    box-shadow: ${({ theme }) => theme.shadows.light};
  }

  &:nth-child(2) {
    background: transparent;
    border: 2px solid ${({ theme }) => theme.colors.primary};
    color: ${({ theme }) => theme.colors.primary};
  }
`;

const HeroSection = () => {
  return (
    <HeroSectionContainer>
      <HeroContent>
        <HeroHeading>Yoked - Renewed Body & Mind</HeroHeading>
        <HeroSubheading>
          Discover a fitness platform designed to help you transform both your body and mind. With Yoked, you’ll gain access to personalized workout plans, expert nutritional guidance, and a supportive community to keep you motivated every step of the way.
        </HeroSubheading>
        <ButtonGroup>
          <StyledButton onClick={() => alert("Get Started")}>Get Started</StyledButton>
          <StyledButton onClick={() => alert("Learn More")}>Learn More</StyledButton>
        </ButtonGroup>
      </HeroContent>
    </HeroSectionContainer>
  );
};

export default HeroSection;