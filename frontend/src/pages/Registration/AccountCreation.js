import React, { useState } from "react";
import styled from "styled-components";
import { toast } from "react-toastify";

const Container = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background-color: #121212;
  color: #fff;
  transition: all 0.3s ease;
`;

const Form = styled.form`
  display: flex;
  flex-direction: column;
  gap: 20px;
  width: 100%;
  max-width: 400px;
  background: #1f1f1f;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
`;

const Input = styled.input`
  padding: 10px;
  border: 1px solid #333;
  border-radius: 5px;
  background: #1e1e1e;
  color: #fff;
  font-size: 1rem;
`;

const Button = styled.button`
  padding: 15px;
  background: #ff5722;
  color: #fff;
  font-size: 1rem;
  font-weight: bold;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background 0.3s ease;

  &:hover {
    background: #e64a19;
  }
`;

const AccountCreation = ({ onNext }) => {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [confirmEmail, setConfirmEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (email !== confirmEmail) {
      toast.error("Emails do not match!");
      return;
    }

    if (password !== confirmPassword) {
      toast.error("Passwords do not match!");
      return;
    }

    try {
      const response = await fetch("http://localhost:8000/api/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, email, password }),
      });

      if (!response.ok) {
        throw new Error("Registration failed");
      }

      toast.success("Account created successfully!");
      onNext(); // Move to the next step (Email Verification)
    } catch (error) {
      toast.error(error.message);
    }
  };

  return (
    <Container>
      <h1>Create Your Account</h1>
      <Form onSubmit={handleSubmit}>
        <Input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
        <Input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <Input
          type="email"
          placeholder="Confirm Email"
          value={confirmEmail}
          onChange={(e) => setConfirmEmail(e.target.value)}
          required
        />
        <Input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <Input
          type="password"
          placeholder="Confirm Password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          required
        />
        <Button type="submit">Create Account</Button>
      </Form>
    </Container>
  );
};

export default AccountCreation;
