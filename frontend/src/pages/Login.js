import React, { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../contexts/AuthContext";
import styled from "styled-components";
import { toast } from "react-toastify";

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
  max-width: 400px;
  background-color: ${({ theme }) => theme.colors.cardBackground};
  padding: 2rem;
  border-radius: ${({ theme }) => theme.borderRadius};
  box-shadow: ${({ theme }) => theme.shadows.medium};
  text-align: center;

  h1 {
    margin-bottom: 1rem;
    color: ${({ theme }) => theme.colors.textPrimary};
  }
`;

const Form = styled.form`
  display: flex;
  flex-direction: column;
  gap: 1rem;
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

  &:hover {
    background-color: ${({ theme }) => theme.colors.primaryHover};
  }
`;

const ErrorMessage = styled.p`
  color: ${({ theme }) => theme.colors.error};
  font-size: 0.9rem;
  margin-top: 0.5rem;
`;

const LinkText = styled.p`
  font-size: 0.9rem;
  color: ${({ theme }) => theme.colors.textSecondary};
  margin-top: 1rem;

  a {
    color: ${({ theme }) => theme.colors.primary};
    text-decoration: none;

    &:hover {
      text-decoration: underline;
    }
  }

  button {
    background-color: transparent;
    border: none;
    color: ${({ theme }) => theme.colors.primary};
    font-size: 1rem;
    cursor: pointer;

    &:hover {
      text-decoration: underline;
    }
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

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const { login } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    try {
      const user = await login(email, password);
      toast.success("Login successful!");

      // Navigate based on setup_step
      if (user?.setup_step === "completed") {
        navigate("/dashboard");
      } else {
        navigate(`/${user?.setup_step}`);
      }
    } catch (err) {
      setError(err.message || "Invalid email or password");
      toast.error(err.message || "Login failed. Please try again.");
    }
  };

  const handleBackClick = () => {
    navigate("/"); // Navigate to the home page when back button is clicked
  };

  const handleForgotPasswordClick = () => {
    navigate("/forgot-password"); // Navigate to a password reset page (you can implement later)
  };

  const handleRegisterClick = () => {
    navigate("/register"); // Navigate to the register page
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
        {/* Back Button */}
        <BackButton onClick={handleBackClick}>←</BackButton>

        <h1>Welcome Back!</h1>
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
          <Button type="submit">Login</Button>
        </Form>
        {error && <ErrorMessage>{error}</ErrorMessage>}

        <LinkText>
          <button onClick={handleForgotPasswordClick}>Forgot Password?</button>
        </LinkText>
        <LinkText>
          Don't have an account?{" "}
          <a href="#" onClick={handleRegisterClick}>
            Register
          </a>
        </LinkText>
      </FormWrapper>
    </Container>
  );
};

export default Login;
