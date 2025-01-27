import React, { useEffect, useState } from "react";
import styled from "styled-components";
import { getAllSubscriptions } from "../../api/subscriptionApi";

const SubscriptionsSection = styled.section`
  background: ${({ theme }) => theme.colors.sectionBackground};
  padding: ${({ theme }) => theme.spacing(6)} 0;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
`;

const SubscriptionsTitleContainer = styled.div`
  background: ${({ theme }) => theme.colors.cardBackground};
  width: 100%;
  max-width: 1200px;
  padding: ${({ theme }) => theme.spacing(3)};
  color: ${({ theme }) => theme.colors.textPrimary};
  font-size: 2rem;
  font-weight: ${({ theme }) => theme.font.weightBold};
  margin-bottom: ${({ theme }) => theme.spacing(4)};
  box-shadow: ${({ theme }) => theme.shadows.medium};
  text-align: center;
`;

const SubscriptionsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: ${({ theme }) => theme.spacing(4)};
  justify-content: center;
  width: 100%;
  max-width: 1200px;
  position: relative;

  &::before {
    content: "";
    position: absolute;
    top: 0;
    bottom: 0;
    left: 33.33%;
    width: 1px;
    background: ${({ theme }) => theme.colors.textSecondary};
  }

  &::after {
    content: "";
    position: absolute;
    top: 0;
    bottom: 0;
    left: 66.66%;
    width: 1px;
    background: ${({ theme }) => theme.colors.textSecondary};
  }
`;

const SubscriptionItem = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  min-height: 250px; /* Ensures all items have the same height */
  padding: ${({ theme }) => theme.spacing(4)};
  color: ${({ theme }) => theme.colors.textPrimary};
`;

const SubscriptionTitle = styled.h3`
  font-size: 1.5rem;
  font-weight: ${({ theme }) => theme.font.weightBold};
  margin-bottom: ${({ theme }) => theme.spacing(2)};
  text-align: center;
`;

const FeaturesList = styled.ul`
  list-style: none;
  padding: 0;
  margin: 0;
  font-size: 1rem;
  text-align: left;
  color: ${({ theme }) => theme.colors.textSecondary};

  li {
    margin-bottom: ${({ theme }) => theme.spacing(1)};
  }
`;

const Price = styled.p`
  font-size: 1.5rem;
  font-weight: ${({ theme }) => theme.font.weightBold};
  color: ${({ price, theme }) => (price === 0 ? theme.colors.success : theme.colors.primary)};
  margin-top: auto;
  text-align: center;
`;

const SubscriptionsSectionComponent = () => {
  const [subscriptions, setSubscriptions] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchSubscriptions = async () => {
      try {
        const data = await getAllSubscriptions();
        setSubscriptions(data);
      } catch (err) {
        setError(err.message || "An error occurred while fetching subscriptions.");
      }
    };

    fetchSubscriptions();
  }, []);

  return (
    <SubscriptionsSection>
      <SubscriptionsTitleContainer>Subscriptions</SubscriptionsTitleContainer>
      {error ? (
        <p style={{ color: "red" }}>{error}</p>
      ) : (
        <SubscriptionsGrid>
          {subscriptions.map((sub) => (
            <SubscriptionItem key={sub.id}>
              <SubscriptionTitle>{sub.name}</SubscriptionTitle>
              <FeaturesList>
                {sub.features.map((feature, index) => (
                  <li key={index}>{feature}</li>
                ))}
              </FeaturesList>
              <Price price={sub.price}>{sub.price === 0 ? "Free" : `$${(sub.price / 100).toFixed(2)}/month`}</Price>
            </SubscriptionItem>
          ))}
        </SubscriptionsGrid>
      )}
    </SubscriptionsSection>
  );
};

export default SubscriptionsSectionComponent;
