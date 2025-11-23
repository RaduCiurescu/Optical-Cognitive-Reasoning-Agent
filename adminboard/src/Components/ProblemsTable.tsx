import React, { useEffect, useState } from "react";

type Problem = {
    id: number;
    title: string;
    message: string;
    created_at: string;
    resolved?: number;
};

const ProblemsTable: React.FC = () => {
    const [problems, setProblems] = useState<Problem[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string>("");

    // Preia problemele din backend
    const loadProblems = async () => {
        try {
            const res = await fetch("http://localhost:5000/api/problems");
            const data = await res.json();
            setProblems(data);
        } catch (err) {
            setError("Nu s-au putut prelua problemele.");
        }
        setLoading(false);
    };

    useEffect(() => {
        loadProblems();
    }, []);

    // Ștergere problemă
    const handleDelete = async (id: number) => {
        if (!window.confirm("Ești sigur că vrei să ștergi această problemă?")) return;

        await fetch(`http://localhost:5000/api/problems/${id}`, {
            method: "DELETE"
        });

        setProblems(prev => prev.filter(p => p.id !== id));
    };

    // Marcare ca rezolvat
    const handleResolve = async (id: number) => {
        await fetch(`http://localhost:5000/api/problems/${id}/resolve`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ resolved: 1 })
        });

        setProblems(prev =>
            prev.map(p => (p.id === id ? { ...p, resolved: 1 } : p))
        );
    };

    // 🔐 LOGOUT BUTTON (exact ca în Dashboard)
    const handleLogout = () => {
        localStorage.removeItem("userType");
        localStorage.removeItem("username");
        window.location.href = "/";
    };

    if (loading) {
        return <div style={{ padding: "40px", color: "white" }}>Se încarcă...</div>;
    }

    return (
        <div
            style={{
                backgroundColor: "#007BFF",
                minHeight: "100vh",
                padding: "40px",
                color: "white",
                fontFamily: "Arial",
            }}
        >
            <h1 style={{ textAlign: "center", marginBottom: "20px" }}>
                Lista Problemelor
            </h1>

            {/* 🔥 BUTON LOGOUT IDENTIC */}
            <div style={{ textAlign: "center", marginBottom: "30px" }}>
                <button
                    onClick={handleLogout}
                    style={{
                        backgroundColor: "#222",
                        color: "white",
                        border: "none",
                        padding: "10px 25px",
                        borderRadius: "8px",
                        cursor: "pointer",
                        fontSize: "0.95rem",
                        boxShadow: "0 3px 5px rgba(0,0,0,0.25)",
                        transition: "0.3s",
                    }}
                >
                    Logout
                </button>
            </div>

            {error && (
                <p style={{ textAlign: "center", color: "yellow" }}>{error}</p>
            )}

            <div
                style={{
                    overflowX: "auto",
                    backgroundColor: "#0056b3",
                    padding: "20px",
                    borderRadius: "12px",
                    boxShadow: "0 4px 10px rgba(0,0,0,0.3)",
                }}
            >
                <table style={{ width: "100%", borderCollapse: "collapse" }}>
                    <thead>
                    <tr style={{ backgroundColor: "#003f88" }}>
                        <th style={thStyle}>Titlu</th>
                        <th style={thStyle}>Descriere</th>
                        <th style={thStyle}>Acțiuni</th>
                    </tr>
                    </thead>

                    <tbody>
                    {problems.map((p) => (
                        <tr
                            key={p.id}
                            style={{
                                backgroundColor: p.resolved
                                    ? "#338a3e"
                                    : "transparent",
                            }}
                        >
                            <td style={tdStyle}>{p.title}</td>
                            <td style={tdStyle}>{p.message}</td>
                            <td style={tdStyle}>
                                <div style={{ display: "flex", gap: "10px" }}>
                                    <button
                                        onClick={() => handleResolve(p.id)}
                                        style={{
                                            ...btnStyle,
                                            backgroundColor: "#4CAF50",
                                        }}
                                    >
                                        Rezolvat
                                    </button>

                                    <button
                                        onClick={() => handleDelete(p.id)}
                                        style={{
                                            ...btnStyle,
                                            backgroundColor: "#ff4d4d",
                                        }}
                                    >
                                        Șterge
                                    </button>
                                </div>
                            </td>
                        </tr>
                    ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

const thStyle: React.CSSProperties = {
    padding: "15px",
    borderBottom: "2px solid #003060",
    fontSize: "1.1rem",
    textAlign: "left",
};

const tdStyle: React.CSSProperties = {
    padding: "15px",
    borderBottom: "1px solid #004080",
    verticalAlign: "top",
};

const btnStyle: React.CSSProperties = {
    padding: "10px 15px",
    border: "none",
    color: "white",
    cursor: "pointer",
    borderRadius: "6px",
    transition: "0.2s",
};

export default ProblemsTable;
