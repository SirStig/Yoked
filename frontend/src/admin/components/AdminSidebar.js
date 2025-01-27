import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import styled from "styled-components";
import {
  FaHome,
  FaUsers,
  FaDollarSign,
  FaClipboardList,
  FaChartBar,
  FaEnvelope,
  FaCommentAlt,
  FaCogs,
} from "react-icons/fa";
import { FiMenu } from "react-icons/fi";

const HEADER_HEIGHT = "60px";

const SidebarContainer = styled.div`
  position: fixed;
  top: ${HEADER_HEIGHT}; /* Adjust for header height */
  left: 0;
  height: calc(100% - ${HEADER_HEIGHT});
  width: ${({ collapsed }) => (collapsed ? "80px" : "250px")};
  background-color: ${({ theme }) => theme.colors.sidebarBackground};
  color: ${({ theme }) => theme.colors.sidebarText};
  display: flex;
  flex-direction: column;
  padding: 0.5rem 0;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
  transition: width 0.3s ease-in-out;
  z-index: 1000;
`;

const Header = styled.div`
  display: flex;
  align-items: center;
  justify-content: ${({ collapsed }) =>
    collapsed ? "center" : "space-between"};
  padding: 1rem;
  border-bottom: 1px solid ${({ theme }) => theme.colors.sidebarBorder};
`;

const ToggleButton = styled.div`
  cursor: pointer;
  color: ${({ theme }) => theme.colors.primary};
  font-size: 1.5rem;
  margin-right: ${({ collapsed }) => (collapsed ? "0" : "1rem")};
`;

const SidebarTitle = styled.h2`
  margin: 0;
  flex-grow: 1;
  text-align: center;
  color: ${({ theme }) => theme.colors.primary};
  font-size: 1.2rem;
  display: ${({ collapsed }) => (collapsed ? "none" : "block")};
`;

const NavItemsContainer = styled.div`
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding-top: 1rem;
`;

const NavItem = styled.div`
  display: flex;
  align-items: center;
  justify-content: ${({ collapsed }) => (collapsed ? "center" : "flex-start")};
  gap: ${({ collapsed }) => (collapsed ? "0" : "1rem")};
  padding: 0.8rem;
  cursor: pointer;
  width: 90%; /* Consistent button width */
  margin: 0 auto; /* Center buttons */
  color: ${({ theme }) => theme.colors.sidebarText};
  transition: all 0.3s;
  border-radius: ${({ theme }) => theme.borderRadius};
  &:hover {
    background-color: ${({ theme }) => theme.colors.primary};
    color: ${({ theme }) => theme.colors.sidebarHoverText};
  }
  span {
    display: ${({ collapsed }) => (collapsed ? "none" : "inline")};
  }
`;

const AdminSidebar = () => {
  const [collapsed, setCollapsed] = useState(false);
  const navigate = useNavigate();

  const handleNavigation = (path) => {
    navigate(`/admin${path}`);
  };

  return (
    <SidebarContainer collapsed={collapsed}>
      <Header collapsed={collapsed}>
        <ToggleButton
          collapsed={collapsed}
          onClick={() => setCollapsed(!collapsed)}
        >
          <FiMenu />
        </ToggleButton>
        <SidebarTitle collapsed={collapsed}>Admin Panel</SidebarTitle>
      </Header>
      <NavItemsContainer>
        <NavItem collapsed={collapsed} onClick={() => handleNavigation("")}>
          <FaHome />
          <span>Dashboard</span>
        </NavItem>
        <NavItem collapsed={collapsed} onClick={() => handleNavigation("/users")}>
          <FaUsers />
          <span>Manage Users</span>
        </NavItem>
        <NavItem
          collapsed={collapsed}
          onClick={() => handleNavigation("/subscriptions")}
        >
          <FaDollarSign />
          <span>Manage Subscriptions</span>
        </NavItem>
        <NavItem
          collapsed={collapsed}
          onClick={() => handleNavigation("/payments")}
        >
          <FaClipboardList />
          <span>Manage Payments</span>
        </NavItem>
        <NavItem collapsed={collapsed} onClick={() => handleNavigation("/reports")}>
          <FaChartBar />
          <span>Reports</span>
        </NavItem>
        <NavItem collapsed={collapsed} onClick={() => handleNavigation("/emails")}>
          <FaEnvelope />
          <span>Emails</span>
        </NavItem>
        <NavItem collapsed={collapsed} onClick={() => handleNavigation("/support")}>
          <FaCommentAlt />
          <span>Support</span>
        </NavItem>
        <NavItem collapsed={collapsed} onClick={() => handleNavigation("/settings")}>
          <FaCogs />
          <span>Settings</span>
        </NavItem>
      </NavItemsContainer>
    </SidebarContainer>
  );
};

export default AdminSidebar;
