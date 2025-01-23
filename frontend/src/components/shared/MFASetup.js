import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import styled from "styled-components";
import axios from "axios";

// Styled Components
const Overlay = styled.div`
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
`;

const Modal = styled.div`
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  width: 400px;
  text-align: center;
`;

const Input = styled.input`
  width: 100%;
  padding: 0.5rem;
  margin: 1rem 0;
  border: 1px solid #ccc;
  border-radius: 4px;
`;

const Button = styled.button`
  padding: 0.5rem 1rem;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;

  &:hover {
    background: #0056b3;
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
        const response = await axios.get(`/admin/mfa/setup?user_id=${userId}`);
        setQrCode(response.data.qr_code_url);
        setManualKey(response.data.manual_key);
      } catch (error) {
        toast.error("Failed to load MFA setup details. Please try again.");
      }
    };

    fetchMFASetup();
  }, [userId]);

  const handleSetup = async () => {
    try {
      const response = await axios.post("/admin/mfa/setup", {
        user_id: userId,
        mfa_secret: manualKey,
        totp_code: totpCode,
      });

      toast.success(response.data.message);
      navigate("/admin/dashboard");
    } catch (error) {
      toast.error(error.response?.data?.detail || "MFA setup failed. Please try again.");
    }
  };

  return (
    <Overlay>
      <Modal>
        <h2>Set Up Multi-Factor Authentication</h2>
        <p>Scan the QR code below with your authenticator app:</p>
        <img src={qrCode} alt="QR Code" />
        <p>Or enter this manual key: <strong>{manualKey}</strong></p>
        <Input
          type="text"
          placeholder="Enter the code from your app"
          value={totpCode}
          onChange={(e) => setTotpCode(e.target.value)}
        />
        <Button onClick={handleSetup}>Verify and Enable MFA</Button>
      </Modal>
    </Overlay>
  );
};

export default MFASetup;
