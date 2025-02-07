export const theme = {
  colors: {
    // Primary and secondary colors
    primary: "#ffffff", // White for buttons and accents
    primaryHover: "#b6b6b6", // Light gray for hover states
    secondary: "#1B1B1B", // Deep smoky black for background

    // Accent and highlights
    accent: "#d5b50d", // Bright gold for interactive elements
    accentHover: "#b89a0a", // Slightly darker gold for hover states

    // Gradients
    gradientPrimary: "linear-gradient(90deg, #4A90E2, #357ABD)", // Blue gradient
    gradientSecondary: "linear-gradient(45deg, #4B0082, #800080)", // Indigo to purple
    gradientAccent: "linear-gradient(90deg, #FFD700, #4A90E2)", // Gold to blue
    gradientCool: "linear-gradient(90deg, #87CEEB, #4682B4)", // Cool tones
    gradientProfessional: "linear-gradient(90deg, #1B1B1B, #3A3A3A)", // Dark gray gradient

    // Text colors
    textPrimary: "#ffffff", // White for primary text
    textSecondary: "#CCCCCC", // Muted gray for secondary text
    textAccent: "#4A90E2", // Blue for accent text
    textButton: "#393939", // Dark gray for buttons

    // Backgrounds
    cardBackground: "#2F2F2F", // Smoky gray for cards
    inputBackground: "#3A3A3A", // Subtle gray for inputs
    inputBorder: "#505050", // Dark gray for input borders
    dropdownBackground: "#20232A", // Neutral dark gray for dropdowns
    tooltipBackground: "#333333", // Dark gray for tooltips
    overlayBackground: "rgba(0, 0, 0, 0.8)", // Dark overlay for modals
    sidebarBackground: "#111117", // Dark navy for sidebars
    sidebarHover: "#191922", // Lighter shade for sidebar hover states
    sidebarActive: "#FFD700", // Gold to highlight active sidebar items

    // Feedback colors
    error: "#FF0000", // Bright red for errors
    errorBackground: "#4A0000", // Dark red for error backgrounds
    success: "#32CD32", // Lime green for success
    successBackground: "#003300", // Dark green for success backgrounds
    info: "#00CED1", // Aqua for informational elements
    warning: "#FFA500", // Bright orange for warnings
    disabled: "#A9A9A9", // Muted gray for disabled elements

    // Links and badges
    link: "#87CEEB", // Sky blue for links
    linkHover: "#4682B4", // Steel blue for link hover states
    badgeBackground: "#357ABD", // Blue for badges
  },

  font: {
    family: "'Poppins', 'Roboto', sans-serif", // Modern and clean fonts
    baseSize: "16px", // Base font size
    weightLight: 300,
    weightRegular: 400,
    weightBold: 700,
    headingSize: "3rem", // Large heading size
    subheadingSize: "2rem", // Subheading size
    smallSize: "0.875rem", // Small text size
  },

  spacing: (factor) => `${factor * 8}px`, // Spacing multiplier

  borderRadius: {
    small: "4px", // For small elements
    medium: "8px", // Default border radius
    large: "12px", // Rounded corners for larger components
  },

  transitions: {
    default: "all 0.3s ease-in-out", // Smooth transitions
    fast: "all 0.2s ease-in-out",
    hoverGlow: "box-shadow 0.4s ease-in-out", // Glow effect for hover states
  },

  breakpoints: {
    xs: "480px", // Mobile devices
    sm: "768px", // Tablets
    md: "1024px", // Small laptops
    lg: "1440px", // Desktops
    xl: "1920px", // Large screens
  },

  shadows: {
    light: "0 2px 4px rgba(0, 0, 0, 0.2)",
    medium: "0 4px 8px rgba(0, 0, 0, 0.4)",
    heavy: "0 6px 12px rgba(0, 0, 0, 0.6)",
    glow: "0 0 15px rgba(74, 144, 226, 0.8)", // Glow effect for blue elements
    inset: "inset 0 2px 4px rgba(0, 0, 0, 0.6)", // Inset shadow for depth
  },

  components: {
    // Specific component styles
    dropdown: {
      background: "#20232A", // Neutral dark gray
      border: "#4B5563", // Border for dropdowns
      text: "#FFFFFF", // White text
      hoverBackground: "#32363E", // Slightly lighter on hover
    },
    sidebar: {
      background: "#111117",
      hover: "#191922",
      active: "#FFD700",
      text: "#CCCCCC", // Muted gray text
      activeText: "#FFFFFF", // Bright white for active items
    },
    button: {
      background: "#4A90E2", // Calm blue
      hoverBackground: "#357ABD", // Slightly darker blue
      text: "#FFFFFF", // White for button text
    },
    tooltip: {
      background: "#333333",
      text: "#FFFFFF",
    },
    overlay: {
      background: "rgba(0, 0, 0, 0.8)", // Dark overlay
    },
    MuiTypography: {
      styleOverrides: {
        root: {
          color: "white",
        },
      },
    },
  },

  animations: {
    fadeIn: "fade-in 0.5s ease-in-out",
    slideUp: "slide-up 0.6s ease-in-out",
    scaleUp: "scale-up 0.4s ease-in-out",
    hoverPulse: "hover-pulse 0.8s infinite ease-in-out", // Subtle pulsing animation
    gradientShift: "gradient-shift 3s ease-in-out infinite", // Dynamic gradient animation
  },
};

// Keyframes for animations
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
