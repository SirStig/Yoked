import React, { useEffect, useContext, useState } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../../contexts/AuthContext";
import styled, { keyframes } from "styled-components";
import { toast } from "react-toastify";
import { createStripePayment, subscribeFreeTier } from "../../api/paymentApi";
import { getAllSubscriptions } from "../../api/subscriptionApi";

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

const OverlayContent = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  max-height: 90vh;
  width: 95%;
  max-width: 1200px;
  padding: 2rem;
  overflow-y: auto;
  text-align: center;

  @media (max-width: 768px) {
    padding: 1.5rem;
    max-height: 85vh;
  }

  @media (max-width: 480px) {
    padding: 1rem;
  }
`;

const Title = styled.h1`
  font-size: 2rem;
  color: ${({ theme }) => theme.colors.textPrimary};
  margin-bottom: 1.5rem;
  animation: ${fadeIn} 0.6s ease-in-out;

  @media (max-width: 768px) {
    font-size: 1.8rem;
  }

  @media (max-width: 480px) {
    font-size: 1.5rem;
  }
`;

const PlansContainer = styled.div`
  display: flex;
  justify-content: center;
  gap: 1rem;
  max-width: 100%;
  flex-wrap: wrap;

  @media (max-width: 768px) {
    gap: 0.5rem;
  }
`;

const PlanCard = styled.div`
  padding: 2rem;
  text-align: center;
  flex: 1 1 calc(33.33% - 1rem);
  max-width: 300px;
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
    font-size: 1.5rem;
    color: ${({ theme }) => theme.colors.primary};

    @media (max-width: 768px) {
      font-size: 1.3rem;
    }

    @media (max-width: 480px) {
      font-size: 1.2rem;
    }
  }

  ul {
    list-style: none;
    padding: 0;
    margin: 1rem 0;

    li {
      font-size: 1rem;
      color: ${({ theme }) => theme.colors.textSecondary};

      @media (max-width: 768px) {
        font-size: 0.9rem;
      }

      @media (max-width: 480px) {
        font-size: 0.8rem;
      }
    }
  }

  p {
    font-size: 1rem;
    color: ${({ theme }) => theme.colors.textSecondary};

    @media (max-width: 768px) {
      font-size: 0.9rem;
    }

    @media (max-width: 480px) {
      font-size: 0.8rem;
    }
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
  transition: background-color 0.3s;

  &:hover {
    background-color: ${({ theme }) => theme.colors.primaryHover};
  }

  &:disabled {
    background-color: ${({ theme }) => theme.colors.disabled};
    cursor: not-allowed;
  }

  @media (max-width: 768px) {
    padding: 0.8rem 1.5rem;
    font-size: 1rem;
  }

  @media (max-width: 480px) {
    padding: 0.7rem 1.2rem;
    font-size: 0.9rem;
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

    if (currentUser.setup_step === "profile_completion") {
      navigate("/dashboard", { state: { overlay: "profileCompletion" } });
    } else if (currentUser.setup_step === "subscription_selection") {
      // Stay on this overlay
    } else if (currentUser.setup_step === "completed") {
      navigate("/dashboard");
    } else {
      navigate("/verify-email");
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
  }, [currentUser, navigate]);

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
      if (selectedPlan.price === 0) {
        await subscribeFreeTier();
        toast.success("You have successfully subscribed to the Free plan.");
        navigate("/dashboard");
      } else {
        const payment = await createStripePayment(selectedPlan.id);

        if (payment.url) {
          sessionStorage.setItem("returnPath", "/dashboard");
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
    <OverlayContent>
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
    </OverlayContent>
  );
};

export default SubscriptionSelection;
