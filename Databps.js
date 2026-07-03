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

function DataRateBps({ selectedDate, selectedDevice, darkMode, selectedRange }) {

    const [traffic, setTraffic] = useState([]);
    const [zoomLevel, setZoomLevel] = useState(1);

    const [unit, setUnit] = useState("bps");

    const nodeRef = useRef(null);

    const [legendPosition] = useState({
        x: 850,
        y: 20
    });

    let divisor = 1;

    if (unit === "kbps") {

        divisor = 1000;

    }

    else if (unit === "mbps") {

        divisor = 1000000;

    }

    else if (unit === "gbps") {

        divisor = 1000000000;

    }

    useEffect(() => {

        const fetchTraffic = () => {

            axios.get(
                `http://10.21.1.38:8000/data_bps?date=${selectedDate}&range=${selectedRange}`
            )

            .then(response => {

                setTraffic(response.data);

            })

            .catch(error => {

                console.log(error);

            });

        };

        fetchTraffic();

        const interval = setInterval(
            fetchTraffic,
            10000
        );

        return () => clearInterval(interval);

    }, [selectedDate, selectedDevice, darkMode, selectedRange]);

    const graphData = traffic.map(item => ({

        ...item,

        input_display:
            Number(item.input_bps || 0) / divisor,

        output_display:
            Number(item.output_bps || 0) / divisor

    }));

    const values = graphData.flatMap(item => [

        Number(item.input_display || 0),

        Number(item.output_display || 0)

    ]);

    const actualMax =

        values.length > 0

            ? Math.max(...values)

            : 100;

    const maxValue =
    actualMax * 1.1;

    const minValue =

        values.length > 0

            ? Math.min(...values)

            : 0;

    const center =

        (maxValue + minValue) / 2;

    const range =

        (maxValue - minValue) / zoomLevel;

    const yMax =
    maxValue / zoomLevel;

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
                    Select a Date to View Data Rate Graph
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
                    color: darkMode
                        ? "#93c5fd"
                        : "#1e3a8a",

                    marginBottom: "20px",

                    textAlign: "center"
                }}
            >
                Interface Data Rate
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
                    onClick={() =>
                        setZoomLevel(
                            zoomLevel * 2
                        )
                    }
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
                            Math.max(
                                1,
                                zoomLevel / 2
                            )
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
                    onClick={() =>
                        setZoomLevel(1)
                    }
                    style={{
                        padding: "8px 15px",
                        borderRadius: "8px",
                        cursor: "pointer"
                    }}
                >
                    ↺ Reset
                </button>

            </div>

            <div
                style={{
                    display: "flex",
                    justifyContent: "center",
                    alignItems: "center",
                    gap: "10px",
                    marginBottom: "20px"
                }}
            >

                <label
                    style={{
                        color: darkMode
                            ? "white"
                            : "#111827",

                        fontWeight: "bold"
                    }}
                >
                    Unit :
                </label>

                <select
                    value={unit}
                    onChange={(e) =>
                        setUnit(
                            e.target.value
                        )
                    }
                    style={{
                        padding: "8px",
                        borderRadius: "8px"
                    }}
                >

                    <option value="bps">
                        Bits/sec
                    </option>

                    <option value="kbps">
                        Kbps
                    </option>

                    <option value="mbps">
                        Mbps
                    </option>

                    <option value="gbps">
                        Gbps
                    </option>

                </select>

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
                        backgroundColor: darkMode
                            ? "#0f172a"
                            : "#ffffff",

                        border: "1px solid #3b82f6",

                        borderRadius: "8px",

                        padding: "10px",

                        cursor: "move",

                        color: darkMode
                            ? "white"
                            : "#111827",

                        userSelect: "none"
                    }}
                >

                    <div
                        style={{
                            color: "#ef4444",
                            marginBottom: "5px"
                        }}
                    >
                        ─ Input Data Rate
                    </div>

                    <div
                        style={{
                            color: "#f97316"
                        }}
                    >
                        ─ Output Data Rate
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

                    data={graphData}

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

                        tickFormatter={(value) =>
                            value.substring(11, 19)
                        }

                        label={{
                            value: "Time",
                            position: "insideBottom",
                            offset: -10,
                            fill: darkMode
                                ? "white"
                                : "#374151",

                            fontSize: 20,
                            fontWeight: "bold"
                        }}

                        tick={{
                            fill: darkMode
                                ? "white"
                                : "#374151",

                            fontSize: 11
                        }}

                    />

                    <YAxis

                        domain={[0, yMax]}

                        width={100}

                        label={{

                            value:

                                unit === "bps"

                                    ? "Change in Bits (bits/sec)"

                                    : unit === "kbps"

                                    ? "Change in Bits (Kbits/sec)"

                                    : unit === "mbps"

                                    ? "Change in Bits (Mbits/sec)"

                                    : "Change in Bits (Gbits/sec)",

                            angle: -90,

                            position: "center",

                            fill: darkMode
                                ? "white"
                                : "#374151",

                            fontSize: 18,

                            fontWeight: "bold"

                        }}

                        tick={{

                            fill: darkMode
                                ? "white"
                                : "#374151",

                            fontSize: 12

                        }}

                    />

                    <Tooltip

                        contentStyle={{

                            backgroundColor: darkMode
                                ? "#0f172a"
                                : "#ffffff",

                            border: "1px solid #3b82f6",

                            borderRadius: "8px",

                            color: darkMode
                                ? "white"
                                : "#111827"

                        }}

                        formatter={(value) => [

                            value.toFixed(2) + " " + unit,

                            ""

                        ]}

                    />

                            <Line

                        type="monotone"

                        dataKey="input_display"

                        stroke="#ef4444"

                        strokeWidth={3}

                        dot={{ r: 4 }}

                        activeDot={{ r: 7 }}

                        name="Input Data Rate"

                    />

                    <Line

                        type="monotone"

                        dataKey="output_display"

                        stroke="#f97316"

                        strokeWidth={3}

                        dot={{ r: 4 }}

                        activeDot={{ r: 7 }}

                        name="Output Data Rate"

                    />

                </LineChart>

            </ResponsiveContainer>

        </div>

    );

}

export default DataRateBps;