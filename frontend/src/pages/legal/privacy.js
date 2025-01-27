import React from "react";
import styled from "styled-components";
import Header from "../../components/shared/Header";
import Footer from "../../components/shared/Footer";

// Styled Components
const Container = styled.div`
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: ${({ theme }) => theme.colors.background};
  color: ${({ theme }) => theme.colors.textPrimary};
`;

const Content = styled.main`
  flex: 1;
  padding: 4rem 2rem; /* Added space to accommodate the header */
  max-width: 1200px;
  margin: 0 auto;
  line-height: 1.8; /* Slightly increased for readability */
  font-size: 1rem;
  color: ${({ theme }) => theme.colors.textSecondary};

  h1 {
    font-size: 2.5rem;
    margin-bottom: 1rem;
    color: ${({ theme }) => theme.colors.primary};
  }

  h2 {
    font-size: 1.8rem;
    margin-top: 2rem;
    margin-bottom: 1rem;
    color: ${({ theme }) => theme.colors.textPrimary};
  }

  h3 {
    font-size: 1.5rem;
    margin-top: 1.5rem;
    color: ${({ theme }) => theme.colors.textPrimary};
  }

  p {
    margin-bottom: 1rem;
  }

  a {
    color: ${({ theme }) => theme.colors.link};
    text-decoration: none;
    &:hover {
      color: ${({ theme }) => theme.colors.linkHover};
      text-decoration: underline;
    }
  }

  ul {
    padding-left: 20px;
    list-style-type: disc;

    li {
      margin-bottom: 0.5rem;
    }
  }
`;

const Spacer = styled.div`
  height: 60px; /* Ensures space below the fixed header */
`;

const PrivacyPolicy = () => {
  return (
    <Container>
      <Header />
      <Spacer />
      <Content>
        <h1>Privacy Policy</h1>
        <p>Last updated: [Insert Date]</p>

        <h2>Introduction</h2>
        <p>
          Welcome to Yoked. We are committed to protecting your privacy and ensuring
          the security of your personal data. This privacy policy explains how we
          collect, use, and share your information when you interact with our services.
        </p>

        <h2>Information We Collect</h2>
        <h3>1. Personal Information</h3>
        <p>
          We may collect personal information you provide directly to us, including but
          not limited to:
        </p>
        <ul>
          <li>Full name</li>
          <li>Email address</li>
          <li>Username</li>
          <li>Profile information, such as fitness goals and preferences</li>
          <li>Payment information</li>
        </ul>

        <h3>2. Automatically Collected Information</h3>
        <p>
          When you use our services, we may collect certain information automatically,
          including:
        </p>
        <ul>
          <li>Device information (e.g., IP address, browser type, operating system)</li>
          <li>Usage data (e.g., pages viewed, time spent on the platform)</li>
          <li>Location data (if location permissions are enabled)</li>
        </ul>

        <h2>How We Use Your Information</h2>
        <p>We use the information we collect for the following purposes:</p>
        <ul>
          <li>To provide and improve our services</li>
          <li>To personalize your user experience</li>
          <li>To process payments and manage subscriptions</li>
          <li>To communicate with you regarding your account or service updates</li>
          <li>To enforce our terms and conditions</li>
        </ul>

        <h2>How We Share Your Information</h2>
        <p>
          We do not sell your personal information. However, we may share your
          information in the following ways:
        </p>
        <ul>
          <li>
            <strong>Service Providers:</strong> We may share information with trusted
            third-party service providers who assist us in delivering our services (e.g.,
            payment processors, hosting providers).
          </li>
          <li>
            <strong>Legal Compliance:</strong> We may disclose your information to
            comply with applicable laws, regulations, or legal proceedings.
          </li>
          <li>
            <strong>Business Transfers:</strong> In the event of a merger, acquisition,
            or sale of assets, your information may be transferred as part of the
            transaction.
          </li>
        </ul>

        <h2>Your Rights</h2>
        <p>You have certain rights regarding your personal information, including:</p>
        <ul>
          <li>The right to access, update, or delete your information</li>
          <li>The right to opt-out of marketing communications</li>
          <li>The right to data portability</li>
          <li>The right to lodge a complaint with a supervisory authority</li>
        </ul>

        <h2>Data Retention</h2>
        <p>
          We retain your personal information for as long as necessary to provide our
          services and fulfill the purposes outlined in this policy, unless a longer
          retention period is required by law.
        </p>

        <h2>Security</h2>
        <p>
          We implement appropriate technical and organizational measures to protect your
          personal information. However, no system is completely secure, and we cannot
          guarantee absolute security.
        </p>

        <h2>Children's Privacy</h2>
        <p>
          Our services are not directed to children under the age of 13, and we do not
          knowingly collect personal information from children.
        </p>

        <h2>Changes to This Privacy Policy</h2>
        <p>
          We may update this privacy policy from time to time. We encourage you to
          review this policy periodically to stay informed about our practices.
        </p>

        <h2>Contact Us</h2>
        <p>
          If you have any questions about this privacy policy, please contact us at:
        </p>
        <p>
          <strong>Email:</strong> support@yoked.com
        </p>
        <p>
          <strong>Mailing Address:</strong> Yoked, 123 Fitness Lane, Workout City, USA
        </p>
      </Content>
      <Footer />
    </Container>
  );
};

export default PrivacyPolicy;
