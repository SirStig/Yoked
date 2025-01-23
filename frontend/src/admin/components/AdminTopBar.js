import React from "react";
import styled from "styled-components";
import { useNavigate } from "react-router-dom";
import { FaSignOutAlt } from "react-icons/fa";

// Styled Components
const TopBarContainer = styled.header`
  width: calc(100% - 250px);
  height: 60px;
  background-color: ${({ theme }) => theme.colors.cardBackground};
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 1rem;
  margin-left: 250px;
  box-shadow: ${({ theme }) => theme.shadows.medium};
  position: fixed;
  top: 0;
  z-index: 1000;

  @media (max-width: 768px) {
    width: 100%;
    margin-left: 0;
  }
`;

const Title = styled.h1`
  color: ${({ theme }) => theme.colors.primary};
  font-size: 1.2rem;
`;

const LogoutButton = styled.button`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background-color: ${({ theme }) => theme.colors.primary};
  color: ${({ theme }) => theme.colors.textSecondary};
  border: none;
  padding: 0.5rem 1rem;
  border-radius: ${({ theme }) => theme.borderRadius};
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s ease;

  &:hover {
    background-color: ${({ theme }) => theme.colors.primaryHover};
  }

  svg {
    font-size: 1.2rem;
  }
`;

// Admin Top Bar Component
const AdminTopBar = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("adminToken");
    navigate("/admin/login");
  };

  return (
    <TopBarContainer>
      <Title>Admin Dashboard</Title>
      <LogoutButton onClick={handleLogout}>
        <FaSignOutAlt />
        Logout
      </LogoutButton>
    </TopBarContainer>
  );
};

export default AdminTopBar;
