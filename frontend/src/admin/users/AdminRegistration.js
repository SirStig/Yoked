import React, { useState } from "react";
import styled, { keyframes } from "styled-components";
import { toast } from "react-toastify";
import { useNavigate } from "react-router-dom";
import authProvider from "../authProvider";
import { generateStrongPassword } from "../../utils/helpers";

// Animations
const fadeIn = keyframes`
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
`;

// Styled Components
const PageContainer = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: ${({ theme }) => theme.colors.background};
  padding: 1rem;

  @media (max-width: ${({ theme }) => theme.breakpoints.sm}) {
    flex-direction: column;
    align-items: stretch;
  }
`;

const Column = styled.div`
  flex: 1;
  max-width: 500px;
  background-color: ${({ theme }) => theme.colors.cardBackground};
  padding: 2rem;
  margin: 0 1rem;
  border-radius: ${({ theme }) => theme.borderRadius};
  box-shadow: ${({ theme }) => theme.shadows.medium};
  animation: ${fadeIn} 0.3s ease-out;

  @media (max-width: ${({ theme }) => theme.breakpoints.sm}) {
    margin: 1rem 0;
  }
`;

const Form = styled.form`
  display: flex;
  flex-direction: column;
  gap: 1.5rem;

  input {
    padding: 0.75rem;
    border: 1px solid ${({ theme }) => theme.colors.border};
    border-radius: ${({ theme }) => theme.borderRadius};
    background-color: ${({ theme }) => theme.colors.inputBackground};
    color: ${({ theme }) => theme.colors.textPrimary};
    font-size: 1rem;
    transition: border-color 0.2s ease;

    &:focus {
      border-color: ${({ theme }) => theme.colors.primary};
      outline: none;
    }

    &::placeholder {
      color: ${({ theme }) => theme.colors.textSecondary};
    }
  }

  button {
    padding: 0.75rem;
    background-color: ${({ theme }) => theme.colors.primary};
    color: ${({ theme }) => theme.colors.textOnPrimary};
    border: none;
    border-radius: ${({ theme }) => theme.borderRadius};
    font-size: 1rem;
    cursor: pointer;
    transition: background-color 0.3s ease;

    &:hover {
      background-color: ${({ theme }) => theme.colors.primaryHover};
    }

    &:disabled {
      background-color: ${({ theme }) => theme.colors.disabled};
      cursor: not-allowed;
    }
  }

  .password-section {
    display: flex;
    align-items: center;
    gap: 1rem;

    input {
      flex: 1;
    }

    .generate-button {
      padding: 0.5rem 1rem;
      font-size: 0.9rem;
      background-color: ${({ theme }) => theme.colors.accent};
      color: ${({ theme }) => theme.colors.textOnAccent};
      border-radius: ${({ theme }) => theme.borderRadius};
      border: none;
      cursor: pointer;

      &:hover {
        background-color: ${({ theme }) => theme.colors.accentHover};
      }
    }
  }
`;

const Title = styled.h2`
  text-align: center;
  color: ${({ theme }) => theme.colors.textPrimary};
  margin-bottom: 1rem;
`;

const InfoContainer = styled.div`
  text-align: center;

  h3 {
    color: ${({ theme }) => theme.colors.textPrimary};
    margin-bottom: 1rem;
  }

  button {
    padding: 0.75rem 1.5rem;
    background-color: ${({ theme }) => theme.colors.secondary};
    color: ${({ theme }) => theme.colors.textOnSecondary};
    border: none;
    border-radius: ${({ theme }) => theme.borderRadius};
    font-size: 1rem;
    cursor: pointer;
    transition: background-color 0.3s ease;

    &:hover {
      background-color: ${({ theme }) => theme.colors.secondaryHover};
    }
  }
`;

const AdminRegistration = () => {
  const [formData, setFormData] = useState({
    fullName: "",
    username: "",
    email: "",
    password: "",
    secret_key: "",
  });

  const isFormValid =
    formData.fullName &&
    formData.username &&
    formData.email &&
    formData.password &&
    formData.secret_key;

  const [generatedPassword, setGeneratedPassword] = useState("");
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleGeneratePassword = () => {
    const newPassword = generateStrongPassword();
    if (!validatePassword(newPassword)) {
      toast.error("Generated password does not meet strength requirements.");
      return;
    }
    setGeneratedPassword(newPassword);
    setFormData((prev) => ({ ...prev, password: newPassword }));
    toast.info("Strong password generated!");
  };

  const validatePassword = (password) => {
    const strongPasswordRegex =
      /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{12,}$/;
    return strongPasswordRegex.test(password);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!isFormValid) {
      toast.error("All fields are required.");
      return;
    }

      const payload = {
        username: formData.username,
        full_name: formData.fullName,
        email: formData.email,
        hashed_password: formData.password,
        admin_secret_key: formData.secret_key,
        accepted_terms: true,
        accepted_privacy_policy: true,
      };

    try {
      await authProvider.registerAdmin(payload);
      toast.success("Admin registered successfully!");
      navigate("/admin/login");
    } catch (error) {
      if (error.status === 400 && error.data?.code === "username_exists") {
        toast.error("Username already exists.");
      } else if (error.status === 400 && error.data?.code === "email_exists") {
        toast.error("Email already exists.");
      } else {
        toast.error(error.message || "Registration failed.");
      }
    }
  };

  return (
    <PageContainer>
      <Column>
        <Title>Admin Registration</Title>
        <Form onSubmit={handleSubmit}>
          <input
            type="text"
            name="fullName"
            value={formData.fullName}
            onChange={handleChange}
            placeholder="Full Name"
            required
          />

          <input
            type="text"
            name="username"
            value={formData.username}
            onChange={handleChange}
            placeholder="Username"
            required
          />

          <input
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            placeholder="Email"
            required
          />

          <div className="password-section">
            <input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              placeholder="Password"
              required
            />
            <button type="button" onClick={handleGeneratePassword}>
              Generate
            </button>
          </div>
          {generatedPassword && (
            <p>
              Generated Password: <strong>{generatedPassword}</strong>
            </p>
          )}

          <input
            type="password"
            name="secret_key"
            value={formData.secret_key}
            onChange={handleChange}
            placeholder="Admin Secret Key"
            required
          />

          <button type="submit" disabled={!isFormValid}>
            Register
          </button>
        </Form>
      </Column>
      <Column>
        <InfoContainer>
          <h3>Don't know how you got here?</h3>
          <button onClick={() => navigate("/")}>Return to Home</button>
        </InfoContainer>
      </Column>
    </PageContainer>
  );
};

export default AdminRegistration;
