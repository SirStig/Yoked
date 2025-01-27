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

const TermsConditions = () => {
  return (
    <Container>
      <Header />
      <Spacer />
      <Content>
        <h1>Terms and Conditions</h1>
        <p>Last updated: [Insert Date]</p>

        <h2>Introduction</h2>
        <p>
          Welcome to Yoked. By accessing or using our platform, you agree to be bound
          by these terms and conditions. Please read them carefully before proceeding.
        </p>

        <h2>Use of the Platform</h2>
        <p>
          By using Yoked, you agree to:
        </p>
        <ul>
          <li>Provide accurate and up-to-date information during registration.</li>
          <li>Use the platform only for its intended purposes.</li>
          <li>Comply with all applicable laws and regulations.</li>
        </ul>

        <h3>Prohibited Activities</h3>
        <p>You agree not to:</p>
        <ul>
          <li>Engage in any fraudulent, abusive, or unlawful activities.</li>
          <li>Use the platform to distribute harmful or inappropriate content.</li>
          <li>Interfere with the platform's functionality or security.</li>
        </ul>

        <h2>Accounts and Security</h2>
        <p>
          You are responsible for maintaining the confidentiality of your account
          credentials. Notify us immediately if you suspect unauthorized access to your
          account.
        </p>

        <h2>Payments and Subscriptions</h2>
        <p>
          By subscribing to a plan, you agree to:
        </p>
        <ul>
          <li>Provide valid payment information.</li>
          <li>Allow us to process payments in accordance with your subscription plan.</li>
          <li>Review our refund and cancellation policies before making a purchase.</li>
        </ul>

        <h2>Content Ownership</h2>
        <p>
          All content on Yoked, including text, images, and videos, is owned by us or
          our licensors. You may not reproduce, distribute, or modify this content
          without prior written consent.
        </p>

        <h2>Third-Party Links</h2>
        <p>
          Our platform may include links to third-party websites or services. We are
          not responsible for the content, policies, or practices of these third-party
          sites.
        </p>

        <h2>Disclaimer of Warranties</h2>
        <p>
          Yoked is provided \"as is\" without warranties of any kind, whether express or
          implied. We do not guarantee the accuracy, completeness, or reliability of
          our platform.
        </p>

        <h2>Limitation of Liability</h2>
        <p>
          To the fullest extent permitted by law, Yoked and its affiliates shall not be
          liable for any indirect, incidental, or consequential damages arising from
          your use of the platform.
        </p>

        <h2>Indemnification</h2>
        <p>
          You agree to indemnify and hold harmless Yoked and its affiliates from any
          claims, damages, or expenses arising from your violation of these terms.
        </p>

        <h2>Termination</h2>
        <p>
          We reserve the right to terminate or suspend your account at our sole
          discretion for any violations of these terms.
        </p>

        <h2>Changes to These Terms</h2>
        <p>
          We may update these terms and conditions from time to time. We encourage you
          to review this page periodically to stay informed.
        </p>

        <h2>Governing Law</h2>
        <p>
          These terms and conditions are governed by the laws of [Your Jurisdiction].
          Any disputes shall be resolved exclusively in the courts of [Your Jurisdiction].
        </p>

        <h2>Contact Us</h2>
        <p>
          If you have any questions or concerns about these terms and conditions, please
          contact us at:
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

export default TermsConditions;
