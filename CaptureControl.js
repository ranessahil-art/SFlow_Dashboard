import axios from "axios";
import { useState } from "react";

function CaptureControl({ darkMode }) {

    const [status, setStatus] = useState("Stopped");

    const startCapture = () => {

        axios.post("http://10.21.1.38:8000/start_capture")

            .then((response) => {

                alert(response.data.message);

                setStatus("Running");

            })

            .catch((error) => {

                console.log(error);

                alert("Failed to Start Capture");

            });

    };

    const stopCapture = () => {

        axios.post("http://10.21.1.38:8000/stop_capture")

            .then((response) => {

                alert(response.data.message);

                setStatus("Stopped");

            })

            .catch((error) => {

                console.log(error);

                alert("Failed to Stop Capture");

            });

    };

    return (

        <div
            style={{
                backgroundColor: darkMode ? "#1e293b" : "#ffffff",
                borderRadius: "15px",
                padding: "20px",
                marginBottom: "30px",
                border: darkMode
                    ? "1px solid #3b82f6"
                    : "1px solid #d1d5db",
                boxShadow: darkMode
                    ? "0 0 20px rgba(59,130,246,0.3)"
                    : "0 4px 15px rgba(0,0,0,0.1)"
            }}
        >

            <h2
                style={{
                    textAlign: "center",
                    color: darkMode ? "#93c5fd" : "#1e3a8a"
                }}
            >
                Packet Capture Control
            </h2>

            <h3
                style={{
                    textAlign: "center",
                    color: status === "Running"
                        ? "#22c55e"
                        : "#ef4444"
                }}
            >
                Status : {status}
            </h3>

            <div
                style={{
                    display: "flex",
                    justifyContent: "center",
                    gap: "20px",
                    marginTop: "25px"
                }}
            >

                <button

                    onClick={startCapture}

                    style={{
                        padding: "12px 25px",
                        fontSize: "16px",
                        cursor: "pointer",
                        borderRadius: "10px"
                    }}

                >
                    ▶ Start Capture
                </button>

                <button

                    onClick={stopCapture}

                    style={{
                        padding: "12px 25px",
                        fontSize: "16px",
                        cursor: "pointer",
                        borderRadius: "10px"
                    }}

                >
                    ■ Stop Capture
                </button>

            </div>

        </div>

    );

}

export default CaptureControl;