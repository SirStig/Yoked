import React, { useState, useContext } from "react";
import { AuthContext } from "../contexts/AuthContext";
import axios from "axios";

const Login = () => {
    const { login } = useContext(AuthContext);
    const [credentials, setCredentials] = useState({ username: "", password: "" });

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post("/api/auth/login", credentials);
            login(response.data.access_token);
        } catch (err) {
            alert("Invalid credentials");
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <input
                type="text"
                placeholder="Username"
                value={credentials.username}
                onChange={(e) => setCredentials({ ...credentials, username: e.target.value })}
            />
            <input
                type="password"
                placeholder="Password"
                value={credentials.password}
                onChange={(e) => setCredentials({ ...credentials, password: e.target.value })}
            />
            <button type="submit">Login</button>
        </form>
    );
};

export default Login;
