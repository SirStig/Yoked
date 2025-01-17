import React from "react";
import styled from "styled-components";
import { Outlet } from "react-router-dom";

const Header = styled.header`
  background-color: ${({ theme }) => theme.colors.accent};
  padding: ${({ theme }) => theme.spacing(2)};
  text-align: center;
  font-size: 1.5em;
`;

const Footer = styled.footer`
  background-color: ${({ theme }) => theme.colors.accent};
  padding: ${({ theme }) => theme.spacing(1)};
  text-align: center;
  font-size: 0.9em;
`;

const MainContent = styled.main`
  padding: ${({ theme }) => theme.spacing(2)};
  min-height: calc(100vh - 160px);
`;

const MainLayout = () => (
    <div>
        <Header>Fitness Foundry</Header>
        <MainContent>
            <Outlet />
        </MainContent>
        <Footer>© 2025 Fitness Foundry. All rights reserved.</Footer>
    </div>
);

export default MainLayout;
