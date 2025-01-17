// src/pages/Home.js
import React, { useContext } from "react";
import { useNavigate } from "react-router-dom";
import styled from "styled-components";
import { AuthContext } from "../contexts/AuthContext";

const Container = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background: linear-gradient(135deg, #121212, #1f1f1f);
  color: #fff;
`;

const Title = styled.h1`
  font-size: 3rem;
  text-align: center;
`;

const Subtitle = styled.p`
  font-size: 1.2rem;
  margin: 20px 0;
  color: #bdbdbd;
  text-align: center;
`;

const ButtonContainer = styled.div`
  display: flex;
  gap: 20px;
  margin-top: 40px;
`;

const Button = styled.button`
  padding: 15px 30px;
  font-size: 1rem;
  font-weight: bold;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background 0.3s ease, transform 0.2s ease;

  background: ${(props) => (props.primary ? "#ff5722" : "#1e1e1e")};
  color: ${(props) => (props.primary ? "#fff" : "#ff5722")};

  &:hover {
    background: ${(props) => (props.primary ? "#e64a19" : "#333")};
    transform: scale(1.05);
  }
`;

const Features = styled.div`
  margin-top: 50px;
  text-align: center;

  h2 {
    margin-bottom: 20px;
    font-size: 2rem;
  }

  ul {
    list-style: none;
    padding: 0;
    font-size: 1.2rem;
    color: #bdbdbd;

    li {
      margin-bottom: 10px;
    }
  }
`;

const Home = () => {
  const { currentUser } = useContext(AuthContext);
  const navigate = useNavigate();

  return (
    <Container>
      {currentUser ? (
        <>
          <Title>Ready to lift weights, {currentUser.username}?</Title>
          <Features>
            <h2>Your Features</h2>
            <ul>
              <li>Access to personalized workouts</li>
              <li>Custom meal plans</li>
              <li>Track your progress</li>
              <li>Join live classes</li>
              <li>Engage with the fitness community</li>
            </ul>
          </Features>
        </>
      ) : (
        <>
          <Title>Welcome to Yoked</Title>
          <Subtitle>Your journey to a healthier, fitter you starts here.</Subtitle>
          <ButtonContainer>
            <Button primary onClick={() => navigate("/register")}>
              Register
            </Button>
            <Button onClick={() => navigate("/login")}>Login</Button>
          </ButtonContainer>
        </>
      )}
    </Container>
  );
};

export default Home;
