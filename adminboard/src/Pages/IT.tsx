import React from 'react';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import '../App.css';
import ProblemsTable from "../Components/ProblemsTable";
function IT() {
    return (
        <div>
            <ProblemsTable></ProblemsTable>
        </div>
    );
}

export default IT;
