import React, { useState, useContext } from "react";
import styled from "styled-components";
import { toast } from "react-toastify";
import { AuthContext } from "../../contexts/AuthContext";
import { useNavigate } from "react-router-dom";
import { updateProfile, getProfile } from "../../api/userApi"; // Import API functions

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
`;

const BackgroundImage = styled.div`
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: url("https://images.pexels.com/photos/669577/pexels-photo-669577.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2") no-repeat center center/cover;
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

const Form = styled.form`
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  background-color: ${({ theme }) => theme.colors.cardBackground};
  padding: 2rem;
  border-radius: ${({ theme }) => theme.borderRadius};
  box-shadow: ${({ theme }) => theme.shadows.medium};
  width: 90%;
  max-width: 600px;
`;

const FieldGroup = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  width: 100%;
`;

const Input = styled.input`
  flex: 1;
  min-width: 150px;
  padding: 1rem;
  border: 1px solid ${({ theme }) => theme.colors.inputBorder};
  border-radius: ${({ theme }) => theme.borderRadius};
  background-color: ${({ theme }) => theme.colors.inputBackground};
  color: ${({ theme }) => theme.colors.textPrimary};
  font-size: 1rem;
`;

const Dropdown = styled.select`
  flex: 1;
  min-width: 150px;
  padding: 1rem;
  border: 1px solid ${({ theme }) => theme.colors.inputBorder};
  border-radius: ${({ theme }) => theme.borderRadius};
  background-color: ${({ theme }) => theme.colors.inputBackground};
  color: ${({ theme }) => theme.colors.textPrimary};
  font-size: 1rem;
`;

const Button = styled.button`
  width: 100%;
  padding: 1rem;
  background-color: ${({ theme }) => theme.colors.primary};
  color: ${({ theme }) => theme.colors.textPrimary};
  border: none;
  border-radius: ${({ theme }) => theme.borderRadius};
  font-size: 1.1rem;
  font-weight: bold;
  cursor: pointer;

  &:hover {
    background-color: ${({ theme }) => theme.colors.primaryHover};
  }
`;

const ProfileCompletion = () => {
  const { loadUser } = useContext(AuthContext);
  const [age, setAge] = useState("");
  const [gender, setGender] = useState("");
  const [fitnessGoal, setFitnessGoal] = useState("");
  const [heightUnit, setHeightUnit] = useState("ft"); // Default to "ft/in"
  const [height, setHeight] = useState({ cm: "", ft: "", in: "" });
  const [weightUnit, setWeightUnit] = useState("lbs"); // Default to "lbs"
  const [weight, setWeight] = useState("");
  const [loading, setLoading] = useState(false); // Loading state
  const navigate = useNavigate();

  const handleProfileCompletion = async (e) => {
    e.preventDefault();

    if (!age || !gender || !fitnessGoal || (!height.cm && !height.ft) || !weight) {
      toast.error("Please complete all fields.");
      return;
    }

    const heightValue =
      heightUnit === "cm"
        ? `${height.cm} cm`
        : `${height.ft} ft ${height.in} in`;

    const weightValue = weightUnit === "kg" ? `${weight} kg` : `${weight} lbs`;

    try {
      setLoading(true); // Start loading

      // Update the profile
      await updateProfile({
        age: parseInt(age, 10),
        gender,
        fitness_goals: fitnessGoal,
        height: heightValue,
        height_unit: heightUnit,
        weight: weightValue,
        weight_unit: weightUnit,
        setup_step: "subscription_selection", // Next step
      });

      toast.success("Profile updated successfully!");

      // Fetch updated profile to determine next step
      const updatedProfile = await getProfile();
      await loadUser(); // Refresh AuthContext with the updated user data

      // Navigate to the next step based on the updated profile's setup_step
      if (updatedProfile.setup_step === "subscription_selection") {
        navigate("/subscription_selection");
      } else if (updatedProfile.setup_step === "completed") {
        navigate("/dashboard");
      } else {
        navigate("/"); // Fallback
      }
    } catch (error) {
      toast.error(error.message || "Failed to complete profile.");
    } finally {
      setLoading(false); // Stop loading
    }
  };

  return (
    <Container>
      <BackgroundImage />
      <h1>Complete Your Profile</h1>
      <Form onSubmit={handleProfileCompletion}>
        <FieldGroup>
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
        </FieldGroup>
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
        <FieldGroup>
          <Dropdown
            value={heightUnit}
            onChange={(e) => setHeightUnit(e.target.value)}
          >
            <option value="ft">Height (ft/in)</option>
            <option value="cm">Height (cm)</option>
          </Dropdown>
          {heightUnit === "cm" ? (
            <Input
              type="number"
              placeholder="Height (cm)"
              value={height.cm}
              onChange={(e) =>
                setHeight((prev) => ({ ...prev, cm: e.target.value, ft: "", in: "" }))
              }
            />
          ) : (
            <>
              <Input
                type="number"
                placeholder="Feet"
                value={height.ft}
                onChange={(e) =>
                  setHeight((prev) => ({ ...prev, ft: e.target.value }))
                }
              />
              <Input
                type="number"
                placeholder="Inches"
                value={height.in}
                onChange={(e) =>
                  setHeight((prev) => ({ ...prev, in: e.target.value }))
                }
              />
            </>
          )}
        </FieldGroup>
        <FieldGroup>
          <Dropdown
            value={weightUnit}
            onChange={(e) => setWeightUnit(e.target.value)}
          >
            <option value="lbs">Weight (lbs)</option>
            <option value="kg">Weight (kg)</option>
          </Dropdown>
          <Input
            type="number"
            placeholder={`Weight (${weightUnit})`}
            value={weight}
            onChange={(e) => setWeight(e.target.value)}
            required
          />
        </FieldGroup>
        <Button type="submit" disabled={loading}>
          {loading ? "Updating..." : "Continue"}
        </Button>
      </Form>
    </Container>
  );
};

export default ProfileCompletion;
