import React, { useState, useContext } from "react";
import styled, { keyframes } from "styled-components";
import { AuthContext } from "../contexts/AuthContext";
import { toast } from "react-toastify";

// Animation for overlay appearance
const fadeIn = keyframes`
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
`;

// Styled Components
const Container = styled.div`
  padding: 2rem;
  width: 100%;
  max-width: 400px;
  animation: ${fadeIn} 0.3s ease-in-out;
  text-align: center;
`;

const Title = styled.h1`
  font-size: 2rem;
  margin-bottom: 1rem;
  color: ${({ theme }) => theme.colors.textPrimary};
`;

const Form = styled.form`
  display: flex;
  flex-direction: column;
  gap: 1rem;
`;

const Input = styled.input`
  width: 100%;
  padding: 0.8rem;
  border: 1px solid ${({ theme }) => theme.colors.inputBorder};
  border-radius: ${({ theme }) => theme.borderRadius};
  background-color: ${({ theme }) => theme.colors.inputBackground};
  color: ${({ theme }) => theme.colors.textPrimary};
  font-size: 1rem;
`;

const Button = styled.button`
  width: 100%;
  padding: 1rem;
  background-color: ${({ theme }) => theme.colors.primary};
  color: ${({ theme }) => theme.colors.textPrimary};
  border: none;
  border-radius: ${({ theme }) => theme.borderRadius};
  font-size: 1.1rem;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s;

  &:hover {
    background-color: ${({ theme }) => theme.colors.primaryHover};
  }
`;

const LinkText = styled.p`
  margin-top: 1rem;
  font-size: 0.9rem;
  color: ${({ theme }) => theme.colors.textSecondary};
  cursor: pointer;
  text-decoration: underline;

  &:hover {
    color: ${({ theme }) => theme.colors.primaryHover};
  }
`;

const StyledError = styled.p`
  color: ${({ theme }) => theme.colors.error || "red"};
  font-size: 0.9rem;
  margin-top: -0.5rem;
`;


// Function to fetch device details
const getDeviceDetails = async () => {
  try {
    const device_type = /Mobi|Android/i.test(navigator.userAgent) ? "Mobile" : "Desktop";
    const device_os = navigator.platform || "Unknown";
    const browser = navigator.userAgent || "Unknown";

    // Fetch public IP
    const ipResponse = await fetch("https://api.ipify.org?format=json");
    const { ip } = await ipResponse.json();

    // Fetch location based on IP
    const locationResponse = await fetch(`https://ipapi.co/${ip}/json/`);
    const locationData = await locationResponse.json();

    return {
      device_type,
      device_os,
      browser,
      ip_address: ip || "Unknown",
      location: locationData.city ? `${locationData.city}, ${locationData.region}, ${locationData.country_name}` : "Unknown",
    };
  } catch (error) {
    console.error("Error fetching IP/Location:", error);
    return {
      device_type: /Mobi|Android/i.test(navigator.userAgent) ? "Mobile" : "Desktop",
      device_os: navigator.platform || "Unknown",
      browser: navigator.userAgent || "Unknown",
      ip_address: "Unknown",
      location: "Unknown",
    };
  }
};

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const { login } = useContext(AuthContext);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setErrorMessage(""); // Clear previous errors

    try {
      const deviceDetails = await getDeviceDetails();
      await login(email, password, deviceDetails);
      toast.success("Login successful!");
    } catch (error) {
      console.error("Login Error:", error);

      if (error?.message) {
        setErrorMessage(error.message);
      } else {
        setErrorMessage("Login failed. Please try again.");
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleForgotPasswordClick = () => {
    toast.info("Password reset feature coming soon!");
  };

  return (
    <Container>
      <Title>Login</Title>
      <Form onSubmit={handleSubmit}>
        <Input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <Input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        {errorMessage && <StyledError>{errorMessage}</StyledError>}
        <Button type="submit" disabled={isLoading}>
          {isLoading ? "Logging in..." : "Login"}
        </Button>
      </Form>
      <LinkText onClick={handleForgotPasswordClick}>Forgot Password?</LinkText>
      <LinkText onClick={() => toast.info("Register feature coming soon!")}>Don’t have an account? Register here.</LinkText>
    </Container>
  );
};

export default Login;
