import React from "react";
import styled from "styled-components";
import ReactPlayer from "react-player";
import { Button } from "@mui/material"; // We'll use Material UI Button

const HeroSectionContainer = styled.div`
  position: relative;
  height: 100vh;
  width: 100%;
  background-color: ${({ theme }) => theme.colors.secondary};
  overflow: hidden;

  .react-player {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    z-index: -1;
  }

  h1 {
    color: ${({ theme }) => theme.colors.textPrimary};
    font-size: 3rem;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    text-align: center;
    text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.7);
    z-index: 2;
    font-family: ${({ theme }) => theme.font.family};
  }
`;

const HeroSection = () => {
  return (
    <HeroSectionContainer>
      <ReactPlayer
        url="https://videos.pexels.com/video-files/4761426/4761426-uhd_4096_2160_25fps.mp4"
        className="react-player"
        playing
        loop
        muted
      />
      <h1>Renew Your Body and Mind with Yoked</h1>
      <Button
        variant="contained"
        color="primary"
        size="large"
        sx={{
          position: "absolute",
          top: "60%",
          left: "50%",
          transform: "translateX(-50%)",
          zIndex: 2,
          fontSize: "1.2rem",
        }}
        onClick={() => window.scrollTo(0, document.getElementById("subscriptions").offsetTop)} // Scroll to subscriptions section
      >
        Join Now
      </Button>
    </HeroSectionContainer>
  );
};

export default HeroSection;
