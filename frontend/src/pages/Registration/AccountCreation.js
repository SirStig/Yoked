import React, { useState, useContext } from "react";
import { toast } from "react-toastify";
import styled, { keyframes } from "styled-components";
import { AuthContext } from "../../contexts/AuthContext"; // Context for registration and session
import { useNavigate } from "react-router-dom";

// Animation for loading spinner
const spin = keyframes`
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
`;

// Styled Components
const Container = styled.div`
  position: relative;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;

  .video-background {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    z-index: 0;
  }

  .video-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.6);
    backdrop-filter: blur(8px);
    z-index: 0;
  }
`;

const FormWrapper = styled.div`
  z-index: 1;
  width: 90%;
  max-width: 600px;
  background-color: ${({ theme }) => theme.colors.cardBackground};
  padding: 2rem;
  border-radius: ${({ theme }) => theme.borderRadius};
  box-shadow: ${({ theme }) => theme.shadows.medium};
`;

const Form = styled.form`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;

  @media (max-width: ${({ theme }) => theme.breakpoints.sm}) {
    grid-template-columns: 1fr;
  }
`;

const Input = styled.input`
  width: 100%;
  padding: 1rem;
  border: 1px solid ${({ theme }) => theme.colors.inputBorder};
  border-radius: ${({ theme }) => theme.borderRadius};
  background-color: ${({ theme }) => theme.colors.inputBackground};
  color: ${({ theme }) => theme.colors.textPrimary};
  font-size: 1rem;
`;

const CheckboxContainer = styled.div`
  grid-column: span 2;
  display: flex;
  align-items: center;
  gap: 0.5rem;

  label {
    color: ${({ theme }) => theme.colors.textSecondary};
    font-size: 0.9rem;
  }
`;

const Button = styled.button`
  grid-column: span 2;
  width: 100%;
  padding: 1rem;
  background-color: ${({ theme }) => theme.colors.primary};
  color: ${({ theme }) => theme.colors.textPrimary};
  border: none;
  border-radius: ${({ theme }) => theme.borderRadius};
  font-size: 1.1rem;
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

const BackButton = styled.button`
  position: absolute;
  top: 20px;
  left: 20px;
  padding: 0.5rem;
  background-color: transparent;
  border: none;
  color: ${({ theme }) => theme.colors.primary};
  font-size: 1.5rem;
  cursor: pointer;

  &:hover {
    color: ${({ theme }) => theme.colors.primaryHover};
  }
`;

const LoadingContainer = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  grid-column: span 2;
`;

const Spinner = styled.div`
  border: 4px solid ${({ theme }) => theme.colors.inputBackground};
  border-top: 4px solid ${({ theme }) => theme.colors.primary};
  border-radius: 50%;
  width: 30px;
  height: 30px;
  animation: ${spin} 1s linear infinite;
  margin: 0 auto;
`;

const ErrorMessage = styled.div`
  grid-column: span 2;
  width: 100%;
  padding: 1rem;
  margin-top: 1rem;
  background-color: ${({ theme }) => theme.colors.errorBackground};
  color: ${({ theme }) => theme.colors.errorText};
  border: 1px solid ${({ theme }) => theme.colors.errorBorder};
  border-radius: ${({ theme }) => theme.borderRadius};
  font-size: 0.9rem;
  font-weight: bold;
  text-align: center;
`;

const AccountCreation = () => {
  const { register } = useContext(AuthContext); // Use register from AuthContext
  const [formData, setFormData] = useState({
    username: "",
    full_name: "",
    email: "",
    verify_email: "",
    password: "",
    verify_password: "",
    accepted_terms_and_privacy: false,
  });
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState(""); // To store custom error messages
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === "checkbox" ? checked : value,
    });
  };

  const handleBackClick = () => {
    navigate("/"); // Navigate to the home page when back button is clicked
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (formData.email !== formData.verify_email) {
      setErrorMessage("Emails do not match.");
      return;
    }

    if (formData.password !== formData.verify_password) {
      setErrorMessage("Passwords do not match.");
      return;
    }

    if (!formData.accepted_terms_and_privacy) {
      setErrorMessage("You must accept the Terms and Privacy Policy to register.");
      return;
    }

    setIsLoading(true);
    setErrorMessage("");

    try {
      const { username, full_name, email, password } = formData;

      // Call register from AuthContext
      const userData = await register({
        username,
        full_name,
        email,
        password,
        accepted_terms: true,
        accepted_privacy_policy: true,
      });

      toast.success("Account created! Please verify your email.");

      // Redirect to the next step based on the setup_step
      if (userData.setup_step) {
        navigate(`/${userData.setup_step}`);
      }
    } catch (err) {
      const errorResponse = err.response?.data?.detail || "Registration failed. Please try again.";
      setErrorMessage(errorResponse);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Container>
      <video
        className="video-background"
        autoPlay
        loop
        muted
        src="https://videos.pexels.com/video-files/4761426/4761426-uhd_4096_2160_25fps.mp4"
      />
      <div className="video-overlay"></div>
      <FormWrapper>
        <BackButton onClick={handleBackClick}>←</BackButton>
        <h1>Create Your Account</h1>
        <Form onSubmit={handleSubmit}>
          <Input
            type="text"
            name="full_name"
            placeholder="Full Name"
            value={formData.full_name}
            onChange={handleChange}
            required
          />
          <Input
            type="text"
            name="username"
            placeholder="Username"
            value={formData.username}
            onChange={handleChange}
            required
          />
          <Input
            type="email"
            name="email"
            placeholder="Email"
            value={formData.email}
            onChange={handleChange}
            required
          />
          <Input
            type="email"
            name="verify_email"
            placeholder="Verify Email"
            value={formData.verify_email}
            onChange={handleChange}
            required
          />
          <Input
            type="password"
            name="password"
            placeholder="Password"
            value={formData.password}
            onChange={handleChange}
            required
          />
          <Input
            type="password"
            name="verify_password"
            placeholder="Verify Password"
            value={formData.verify_password}
            onChange={handleChange}
            required
          />
          <CheckboxContainer>
            <input
              type="checkbox"
              name="accepted_terms_and_privacy"
              checked={formData.accepted_terms_and_privacy}
              onChange={handleChange}
              required
            />
            <label>
              I accept the <a href="/terms">Terms and Conditions</a> and{" "}
              <a href="/privacy">Privacy Policy</a>.
            </label>
          </CheckboxContainer>
          <Button type="submit" disabled={isLoading}>
            {isLoading ? "Registering..." : "Register"}
          </Button>
        </Form>
        {errorMessage && <ErrorMessage>{errorMessage}</ErrorMessage>}
      </FormWrapper>
    </Container>
  );
};

export default AccountCreation;
