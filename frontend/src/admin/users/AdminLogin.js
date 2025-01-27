import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import styled from "styled-components";
import authProvider from "../authProvider";
import MFASetup from "../components/MFASetup";
import MFAVerify from "../components/MFAVerify";



// Styled Components
const Container = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background-color: ${({ theme }) => theme.colors.background};
`;

const Form = styled.form`
  display: flex;
  flex-direction: column;
  width: 300px;
  padding: 2rem;
  background: ${({ theme }) => theme.colors.cardBackground};
  border-radius: ${({ theme }) => theme.borderRadius};
  box-shadow: ${({ theme }) => theme.shadows.medium};
`;

const Input = styled.input`
  margin-bottom: 1rem;
  padding: 0.8rem;
  font-size: 1rem;
  border: 1px solid ${({ theme }) => theme.colors.border};
  border-radius: ${({ theme }) => theme.borderRadius};
  &:focus {
    border-color: ${({ theme }) => theme.colors.primary};
    outline: none;
  }
`;

const Button = styled.button`
  padding: 0.8rem;
  font-size: 1rem;
  font-weight: bold;
  color: ${({ theme }) => theme.colors.textPrimary};
  background-color: ${({ theme }) => theme.colors.primary};
  border: none;
  border-radius: ${({ theme }) => theme.borderRadius};
  cursor: pointer;
  &:hover {
    background-color: ${({ theme }) => theme.colors.primaryHover};
  }
`;

const AdminLogin = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [userId, setUserId] = useState(null);
  const [mfaSetupRequired, setMfaSetupRequired] = useState(false);
  const [mfaRequired, setMfaRequired] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

const [sessionToken, setSessionToken] = useState(null);

  const handleSubmit = async (e) => {
      e.preventDefault();
      setIsLoading(true);

      try {
          const response = await authProvider.login({
              username: email,
              password: password,
          });

          if (response.mfa_required) {
              setUserId(response.user_id);
              setSessionToken(response.session_token);
              setMfaRequired(true);
              toast.info("MFA verification required. Please enter your code.");
          } else if (response.success) {
              toast.success("Login successful!");
              navigate("/admin");
          } else {
              throw new Error(response.message || "Login failed.");
          }
      } catch (error) {
          toast.error(error.message || "An error occurred during login.");
      } finally {
          setIsLoading(false);
      }
  };


  // Conditionally render MFA components
  if (mfaSetupRequired) {
    return <MFASetup userId={userId} />;
  }

  if (mfaRequired) {
    return <MFAVerify userId={userId} sessionToken={sessionToken} />;
  }

  return (
    <Container>
      <Form onSubmit={handleSubmit}>
        <h2>Admin Login</h2>
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
        <Button type="submit" disabled={isLoading}>
          {isLoading ? "Logging in..." : "Login"}
        </Button>
      </Form>
    </Container>
  );
};

export default AdminLogin;
