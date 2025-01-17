const darkTheme = {
    colors: {
        primary: "#1DB954", // Spotify green for a modern look
        secondary: "#121212", // Dark background
        accent: "#535353", // Accent for cards and panels
        textPrimary: "#FFFFFF",
        textSecondary: "#B3B3B3",
    },
    font: {
        family: "Arial, sans-serif",
        size: "16px",
        weight: "400",
    },
        shadows: {
        default: "0px 4px 6px rgba(0, 0, 0, 0.1)",
    },
    spacing: (factor) => `${factor * 8}px`, // 8px grid spacing
};

export default darkTheme;
