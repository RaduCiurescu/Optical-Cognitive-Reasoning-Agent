import React, { useEffect, useState } from "react";
import {
    PieChart,
    Pie,
    Cell,
    Tooltip,
    Legend,
    ResponsiveContainer,
} from "recharts";

// Tipul datelor care vin din backend (din SQLite prin /api/dashboard)
type DashboardApiData = {
    totalPeople: number;
    todayPeople: number;
    categories: { Oferte: number; Facturi: number; Diverse: number };
};

// Tipul complet folosit în componentă
type DashboardData = DashboardApiData;

const Dashboard: React.FC = () => {
    const [data, setData] = useState<DashboardData>({
        totalPeople: 0,
        todayPeople: 0,
        categories: { Oferte: 0, Facturi: 0, Diverse: 0 },
    });

    const [dashLoading, setDashLoading] = useState<boolean>(true);
    const [dashError, setDashError] = useState<string>("");

    // Modal form state
    const [isModalOpen, setIsModalOpen] = useState<boolean>(false);
    const [problemTitle, setProblemTitle] = useState<string>("");
    const [problemMessage, setProblemMessage] = useState<string>("");
    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState<string>("");
    const [success, setSuccess] = useState<string>("");

    // ===================== FETCH DASHBOARD DATA DIN SQLITE =====================
    useEffect(() => {
        const loadDashboard = async () => {
            try {
                setDashError("");
                setDashLoading(true);

                const res = await fetch("http://localhost:5000/api/dashboard");
                if (!res.ok) {
                    console.error("Eroare dashboard:", res.status);
                    setDashError("Nu s-au putut încărca datele din dashboard.");
                    return;
                }

                const json: DashboardApiData = await res.json();
                console.log("📊 Dashboard from backend (DB):", json);

                setData(json);
            } catch (err) {
                console.error("Eroare la fetch dashboard:", err);
                setDashError("A apărut o eroare la încărcarea dashboard-ului.");
            } finally {
                setDashLoading(false);
            }
        };

        loadDashboard();
    }, []);

    const categoriesData = [
        { name: "Oferte", value: data.categories.Oferte },
        { name: "Facturi", value: data.categories.Facturi },
        { name: "Diverse", value: data.categories.Diverse },
    ];

    const categoryColors = ["#00CFFF", "#007BFF", "#6dbdda"];

    // ===================== SUBMIT PROBLEM =====================
    const handleSubmitProblem = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        setError("");
        setSuccess("");

        if (!problemTitle.trim() || !problemMessage.trim()) {
            setError("Te rog completează Titlu și Mesaj.");
            return;
        }

        try {
            setLoading(true);
            const res = await fetch("http://localhost:5000/api/problems", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ title: problemTitle, message: problemMessage }),
            });

            if (!res.ok) {
                const errJson = await res.json().catch(() => ({}));
                throw new Error(errJson.error || "Eroare la trimitere.");
            }

            setSuccess("Problema a fost trimisă!");
            setProblemTitle("");
            setProblemMessage("");
        } catch (err) {
            console.error(err);
            if (err instanceof Error) setError(err.message);
            else setError("A apărut o eroare.");
        } finally {
            setLoading(false);
        }
    };

    // ===================== LOGOUT =====================
    const handleLogout = () => {
        localStorage.removeItem("userType");
        localStorage.removeItem("username");
        window.location.href = "/";
    };

    if (dashLoading) {
        return (
            <div
                style={{
                    backgroundColor: "#007BFF",
                    minHeight: "100vh",
                    color: "white",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    fontFamily: "Arial, sans-serif",
                }}
            >
                Se încarcă dashboard-ul...
            </div>
        );
    }

    return (
        <div
            style={{
                backgroundColor: "#007BFF",
                minHeight: "100vh",
                padding: "50px",
                color: "white",
                fontFamily: "Arial, sans-serif",
                display: "flex",
                flexDirection: "column",
                gap: "50px",
                overflowX: "hidden",
            }}
        >
            {/* Header */}
            <h1 style={{ textAlign: "center", marginBottom: "10px" }}>
                Dashboard Oameni Ajutați
            </h1>

            {dashError && (
                <p style={{ textAlign: "center", color: "yellow", marginBottom: "20px" }}>
                    {dashError}
                </p>
            )}

            {/* Statistici generale */}
            <div
                style={{
                    display: "flex",
                    justifyContent: "space-around",
                    gap: "20px",
                    flexWrap: "wrap",
                }}
            >
                <div
                    style={{
                        backgroundColor: "#0056b3",
                        borderRadius: "10px",
                        padding: "30px 50px",
                        textAlign: "center",
                        flex: 1,
                        minWidth: "250px",
                        boxShadow: "0 4px 6px rgba(0,0,0,0.2)",
                    }}
                >
                    <p style={{ margin: 0, fontWeight: "bold" }}>
                        Persoane ajutate până acum
                    </p>
                    <p style={{ margin: 0, fontSize: "2rem" }}>{data.totalPeople}</p>
                </div>

                <div
                    style={{
                        backgroundColor: "#0056b3",
                        borderRadius: "10px",
                        padding: "30px 50px",
                        textAlign: "center",
                        flex: 1,
                        minWidth: "250px",
                        boxShadow: "0 4px 6px rgba(0,0,0,0.2)",
                    }}
                >
                    <p style={{ margin: 0, fontWeight: "bold" }}>
                        Persoane ajutate astăzi
                    </p>
                    <p style={{ margin: 0, fontSize: "2rem" }}>{data.todayPeople}</p>
                </div>
            </div>

            {/* Grafice + butoane */}
            <div
                style={{
                    display: "flex",
                    justifyContent: "space-around",
                    gap: "50px",
                    flexWrap: "wrap",
                }}
            >
                {/* Categories Pie Chart */}
                <div
                    style={{
                        backgroundColor: "#0056b3",
                        borderRadius: "10px",
                        padding: "20px",
                        flex: 1,
                        minWidth: "300px",
                        height: "300px",
                    }}
                >
                    <h3 style={{ textAlign: "center", marginBottom: "10px" }}>
                        Categorii
                    </h3>
                    <ResponsiveContainer width="100%" height="80%">
                        <PieChart>
                            <Pie
                                data={categoriesData}
                                dataKey="value"
                                nameKey="name"
                                outerRadius={100}
                                label
                            >
                                {categoriesData.map((entry, index) => (
                                    <Cell key={`cat-${index}`} fill={categoryColors[index]} />
                                ))}
                            </Pie>
                            <Tooltip />
                            <Legend verticalAlign="bottom" />
                        </PieChart>
                    </ResponsiveContainer>
                </div>

                {/* Butoane Raportează + Logout */}
                <div
                    style={{
                        textAlign: "center",
                        marginTop: "20vh",
                        display: "flex",
                        flexDirection: "column",
                        gap: "15px",
                        alignItems: "center",
                    }}
                >
                    <button
                        style={{
                            backgroundColor: "#ff4d4d",
                            color: "white",
                            border: "none",
                            borderRadius: "8px",
                            padding: "15px 30px",
                            fontSize: "1rem",
                            cursor: "pointer",
                            boxShadow: "0 4px 6px rgba(0,0,0,0.2)",
                            transition: "0.3s",
                        }}
                        onClick={() => setIsModalOpen(true)}
                    >
                        Raportează o problemă
                    </button>

                    <button
                        style={{
                            backgroundColor: "#222",
                            color: "white",
                            border: "none",
                            borderRadius: "8px",
                            padding: "10px 25px",
                            fontSize: "0.95rem",
                            cursor: "pointer",
                            boxShadow: "0 3px 5px rgba(0,0,0,0.25)",
                            transition: "0.3s",
                        }}
                        onClick={handleLogout}
                    >
                        Logout
                    </button>
                </div>
            </div>

            {/* Modal */}
            {isModalOpen && (
                <div
                    style={{
                        position: "fixed",
                        inset: 0,
                        backgroundColor: "rgba(0,0,0,0.6)",
                        display: "flex",
                        justifyContent: "center",
                        alignItems: "center",
                        zIndex: 9999,
                    }}
                    onClick={() => setIsModalOpen(false)}
                >
                    <div
                        style={{
                            backgroundColor: "white",
                            color: "#333",
                            borderRadius: "10px",
                            padding: "30px",
                            width: "90%",
                            maxWidth: "500px",
                            boxShadow: "0 4px 10px rgba(0,0,0,0.3)",
                        }}
                        onClick={(e) => e.stopPropagation()}
                    >
                        <h2
                            style={{
                                marginTop: 0,
                                marginBottom: "20px",
                                textAlign: "center",
                            }}
                        >
                            Raportează o problemă
                        </h2>

                        <form
                            onSubmit={handleSubmitProblem}
                            style={{ display: "flex", flexDirection: "column", gap: "15px" }}
                        >
                            <div>
                                <label
                                    style={{ display: "block", marginBottom: "5px", fontWeight: "bold" }}
                                >
                                    Titlu
                                </label>
                                <input
                                    type="text"
                                    value={problemTitle}
                                    onChange={(e) => setProblemTitle(e.target.value)}
                                    style={{
                                        width: "100%",
                                        padding: "10px",
                                        borderRadius: "6px",
                                        border: "1px solid #ccc",
                                        fontSize: "1rem",
                                    }}
                                    placeholder="Titlul problemei"
                                />
                            </div>

                            <div>
                                <label
                                    style={{ display: "block", marginBottom: "5px", fontWeight: "bold" }}
                                >
                                    Mesaj
                                </label>
                                <textarea
                                    value={problemMessage}
                                    onChange={(e) => setProblemMessage(e.target.value)}
                                    rows={4}
                                    style={{
                                        width: "100%",
                                        padding: "10px",
                                        borderRadius: "6px",
                                        border: "1px solid #ccc",
                                        fontSize: "1rem",
                                        resize: "vertical",
                                    }}
                                    placeholder="Descrie problema..."
                                />
                            </div>

                            {error && <p style={{ color: "red" }}>{error}</p>}
                            {success && <p style={{ color: "green" }}>{success}</p>}

                            <div
                                style={{
                                    display: "flex",
                                    justifyContent: "flex-end",
                                    gap: "10px",
                                }}
                            >
                                <button
                                    type="button"
                                    onClick={() => setIsModalOpen(false)}
                                    style={{
                                        padding: "10px 20px",
                                        borderRadius: "6px",
                                        border: "none",
                                        backgroundColor: "#ccc",
                                        cursor: "pointer",
                                    }}
                                >
                                    Închide
                                </button>

                                <button
                                    type="submit"
                                    disabled={loading}
                                    style={{
                                        padding: "10px 20px",
                                        borderRadius: "6px",
                                        border: "none",
                                        backgroundColor: "#007BFF",
                                        color: "white",
                                        cursor: "pointer",
                                        opacity: loading ? 0.7 : 1,
                                    }}
                                >
                                    {loading ? "Se trimite..." : "Trimite"}
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Dashboard;
