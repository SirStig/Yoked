import React, { useEffect, useState } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import styled, { css } from "styled-components";
import { toast } from "react-toastify";
import { verifyPayment } from "../api/paymentApi";

// Styled Components
const Container = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  text-align: center;
`;

const Message = styled.h1`
  font-size: 2rem;
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
  padding: 10px 20px;
  background-color: ${({ theme }) => theme.colors.primary};
  color: ${({ theme }) => theme.colors.textPrimary};
  border: none;
  border-radius: ${({ theme }) => theme.borderRadius};
  cursor: pointer;
  margin-top: 20px;

  &:hover {
    background-color: ${({ theme }) => theme.colors.primaryHover};
  }
`;

const PaymentSuccess = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [success, setSuccess] = useState(null); // Set as `null` to handle initial loading
  const [message, setMessage] = useState("Verifying payment...");
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();

  useEffect(() => {
    const verifyPaymentSession = async () => {
      const sessionId = searchParams.get("session_id");

      if (!sessionId || typeof sessionId !== "string") {
        setMessage("Invalid session ID. Unable to verify payment.");
        setSuccess(false);
        setIsLoading(false);
        return;
      }

      try {
        const response = await verifyPayment(sessionId); // Pass the sessionId directly
        setMessage(response.message || "Payment verified successfully!");
        setSuccess(true);
      } catch (error) {
        setMessage(error.message || "Payment verification failed. Please try again.");
        setSuccess(false);
      } finally {
        setIsLoading(false);
      }
    };

    verifyPaymentSession();
  }, [searchParams]);

  const handleRedirect = () => {
    navigate(success ? "/dashboard" : "/choose-subscription");
  };

  return (
    <Container>
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
    </Container>
  );
};

export default PaymentSuccess;
