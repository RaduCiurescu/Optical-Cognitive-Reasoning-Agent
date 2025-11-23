import React from 'react';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import '../App.css';
import Dashboard from "../Components/Dashboard";

function Home() {
    return (
        <div>
            <Dashboard></Dashboard>
        </div>
    );
}

export default Home;
