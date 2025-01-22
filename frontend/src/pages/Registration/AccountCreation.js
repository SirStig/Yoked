import React, { useState, useContext } from "react";
import { toast } from "react-toastify";
import styled, { keyframes } from "styled-components";
import { AuthContext } from "../../contexts/AuthContext";
import { useNavigate } from "react-router-dom";

// Animation for loading spinner
const spin = keyframes`
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
`;

// Styled Components
const Container = styled.div`
  position: relative;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;

  .video-background {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    z-index: 0;
  }

  .video-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.6);
    backdrop-filter: blur(8px);
    z-index: 0;
  }
`;

const FormWrapper = styled.div`
  z-index: 1;
  width: 90%;
  max-width: 600px;
  background-color: ${({ theme }) => theme.colors.cardBackground};
  padding: 2rem;
  border-radius: ${({ theme }) => theme.borderRadius};
  box-shadow: ${({ theme }) => theme.shadows.medium};
  position: relative;
`;

const BackButton = styled.button`
  position: absolute;
  top: 20px;
  left: 20px;
  padding: 0.5rem;
  background-color: transparent;
  border: none;
  color: ${({ theme }) => theme.colors.textPrimary};
  font-size: 1.5rem;
  cursor: pointer;

  &:hover {
    color: ${({ theme }) => theme.colors.primaryHover};
  }
`;

const Form = styled.form`
  display: flex;
  flex-direction: column;
  gap: 1rem;
`;

const Row = styled.div`
  display: flex;
  gap: 1rem;

  @media (max-width: ${({ theme }) => theme.breakpoints.sm}) {
    flex-direction: column;
  }
`;

const InputGroup = styled.div`
  flex: 1;
  display: flex;
  flex-direction: column;
`;

const Input = styled.input`
  width: 100%;
  padding: 0.8rem;
  border: 1px solid ${({ error, theme }) => (error ? theme.colors.errorBorder : theme.colors.inputBorder)};
  border-radius: ${({ theme }) => theme.borderRadius};
  background-color: ${({ theme }) => theme.colors.inputBackground};
  color: ${({ theme }) => theme.colors.textPrimary};
  font-size: 1rem;
`;

const ErrorText = styled.span`
  font-size: 0.8rem;
  color: ${({ theme }) => theme.colors.errorText};
  margin-top: 0.2rem;
`;

const PasswordStrengthWrapper = styled.div`
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  width: 100%; /* Ensure the strength bar is the same width as the input fields */
`;

const PasswordStrengthText = styled.div`
  font-size: 0.9rem;
  color: ${({ $strength }) =>
    $strength === "Very Strong" ? "green" :
    $strength === "Strong" ? "#4caf50" :
    $strength === "Medium" ? "#ff9800" :
    $strength === "Weak" ? "#f44336" : "gray"};
`;

const PasswordStrengthBar = styled.div`
  height: 8px;
  background-color: ${({ theme }) => theme.colors.inputBackground};
  border-radius: ${({ theme }) => theme.borderRadius};
  overflow: hidden;

  div {
    height: 100%;
    width: ${({ $percentage }) => `${$percentage}%`};
    background-color: ${({ $percentage }) =>
      $percentage > 80 ? "green" :
      $percentage > 60 ? "#4caf50" :
      $percentage > 40 ? "#ff9800" :
      $percentage > 20 ? "#f44336" : "gray"};
  }
`;

const CheckboxContainer = styled.div`
  display: flex;
  align-items: center;
  gap: 0.5rem;

  label {
    color: ${({ theme }) => theme.colors.textSecondary};
    font-size: 0.9rem;
  }
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

  &:disabled {
    background-color: ${({ theme }) => theme.colors.disabled};
    cursor: not-allowed;
  }
`;

