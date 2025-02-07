import React, { useEffect, useState, useContext } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import styled, { css } from "styled-components";
import { toast } from "react-toastify";
import { verifyPayment } from "../api/paymentApi";
import { AuthContext } from "../contexts/AuthContext";

// Styled Components
const Container = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  text-align: center;
  background: ${({ theme }) => theme.colors.background};
`;

const Card = styled.div`
  background: ${({ theme }) => theme.colors.secondary};
  padding: 2rem;
  box-shadow: ${({ theme }) => theme.shadows.medium};
  border-radius: ${({ theme }) => theme.borderRadius.large};
  max-width: 500px;
  width: 90%;
  text-align: center;
`;

const Message = styled.h1`
  font-size: 1.8rem;
  margin-bottom: 1rem;
  ${(props) =>
    props.success
      ? css`
          color: green;
        `
      : css`
          color: red;
        `}
`;

const Button = styled.button`
  padding: 12px 24px;
  background-color: ${({ theme }) => theme.colors.primary};
  color: ${({ theme }) => theme.colors.textPrimary};
  border: none;
  border-radius: ${({ theme }) => theme.borderRadius};
  cursor: pointer;
  margin-top: 20px;
  font-size: 1rem;
  font-weight: bold;
  transition: background-color 0.3s ease-in-out;

  &:hover {
    background-color: ${({ theme }) => theme.colors.primaryHover};
  }
`;

const PaymentSuccess = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [success, setSuccess] = useState(null);
  const [message, setMessage] = useState("Verifying payment...");
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const { loadUser } = useContext(AuthContext);

  useEffect(() => {
    const verifyPaymentSession = async () => {
      const sessionId = searchParams.get("session_id");

      if (!sessionId) {
        setMessage("Invalid session ID. Unable to verify payment.");
        setSuccess(false);
        setIsLoading(false);
        return;
      }

      try {
        console.log(`Verifying payment with session ID: ${sessionId}`);
        const response = await verifyPayment(sessionId);
        setMessage(response.message || "Payment verified successfully!");
        setSuccess(true);

        // Reload user profile after successful verification
        await loadUser(true);
      } catch (error) {
        console.error("Payment verification failed:", error);
        setMessage(error.message || "Payment verification failed. Please try again.");
        setSuccess(false);
      } finally {
        setIsLoading(false);
      }
    };

    verifyPaymentSession();
  }, [searchParams, loadUser]);

  const handleRedirect = () => {
    if (success) {
      navigate("/dashboard");
    } else {
      navigate("/dashboard", { state: { overlay: "subscriptionSelection" } });
    }
  };

  return (
    <Container>
      <Card>
        {isLoading ? (
          <Message>Loading...</Message>
        ) : (
          <>
            <Message success={success}>{message}</Message>
            <Button onClick={handleRedirect}>
              {success ? "Go to Dashboard" : "Retry Subscription"}
            </Button>
          </>
        )}
      </Card>
    </Container>
  );
};

export default PaymentSuccess;
