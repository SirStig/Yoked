import { createGlobalStyle } from "styled-components";

const GlobalStyles = createGlobalStyle`
  /* Global Animations */
  @keyframes fade-in {
    from {
      opacity: 0;
    }
    to {
      opacity: 1;
    }
  }

  @keyframes slide-up {
    from {
      transform: translateY(20px);
      opacity: 0;
    }
    to {
      transform: translateY(0);
      opacity: 1;
    }
  }

  @keyframes hover-pulse {
    0%, 100% {
      transform: scale(1);
    }
    50% {
      transform: scale(1.05);
    }
  }

  /* Global Reset and Base Styles */
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }

  body {
    background-color: ${({ theme }) => theme.colors.secondary};
    color: ${({ theme }) => theme.colors.textPrimary};
    font-family: ${({ theme }) => theme.font.family};
    font-size: ${({ theme }) => theme.font.size};
    line-height: 1.6;
    animation: fade-in 0.5s ease-in-out;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    overflow-x: hidden;
  }

  a {
    color: ${({ theme }) => theme.colors.link};
    text-decoration: none;
    font-weight: ${({ theme }) => theme.font.weightBold};
    transition: ${({ theme }) => theme.transitions.default};

    &:hover {
      color: ${({ theme }) => theme.colors.linkHover};
    }
  }

  button {
    font-family: ${({ theme }) => theme.font.family};
    background: ${({ theme }) => theme.colors.gradientPrimary};
    color: ${({ theme }) => theme.colors.textPrimary};
    border: none;
    padding: ${({ theme }) => theme.spacing(2)} ${({ theme }) => theme.spacing(3)};
    border-radius: ${({ theme }) => theme.borderRadius};
    cursor: pointer;
    transition: ${({ theme }) => theme.transitions.hoverGlow};
    box-shadow: ${({ theme }) => theme.shadows.light};

    &:hover {
      box-shadow: ${({ theme }) => theme.shadows.glow};
      transform: scale(1.02);
    }

    &:disabled {
      background-color: ${({ theme }) => theme.colors.inputBorder};
      cursor: not-allowed;
    }
  }

  h1, h2, h3 {
    font-family: ${({ theme }) => theme.font.family};
    font-weight: ${({ theme }) => theme.font.weightBold};
    color: ${({ theme }) => theme.colors.textPrimary};
    text-align: center;
    line-height: 1.2;
  }

  h1 {
    font-size: ${({ theme }) => theme.font.headingSize};
    position: relative;

    &::after {
      content: "";
      width: 50%;
      height: 4px;
      background: ${({ theme }) => theme.colors.primary};
      display: block;
      margin: ${({ theme }) => theme.spacing(2)} auto 0;
      border-radius: ${({ theme }) => theme.borderRadius};
    }
  }

  h2 {
    font-size: ${({ theme }) => theme.font.subheadingSize};
    text-transform: uppercase;
    color: ${({ theme }) => theme.colors.accent};
  }

  h3 {
    font-size: 1.5rem;
  }

  p {
    line-height: 1.8;
    font-size: 1.1rem;
    color: ${({ theme }) => theme.colors.textSecondary};
  }

  input, textarea {
    background: ${({ theme }) => theme.colors.inputBackground};
    color: ${({ theme }) => theme.colors.textPrimary};
    border: 1px solid ${({ theme }) => theme.colors.inputBorder};
    padding: ${({ theme }) => theme.spacing(2)};
    border-radius: ${({ theme }) => theme.borderRadius};
    font-size: ${({ theme }) => theme.font.size};
    transition: border-color ${({ theme }) => theme.transitions.default};

    &:focus {
      border-color: ${({ theme }) => theme.colors.primary};
      outline: none;
    }

    &::placeholder {
      color: ${({ theme }) => theme.colors.textSecondary};
    }
  }

  textarea {
    resize: none;
  }

  /* Card Styles */
  .card {
    background: ${({ theme }) => theme.colors.cardBackground};
    box-shadow: ${({ theme }) => theme.shadows.medium};
    border-radius: ${({ theme }) => theme.borderRadius};
    padding: ${({ theme }) => theme.spacing(3)};
    margin-bottom: ${({ theme }) => theme.spacing(4)};
    transition: ${({ theme }) => theme.transitions.hoverGlow};

    &:hover {
      box-shadow: ${({ theme }) => theme.shadows.glow};
      transform: scale(1.05);
    }
  }

  /* Footer */
  footer {
    background: ${({ theme }) => theme.colors.secondary};
    color: ${({ theme }) => theme.colors.textSecondary};
    padding: ${({ theme }) => theme.spacing(4)};
    text-align: center;
    box-shadow: ${({ theme }) => theme.shadows.light};

    a {
      color: ${({ theme }) => theme.colors.link};
      transition: ${({ theme }) => theme.transitions.default};

      &:hover {
        color: ${({ theme }) => theme.colors.linkHover};
      }
    }
  }

  /* Responsive Design */
  @media (max-width: ${({ theme }) => theme.breakpoints.sm}) {
    body {
      font-size: 0.9rem;
    }

    h1 {
      font-size: 2rem;
    }

    h2 {
      font-size: 1.5rem;
    }

    h3 {
      font-size: 1.25rem;
    }
  }

  @media (max-width: ${({ theme }) => theme.breakpoints.xs}) {
    body {
      font-size: 0.8rem;
    }

    h1 {
      font-size: 1.5rem;
    }

    h2 {
      font-size: 1.2rem;
    }

    h3 {
      font-size: 1rem;
    }
  }
`;

export default GlobalStyles;
