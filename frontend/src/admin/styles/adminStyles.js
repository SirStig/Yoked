import { createGlobalStyle } from "styled-components";

const AdminGlobalStyles = createGlobalStyle`
  /* General Reset */
  *, *::before, *::after {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }

  body {
    margin: 0;
    padding: 0;
    font-family: ${({ theme }) => theme.typography.fontFamily};
    font-size: ${({ theme }) => theme.typography.fontSizeNormal};
    background-color: ${({ theme }) => theme.colors.background};
    color: ${({ theme }) => theme.colors.textPrimary};
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }

  h1, h2, h3, h4, h5, h6 {
    color: ${({ theme }) => theme.colors.textPrimary};
    font-weight: ${({ theme }) => theme.typography.fontWeightBold};
    margin-bottom: ${({ theme }) => theme.spacing.md};
  }

  p {
    color: ${({ theme }) => theme.colors.textSecondary};
    font-size: ${({ theme }) => theme.typography.fontSizeNormal};
    margin-bottom: ${({ theme }) => theme.spacing.sm};
  }

  a {
    color: ${({ theme }) => theme.colors.primary};
    text-decoration: none;

    &:hover {
      color: ${({ theme }) => theme.colors.primaryHover};
    }
  }

  button {
    font-family: ${({ theme }) => theme.typography.fontFamily};
    font-size: ${({ theme }) => theme.typography.fontSizeNormal};
    border: none;
    border-radius: ${({ theme }) => theme.borderRadius};
    cursor: pointer;

    &:disabled {
      background-color: ${({ theme }) => theme.colors.disabled};
      cursor: not-allowed;
    }
  }

  input, textarea {
    font-family: ${({ theme }) => theme.typography.fontFamily};
    font-size: ${({ theme }) => theme.typography.fontSizeNormal};
    padding: ${({ theme }) => theme.spacing.sm};
    border: 1px solid ${({ theme }) => theme.colors.border};
    border-radius: ${({ theme }) => theme.borderRadius};
    background-color: ${({ theme }) => theme.colors.inputBackground};
    color: ${({ theme }) => theme.colors.textPrimary};

    &:focus {
      outline: none;
      border-color: ${({ theme }) => theme.colors.primary};
    }
  }

  /* Sidebar Styles */
  .admin-sidebar {
    background-color: ${({ theme }) => theme.colors.sidebarBackground};
    color: ${({ theme }) => theme.colors.textOnPrimary};
    width: 250px;
    height: 100vh;
    padding: ${({ theme }) => theme.spacing.md};
    position: fixed;
    top: 0;
    left: 0;
    display: flex;
    flex-direction: column;
  }

  .admin-sidebar a {
    color: ${({ theme }) => theme.colors.textOnPrimary};
    margin-bottom: ${({ theme }) => theme.spacing.sm};
    font-size: ${({ theme }) => theme.typography.fontSizeNormal};
  }

  .admin-sidebar a:hover {
    color: ${({ theme }) => theme.colors.primary};
  }

  /* Table Styles */
  .admin-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: ${({ theme }) => theme.spacing.lg};
  }

  .admin-table th, .admin-table td {
    border: 1px solid ${({ theme }) => theme.colors.border};
    padding: ${({ theme }) => theme.spacing.sm};
    text-align: left;
  }

  .admin-table th {
    background-color: ${({ theme }) => theme.colors.cardBackground};
    font-weight: ${({ theme }) => theme.typography.fontWeightBold};
    color: ${({ theme }) => theme.colors.textPrimary};
  }

  .admin-table tr:hover {
    background-color: ${({ theme }) => theme.colors.tableRowHover};
  }

  .admin-table td {
    color: ${({ theme }) => theme.colors.textSecondary};
  }
`;

export default AdminGlobalStyles;
