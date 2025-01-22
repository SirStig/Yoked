import React from "react";
import styled from "styled-components";

// Styled Components
const CardContainer = styled.div`
  background: ${({ theme }) =>
    `linear-gradient(135deg, #6a5acd, #4a90e2)`}; /* Purple to Blue gradient */
  padding: ${({ theme }) => theme.spacing(5)};
  border-radius: ${({ theme }) => theme.borderRadius};
  text-align: center;
  box-shadow: ${({ theme }) => theme.shadows.medium};
  flex: 1 1 300px;
  position: relative;
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;

  &:hover {
    transform: translateY(-5px);
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

const Title = styled.h3`
  color: #faffc0; /* Soft Yellow */
  margin-bottom: ${({ theme }) => theme.spacing(3)};
  font-size: 1.8rem;
  text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.8);
  z-index: 2;
  position: relative;
`;

const FeaturesList = styled.ul`
  list-style: none;
  padding: 0;
  margin: 0;
  color: ${({ theme }) => theme.colors.textPrimary};
  z-index: 2;
  position: relative;

  li {
    margin-bottom: ${({ theme }) => theme.spacing(2)};
    font-size: 1rem;
    text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.6);
  }
`;

const Price = styled.p`
  margin-top: ${({ theme }) => theme.spacing(3)};
  color: #b0e57c; /* Soft Green for price */
  font-size: 1.2rem;
  font-weight: bold;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.6);
  z-index: 2;
  position: relative;
`;

const SubscriptionCard = ({ title, features, price }) => {
  return (
    <CardContainer>
      <Title>{title}</Title>
      <FeaturesList>
        {features.map((feature, index) => (
          <li key={index}>{feature}</li>
        ))}
      </FeaturesList>
      <Price>{price === 0 ? "Free" : `$${(price / 100).toFixed(2)}/month`}</Price>
    </CardContainer>
  );
};

export default SubscriptionCard;
