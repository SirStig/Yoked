import React, { useState } from "react";
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

const MFAVerify = ({ sessionToken }) => {
  const [totpCode, setTotpCode] = useState("");
  const navigate = useNavigate();

  const handleVerify = async () => {
    try {
      const response = await axios.post("/admin/mfa/verify", {
        token: sessionToken,
        totp_code: totpCode,
      });

      toast.success(response.data.message);
      navigate("/admin/dashboard");
    } catch (error) {
      toast.error(error.response?.data?.detail || "MFA verification failed. Please try again.");
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
        <Button onClick={handleVerify}>Verify</Button>
      </Modal>
    </Overlay>
  );
};

export default MFAVerify;
