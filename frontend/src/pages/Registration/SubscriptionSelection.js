import React from "react";
import styled, { keyframes } from "styled-components";

const fadeIn = keyframes`
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
`;

const Container = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background: linear-gradient(135deg, #121212, #1f1f1f);
  color: #fff;
  animation: ${fadeIn} 1s ease-out;
`;

const Title = styled.h1`
  font-size: 2.5rem;
  margin-bottom: 20px;
`;

const Subtitle = styled.p`
  font-size: 1.2rem;
  margin-bottom: 40px;
  color: #bdbdbd;
`;

const PlansContainer = styled.div`
  display: flex;
  justify-content: space-around;
  width: 80%;
  gap: 20px;
`;

const PlanCard = styled.div`
  background: ${(props) => (props.highlighted ? "#ff5722" : "#1e1e1e")};
  border-radius: 10px;
  padding: 20px;
  width: 300px;
  text-align: center;
  color: ${(props) => (props.highlighted ? "#fff" : "#bdbdbd")};
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
  transition: transform 0.3s ease, box-shadow 0.3s ease;

  &:hover {
    transform: scale(1.05);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.5);
  }
`;

const PlanTitle = styled.h2`
  font-size: 1.8rem;
  margin-bottom: 15px;
  color: ${(props) => (props.highlighted ? "#fff" : "#e0e0e0")};
`;

const PlanPrice = styled.p`
  font-size: 1.5rem;
  font-weight: bold;
  margin: 20px 0;
`;

const PlanFeatures = styled.ul`
  list-style: none;
  padding: 0;
  text-align: left;
  font-size: 1rem;
`;

const PlanFeature = styled.li`
  margin: 10px 0;
  &::before {
    content: "✔";
    color: ${(props) => (props.highlighted ? "#fff" : "#ff5722")};
    margin-right: 10px;
  }
`;

const Button = styled.button`
  background: ${(props) => (props.highlighted ? "#fff" : "#ff5722")};
  color: ${(props) => (props.highlighted ? "#ff5722" : "#fff")};
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  font-size: 1rem;
  font-weight: bold;
  margin-top: 20px;
  cursor: pointer;
  transition: background 0.3s ease, color 0.3s ease;

  &:hover {
    background: ${(props) => (props.highlighted ? "#e0e0e0" : "#e64a19")};
  }
`;

const SubscriptionSelection = () => {
  const handleSubscriptionSelection = (plan) => {
    // Add logic to redirect to Stripe checkout or process subscription
    console.log(`Selected Plan: ${plan}`);
  };

  return (
    <Container>
      <Title>Select Your Plan</Title>
      <Subtitle>Choose the plan that best suits your fitness journey</Subtitle>
      <PlansContainer>
        {/* Basic Plan */}
        <PlanCard>
          <PlanTitle>Basic</PlanTitle>
          <PlanPrice>Free</PlanPrice>
          <PlanFeatures>
            <PlanFeature>Limited workouts</PlanFeature>
            <PlanFeature>Basic recipes</PlanFeature>
            <PlanFeature>Community access</PlanFeature>
          </PlanFeatures>
          <Button onClick={() => handleSubscriptionSelection("Basic")}>
            Select Plan
          </Button>
        </PlanCard>

        {/* Essential Plan */}
        <PlanCard highlighted>
          <PlanTitle>Essential</PlanTitle>
          <PlanPrice>$9.99/month</PlanPrice>
          <PlanFeatures>
            <PlanFeature highlighted>Everything in Basic</PlanFeature>
            <PlanFeature highlighted>Personalized meal plans</PlanFeature>
            <PlanFeature highlighted>Advanced progress tracking</PlanFeature>
          </PlanFeatures>
          <Button
            highlighted
            onClick={() => handleSubscriptionSelection("Essential")}
          >
            Select Plan
          </Button>
        </PlanCard>

        {/* Elite Plan */}
        <PlanCard>
          <PlanTitle>Elite</PlanTitle>
          <PlanPrice>$19.99/month</PlanPrice>
          <PlanFeatures>
            <PlanFeature>Everything in Essential</PlanFeature>
            <PlanFeature>Live classes</PlanFeature>
            <PlanFeature>One-on-one coaching</PlanFeature>
          </PlanFeatures>
          <Button onClick={() => handleSubscriptionSelection("Elite")}>
            Select Plan
          </Button>
        </PlanCard>
      </PlansContainer>
    </Container>
  );
};

export default SubscriptionSelection;
