import React from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import styled from "styled-components";
import { toast } from "react-toastify";

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
  color: red;
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

const PaymentCancel = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const sessionId = searchParams.get("session_id");

  const handleRetry = () => {
    navigate("/choose-subscription"); // Updated route
  };

  React.useEffect(() => {
    if (!sessionId) {
      toast.error("No session ID found. Unable to log cancellation.");
    } else {
      toast.info("Your payment session was cancelled. You can try again.");
    }
  }, [sessionId]);

  return (
    <Container>
      <Message>Your payment session has been cancelled.</Message>
      <Button onClick={handleRetry}>Choose a Plan</Button>
    </Container>
  );
};

export default PaymentCancel;
