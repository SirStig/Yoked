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

const Dropdown = styled.select`
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

const ProfileCompletion = ({ onNext }) => {
    const [age, setAge] = useState("");
    const [gender, setGender] = useState("");
    const [fitnessGoal, setFitnessGoal] = useState("");

    const handleProfileCompletion = () => {
        // Perform API call to update profile
        onNext();
    };

    return (
        <Container>
            <h2>Complete Your Profile</h2>
            <Input
                type="number"
                placeholder="Age"
                value={age}
                onChange={(e) => setAge(e.target.value)}
                required
            />
            <Dropdown
                value={gender}
                onChange={(e) => setGender(e.target.value)}
                required
            >
                <option value="">Select Gender</option>
                <option value="male">Male</option>
                <option value="female">Female</option>
                <option value="other">Other</option>
            </Dropdown>
            <Dropdown
                value={fitnessGoal}
                onChange={(e) => setFitnessGoal(e.target.value)}
                required
            >
                <option value="">Select Fitness Goal</option>
                <option value="weight_loss">Weight Loss</option>
                <option value="muscle_gain">Muscle Gain</option>
                <option value="general_fitness">General Fitness</option>
            </Dropdown>
            <Button onClick={handleProfileCompletion}>Continue</Button>
        </Container>
    );
};

export default ProfileCompletion;
