import React from "react";
import styled from "styled-components";
import { useNavigate } from "react-router-dom";
import { FaUsers, FaDollarSign, FaClipboardList, FaCogs, FaHome, FaComments } from "react-icons/fa";

// Styled Components
const SidebarContainer = styled.aside`
  width: 250px;
  height: 100vh;
  background-color: ${({ theme }) => theme.colors.cardBackground};
  display: flex;
  flex-direction: column;
  padding: 1rem;
  box-shadow: ${({ theme }) => theme.shadows.medium};
  position: fixed;
  left: 0;
`;

const NavLink = styled.div`
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.8rem 1rem;
  margin-bottom: 1rem;
  border-radius: ${({ theme }) => theme.borderRadius};
  color: ${({ theme }) => theme.colors.textPrimary};
  cursor: pointer;
  transition: background-color 0.3s ease;

  &:hover {
    background-color: ${({ theme }) => theme.colors.primary};
    color: ${({ theme }) => theme.colors.textSecondary};
  }

  svg {
    font-size: 1.5rem;
  }
`;

const SidebarTitle = styled.h2`
  margin-bottom: 2rem;
  color: ${({ theme }) => theme.colors.primary};
  font-size: 1.5rem;
  text-align: center;
`;

// Admin Sidebar Component
const AdminSidebar = () => {
  const navigate = useNavigate();

  return (
    <SidebarContainer>
      <SidebarTitle>Admin Panel</SidebarTitle>
      <NavLink onClick={() => navigate("/admin/dashboard")}>
        <FaHome />
        Dashboard
      </NavLink>
      <NavLink onClick={() => navigate("/admin/users")}>
        <FaUsers />
        Manage Users
      </NavLink>
      <NavLink onClick={() => navigate("/admin/subscriptions")}>
        <FaDollarSign />
        Manage Subscriptions
      </NavLink>
      <NavLink onClick={() => navigate("/admin/content")}>
        <FaClipboardList />
        Manage Content
      </NavLink>
      <NavLink onClick={() => navigate("/admin/payments")}>
        <FaDollarSign />
        Manage Payments
      </NavLink>
      <NavLink onClick={() => navigate("/admin/community")}>
        <FaComments />
        Moderate Community
      </NavLink>
      <NavLink onClick={() => navigate("/admin/settings")}>
        <FaCogs />
        Settings
      </NavLink>
    </SidebarContainer>
  );
};

export default AdminSidebar;
