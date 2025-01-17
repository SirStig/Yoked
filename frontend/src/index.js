import React from "react";
import ReactDOM from "react-dom/client"; // Updated for React 18
import App from "./App";

const root = ReactDOM.createRoot(document.getElementById("root")); // Create root for React 18
root.render(
    <React.StrictMode>
        <App />
    </React.StrictMode>
);
