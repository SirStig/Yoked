import React, { useState } from "react";
import AccountCreation from "./Registration/AccountCreation";
import EmailVerification from "./Registration/EmailVerification";
import ProfileCompletion from "./Registration/ProfileCompletion";
import SubscriptionSelection from "./Registration/SubscriptionSelection";
import styled from "styled-components";

const RegisterContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background: linear-gradient(135deg, #121212, #1f1f1f);
  color: #fff;
`;

const Register = () => {
  const [step, setStep] = useState(1);

  const handleNextStep = () => {
    setStep((prev) => prev + 1);
  };

  return (
    <RegisterContainer>
      {step === 1 && <AccountCreation onNext={handleNextStep} />}
      {step === 2 && <EmailVerification onNext={handleNextStep} />}
      {step === 3 && <ProfileCompletion onNext={handleNextStep} />}
      {step === 4 && <SubscriptionSelection />}
    </RegisterContainer>
  );
};

export default Register;
