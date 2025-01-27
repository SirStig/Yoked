import React from "react";
import styled from "styled-components";

const CardContainer = styled.div`
  background: ${({ theme }) => theme.colors.cardBackground};
  border-radius: ${({ theme }) => theme.borderRadius};
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: ${({ theme }) => theme.spacing(3)};
  max-width: 150px;
  color: ${({ theme }) => theme.colors.textPrimary};
  transition: transform 0.3s ease;

  &:hover {
    transform: scale(1.05);
  }

  @media (max-width: ${({ theme }) => theme.breakpoints.sm}) {
    max-width: 100%;
  }
`;

const IconWrapper = styled.div`
  background: ${({ theme }) => theme.colors.primary};
  width: 70px;
  height: 70px;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: ${({ theme }) => theme.spacing(2)};

  svg {
    color: #ffffff;
    font-size: 2rem;
  }
`;

const Title = styled.h4`
  font-size: 1.1rem;
  font-weight: ${({ theme }) => theme.font.weightBold};
  margin-bottom: ${({ theme }) => theme.spacing(1)};
  color: ${({ theme }) => theme.colors.textPrimary};
`;

const Description = styled.p`
  font-size: 0.9rem;
  font-weight: ${({ theme }) => theme.font.weightRegular};
  color: ${({ theme }) => theme.colors.textSecondary};
  margin: 0;

  @media (max-width: ${({ theme }) => theme.breakpoints.sm}) {
    font-size: 0.8rem;
  }
`;

const FeatureCard = ({ icon: Icon, title, description }) => {
  return (
    <CardContainer>
      {Icon && (
        <IconWrapper>
          <Icon />
        </IconWrapper>
      )}
      <Title>{title}</Title>
      {description && <Description>{description}</Description>}
    </CardContainer>
  );
};

export default FeatureCard;
