import React, { useEffect, useContext, useState } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../../contexts/AuthContext";
import styled from "styled-components";
import { toast } from "react-toastify";

// Styled Components
const Container = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  background-color: ${({ theme }) => theme.colors.secondary};
  color: ${({ theme }) => theme.colors.textPrimary};
`;

const Title = styled.h1`
  font-size: 2.5rem;
  margin-bottom: 2rem;
`;

const SubscriptionCard = styled.div`
  background: ${({ theme }) => theme.colors.cardBackground};
  padding: 2rem;
  margin: 1rem;
  border-radius: ${({ theme }) => theme.borderRadius};
  box-shadow: ${({ theme }) => theme.shadows.medium};
  width: 100%;
  max-width: 400px;
  text-align: center;

  h3 {
    font-size: 1.8rem;
    color: ${({ theme }) => theme.colors.primary};
  }

  p {
    margin-top: 1rem;
    font-size: 1.2rem;
  }

  button {
    padding: 1rem;
    background-color: ${({ theme }) => theme.colors.primary};
    color: ${({ theme }) => theme.colors.textPrimary};
    border: none;
    border-radius: ${({ theme }) => theme.borderRadius};
    font-size: 1.1rem;
    font-weight: bold;
    cursor: pointer;
    margin-top: 1rem;

    &:hover {
      background-color: ${({ theme }) => theme.colors.primaryHover};
    }

    &:disabled {
      background-color: ${({ theme }) => theme.colors.disabled};
      cursor: not-allowed;
    }
  }
`;

const SubscriptionSelection = () => {
  const { currentUser, updateSubscription, loading } = useContext(AuthContext);
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    if (loading) return; // Wait for the AuthContext to load user data

    if (!currentUser) {
      navigate("/login"); // Redirect to login if not logged in
      return;
    }

    // Ensure the user has completed previous steps
    if (!currentUser.is_verified) {
      navigate("/verify_email");
    } else if (!currentUser.profile_completed) {
      navigate("/profile_completion");
    }
  }, [currentUser, loading, navigate]);

  const handleSubscription = async (tier) => {
    if (tier === "Free") {
      try {
        setIsLoading(true);
        await updateSubscription({ plan: "free" });
        toast.success("You have selected the Free tier.");
        navigate("/dashboard"); // Redirect to dashboard
      } catch (error) {
        toast.error("Failed to update subscription. Please try again.");
      } finally {
        setIsLoading(false);
      }
    } else {
      // Proceed to payment gateway for paid plans (e.g., Stripe)
      try {
        setIsLoading(true);
        toast.info(`Redirecting to payment for the ${tier} subscription...`);

        // Simulate payment process
        setTimeout(async () => {
          await updateSubscription({ plan: tier.toLowerCase() });
          toast.success(`${tier} subscription successfully activated!`);
          navigate("/dashboard"); // Redirect to dashboard
        }, 2000);
      } catch (error) {
        toast.error("Failed to activate subscription. Please try again.");
      } finally {
        setIsLoading(false);
      }
    }
  };

  return (
    <Container>
      <Title>Select Your Subscription Plan</Title>

      <SubscriptionCard>
        <h3>Free (Basic)</h3>
        <p>Access to basic features with ads and limited content.</p>
        <button
          onClick={() => handleSubscription("Free")}
          disabled={isLoading}
        >
          {isLoading ? "Processing..." : "Select Free"}
        </button>
      </SubscriptionCard>

      <SubscriptionCard>
        <h3>Pro ($9.99/month)</h3>
        <p>Ad-free, access to expanded features, and more workout content.</p>
        <button
          onClick={() => handleSubscription("Pro")}
          disabled={isLoading}
        >
          {isLoading ? "Processing..." : "Select Pro"}
        </button>
      </SubscriptionCard>

      <SubscriptionCard>
        <h3>Elite ($19.99/month)</h3>
        <p>All Pro features plus personalized coaching and exclusive content.</p>
        <button
          onClick={() => handleSubscription("Elite")}
          disabled={isLoading}
        >
          {isLoading ? "Processing..." : "Select Elite"}
        </button>
      </SubscriptionCard>
    </Container>
  );
};

export default SubscriptionSelection;
