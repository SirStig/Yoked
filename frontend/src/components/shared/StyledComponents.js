import styled, { keyframes } from "styled-components";

// Shared Container
export const Container = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background-color: ${({ theme }) => theme.colors.background};
  color: ${({ theme }) => theme.colors.text};
`;

// Shared Form
export const Form = styled.form`
  display: flex;
  flex-direction: column;
  gap: 20px;
  width: 100%;
  max-width: 400px;
  background: ${({ theme }) => theme.colors.cardBackground};
  padding: 20px;
  border-radius: 10px;
  box-shadow: ${({ theme }) => theme.shadows.card};
`;

// Shared Input
export const Input = styled.input`
  padding: 10px;
  border: 1px solid ${({ theme }) => theme.colors.inputBorder};
  border-radius: 5px;
  background: ${({ theme }) => theme.colors.inputBackground};
  color: ${({ theme }) => theme.colors.inputText};
  font-size: 1rem;
`;

// Shared Button
export const Button = styled.button`
  padding: 15px;
  background: ${({ theme, primary }) =>
    primary ? theme.colors.primary : theme.colors.secondary};
  color: ${({ theme, primary }) =>
    primary ? theme.colors.textPrimary : theme.colors.primary};
  font-size: 1rem;
  font-weight: bold;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background 0.3s ease, transform 0.2s ease;

  &:hover {
    background: ${({ theme }) => theme.colors.primaryHover};
    transform: scale(1.05);
  }

  &:disabled {
    background: ${({ theme }) => theme.colors.disabled};
    cursor: not-allowed;
  }
`;

// Shared Checkbox Container
export const CheckboxContainer = styled.div`
  display: flex;
  align-items: center;
  gap: 10px;
`;

// Dropdown for ProfileCompletion
export const Dropdown = styled.select`
  margin: 10px 0;
  padding: 10px;
  border: 1px solid ${({ theme }) => theme.colors.inputBorder};
  border-radius: 5px;
  background: ${({ theme }) => theme.colors.inputBackground};
  color: ${({ theme }) => theme.colors.inputText};
  font-size: 1rem;
`;

// Keyframes for animations
const fadeIn = keyframes`
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
`;

// Plan Card Container
export const PlanCard = styled.div`
  background: ${({ theme, highlighted }) =>
    highlighted ? theme.colors.primary : theme.colors.cardBackground};
  border-radius: 10px;
  padding: 20px;
  width: 300px;
  text-align: center;
  color: ${({ theme, highlighted }) =>
    highlighted ? theme.colors.textPrimary : theme.colors.textSecondary};
  box-shadow: ${({ theme }) => theme.shadows.card};
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  animation: ${fadeIn} 1s ease-out;

  &:hover {
    transform: scale(1.05);
    box-shadow: ${({ theme }) => theme.shadows.cardHover};
  }
`;

// Plan Title
export const PlanTitle = styled.h2`
  font-size: 1.8rem;
  margin-bottom: 15px;
  color: ${({ theme, highlighted }) =>
    highlighted ? theme.colors.textPrimary : theme.colors.text};
`;

// Plan Price
export const PlanPrice = styled.p`
  font-size: 1.5rem;
  font-weight: bold;
  margin: 20px 0;
  color: ${({ theme }) => theme.colors.textPrimary};
`;

// Plan Features List
export const PlanFeatures = styled.ul`
  list-style: none;
  padding: 0;
  text-align: left;
  font-size: 1rem;
  color: ${({ theme }) => theme.colors.textSecondary};

  li {
    margin: 10px 0;
    display: flex;
    align-items: center;

    &::before {
      content: "✔";
      color: ${({ theme }) => theme.colors.primary};
      margin-right: 10px;
    }
  }
`;

// Error Message
export const ErrorMessage = styled.div`
  color: ${({ theme }) => theme.colors.error};
  margin-top: 10px;
`;
