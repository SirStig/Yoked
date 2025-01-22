import React from "react";
import styled from "styled-components";

// Card container
const CardContainer = styled.div`
  background: ${({ theme }) => theme.colors.gradientSecondary};
  border-radius: ${({ theme }) => theme.borderRadius};
  box-shadow: ${({ theme }) => theme.shadows.medium};
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;

  &:hover {
    transform: translateY(-8px);
    box-shadow: ${({ theme }) => theme.shadows.glow};
    background: ${({ theme }) => theme.colors.gradientPrimary}; /* Slight background change on hover */
  }

  @media (max-width: ${({ theme }) => theme.breakpoints.sm}) {
    margin: ${({ theme }) => theme.spacing(1)};
  }
`;

// Card image section
const CardImage = styled.div`
  width: 100%;
  height: 200px;
  background-image: ${({ image }) => `url(${image})`};
  background-size: cover;
  background-position: center;
  transition: transform 0.4s ease;

  ${CardContainer}:hover & {
    transform: scale(1.1); /* Slight zoom on hover */
  }
`;

// Card content (text)
const CardContent = styled.div`
  padding: ${({ theme }) => theme.spacing(3)};
  color: ${({ theme }) => theme.colors.textPrimary};
  text-align: center;
  animation: ${({ theme }) => theme.animations.fadeIn};

  @media (max-width: ${({ theme }) => theme.breakpoints.sm}) {
    padding: ${({ theme }) => theme.spacing(2)};
  }
`;

const CardTitle = styled.h3`
  font-size: 1.8rem;
  margin-bottom: ${({ theme }) => theme.spacing(2)};
  background: ${({ theme }) => theme.colors.gradientPrimary};
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
`;

const CardDescription = styled.p`
  font-size: 1rem;
  line-height: 1.6;
  color: ${({ theme }) => theme.colors.textSecondary};
`;

const CardButton = styled.button`
  display: flex;
  align-items: center;
  justify-content: center;
  gap: ${({ theme }) => theme.spacing(1)};
  margin-top: ${({ theme }) => theme.spacing(3)};
  padding: ${({ theme }) => theme.spacing(1)} ${({ theme }) => theme.spacing(3)};
  background: ${({ theme }) => theme.colors.gradientPrimary};
  color: ${({ theme }) => theme.colors.textPrimary};
  border: none;
  border-radius: ${({ theme }) => theme.borderRadius};
  cursor: pointer;
  transition: ${({ theme }) => theme.transitions.hoverGlow};
  box-shadow: ${({ theme }) => theme.shadows.light};

  &:hover {
    box-shadow: ${({ theme }) => theme.shadows.glow};
    transform: scale(1.05); /* Slight scale on hover */
    background: ${({ theme }) => theme.colors.primaryHover}; /* Highlight on hover */
  }

  &:disabled {
    background-color: ${({ theme }) => theme.colors.disabled};
    cursor: not-allowed;
    box-shadow: none;
  }
`;

const Card = ({ title, description, image, buttonText, onButtonClick, buttonIcon: ButtonIcon }) => {
  return (
    <CardContainer>
      <CardImage image={image} />
      <CardContent>
        <CardTitle>{title}</CardTitle>
        <CardDescription>{description}</CardDescription>
        {buttonText && (
          <CardButton onClick={onButtonClick}>
            {ButtonIcon && <ButtonIcon />}
            {buttonText}
          </CardButton>
        )}
      </CardContent>
    </CardContainer>
  );
};

export default Card;
