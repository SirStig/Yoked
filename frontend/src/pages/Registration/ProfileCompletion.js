import React, { useState, useContext } from "react";
import styled from "styled-components";
import { toast } from "react-toastify";
import { AuthContext } from "../../contexts/AuthContext";
import { useNavigate } from "react-router-dom";
import { updateProfile } from "../../api/userApi";

// Styled Components
const Container = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  width: 100%;
  background-color: ${({ theme }) => theme.colors.secondary};
  color: ${({ theme }) => theme.colors.textPrimary};
  position: relative;
  overflow: hidden;
`;

const BackgroundImage = styled.div`
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: url("https://images.pexels.com/photos/669577/pexels-photo-669577.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2")
    no-repeat center center/cover;
  z-index: 0;

  &::after {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.6);
    backdrop-filter: blur(8px);
  }
`;

const Header = styled.div`
  position: absolute;
  top: 20px;
  left: 20px;
  display: flex;
  gap: 1rem;
  z-index: 2;

  button {
    background: transparent;
    border: none;
    color: ${({ theme }) => theme.colors.primary};
    font-size: 1.5rem;
    cursor: pointer;

    &:hover {
      color: ${({ theme }) => theme.colors.primaryHover};
    }
  }
`;

const CardWrapper = styled.div`
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 70%;
  width: 100%;
  padding: 1rem;
  z-index: 1;
`;

const Card = styled.div`
  position: absolute;
  width: 80%;
  max-width: 500px;
  padding: 2rem;
  border-radius: ${({ theme }) => theme.borderRadius};
  background-color: ${({ theme }) => theme.colors.cardBackground};
  box-shadow: ${({ theme }) => theme.shadows.medium};
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
  text-align: center;
  animation: ${(props) => (props.isEntering ? "fadeIn" : "fadeOut")} 0.5s ease-in-out forwards;

  @keyframes fadeIn {
    from {
      opacity: 0;
      transform: translateX(100%);
    }
    to {
      opacity: 1;
      transform: translateX(0);
    }
  }

  @keyframes fadeOut {
    from {
      opacity: 1;
      transform: translateX(0);
    }
    to {
      opacity: 0;
      transform: translateX(-100%);
    }
  }
`;

const Input = styled.input`
  width: 90%;
  padding: 1rem;
  border: 1px solid ${({ theme }) => theme.colors.inputBorder};
  border-radius: ${({ theme }) => theme.borderRadius};
  background-color: ${({ theme }) => theme.colors.inputBackground};
  color: ${({ theme }) => theme.colors.textPrimary};
  font-size: 1rem;
`;

const Dropdown = styled.select`
  width: 90%;
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

  const handleSubmit = async () => {
    let heightValue;
    let weightValue;

    // Convert height to the appropriate unit (e.g., in cm)
    if (profileData.height_unit === "cm") {
      heightValue = parseInt(profileData.height.cm, 10);
    } else if (profileData.height_unit === "ft") {
      const feetInches = profileData.height.ft * 12 + profileData.height.in;
      heightValue = feetInches * 2.54; // Convert to cm
    }

    // Convert weight to the appropriate unit (e.g., kg)
    if (profileData.weight_unit === "kg") {
      weightValue = parseFloat(profileData.weight);
    } else if (profileData.weight_unit === "lbs") {
      weightValue = parseFloat(profileData.weight) * 0.453592; // Convert to kg
    }

    try {
      // Send numeric values to backend
      await updateProfile({
        ...profileData,
        height: heightValue,
        weight: weightValue,
        setup_step: "subscription-selection",
      });
      await loadUser();
      toast.success("Profile updated successfully!");
      navigate("/choose-subscription");  // Redirect after completion
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
            onChange={(e) =>
              setProfileData((prev) => ({ ...prev, age: e.target.value }))
            }
          />
          <Dropdown
            value={profileData.gender}
            onChange={(e) =>
              setProfileData((prev) => ({ ...prev, gender: e.target.value }))
            }
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
    <Container>
      <BackgroundImage />
      <Header>
        <button onClick={() => navigate("/")}>← Home</button>
        <button onClick={handleLogout}>Logout</button>
      </Header>
      <CardWrapper>
        {cards.map((card, index) =>
          index === activeIndex ? (
            <Card key={index} isEntering>
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
      </CardWrapper>
    </Container>
  );
};

export default ProfileCompletion;
