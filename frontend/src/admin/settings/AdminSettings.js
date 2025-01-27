import React, { useState } from "react";
import styled from "styled-components";
import { FaEdit, FaSave, FaEye, FaKey, FaDatabase, FaTrashAlt } from "react-icons/fa";

const Container = styled.div`
  padding: 2rem;
  background-color: ${({ theme }) => theme.colors.background};
  color: ${({ theme }) => theme.colors.textPrimary};
`;

const Header = styled.h2`
  margin-bottom: 1.5rem;
  color: ${({ theme }) => theme.colors.primary};
`;

const Section = styled.div`
  margin-bottom: 2rem;
  padding: 1rem;
  border: 1px solid ${({ theme }) => theme.colors.border};
  border-radius: ${({ theme }) => theme.borderRadius};
  background-color: ${({ theme }) => theme.colors.cardBackground};
`;

const SectionHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  color: ${({ theme }) => theme.colors.primary};
`;

const SectionContent = styled.div`
  margin-top: 1rem;
  display: ${({ isOpen }) => (isOpen ? "block" : "none")};
`;

const Input = styled.input`
  margin-bottom: 1rem;
  padding: 0.5rem;
  width: 100%;
  border: 1px solid ${({ theme }) => theme.colors.border};
  border-radius: ${({ theme }) => theme.borderRadius};
`;

const Button = styled.button`
  padding: 0.5rem 1rem;
  margin-right: 1rem;
  color: white;
  background-color: ${({ theme }) => theme.colors.primary};
  border: none;
  border-radius: ${({ theme }) => theme.borderRadius};
  cursor: pointer;

  &:hover {
    background-color: ${({ theme }) => theme.colors.primaryHover};
  }

  &:disabled {
    background-color: ${({ theme }) => theme.colors.disabled};
    cursor: not-allowed;
  }
`;

const Settings = () => {
  const [openSections, setOpenSections] = useState({
    profile: true,
    security: false,
    system: false,
    logs: false,
  });

  const toggleSection = (section) => {
    setOpenSections((prev) => ({ ...prev, [section]: !prev[section] }));
  };

  return (
    <Container>
      <Header>Admin Settings</Header>

      {/* Admin Profile Settings */}
      <Section>
        <SectionHeader onClick={() => toggleSection("profile")}>
          <h3>Profile Settings</h3>
        </SectionHeader>
        <SectionContent isOpen={openSections.profile}>
          <Input type="text" placeholder="Name" />
          <Input type="email" placeholder="Email" />
          <Button>
            <FaSave /> Save Changes
          </Button>
        </SectionContent>
      </Section>

      {/* Security Settings */}
      <Section>
        <SectionHeader onClick={() => toggleSection("security")}>
          <h3>Security Settings</h3>
        </SectionHeader>
        <SectionContent isOpen={openSections.security}>
          <Button>
            <FaKey /> Reset MFA
          </Button>
          <Button>
            <FaEye /> View Sessions
          </Button>
        </SectionContent>
      </Section>

      {/* System Settings */}
      <Section>
        <SectionHeader onClick={() => toggleSection("system")}>
          <h3>System Settings</h3>
        </SectionHeader>
        <SectionContent isOpen={openSections.system}>
          <Input type="text" placeholder="Custom Maintenance Message" />
          <Button>
            <FaSave /> Save
          </Button>
        </SectionContent>
      </Section>

      {/* Logs */}
      <Section>
        <SectionHeader onClick={() => toggleSection("logs")}>
          <h3>Logs & Audit Trail</h3>
        </SectionHeader>
        <SectionContent isOpen={openSections.logs}>
          <Button>
            <FaDatabase /> Export Logs
          </Button>
          <Button>
            <FaTrashAlt /> Clear Logs
          </Button>
        </SectionContent>
      </Section>
    </Container>
  );
};

export default Settings;
