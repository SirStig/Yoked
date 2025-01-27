import React from "react";
import Header from "../components/shared/Header";
import HeroSection from "../components/shared/HeroSection";
import FeaturesSection from "../components/shared/FeatureSection";
import SubscriptionsSection from "../components/shared/SubscriptionsSection";
import Footer from "../components/shared/Footer";
import styled from "styled-components";

const PageContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  background: ${({ theme }) => theme.colors.pageBackground};
`;

const SectionWrapper = styled.div`
  width: 100%;
  scroll-margin-top: 1px;
`;

const Home = () => {
  return (
    <PageContainer>
      <Header />
      <SectionWrapper id="home">
        <HeroSection />
      </SectionWrapper>
      <SectionWrapper id="features">
        <FeaturesSection />
      </SectionWrapper>
      <SectionWrapper id="subscriptions">
        <SubscriptionsSection />
      </SectionWrapper>
      <Footer />
    </PageContainer>
  );
};

export default Home;
