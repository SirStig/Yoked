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

  @keyframes scale-up {
    from {
      transform: scale(0.9);
      opacity: 0;
    }
    to {
      transform: scale(1);
      opacity: 1;
    }
  }

  /* Global Reset and Base Styles */
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }

  body {
    margin: 0;
    padding: 0;
    background-color: ${({ theme }) => theme.colors.secondary}; /* Use dark theme background */
    color: ${({ theme }) => theme.colors.textPrimary};
    font-family: ${({ theme }) => theme.font.family};
    font-size: ${({ theme }) => theme.font.size};
    line-height: 1.6;
    animation: fade-in 0.5s ease-in-out;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }

  a {
    color: ${({ theme }) => theme.colors.primary};
    text-decoration: none;
    transition: color ${({ theme }) => theme.transitions.default};

    &:hover {
      color: ${({ theme }) => theme.colors.accent};
    }
  }

  button {
    font-family: ${({ theme }) => theme.font.family};
    background-color: ${({ theme }) => theme.colors.primary};
    color: ${({ theme }) => theme.colors.textPrimary};
    border: none;
    padding: ${({ theme }) => theme.spacing(2)} ${({ theme }) => theme.spacing(3)};
    border-radius: ${({ theme }) => theme.borderRadius};
    cursor: pointer;
    transition: background-color ${({ theme }) => theme.transitions.default};

    &:hover {
      background-color: ${({ theme }) => theme.colors.primaryHover};
    }

    &:disabled {
      background-color: ${({ theme }) => theme.colors.inputBorder};
      cursor: not-allowed;
    }
  }

  h1, h2, h3 {
    margin: 0;
    padding: 0;
    font-family: ${({ theme }) => theme.font.family};
    font-weight: ${({ theme }) => theme.font.weightBold};
    color: ${({ theme }) => theme.colors.textPrimary};
  }

  h1 {
    font-size: 2.5rem;
  }

  h2 {
    font-size: 2rem;
  }

  h3 {
    font-size: 1.5rem;
  }

  p {
    margin: 0;
    line-height: 1.6;
    font-size: 1rem;
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

  ul {
    list-style: none;
    padding: 0;
  }

  img {
    max-width: 100%;
    height: auto;
    display: block;
  }

  /* Default fallback background for video sections */
  .hero-section {
    background-color: ${({ theme }) => theme.colors.secondary};
    min-height: 100vh;
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
    color: ${({ theme }) => theme.colors.textPrimary};
  }
`;

export default GlobalStyles;
