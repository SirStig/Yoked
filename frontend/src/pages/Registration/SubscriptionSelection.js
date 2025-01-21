import React, { useEffect, useContext, useState } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../../contexts/AuthContext";
import styled, { keyframes } from "styled-components";
import { toast } from "react-toastify";
import { createStripePayment, subscribeFreeTier } from "../../api/paymentApi";
import { getAllSubscriptions } from "../../api/subscriptionApi";
import { logoutUser } from "../../api/authApi";

// Styled Components
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
  position: relative;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  padding: 2rem;
  overflow: hidden;
`;

const BackgroundImage = styled.div`
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: url("https://images.pexels.com/photos/1552252/pexels-photo-1552252.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2")
    no-repeat center center/cover;
  z-index: 0;

  &::after {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.6);
    backdrop-filter: blur(8px);
  }
`;

const Header = styled.div`
  position: absolute;
  top: 20px;
  left: 20px;
  display: flex;
  gap: 1rem;
  z-index: 2;

  button {
    background: transparent;
    border: none;
    color: ${({ theme }) => theme.colors.primary};
    font-size: 1.5rem;
    cursor: pointer;

    &:hover {
      color: ${({ theme }) => theme.colors.primaryHover};
    }
  }
`;

const Title = styled.h1`
  font-size: 2.5rem;
  color: ${({ theme }) => theme.colors.textPrimary};
  margin-bottom: 2rem;
  z-index: 2;
  animation: ${fadeIn} 0.6s ease-in-out;
`;

const PlansContainer = styled.div`
  display: flex;
  justify-content: center;
  gap: 2rem;
  z-index: 2;
  max-width: 100%;
  flex-wrap: wrap;
  margin: 0 auto;
  padding: 0 1rem;
`;

const PlanCard = styled.div`
  background: ${({ theme }) => theme.colors.cardBackground};
  padding: 2rem;
  border-radius: ${({ theme }) => theme.borderRadius};
  box-shadow: ${({ theme }) => theme.shadows.medium};
  text-align: center;
  flex: 1 1 calc(33.33% - 2rem);
  max-width: 300px;
  margin: 0 auto;
  position: relative;
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;

  &:hover {
    transform: scale(1.05);
    box-shadow: ${({ theme }) => theme.shadows.large};
  }

  &.selected {
    border: 2px solid ${({ theme }) => theme.colors.primary};
    transform: scale(1.1);
  }

  h3 {
    font-size: 1.8rem;
    color: ${({ theme }) => theme.colors.primary};
  }

  ul {
    list-style: none;
    padding: 0;
    margin: 1rem 0;
    text-align: left;

    li {
      margin-bottom: 0.5rem;
    }
  }

  p {
    font-size: 1.2rem;
    color: ${({ theme }) => theme.colors.textSecondary};
  }
`;

const ContinueButton = styled.button`
  margin-top: 2rem;
  padding: 1rem 2rem;
  background-color: ${({ theme }) => theme.colors.primary};
  color: ${({ theme }) => theme.colors.textPrimary};
  border: none;
  border-radius: ${({ theme }) => theme.borderRadius};
  font-size: 1.2rem;
  font-weight: bold;
  cursor: pointer;
  z-index: 2;
  transition: background-color 0.3s;

  &:hover {
    background-color: ${({ theme }) => theme.colors.primaryHover};
  }

  &:disabled {
    background-color: ${({ theme }) => theme.colors.disabled};
    cursor: not-allowed;
  }
`;

const SubscriptionSelection = () => {
  const { currentUser, loadUser } = useContext(AuthContext);
  const [selectedPlan, setSelectedPlan] = useState(null);
  const [subscriptionTiers, setSubscriptionTiers] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    if (!currentUser) {
      navigate("/login");
      return;
    }

    // Handle redirection based on updated setup steps
    if (currentUser.setup_step === "profile_completion") {
      navigate("/profile-setup");
    } else if (currentUser.setup_step === "subscription_selection") {
      // Allow to stay on the subscription selection page
    } else if (currentUser.setup_step === "completed") {
      navigate("/dashboard");
    } else {
      navigate("/verify_email");
    }
  }, [currentUser, navigate]);

  useEffect(() => {
    const storedPlan = sessionStorage.getItem("selectedPlan");

    if (storedPlan) {
      setSelectedPlan(JSON.parse(storedPlan));
      sessionStorage.removeItem("selectedPlan");
    }

    const fetchTiers = async () => {
      try {
        const tiers = await getAllSubscriptions();
        setSubscriptionTiers(tiers);
      } catch (error) {
        toast.error("Failed to fetch subscription tiers.");
      }
    };

    fetchTiers();
  }, []);

  const handleLogout = async () => {
    try {
      await logoutUser();
      toast.success("Successfully logged out.");
      navigate("/login");
    } catch (error) {
      toast.error(error.message || "Failed to log out.");
    }
  };

  const handleSelectPlan = (plan) => {
    setSelectedPlan(plan);
  };

  const handleContinue = async () => {
    if (!selectedPlan) {
      toast.error("Please select a plan.");
      return;
    }

    setIsLoading(true);

    try {
      if (selectedPlan.price === "0") {
        await subscribeFreeTier();
        toast.success("You have successfully subscribed to the Free plan.");
        navigate("/dashboard");
      } else {
        const payment = await createStripePayment(selectedPlan.id);

        if (payment.url) {
          sessionStorage.setItem("returnPath", "/choose-subscription");
          sessionStorage.setItem("selectedPlan", JSON.stringify(selectedPlan));
          window.location.href = payment.url;
        } else {
          throw new Error("Payment URL not received from the server.");
        }
      }
    } catch (error) {
      toast.error(error.message || "Failed to proceed with the subscription.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Container>
      <BackgroundImage />
      <Header>
        <button onClick={() => navigate("/")}>← Home</button>
        <button onClick={handleLogout}>Logout</button>
      </Header>
      <Title>Choose Your Plan</Title>
      <PlansContainer>
        {subscriptionTiers.map((tier) => (
          <PlanCard
            key={tier.id}
            className={selectedPlan?.id === tier.id ? "selected" : ""}
            onClick={() => handleSelectPlan(tier)}
          >
            <h3>{tier.name}</h3>
            <ul>
              {tier.features.map((feature, index) => (
                <li key={index}>{feature}</li>
              ))}
            </ul>
            <p>
              Price: {tier.price > 0 ? `$${(tier.price / 100).toFixed(2)}/month` : "Free"}
            </p>
          </PlanCard>
        ))}
      </PlansContainer>
      <ContinueButton onClick={handleContinue} disabled={isLoading}>
        {isLoading ? "Processing..." : "Continue to Payment"}
      </ContinueButton>
    </Container>
  );
};

export default SubscriptionSelection;
