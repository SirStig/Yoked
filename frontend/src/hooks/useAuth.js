import { useContext, createContext } from "react";

const AuthContext = createContext();

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
    const login = async (credentials) => {
        // Handle login logic
    };

    const logout = () => {
        // Clear session
    };

    const value = { login, logout };

    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
