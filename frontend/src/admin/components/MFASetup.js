import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import styled from "styled-components";
import authProvider from "../authProvider"; // Adjusted path for admin directory

// Styled Components
const Overlay = styled.div`
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
`;

const Modal = styled.div`
  background: ${({ theme }) => theme.colors.cardBackground};
  padding: 2rem;
  border-radius: ${({ theme }) => theme.borderRadius};
  box-shadow: ${({ theme }) => theme.shadows.large};
  width: 400px;
  max-width: 90%;
  text-align: center;
`;

const Input = styled.input`
  width: 100%;
  padding: 0.8rem;
  margin: 1rem 0;
  border: 1px solid ${({ theme }) => theme.colors.border};
  border-radius: ${({ theme }) => theme.borderRadius};
  font-size: 1rem;
  background-color: ${({ theme }) => theme.colors.inputBackground};
  color: ${({ theme }) => theme.colors.textPrimary};

  &:focus {
    border-color: ${({ theme }) => theme.colors.primary};
    outline: none;
  }
`;

const Button = styled.button`
  padding: 0.8rem 1rem;
  background: ${({ theme }) => theme.colors.primary};
  color: ${({ theme }) => theme.colors.textOnPrimary};
  border: none;
  border-radius: ${({ theme }) => theme.borderRadius};
  cursor: pointer;
  font-size: 1rem;
  font-weight: bold;

  &:hover {
    background: ${({ theme }) => theme.colors.primaryHover};
  }

  &:disabled {
    background: ${({ theme }) => theme.colors.disabled};
    cursor: not-allowed;
  }
`;

const MFASetup = ({ userId }) => {
  const [qrCode, setQrCode] = useState("");
  const [manualKey, setManualKey] = useState("");
  const [totpCode, setTotpCode] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const fetchMFASetup = async () => {
      try {
        const response = await authProvider.fetchMFASetup({ user_id: userId });
        setQrCode(response.qr_code);
        setManualKey(response.manual_key);
      } catch (error) {
        toast.error("Failed to load MFA setup details. Please try again.");
      }
    };

    fetchMFASetup();
  }, [userId]);

  const handleSetup = async () => {
    try {
      await authProvider.setupMFA({ user_id: userId, mfa_secret: manualKey, totp_code: totpCode });
      toast.success("MFA setup complete!");
      navigate("/admin/dashboard");
    } catch (error) {
      toast.error(error.message || "MFA setup failed. Please try again.");
    }
  };

  return (
    <Overlay>
      <Modal>
        <h2>Set Up Multi-Factor Authentication</h2>
        {qrCode && <img src={qrCode} alt="QR Code" />}
        <p>Manual Key: <strong>{manualKey}</strong></p>
        <Input
          type="text"
          placeholder="Enter the code from your app"
          value={totpCode}
          onChange={(e) => setTotpCode(e.target.value)}
        />
        <Button onClick={handleSetup} disabled={!totpCode}>
          Verify and Enable MFA
        </Button>
      </Modal>
    </Overlay>
  );
};

export default MFASetup;
