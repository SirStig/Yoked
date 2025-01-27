import React from "react";
import styled from "styled-components";

const TopBarContainer = styled.div`
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 60px;
  background-color: ${({ theme }) => theme.colors.topBarBackground};
  color: ${({ theme }) => theme.colors.topBarText};
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 1.5rem;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  z-index: 1000;
`;

const Title = styled.h1`
  color: ${({ theme }) => theme.colors.primary};
`;

const UserMenu = styled.div`
  display: flex;
  align-items: center;
  gap: 1rem;

  button {
    background-color: transparent;
    border: none;
    color: ${({ theme }) => theme.colors.topBarText};
    cursor: pointer;
    &:hover {
      text-decoration: underline;
    }
  }
`;

const AdminTopBar = () => {
  return (
    <TopBarContainer>
      <Title>Admin Dashboard</Title>
      <UserMenu>
        <span>Welcome, Admin</span>
        <button>Logout</button>
      </UserMenu>
    </TopBarContainer>
  );
};

export default AdminTopBar;
