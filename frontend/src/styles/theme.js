export const theme = {
  colors: {
    primary: "#ff5722", // Vibrant accent color for call-to-actions
    primaryHover: "#e64a19",
    secondary: "#121212", // Dark background for the theme
    accent: "#4caf50", // Secondary accent for hover effects or highlights
    textPrimary: "#ffffff", // Main text color
    textSecondary: "#aaaaaa", // Muted text for secondary information
    cardBackground: "#1f1f1f", // Background for cards or containers
    inputBackground: "#2b2b2b", // Background for input fields
    inputBorder: "#333333", // Border for inputs and other elements
    error: "#f44336", // Error messages or states
    errorBackground: "#3e1c1c", // Background for error messages
    success: "#4caf50", // Success messages or states
    successBackground: "#1e4620", // Background for success messages
    info: "#2196f3", // Informational messages or states
    infoBackground: "#1c3e58", // Background for informational messages
    warning: "#ff9800", // Warning messages or states
    warningBackground: "#4a351c", // Background for warning messages
    disabled: "#555555", // Disabled state for buttons, inputs, etc.
    link: "#1976d2", // Links
    linkHover: "#0d47a1", // Hover state for links
  },
  font: {
    family: "'Inter', sans-serif", // Clean, modern font
    size: "16px", // Default font size
    weightLight: 300,
    weightRegular: 400,
    weightBold: 700,
  },
  spacing: (factor) => `${factor * 8}px`, // Spacing system (e.g., spacing(2) = 16px)
  borderRadius: "8px", // Consistent border-radius for buttons, inputs, etc.
  transitions: {
    default: "all 0.3s ease", // Default transition
    fast: "all 0.2s ease-in-out",
    slow: "all 0.5s ease-in-out",
  },
  breakpoints: {
    xs: "480px", // Mobile devices
    sm: "768px", // Tablets
    md: "1024px", // Small laptops
    lg: "1440px", // Desktop
    xl: "1920px", // Large screens
  },
  shadows: {
    light: "0 2px 4px rgba(0, 0, 0, 0.1)",
    medium: "0 4px 8px rgba(0, 0, 0, 0.2)",
    heavy: "0 6px 12px rgba(0, 0, 0, 0.4)",
  },
  animations: {
    fadeIn: "fade-in 0.5s ease-in-out",
    slideUp: "slide-up 0.6s ease-in-out",
    scaleUp: "scale-up 0.4s ease-in-out",
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
`;

export default theme;
