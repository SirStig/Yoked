import React, { useState, useContext } from "react";
import { toast } from "react-toastify";
import styled, {keyframes} from "styled-components";
import { AuthContext } from "../../contexts/AuthContext";

const fadeIn = keyframes`
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
`;

// Styled Components
const OverlayContainer = styled.div`
  padding: 2rem;
  width: 100%;
  max-width: 600px;
  text-align: center;
  animation: ${fadeIn} 0.3s ease-in-out;
`;

const Form = styled.form`
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 1rem;
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
  width: 100%;
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
  width: auto;


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

    a {
      color: ${({ theme }) => theme.colors.primary};
      text-decoration: underline;

      &:hover {
        color: ${({ theme }) => theme.colors.primaryHover};
      }
    }
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

  const calculatePasswordStrength = (password) => {
    if (!password) return { strength: "", percentage: 0 };

    let score = 0;
    if (password.length >= 8) score += 1;
    if (/[A-Z]/.test(password)) score += 1;
    if (/[a-z]/.test(password)) score += 1;
    if (/[0-9]/.test(password)) score += 1;
    if (/[@$!%*?&#]/.test(password)) score += 1;

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

    if (name === "password") {
      const { strength, percentage } = calculatePasswordStrength(value);
      setPasswordStrength(strength);
      setPasswordStrengthPercentage(percentage);
    }
  };

  const getDeviceDetails = async () => {
  try {
    const device_type = /Mobi|Android/i.test(navigator.userAgent) ? "Mobile" : "Desktop";
    const device_os = navigator.platform || "Unknown";
    const browser = navigator.userAgent || "Unknown";

    // Fetch public IP
    const ipResponse = await fetch("https://api.ipify.org?format=json");
    const { ip } = await ipResponse.json();

    // Fetch location based on IP
    const locationResponse = await fetch(`https://ipapi.co/${ip}/json/`);
    const locationData = await locationResponse.json();

    return {
      device_type,
      device_os,
      browser,
      ip_address: ip || "Unknown",
      location: locationData.city ? `${locationData.city}, ${locationData.region}, ${locationData.country_name}` : "Unknown",
    };
  } catch (error) {
    console.error("Error fetching IP/Location:", error);
    return {
      device_type: /Mobi|Android/i.test(navigator.userAgent) ? "Mobile" : "Desktop",
      device_os: navigator.platform || "Unknown",
      browser: navigator.userAgent || "Unknown",
      ip_address: "Unknown",
      location: "Unknown",
    };
  }
};


 const handleSubmit = async (e) => {
  e.preventDefault();
  const newErrors = {};

  if (formData.email !== formData.verify_email) newErrors.email = "Emails do not match.";
  if (formData.password !== formData.verify_password) newErrors.password = "Passwords do not match.";
  if (!formData.accepted_terms_and_privacy) newErrors.terms = "You must accept the terms to proceed.";

  setErrors(newErrors);

  if (Object.keys(newErrors).length > 0) return;

  setIsLoading(true);

  try {
    const deviceDetails = await getDeviceDetails();

    await register({
      username: formData.username,
      full_name: formData.full_name,
      email: formData.email,
      hashed_password: formData.password,
      accepted_terms: true,
      accepted_privacy_policy: true,
      ...deviceDetails, // Send device details
    });

    toast.success("Account created successfully! Please verify your email.");
  } catch (error) {
    toast.error(error.message || "Registration failed. Please try again.");
  } finally {
    setIsLoading(false);
  }
};


  return (
    <OverlayContainer>
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
            <PasswordStrengthWrapper>
              <PasswordStrengthText $strength={passwordStrength}>
                {passwordStrength}
              </PasswordStrengthText>
              <PasswordStrengthBar $percentage={passwordStrengthPercentage}>
                <div />
              </PasswordStrengthBar>
            </PasswordStrengthWrapper>
        <CheckboxContainer>
          <input
            type="checkbox"
            name="accepted_terms_and_privacy"
            checked={formData.accepted_terms_and_privacy}
            onChange={(e) =>
              setFormData((prev) => ({
                ...prev,
                accepted_terms_and_privacy: e.target.checked,
              }))
            }
            required
          />
          <label>
            I accept the <a href="/terms">Terms and Conditions</a> and <a href="/privacy">Privacy Policy</a>.
          </label>
        </CheckboxContainer>
        {errors.terms && <ErrorText>{errors.terms}</ErrorText>}
        <Button type="submit" disabled={isLoading}>
          {isLoading ? "Registering..." : "Register"}
        </Button>
      </Form>
    </OverlayContainer>
  );
};

export default AccountCreation;
