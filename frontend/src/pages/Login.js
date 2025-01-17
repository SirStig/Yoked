import React, { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../contexts/AuthContext";
import styled from "styled-components";

const LoginContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background-color: ${({ theme }) => theme.colors.background};
  color: ${({ theme }) => theme.colors.text};
`;

const Form = styled.form`
  display: flex;
  flex-direction: column;
  width: 300px;
  background: ${({ theme }) => theme.colors.cardBackground};
  padding: 20px;
  border-radius: 10px;
  box-shadow: ${({ theme }) => theme.shadows.card};
`;

const Input = styled.input`
  margin: 10px 0;
  padding: 10px;
  border: 1px solid ${({ theme }) => theme.colors.inputBorder};
  border-radius: 5px;
  background: ${({ theme }) => theme.colors.inputBackground};
  color: ${({ theme }) => theme.colors.inputText};
`;

const Button = styled.button`
  padding: 10px;
  margin-top: 20px;
  background: ${({ theme }) => theme.colors.primary};
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;

  &:hover {
    background: ${({ theme }) => theme.colors.primaryHover};
  }
`;

const ErrorMessage = styled.div`
  color: ${({ theme }) => theme.colors.error};
  margin-top: 10px;
`;

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const { login } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    try {
      await login(email, password);
      navigate("/profile");
    } catch (err) {
      setError("Invalid email or password");
    }
  };

  return (
    <LoginContainer>
      <h1>Login to Yoked</h1>
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
    </LoginContainer>
  );
}

export default Login;
