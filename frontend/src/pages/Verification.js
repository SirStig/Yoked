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
  gap: 1.5rem;
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

const Verification = () => {
  const [status, setStatus] = useState("loading");
  const [cooldown, setCooldown] = useState(0);
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const { currentUser, loadUser, loading } = useContext(AuthContext);

  // Set status based on query string or currentUser
  useEffect(() => {
    const queryStatus = searchParams.get("status");

    if (queryStatus) {
      setStatus(queryStatus);
    } else if (currentUser?.is_verified) {
      setStatus("success");
    } else {
      setStatus("pending");
    }
  }, [searchParams, currentUser]);

  // Polling verification status every 5 seconds
  useEffect(() => {
    const interval = setInterval(async () => {
      if (!loading && currentUser) {
        try {
          await loadUser();
          if (currentUser?.is_verified) {
            setStatus("success");
          }
        } catch (err) {
          console.error("Failed to load user status:", err);
          setStatus("error");
        }
      }
    }, 5000); // Poll every 5 seconds

    return () => clearInterval(interval);
  }, [currentUser, loading, loadUser]);

  const handleNextStep = () => {
    if (status === "success") {
      navigate("/profile-setup");
    } else {
      toast.error("Please verify your email before proceeding.");
    }
  };

  const handleResendEmail = async () => {
    try {
      const response = await fetch("/api/auth/resend-verification", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });

      if (!response.ok) {
        throw new Error("Failed to resend verification email");
      }

      toast.success("Verification email resent! Please check your inbox.");
      setCooldown(30); // Start cooldown
    } catch (error) {
      console.error("Resend email error:", error);
      toast.error("Failed to resend verification email.");
    }
  };

  // Cooldown timer for resend email
  useEffect(() => {
    if (cooldown > 0) {
      const timer = setTimeout(() => setCooldown(cooldown - 1), 1000);
      return () => clearTimeout(timer);
    }
  }, [cooldown]);

  const renderContent = () => {
    if (status === "loading") {
      return <Message>Verifying your email...</Message>;
    }

    if (status === "error") {
      return (
        <>
          <Message>Something Went Wrong</Message>
          <Description>
            There was an issue verifying your email. Please try again or contact support if the issue persists.
          </Description>
          <Button onClick={() => navigate("/")}>Go to Home</Button>
        </>
      );
    }

    return (
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
    );
  };

  return <Container>{renderContent()}</Container>;
};

export default Verification;
