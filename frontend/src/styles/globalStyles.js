import { createGlobalStyle } from "styled-components";

const GlobalStyles = createGlobalStyle`
  body {
    margin: 0;
    padding: 0;
    background-color: ${({ theme }) => theme.colors.secondary};
    color: ${({ theme }) => theme.colors.textPrimary};
    font-family: ${({ theme }) => theme.font.family};
    font-size: ${({ theme }) => theme.font.size};
  }

  a {
    color: ${({ theme }) => theme.colors.primary};
    text-decoration: none;
    transition: color 0.3s;

    &:hover {
      color: ${({ theme }) => theme.colors.accent};
    }
  }

  button {
    font-family: ${({ theme }) => theme.font.family};
    background-color: ${({ theme }) => theme.colors.primary};
    color: ${({ theme }) => theme.colors.textPrimary};
    border: none;
    padding: ${({ theme }) => theme.spacing(1)} ${({ theme }) => theme.spacing(2)};
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s;

    &:hover {
      background-color: ${({ theme }) => theme.colors.accent};
    }
  }
`;

export default GlobalStyles;
