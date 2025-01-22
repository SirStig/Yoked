import React from "react";
import styled from "styled-components";

const StyledSection = styled.section`
  padding: ${({ theme }) => theme.spacing(10)} ${({ theme }) => theme.spacing(4)};
  text-align: center;
  background: ${({ theme }) => theme.colors.cardBackground};
  color: ${({ theme }) => theme.colors.textPrimary};

  h2 {
    margin-bottom: ${({ theme }) => theme.spacing(3)};
    font-size: 3rem;
  }

  p {
    font-size: 1.4rem;
    margin: ${({ theme }) => theme.spacing(3)} 0;
    color: ${({ theme }) => theme.colors.textSecondary};
  }
`;

const Section = ({ id, children }) => (
  <StyledSection id={id}>
    {children}
  </StyledSection>
);

export default Section;
