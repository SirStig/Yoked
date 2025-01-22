import React from "react";
import styled from "styled-components";

// Styled Component for individual feature cards
const CardContainer = styled.div`
  background: ${({ theme }) =>
    `linear-gradient(135deg, #4a90e2, #6a5acd)`}; /* Blue and purple gradient */
  position: relative;
  padding: ${({ theme }) => theme.spacing(4)};
  border-radius: ${({ theme }) => theme.borderRadius};
  box-shadow: ${({ theme }) => theme.shadows.medium};
  flex: 1 1 300px;
  text-align: center;
  margin: ${({ theme }) => theme.spacing(2)};
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;

  &:hover {
    transform: translateY(-8px);
    box-shadow: ${({ theme }) => theme.shadows.glow};
  }

  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.3); /* Semi-transparent overlay */
    z-index: 1;
    pointer-events: none;
  }
`;

const CardTitle = styled.h3`
  color: #faffc0; /* A soft yellow for contrast */
  font-size: 1.8rem;
  margin-bottom: ${({ theme }) => theme.spacing(2)};
  text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.8); /* Add shadow for better readability */
  z-index: 2;
  position: relative;
`;

const CardDescription = styled.p`
  color: ${({ theme }) => theme.colors.textPrimary};
  font-size: 1rem;
  line-height: 1.6;
  z-index: 2;
  position: relative;
`;

const FeatureCard = ({ title, description }) => {
  return (
    <CardContainer>
      <CardTitle>{title}</CardTitle>
      <CardDescription>{description}</CardDescription>
    </CardContainer>
  );
};

export default FeatureCard;
