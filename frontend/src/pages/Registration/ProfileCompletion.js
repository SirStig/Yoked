import React, { useState, useContext } from "react";
import styled from "styled-components";
import { toast } from "react-toastify";
import { AuthContext } from "../../contexts/AuthContext";
import { useNavigate } from "react-router-dom";
import { updateProfile } from "../../api/userApi";

// Styled Components
const OverlayContent = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;

  width: 100%;
  max-width: 500px;
  text-align: center;
`;

const Card = styled.div`
  width: 100%;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  text-align: center;
`;

const Input = styled.input`
  width: 100%;
  padding: 1rem;
  border: 1px solid ${({ theme }) => theme.colors.inputBorder};
  border-radius: ${({ theme }) => theme.borderRadius};
  background-color: ${({ theme }) => theme.colors.inputBackground};
  color: ${({ theme }) => theme.colors.textPrimary};
  font-size: 1rem;
`;

const Dropdown = styled.select`
  width: 100%;
  padding: 1rem;
  border: 1px solid ${({ theme }) => theme.colors.inputBorder};
  border-radius: ${({ theme }) => theme.borderRadius};
  background-color: ${({ theme }) => theme.colors.inputBackground};
  color: ${({ theme }) => theme.colors.textPrimary};
  font-size: 1rem;
`;

const ButtonContainer = styled.div`
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 1rem;
`;

const Button = styled.button`
  padding: 0.8rem 1.5rem;
  background-color: ${({ theme }) => theme.colors.primary};
  color: ${({ theme }) => theme.colors.textPrimary};
  border: none;
  border-radius: ${({ theme }) => theme.borderRadius};
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  box-shadow: ${({ theme }) => theme.shadows.light};
  transition: all 0.3s ease-in-out;

  &:hover {
    background-color: ${({ theme }) => theme.colors.primaryHover};
    transform: scale(1.05);
    box-shadow: ${({ theme }) => theme.shadows.medium};
  }

  &:disabled {
    background-color: ${({ theme }) => theme.colors.disabled};
    cursor: not-allowed;
  }
`;

const ProfileCompletion = () => {
  const { logout, loadUser } = useContext(AuthContext);
  const [activeIndex, setActiveIndex] = useState(0);
  const [profileData, setProfileData] = useState({
    age: "",
    gender: "",
    fitness_goals: "",
    height_unit: "ft",
    height: { cm: "", ft: "", in: "" },
    weight_unit: "lbs",
    weight: "",
  });
  const navigate = useNavigate();

  const handleNext = () => {
    setActiveIndex((prev) => Math.min(prev + 1, cards.length - 1));
  };

  const handleBack = () => {
    setActiveIndex((prev) => Math.max(prev - 1, 0));
  };

  const handleLogout = () => {
    logout();
    navigate("/");
  };

  const convertHeightToCm = () => {
    if (profileData.height_unit === "cm") return parseInt(profileData.height.cm, 10);
    const feetInches = profileData.height.ft * 12 + parseInt(profileData.height.in, 10);
    return feetInches * 2.54;
  };

  const convertWeightToKg = () => {
    if (profileData.weight_unit === "kg") return parseFloat(profileData.weight);
    return parseFloat(profileData.weight) * 0.453592;
  };

  const handleSubmit = async () => {
    try {
      const heightValue = convertHeightToCm();
      const weightValue = convertWeightToKg();

      await updateProfile({
        ...profileData,
        height: heightValue,
        weight: weightValue,
        setup_step: "subscription_selection",
      });
      await loadUser();
      toast.success("Profile updated successfully!");
      navigate("/dashboard", { state: { overlay: "subscriptionSelection" } });
    } catch (error) {
      toast.error(error.message || "Failed to update profile.");
    }
  };

  const cards = [
    {
      title: "Tell us about yourself",
      content: (
        <>
          <Input
            type="number"
            placeholder="Age"
            value={profileData.age}
            onChange={(e) => setProfileData((prev) => ({ ...prev, age: e.target.value }))}
          />
          <Dropdown
            value={profileData.gender}
            onChange={(e) => setProfileData((prev) => ({ ...prev, gender: e.target.value }))}
          >
            <option value="">Select Gender</option>
            <option value="male">Male</option>
            <option value="female">Female</option>
            <option value="other">Other</option>
          </Dropdown>
        </>
      ),
    },
    {
      title: "What's your fitness goal?",
      content: (
        <Dropdown
          value={profileData.fitness_goals}
          onChange={(e) =>
            setProfileData((prev) => ({ ...prev, fitness_goals: e.target.value }))
          }
        >
          <option value="">Select Fitness Goal</option>
          <option value="weight_loss">Weight Loss</option>
          <option value="muscle_gain">Muscle Gain</option>
          <option value="general_fitness">General Fitness</option>
        </Dropdown>
      ),
    },
    {
      title: "What's your height?",
      content: (
        <>
          <Dropdown
            value={profileData.height_unit}
            onChange={(e) =>
              setProfileData((prev) => ({ ...prev, height_unit: e.target.value }))
            }
          >
            <option value="ft">Feet/Inches</option>
            <option value="cm">Centimeters</option>
          </Dropdown>
          {profileData.height_unit === "cm" ? (
            <Input
              type="number"
              placeholder="Height (cm)"
              value={profileData.height.cm}
              onChange={(e) =>
                setProfileData((prev) => ({
                  ...prev,
                  height: { cm: e.target.value, ft: "", in: "" },
                }))
              }
            />
          ) : (
            <>
              <Input
                type="number"
                placeholder="Feet"
                value={profileData.height.ft}
                onChange={(e) =>
                  setProfileData((prev) => ({
                    ...prev,
                    height: { ...prev.height, ft: e.target.value },
                  }))
                }
              />
              <Input
                type="number"
                placeholder="Inches"
                value={profileData.height.in}
                onChange={(e) =>
                  setProfileData((prev) => ({
                    ...prev,
                    height: { ...prev.height, in: e.target.value },
                  }))
                }
              />
            </>
          )}
        </>
      ),
    },
    {
      title: "What's your weight?",
      content: (
        <>
          <Dropdown
            value={profileData.weight_unit}
            onChange={(e) =>
              setProfileData((prev) => ({ ...prev, weight_unit: e.target.value }))
            }
          >
            <option value="lbs">Pounds</option>
            <option value="kg">Kilograms</option>
          </Dropdown>
          <Input
            type="number"
            placeholder={`Weight (${profileData.weight_unit})`}
            value={profileData.weight}
            onChange={(e) =>
              setProfileData((prev) => ({ ...prev, weight: e.target.value }))
            }
          />
        </>
      ),
    },
  ];

  return (
    <OverlayContent>
      {cards.map((card, index) =>
        index === activeIndex ? (
          <Card key={index}>
            <h2>{card.title}</h2>
            {card.content}
            <ButtonContainer>
              {index > 0 && <Button onClick={handleBack}>Back</Button>}
              <Button
                onClick={index === cards.length - 1 ? handleSubmit : handleNext}
              >
                {index === cards.length - 1 ? "Finish" : "Continue"}
              </Button>
            </ButtonContainer>
          </Card>
        ) : null
      )}
    </OverlayContent>
  );
};

export default ProfileCompletion;
