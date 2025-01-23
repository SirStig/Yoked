import React, { useState } from "react";
import styled from "styled-components";

// Styled Components
const FormContainer = styled.div`
  width: 100%;
  max-width: 600px;
  margin: 0 auto;
  background-color: ${({ theme }) => theme.colors.cardBackground};
  padding: 2rem;
  border-radius: ${({ theme }) => theme.borderRadius};
  box-shadow: ${({ theme }) => theme.shadows.medium};
`;

const Form = styled.form`
  display: flex;
  flex-direction: column;
  gap: 1rem;

  label {
    font-weight: bold;
    color: ${({ theme }) => theme.colors.textPrimary};
  }

  input,
  select,
  textarea {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid ${({ theme }) => theme.colors.border};
    border-radius: ${({ theme }) => theme.borderRadius};
    background-color: ${({ theme }) => theme.colors.background};
    color: ${({ theme }) => theme.colors.textPrimary};
    font-size: 1rem;
  }

  button {
    background-color: ${({ theme }) => theme.colors.primary};
    color: ${({ theme }) => theme.colors.textSecondary};
    border: none;
    padding: 0.75rem;
    border-radius: ${({ theme }) => theme.borderRadius};
    font-size: 1rem;
    cursor: pointer;
    transition: background-color 0.3s ease;

    &:hover {
      background-color: ${({ theme }) => theme.colors.primaryHover};
    }
  }
`;

// AdminForm Component
const AdminForm = ({ fields, onSubmit, initialValues }) => {
  const [formData, setFormData] = useState(initialValues || {});

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <FormContainer>
      <Form onSubmit={handleSubmit}>
        {fields.map((field) => (
          <div key={field.name}>
            <label htmlFor={field.name}>{field.label}</label>
            {field.type === "textarea" ? (
              <textarea
                name={field.name}
                value={formData[field.name] || ""}
                onChange={handleChange}
              />
            ) : field.type === "select" ? (
              <select
                name={field.name}
                value={formData[field.name] || ""}
                onChange={handleChange}
              >
                {field.options.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            ) : (
              <input
                type={field.type}
                name={field.name}
                value={formData[field.name] || ""}
                onChange={handleChange}
              />
            )}
          </div>
        ))}
        <button type="submit">Submit</button>
      </Form>
    </FormContainer>
  );
};

export default AdminForm;
