import React, { useState } from "react";
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
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
`;

const Modal = styled.div`
  background: ${({ theme }) => theme.colors.cardBackground};
  color: ${({ theme }) => theme.colors.textPrimary};
  padding: 2rem;
  border-radius: ${({ theme }) => theme.borderRadius};
  box-shadow: ${({ theme }) => theme.shadows.medium};
  width: 400px;
  text-align: center;
`;

const Input = styled.input`
  width: 100%;
  padding: 0.8rem;
  margin: 1rem 0;
  font-size: 1rem;
  border: 1px solid ${({ theme }) => theme.colors.border};
  border-radius: ${({ theme }) => theme.borderRadius};
`;

const Button = styled.button`
  padding: 0.8rem 1.5rem;
  font-size: 1rem;
  font-weight: bold;
  color: ${({ theme }) => theme.colors.textPrimary};
  background-color: ${({ theme }) => theme.colors.primary};
  border: none;
  border-radius: ${({ theme }) => theme.borderRadius};
  cursor: pointer;

  &:hover {
    background-color: ${({ theme }) => theme.colors.primaryHover};
  }
`;

const MFAVerify = ({ userId, sessionToken }) => {
    const [totpCode, setTotpCode] = useState("");
    const navigate = useNavigate();

    const handleVerify = async () => {
        try {
            await authProvider.verifyMFA({
                user_id: userId,
                totp_code: totpCode,
                session_token: sessionToken, // Pass the session token here
            });
            toast.success("MFA verified successfully!");
            navigate("/admin/dashboard");
        } catch (error) {
            toast.error(error.message || "MFA verification failed. Please try again.");
        }
    };

    return (
        <Overlay>
            <Modal>
                <h2>Verify Your Identity</h2>
                <p>Enter the code from your authenticator app:</p>
                <Input
                    type="text"
                    placeholder="Enter the code"
                    value={totpCode}
                    onChange={(e) => setTotpCode(e.target.value)}
                />
                <Button onClick={handleVerify} disabled={!totpCode}>
                    Verify
                </Button>
            </Modal>
        </Overlay>
    );
};

export default MFAVerify;

