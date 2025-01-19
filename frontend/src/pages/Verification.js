import React, { useEffect, useState, useContext } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import styled from "styled-components";
import { AuthContext } from "../contexts/AuthContext";

// Styled Components
const Container = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background-color: ${({ theme }) => theme.colors.secondary};
  color: ${({ theme }) => theme.colors.textPrimary};
  gap: 1.5rem; /* Space between elements */
`;

const Message = styled.h1`
  margin-bottom: 1rem;
  font-size: 2.5rem;
  text-align: center;
`;

const Description = styled.p`
  margin-bottom: 1rem;
  font-size: 1.2rem;
  text-align: center;
  max-width: 600px;
`;

const Button = styled.button`
  padding: 1rem 2rem;
  background-color: ${({ theme }) => theme.colors.primary};
  color: ${({ theme }) => theme.colors.textPrimary};
  border: none;
  border-radius: ${({ theme }) => theme.borderRadius};
  font-size: 1.2rem;
  font-weight: bold;
  cursor: pointer;

  &:hover {
    background-color: ${({ theme }) => theme.colors.primaryHover};
  }

  &:disabled {
    background-color: ${({ theme }) => theme.colors.disabled};
    cursor: not-allowed;
  }
`;

const ResendLink = styled.p`
  color: ${({ theme }) => theme.colors.primary};
  font-size: 1rem;
  text-decoration: underline;
  cursor: pointer;

  &:hover {
    color: ${({ theme }) => theme.colors.primaryHover};
  }
`;

const Loader = styled.div`
  border: 4px solid ${({ theme }) => theme.colors.inputBackground};
  border-top: 4px solid ${({ theme }) => theme.colors.primary};
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;

  @keyframes spin {
    0% {
      transform: rotate(0deg);
    }
    100% {
      transform: rotate(360deg);
    }
  }
`;

const Verification = () => {
  const [status, setStatus] = useState("loading");
  const [cooldown, setCooldown] = useState(0); // Cooldown for resend button
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const { currentUser, loadUser, loading } = useContext(AuthContext);

  useEffect(() => {
    const interval = setInterval(async () => {
      if (!loading && currentUser) {
        await loadUser(); // Refresh user data
        if (currentUser.is_verified) {
          setStatus("success");
          clearInterval(interval); // Stop polling when verified
        }
      }
    }, 2000); // Poll every 2 seconds

    return () => clearInterval(interval);
  }, [currentUser, loading, loadUser]);

  useEffect(() => {
    if (loading) return;

    const queryStatus = searchParams.get("status");
    if (queryStatus) {
      setStatus(queryStatus);
    } else if (currentUser?.is_verified) {
      setStatus("success");
    } else {
      setStatus("pending");
    }
  }, [loading, searchParams, currentUser]);

  const handleNextStep = () => {
    if (status === "success") {
      navigate("/profile_completion");
    } else {
      toast.error("Please verify your email before proceeding.");
    }
  };

  const handleResendEmail = async () => {
    try {
      await fetch("/api/auth/resend-verification", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });
      toast.success("Verification email resent! Please check your inbox.");
      setCooldown(30); // Start cooldown
    } catch {
      toast.error("Failed to resend verification email.");
    }
  };

  return (
    <Container>
      {status === "loading" ? (
        <>
          <Message>Verifying your email...</Message>
          <Loader />
        </>
      ) : (
        <>
          <Message>
            {status === "success"
              ? "Email Verified Successfully!"
              : status === "already_verified"
              ? "Email Already Verified"
              : status === "expired"
              ? "Verification Link Expired"
              : status === "invalid"
              ? "Invalid Verification Link"
              : "Verification Pending"}
          </Message>
          <Description>
            {status === "success"
              ? "Your email has been verified. Let's complete your profile."
              : status === "already_verified"
              ? "Your email has already been verified. Proceed to the next step."
              : status === "expired"
              ? "The verification link has expired. Please request a new one."
              : status === "invalid"
              ? "The verification link is invalid. Please request a new one."
              : "We sent you a verification email. Please check your inbox and click the link to proceed."}
          </Description>
          <Button onClick={handleNextStep} disabled={status !== "success"}>
            Continue
          </Button>
          {(status === "pending" || status === "expired") && (
            <ResendLink onClick={handleResendEmail}>
              {cooldown > 0 ? `Resend email in ${cooldown}s` : "Send another email"}
            </ResendLink>
          )}
        </>
      )}
    </Container>
  );
};

export default Verification;
