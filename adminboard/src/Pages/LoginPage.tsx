import React, { useState } from "react";

type LoginResponse = {
    username: string;
    type: string;
};

const LoginPage: React.FC = () => {
    const [username, setUsername] = useState<string>("");
    const [password, setPassword] = useState<string>("");
    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState<string>("");
    const [success, setSuccess] = useState<string>("");

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        setError("");
        setSuccess("");

        if (!username.trim() || !password.trim()) {
            setError("Te rog completează user și parolă.");
            return;
        }

        // 🔍 DEBUG: ce trimitem la backend
        console.log("🔍 Trimitem către backend:", {
            username,
            password,
        });

        try {
            setLoading(true);

            const res = await fetch("http://localhost:5000/api/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ username, password }),
            });

            // 🔍 DEBUG: status răspuns
            console.log("🔍 Status răspuns backend:", res.status);

            if (!res.ok) {
                const text = await res.text();
                console.log("🔍 Răspuns EROARE din backend:", text);
                throw new Error("Credențiale invalide sau eroare la login.");
            }

            const data: LoginResponse = await res.json();

            // 🔍 DEBUG: ce primim de la backend
            console.log("🔍 Date primite de la backend:", data);

            // Salvăm în localStorage
            localStorage.setItem("username", data.username);
            localStorage.setItem("userType", data.type);

            // 🔍 DEBUG: verificăm ce e în localStorage
            console.log("✅ username în localStorage:", localStorage.getItem("username"));
            console.log("✅ userType în localStorage:", localStorage.getItem("userType"));

            setSuccess(`Autentificare reușită ca ${data.type}`);

            // Redirect în funcție de type
            if (data.type === "Developer") {
                console.log("➡ Redirect către /dev");
                window.location.href = "/dev";
            } else {
                console.log("➡ Redirect către /acasa");
                window.location.href = "/acasa";
            }
        } catch (err) {
            console.error("❌ Eroare la login:", err);
            if (err instanceof Error) {
                setError(err.message);
            } else {
                setError("A apărut o eroare la autentificare.");
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <div
            style={{
                backgroundColor: "#007BFF",
                minHeight: "100vh",
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                fontFamily: "Arial, sans-serif",
                padding: "20px",
                color: "white",
            }}
        >
            <div
                style={{
                    backgroundColor: "#0056b3",
                    borderRadius: "16px",
                    padding: "30px 35px",
                    width: "100%",
                    maxWidth: "400px",
                    boxShadow: "0 6px 15px rgba(0,0,0,0.3)",
                }}
            >
                <h1 style={{ textAlign: "center", marginBottom: "20px" }}>Login</h1>
                <p
                    style={{
                        textAlign: "center",
                        marginBottom: "25px",
                        opacity: 0.9,
                    }}
                >
                    Autentifică-te pentru a accesa dashboard-ul.
                </p>

                <form
                    onSubmit={handleSubmit}
                    style={{ display: "flex", flexDirection: "column", gap: "15px" }}
                >
                    <div>
                        <label
                            htmlFor="username"
                            style={{
                                display: "block",
                                marginBottom: "5px",
                                fontWeight: "bold",
                            }}
                        >
                            User
                        </label>
                        <input
                            id="username"
                            type="text"
                            value={username}
                            onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                                setUsername(e.target.value)
                            }
                            style={{
                                width: "100%",
                                padding: "10px",
                                borderRadius: "6px",
                                border: "1px solid #ccc",
                                fontSize: "1rem",
                            }}
                            placeholder="Functionar sau Dev"
                        />
                    </div>

                    <div>
                        <label
                            htmlFor="password"
                            style={{
                                display: "block",
                                marginBottom: "5px",
                                fontWeight: "bold",
                            }}
                        >
                            Parolă
                        </label>
                        <input
                            id="password"
                            type="password"
                            value={password}
                            onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                                setPassword(e.target.value)
                            }
                            style={{
                                width: "100%",
                                padding: "10px",
                                borderRadius: "6px",
                                border: "1px solid #ccc",
                                fontSize: "1rem",
                            }}
                            placeholder="Introdu parola"
                        />
                    </div>

                    {error && (
                        <p
                            style={{
                                color: "#ffdddd",
                                backgroundColor: "#802020",
                                padding: "8px 10px",
                                borderRadius: "6px",
                                margin: 0,
                            }}
                        >
                            {error}
                        </p>
                    )}
                    {success && (
                        <p
                            style={{
                                color: "#ddffdd",
                                backgroundColor: "#206020",
                                padding: "8px 10px",
                                borderRadius: "6px",
                                margin: 0,
                            }}
                        >
                            {success}
                        </p>
                    )}

                    <button
                        type="submit"
                        disabled={loading}
                        style={{
                            marginTop: "10px",
                            padding: "10px 20px",
                            borderRadius: "8px",
                            border: "none",
                            backgroundColor: "#00CFFF",
                            color: "white",
                            fontSize: "1rem",
                            cursor: "pointer",
                            fontWeight: "bold",
                            opacity: loading ? 0.8 : 1,
                            transition: "0.2s",
                        }}
                    >
                        {loading ? "Se autentifică..." : "Login"}
                    </button>
                </form>
            </div>
        </div>
    );
};

export default LoginPage;
