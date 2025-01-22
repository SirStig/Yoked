export const theme = {
  colors: {
    primary: "#ff5722", // Vibrant accent for call-to-actions
    primaryHover: "#ff784e", // Hover effect for primary elements
    secondary: "#121212", // Slightly lighter background for contrast
    accent: "#ffa726", // Bright accent for highlights
    gradientPrimary: "linear-gradient(90deg, #ff5722, #ffa726)", // Gradient for buttons and key areas
    gradientSecondary: "linear-gradient(45deg, #ff784e, #ff3d00)", // Secondary gradient for emphasis
    textPrimary: "#ffffff", // Main text color
    textSecondary: "#e0e0e0", // Softer muted text
    cardBackground: "#1f1f1f", // Elevated card background
    inputBackground: "#2b2b2b", // Subtle background for inputs
    inputBorder: "#404040", // Inputs and border emphasis
    error: "#e53935", // Error color for messages
    errorBackground: "#4e1c1c", // Background for error messages
    success: "#43a047", // Success states
    successBackground: "#1e4620", // Success message background
    info: "#1e88e5", // Info messages or states
    infoBackground: "#123456", // Background for informational messages
    warning: "#fb8c00", // Warning messages
    warningBackground: "#4a350c", // Warning background
    disabled: "#6d6d6d", // Disabled states
    link: "#42a5f5", // Link color
    linkHover: "#1976d2", // Hover state for links
  },
  font: {
    family: "'Poppins', 'Inter', sans-serif", // Clean and professional font stack
    size: "16px", // Default font size
    weightLight: 300,
    weightRegular: 400,
    weightBold: 700,
    headingSize: "32px", // Large headings
    subheadingSize: "24px", // Subheadings
  },
  spacing: (factor) => `${factor * 8}px`, // Spacing system (e.g., spacing(2) = 16px)
  borderRadius: "16px", // Slightly larger radius for a modern aesthetic
  transitions: {
    default: "all 0.3s ease", // Default transition
    fast: "all 0.2s ease-in-out",
    slow: "all 0.5s ease-in-out",
    hoverGlow: "box-shadow 0.4s ease-in-out", // Glow for hover effects
  },
  breakpoints: {
    xs: "480px", // Mobile devices
    sm: "768px", // Tablets
    md: "1024px", // Small laptops
    lg: "1440px", // Desktop
    xl: "1920px", // Large screens
  },
  shadows: {
    light: "0 2px 4px rgba(0, 0, 0, 0.2)",
    medium: "0 4px 8px rgba(0, 0, 0, 0.4)",
    heavy: "0 6px 12px rgba(0, 0, 0, 0.6)",
    glow: "0 0 12px rgba(255, 87, 34, 0.8)", // Glow effect for key elements
  },
  animations: {
    fadeIn: "fade-in 0.5s ease-in-out",
    slideUp: "slide-up 0.6s ease-in-out",
    scaleUp: "scale-up 0.4s ease-in-out",
    hoverPulse: "hover-pulse 0.8s infinite ease-in-out", // Subtle pulsing animation
    gradientShift: "gradient-shift 3s ease-in-out infinite", // Dynamic gradient effect
  },
};

// Keyframes for animations (can be added in GlobalStyles)
export const animations = `
  @keyframes fade-in {
    from {
      opacity: 0;
    }
    to {
      opacity: 1;
    }
  }

  @keyframes slide-up {
    from {
      transform: translateY(20px);
      opacity: 0;
    }
    to {
      transform: translateY(0);
      opacity: 1;
    }
  }

  @keyframes scale-up {
    from {
      transform: scale(0.9);
      opacity: 0;
    }
    to {
      transform: scale(1);
      opacity: 1;
    }
  }

  @keyframes hover-pulse {
    0%, 100% {
      transform: scale(1);
    }
    50% {
      transform: scale(1.05);
    }
  }

  @keyframes gradient-shift {
    0% {
      background-position: 0% 50%;
    }
    50% {
      background-position: 100% 50%;
    }
    100% {
      background-position: 0% 50%;
    }
  }
`;

export default theme;
