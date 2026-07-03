import { useEffect, useState } from "react";
import axios from "axios";

function EventLog({ darkMode }) {

    const [events, setEvents] = useState([]);

    useEffect(() => {

        const fetchEvents = () => {

            axios.get("http://10.21.1.38:8000/events")
                .then(res => {

                    setEvents(res.data);

                })
                .catch(err => {

                    console.log(err);

                });

        };

        fetchEvents();

        const interval = setInterval(fetchEvents, 3000);

        return () => clearInterval(interval);

    }, []);

    return (

        <div
            style={{
                backgroundColor: darkMode ? "#1e293b" : "#ffffff",
                color: darkMode ? "white" : "#111827",
                padding: "15px",
                borderRadius: "12px",
                border: "1px solid #3b82f6",
                boxShadow: darkMode
                    ? "0 0 20px rgba(59,130,246,0.25)"
                    : "0 6px 15px rgba(0,0,0,0.12)",
                marginBottom: "20px"
            }}
        >

            <h2
                style={{
                    textAlign: "center",
                    marginBottom: "18px",
                    color: darkMode ? "#ffffff" : "#1e3a8a",
                    fontSize: "28px",
                    fontWeight: "bold"
                }}
            >
                📡 Recent Network Events
            </h2>

            {

                events.length === 0 ?

                (

                    <p
                        style={{
                            textAlign: "center",
                            fontSize: "17px"
                        }}
                    >
                        No Events Yet
                    </p>

                )

                :

                (

                    events.map((e, i) => {

                        let borderColor = "#3b82f6";
                        let severityColor = "#3b82f6";
                        let icon = "📦";

                        if (e.event_type === "Packet Processing") {

                            icon = "📦";

                        }

                        else if (e.event_type === "Device Restart") {

                            icon = "🔄";
                            borderColor = "#f59e0b";
                            severityColor = "#f59e0b";

                        }

                        else if (e.event_type === "Counter Reset") {

                            icon = "⚠️";
                            borderColor = "#f59e0b";
                            severityColor = "#f59e0b";

                        }

                        else if (e.event_type === "High Traffic") {

                            icon = "🚨";
                            borderColor = "#ef4444";
                            severityColor = "#ef4444";

                        }

                        else if (e.event_type === "New Device") {

                            icon = "🖥️";
                            borderColor = "#22c55e";
                            severityColor = "#22c55e";

                        }

                        return (

                            <div
                                key={i}
                                style={{
                                    marginBottom: "10px",
                                    padding: "12px 16px",
                                    borderLeft: `5px solid ${borderColor}`,
                                    borderRadius: "8px",
                                    backgroundColor: darkMode ? "#0f172a" : "#f8fafc",
                                    boxShadow: darkMode
                                        ? "0 0 8px rgba(0,0,0,0.35)"
                                        : "0 2px 6px rgba(0,0,0,0.12)"
                                }}
                            >

                                <div
                                    style={{
                                        display: "flex",
                                        justifyContent: "space-between",
                                        alignItems: "center",
                                        marginBottom: "8px"
                                    }}
                                >

                                    <div
                                        style={{
                                            fontSize: "17px",
                                            fontWeight: "bold"
                                        }}
                                    >
                                        {icon} {e.event_type}
                                    </div>

                                    <div
                                        style={{
                                            fontSize: "12px",
                                            color: "#94a3b8"
                                        }}
                                    >
                                        {e.time}
                                    </div>

                                </div>

                                <div
                                    style={{
                                        fontSize: "14px",
                                        marginBottom: "6px",
                                        color: darkMode ? "#d1d5db" : "#374151"
                                    }}
                                >
                                    <b>Message :</b> {e.message}
                                </div>

                                <div
                                    style={{
                                        fontSize: "13px",
                                        fontWeight: "bold",
                                        color: severityColor
                                    }}
                                >
                                    Severity : {e.severity.toUpperCase()}
                                </div>

                            </div>

                        );

                    })

                )

            }

        </div>

    );

}

export default EventLog;