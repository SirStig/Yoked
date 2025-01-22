import React, { useState, useRef, useEffect } from "react";
import styled from "styled-components";

const MenuContainer = styled.div`
  position: relative;
  display: inline-block;
`;

const MenuButton = styled.button`
  background: linear-gradient(90deg, ${({ theme }) => theme.colors.accent}, ${({ theme }) => theme.colors.primary});
  color: ${({ theme }) => theme.colors.textPrimary};
  font-size: 1.1rem;
  font-weight: ${({ theme }) => theme.font.weightBold};
  border: none;
  border-radius: ${({ theme }) => theme.borderRadius};
  padding: ${({ theme }) => theme.spacing(1.5)} ${({ theme }) => theme.spacing(3)};
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: ${({ theme }) => theme.spacing(1)};
  transition: all 0.3s ease;

  &::after {
    content: "▼";
    font-size: 0.8rem;
    color: ${({ theme }) => theme.colors.textPrimary};
    margin-left: ${({ theme }) => theme.spacing(1)};
  }

  &:hover {
    background: linear-gradient(90deg, ${({ theme }) => theme.colors.accentHover}, ${({ theme }) => theme.colors.primaryHover});
  }
`;

const DropdownContent = styled.div`
  display: ${({ open }) => (open ? "block" : "none")};
  position: absolute;
  top: 100%;
  right: 0;
  background: ${({ theme }) => theme.colors.cardBackground};
  border-radius: ${({ theme }) => theme.borderRadius};
  box-shadow: ${({ theme }) => theme.shadows.medium};
  width: 100%; /* Match the button width */
  z-index: 1000;
`;

const DropdownMenu = ({ username, handleLogout, navigate }) => {
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const dropdownRef = useRef(null);

  useEffect(() => {
    const handleOutsideClick = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setDropdownOpen(false);
      }
    };

    document.addEventListener("mousedown", handleOutsideClick);
    return () => {
      document.removeEventListener("mousedown", handleOutsideClick);
    };
  }, []);

  return (
    <MenuContainer ref={dropdownRef}>
      <MenuButton onClick={() => setDropdownOpen((prev) => !prev)}>
        {`Let’s Go, ${username}`}
      </MenuButton>
      <DropdownContent open={dropdownOpen}>
        <button onClick={() => navigate("/dashboard")}>Dashboard</button>
        <button onClick={handleLogout}>Logout</button>
      </DropdownContent>
    </MenuContainer>
  );
};

export default DropdownMenu;
