import { useEffect, useState, useRef } from "react";
import axios from "axios";
import Draggable from "react-draggable";

import {
    ResponsiveContainer,
    LineChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
} from "recharts";

function MulticastChart({selectedDate, selectedDevice, darkMode, selectedRange}) {

    const [traffic, setTraffic] = useState([]);
    const [zoomLevel, setZoomLevel] = useState(1);
    const nodeRef = useRef(null);
    const [legendPosition] = useState({
        x: 850,
        y: 20
    });

    const values = traffic.flatMap(item => [
        Number(item.ifinoct || 0),
        Number(item.ifoutoct || 0)
    ]);

    const actualMax =
    values.length > 0
        ? Math.max(...values)
        : 100;

    const maxValue =
    Math.ceil(actualMax / 100000) * 100000;

    const minValue =
        values.length > 0
            ? Math.min(...values)
            : 0;

    const center =
        (maxValue + minValue) / 2;

    const range =
        (maxValue - minValue) / zoomLevel;

    const yMax =
        center + range / 2;

    useEffect(() => {

        const fetchTraffic = () => {

            axios.get(
                `http://10.21.1.38:8000/multicast?date=${selectedDate}&range=${selectedRange}`
            )
                .then(response => {

                    setTraffic(response.data);

                })
                .catch(error => {

                    console.log(error);

                });

        };

        fetchTraffic();

        const interval = setInterval(fetchTraffic, 10000);

        return () => clearInterval(interval);

    }, [selectedDate, selectedDevice, darkMode, selectedRange]);

   if (!selectedDate) {

    return (

        <div
            style={{
                position: "relative",
                backgroundColor: darkMode
                    ? "#1e293b"
                    : "#ffffff",

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
                    color: darkMode
                        ? "#93c5fd"
                        : "#1e3a8a",

                    textAlign: "center"
                }}
            >
                Select a Date to View Traffic Graph
            </h2>

        </div>

    );

}

    return (

    <div
        style={{
            backgroundColor:
                darkMode
                    ? "#1e293b"
                    : "#ffffff",

            borderRadius: "15px",

            padding: "20px",

            marginBottom: "30px",

            border:
                darkMode
                    ? "1px solid #3b82f6"
                    : "1px solid #d1d5db",

            boxShadow:
                darkMode
                    ? "0 0 20px rgba(59,130,246,0.3)"
                    : "0 4px 15px rgba(0,0,0,0.1)"
        }}
    >
            <h2
                style={{
                    color: darkMode ? "#93c5fd" : "#1e3a8a",
                    marginBottom: "20px",
                    textAlign: "center"
                }}
            >
                Multicast Traffic Graph
            </h2>

            <div
                style={{
                    display: "flex",
                    justifyContent: "center",
                    gap: "15px",
                    marginBottom: "20px"
                }}
            >

                <button
                    onClick={() => setZoomLevel(zoomLevel * 2)}
                    style={{
                        padding: "8px 15px",
                        borderRadius: "8px",
                        cursor: "pointer"
                    }}
                >
                    🔍 Zoom In
                </button>

                <button
                    onClick={() =>
                        setZoomLevel(
                            Math.max(1, zoomLevel / 2)
                        )
                    }
                    style={{
                        padding: "8px 15px",
                        borderRadius: "8px",
                        cursor: "pointer"
                    }}
                >
                    🔎 Zoom Out
                </button>

                <button
                    onClick={() => setZoomLevel(1)}
                    style={{
                        padding: "8px 15px",
                        borderRadius: "8px",
                        cursor: "pointer"
                    }}
                >
                    ↺ Reset
                </button>

            </div>

            <Draggable
                nodeRef={nodeRef}
                defaultPosition={legendPosition}
            >

                 <div
                     ref={nodeRef}
                    style={{
                         position: "absolute",
                         zIndex: 1000,
                         backgroundColor: darkMode ? "#0f172a" : "#ffffff",
                         border: "1px solid #3b82f6",
                         borderRadius: "8px",
                         padding: "10px",
                         cursor: "move",
                         color: darkMode ? "white" : "#111827",
                         userSelect: "none"
                    }}
                 >

                 <div
                    style={{
                         color: "#ef4444",
                         marginBottom: "5px"
                    }}
                 >
                    ─ Incoming Multicast Packets
                 </div>

                 <div
                    style={{
                         color: "#f97316"
                    }}
                 >
                     ─ Outgoing Multicast Packets
                 </div>

                 </div>

           </Draggable>

           <div
             style={{
                  width: "100%",
                  margin: "0 auto"
             }}
          >
            </div>

             <ResponsiveContainer
                width="90%"
                height={450}
            >

            <LineChart
                width={1100}
                height={450}
                data={traffic}
                margin={{
                    top: 40,
                    right: 40,
                    left: 50,
                    bottom: 30
                }}
            >

                <CartesianGrid
                    strokeDasharray="3 3"
                    stroke="#475569"
                />

                <XAxis
                    dataKey="capture_time"
                    label={{
                        value: "Time",
                        position: "insideBottom",
                        offset: -10,
                        fill: darkMode ? "white" : "#374151",
                        fontSize: 20,
                        fontWeight: "bold"
                    }}
                    tick={{
                        fill: darkMode ? "white" : "#374151",
                        fontSize: 11
                    }}
                    tickFormatter={(value) => value.substring(11, 19)}
                />

                <YAxis
                    domain={[0, yMax]}
                    width={80}
                    label={{
                        value: "Difference in Multicast Packets",
                        angle: -90,
                        position: "insideLeft",
                        fill: darkMode ? "white" : "#374151",
                        fontSize: 20,
                        fontWeight: "bold"
                    }}
                    tick={{
                        fill: darkMode ? "white" : "#374151",
                        fontSize: 12
                    }}
                />

                <Tooltip
                    contentStyle={{
                        backgroundColor: "#0f172a",
                        border: "1px solid #3b82f6",
                        borderRadius: "8px",
                        color: "white"
                    }}
                />

                <Line
                    type="monotone"
                    dataKey="input_mcast"
                    stroke="#ef4444"
                    strokeWidth={3}
                    dot={{ r: 4 }}
                    activeDot={{ r: 7 }}
                    name="Incoming Multicast Packets"
                />

                <Line
                    type="monotone"
                    dataKey="output_mcast"
                    stroke="#f97316"
                    strokeWidth={3}
                    dot={{ r: 4 }}
                    activeDot={{ r: 7 }}
                    name="Outgoing Multicast Packets"
                />

            </LineChart>
             </ResponsiveContainer>

        </div>

    );

}

export default MulticastChart;