const AccountCreation = () => {
  const { register } = useContext(AuthContext);
  const [formData, setFormData] = useState({
    username: "",
    full_name: "",
    email: "",
    verify_email: "",
    password: "",
    verify_password: "",
    accepted_terms_and_privacy: false,
  });
  const [errors, setErrors] = useState({});
  const [passwordStrength, setPasswordStrength] = useState("");
  const [passwordStrengthPercentage, setPasswordStrengthPercentage] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const calculatePasswordStrength = (password) => {
    if (!password) return { strength: "", percentage: 0 };

    let score = 0;
    if (password.length >= 8) score += 1; // Minimum length of 8
    if (/[A-Z]/.test(password)) score += 1; // Uppercase letter
    if (/[a-z]/.test(password)) score += 1; // Lowercase letter
    if (/[0-9]/.test(password)) score += 1; // Number
    if (/[@$!%*?&#]/.test(password)) score += 1; // Special character

    const percentage = (score / 5) * 100;
    const strength =
      score === 5 ? "Very Strong" :
      score === 4 ? "Strong" :
      score === 3 ? "Medium" :
      score === 2 ? "Weak" : "Very Weak";

    return { strength, percentage };
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));

    if (name === "password" || name === "verify_password") {
      const { strength, percentage } = calculatePasswordStrength(value);
      setPasswordStrength(strength);
      setPasswordStrengthPercentage(percentage);
    }
  };

  const handleBackClick = () => {
    navigate("/"); // Navigate to the home page when back button is clicked
  };

const handleSubmit = async (e) => {
  e.preventDefault();
  const newErrors = {};

  // Validate email and password match
  if (formData.email !== formData.verify_email) newErrors.email = "Emails do not match.";
  if (formData.password !== formData.verify_password) newErrors.password = "Passwords do not match.";
  if (!formData.accepted_terms_and_privacy) newErrors.terms = "You must accept the terms to proceed.";

  setErrors(newErrors);

  // If there are validation errors, stop submission
  if (Object.keys(newErrors).length > 0) return;

  setIsLoading(true);

  try {
    const { username, full_name, email, password } = formData;

    // Call the register function
    await register({ username, full_name, email, password });

    // Success: notify the user and redirect to verification
    toast.success("Account created successfully! Please verify your email.");
    navigate("/verify-email");
  } catch (err) {
    // Handle specific backend errors
    const backendErrors = {};
    if (err?.errors) {
      Object.entries(err.errors).forEach(([field, messages]) => {
        backendErrors[field] = messages.join(" ");
        toast.error(`${field}: ${messages.join(" ")}`);
      });
    } else {
      // General error
      const errorMessage = err?.detail || "Registration failed. Please try again.";
      toast.error(errorMessage);
    }

    // Update local errors state for field-specific error display
    setErrors(backendErrors);
  } finally {
    setIsLoading(false);
  }
};

  return (
    <Container>
      <video
        className="video-background"
        autoPlay
        loop
        muted
        src="https://videos.pexels.com/video-files/4761426/4761426-uhd_4096_2160_25fps.mp4"
      />
      <div className="video-overlay"></div>
      <BackButton onClick={handleBackClick}>←</BackButton>
      <FormWrapper>
        <h1>Create Your Account</h1>
        <Form onSubmit={handleSubmit}>
          <Row>
            <InputGroup>
              <Input
                type="text"
                name="full_name"
                placeholder="Full Name"
                value={formData.full_name}
                onChange={handleChange}
                required
              />
            </InputGroup>
            <InputGroup>
              <Input
                type="text"
                name="username"
                placeholder="Username"
                value={formData.username}
                onChange={handleChange}
                error={errors.username}
                required
              />
              {errors.username && <ErrorText>{errors.username}</ErrorText>}
            </InputGroup>
          </Row>
          <Row>
            <InputGroup>
              <Input
                type="email"
                name="email"
                placeholder="Email"
                value={formData.email}
                onChange={handleChange}
                error={errors.email}
                required
              />
              {errors.email && <ErrorText>{errors.email}</ErrorText>}
            </InputGroup>
            <InputGroup>
              <Input
                type="email"
                name="verify_email"
                placeholder="Verify Email"
                value={formData.verify_email}
                onChange={handleChange}
                required
              />
            </InputGroup>
          </Row>
          <Row>
            <InputGroup>
              <Input
                type="password"
                name="password"
                placeholder="Password"
                value={formData.password}
                onChange={handleChange}
                error={errors.password}
                required
              />
              <PasswordStrengthWrapper>
                <PasswordStrengthText $strength={passwordStrength}>
                  {passwordStrength}
                </PasswordStrengthText>
                <PasswordStrengthBar $percentage={passwordStrengthPercentage}>
                  <div />
                </PasswordStrengthBar>
              </PasswordStrengthWrapper>
            </InputGroup>
            <InputGroup>
              <Input
                type="password"
                name="verify_password"
                placeholder="Verify Password"
                value={formData.verify_password}
                onChange={handleChange}
                required
              />
              {errors.password && <ErrorText>{errors.password}</ErrorText>}
            </InputGroup>
          </Row>
          <CheckboxContainer>
            <input
              type="checkbox"
              name="accepted_terms_and_privacy"
              checked={formData.accepted_terms_and_privacy}
              onChange={(e) => handleChange(e)}
              required
            />
            <label>I accept the Terms and Conditions and Privacy Policy.</label>
          </CheckboxContainer>
          {errors.terms && <ErrorText>{errors.terms}</ErrorText>}
          <Button type="submit" disabled={isLoading}>
            {isLoading ? "Registering..." : "Register"}
          </Button>
        </Form>
      </FormWrapper>
    </Container>
  );
};

export default AccountCreation;
