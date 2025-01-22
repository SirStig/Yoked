import React from "react";
import styled from "styled-components";

// Button container
const ButtonContainer = styled.button`
  background-color: ${({ theme }) => theme.colors.primary};
  color: ${({ theme }) => theme.colors.textPrimary};
  font-size: ${({ size }) => (size === "small" ? "0.875rem" : size === "large" ? "1.25rem" : "1rem")};
  font-weight: bold;
  padding: ${({ theme, size }) =>
    size === "small"
      ? `${theme.spacing(1)} ${theme.spacing(2)}`
      : size === "large"
      ? `${theme.spacing(3)} ${theme.spacing(6)}`
      : `${theme.spacing(2)} ${theme.spacing(4)}`};
  border: none;
  border-radius: ${({ theme }) => theme.borderRadius};
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: ${({ theme }) => theme.spacing(1)}; /* Space between text and icon */
  transition: ${({ theme }) => theme.transitions.hoverGlow}, transform 0.2s ease;
  box-shadow: ${({ theme }) => theme.shadows.light};

  &:hover {
    background-color: ${({ theme }) => theme.colors.primaryHover};
    box-shadow: ${({ theme }) => theme.shadows.glow};
    transform: translateY(-3px); /* Slight lift effect on hover */
  }

  &:focus {
    outline: 2px solid ${({ theme }) => theme.colors.accent};
    outline-offset: 2px;
  }

  &:disabled {
    background-color: ${({ theme }) => theme.colors.disabled};
    cursor: not-allowed;
    box-shadow: none;
    transform: none;
  }

  @media (max-width: ${({ theme }) => theme.breakpoints.sm}) {
    padding: ${({ theme, size }) =>
      size === "small"
        ? `${theme.spacing(0.5)} ${theme.spacing(1.5)}`
        : size === "large"
        ? `${theme.spacing(2)} ${theme.spacing(4)}`
        : `${theme.spacing(1)} ${theme.spacing(2)}`};
  }
`;

const Button = ({ onClick, text, disabled, size = "medium", icon: Icon }) => {
  return (
    <ButtonContainer onClick={onClick} disabled={disabled} size={size}>
      {Icon && <Icon />}
      {text}
    </ButtonContainer>
  );
};

export default Button;
