import { useEffect, useState } from "react";
import axios from "axios";

function StatsCard({viewMode, selectedDate, selectedDevice, darkMode}) {

    const [stats, setStats] = useState({});

    useEffect(() => {

        const fetchStats = () => {

        let url = "http://10.21.1.38:8000/stats";

const params = [];

if (
    viewMode === "date" &&
    selectedDate
)
{
    params.push(
        `date=${selectedDate}`
    );
}

if (selectedDevice)
{
    params.push(
        `device=${selectedDevice}`
    );
}

if (params.length > 0)
{
    url += "?" + params.join("&");
}

axios.get(url)
                .then(response => {

                    setStats(response.data);

                })
                .catch(error => {

                    console.log(error);

                });

        };

        fetchStats();

        const interval = setInterval(fetchStats, 10000);

        return () => clearInterval(interval);

    }, [viewMode, selectedDate, selectedDevice, darkMode]);

    const cardStyle = {
    backgroundColor: darkMode ? "#1e293b" : "#ffffff",

    borderRadius: "15px",
    padding: "20px",
    minWidth: "220px",
    textAlign: "center",

    color: darkMode ? "white" : "#111827",

    border: darkMode
        ? "1px solid #3b82f6"
        : "1px solid #e5e7eb",

    boxShadow: darkMode
        ? "0 0 20px rgba(59,130,246,0.4)"
        : "0 4px 12px rgba(0,0,0,0.08)",

    transition: "0.3s"
};

    const titleStyle = {

        marginBottom: "12px",
        color: darkMode ? "#93c5fd" : "#1e3a8a",
        fontSize: "16px"

    };

    const valueStyle = {

        margin: "0",
        fontSize: "32px",
        fontWeight: "bold",
        color: darkMode ? "#ffffff" : "#111827"

    };

    return (

        <div
            style={{
                display: "flex",
                gap: "20px",
                flexWrap: "wrap",
                marginBottom: "30px",
                justifyContent: "center"
            }}
        >

            <div style={cardStyle}>
                <h3 style={titleStyle}>Total sFlow Packets</h3>
                <h1 style={valueStyle}>{stats.total_packets}</h1>
            </div>

            <div style={cardStyle}>
                <h3 style={titleStyle}>Average Input Octets</h3>
                <h1 style={valueStyle}>{stats.avg_ifinoct}</h1>
            </div>

            <div style={cardStyle}>
                <h3 style={titleStyle}>Average Output Octets</h3>
                <h1 style={valueStyle}>{stats.avg_ifoutoct}</h1>
            </div>

            <div style={cardStyle}>
                <h3 style={titleStyle}>Average Delta Input</h3>
                <h1 style={valueStyle}>{stats.avg_delta_ifinoct}</h1>
            </div>

            <div style={cardStyle}>
                <h3 style={titleStyle}>Average Delta Output</h3>
                <h1 style={valueStyle}>{stats.avg_delta_ifoutoct}</h1>
            </div>

        </div>

    );

}

export default StatsCard;