import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";

import Home from "./Pages/Home";
import IT from "./Pages/IT";
import LoginPage from "./Pages/LoginPage";
import "./App.css";

// 🔐 ProtectedRoute
type ProtectedRouteProps = {
    allowedTypes: string[];
    children: React.ReactNode; // ⬅️ FIX AICI
};

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ allowedTypes, children }) => {
    const userType = localStorage.getItem("userType");

    if (!userType) {
        return <Navigate to="/" replace />;
    }

    if (!allowedTypes.includes(userType)) {
        return <Navigate to="/" replace />;
    }

    return <>{children}</>;
};

function App() {
    return (
        <Router>
            <Routes>
                {/* LOGIN */}
                <Route path="/" element={<LoginPage />} />

                {/* FUNCTIONAR */}
                <Route
                    path="/acasa"
                    element={
                        <ProtectedRoute allowedTypes={["Functionar"]}>
                            <Home />
                        </ProtectedRoute>
                    }
                />

                {/* DEVELOPER */}
                <Route
                    path="/dev"
                    element={
                        <ProtectedRoute allowedTypes={["Developer"]}>
                            <IT />
                        </ProtectedRoute>
                    }
                />
            </Routes>
        </Router>
    );
}

export default App;
