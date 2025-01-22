import React, { Component } from "react";
import styled from "styled-components";

// Styled components for ErrorBoundary
const ErrorContainer = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: ${({ theme }) => theme.colors.secondary};
  color: ${({ theme }) => theme.colors.textPrimary};
  font-family: ${({ theme }) => theme.font.family};
  text-align: center;
`;

const ErrorMessage = styled.h2`
  font-size: 2rem;
  color: ${({ theme }) => theme.colors.accent};
`;

const ErrorDetails = styled.p`
  font-size: 1rem;
  color: ${({ theme }) => theme.colors.textSecondary};
`;

class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = {
      hasError: false,
      error: null,
      errorInfo: null,
    };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    this.setState({
      error: error,
      errorInfo: errorInfo,
    });
  }

  render() {
    if (this.state.hasError) {
      return (
        <ErrorContainer>
          <div>
            <ErrorMessage>Something went wrong.</ErrorMessage>
            <ErrorDetails>{this.state.error && this.state.error.toString()}</ErrorDetails>
            <ErrorDetails>{this.state.errorInfo && this.state.errorInfo.componentStack}</ErrorDetails>
          </div>
        </ErrorContainer>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
