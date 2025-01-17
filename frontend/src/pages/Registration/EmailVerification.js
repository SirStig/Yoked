import React, { useState } from "react";
import styled from "styled-components";

const Container = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background-color: #121212;
  color: #fff;
`;

const Input = styled.input`
  margin: 10px 0;
  padding: 10px;
  border: 1px solid #333;
  border-radius: 5px;
  background: #1e1e1e;
  color: #fff;
`;

const Button = styled.button`
  margin-top: 20px;
  padding: 10px;
  background: #ff5722;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;

  &:hover {
    background: #e64a19;
  }
`;

const EmailVerification = ({ onNext }) => {
    const [code, setCode] = useState("");

    const handleVerifyEmail = () => {
        // Perform API call to verify email
        onNext();
    };

    return (
        <Container>
            <h2>Verify Your Email</h2>
            <p>Enter the code sent to your email:</p>
            <Input
                type="text"
                placeholder="Verification Code"
                value={code}
                onChange={(e) => setCode(e.target.value)}
                required
            />
            <Button onClick={handleVerifyEmail}>Verify</Button>
        </Container>
    );
};

export default EmailVerification;
