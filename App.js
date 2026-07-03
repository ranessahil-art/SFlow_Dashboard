import DeviceCard from "./components/DeviceCard";
import TrafficChart from "./components/TrafficChart";
import DeltaTrafficChart from "./components/DeltaTrafficChart";
import PacketTable from "./components/PacketTable";
import StatsCard from "./components/StatsCard";
import DataRate from "./components/DataRate";
import MulticastChart from "./components/MulticastChart";
import BroadcastChart from "./components/BroadcastChart";
import EventLog from "./components/EventLog";
import Databps from "./components/Databps";
import CaptureControl from "./components/CaptureControl";
import { useState, useEffect } from "react";
import axios from "axios";

function App() {

    const [selectedDate, setSelectedDate] = useState("");
    const [selectedRange, setSelectedRange] = useState("24h");
    const [darkMode, setDarkMode] = useState(true);
    const [selectedDevice, setSelectedDevice] = useState("");
    const [devices, setDevices] = useState([]);
    const [viewMode, setViewMode] = useState("all");
    useEffect(() => {

    axios.get(
        "http://10.21.1.38:8000/devices_list"
    )
    .then(response => {

        setDevices(response.data);

    })
    .catch(error => {

        console.log(error);

    });

}, []);

    return (

        <div
            style={{
                textAlign: "center",
                minHeight: "100vh",
                background: darkMode
    ? "linear-gradient(135deg, #0f172a, #1e3a8a, #0f172a)"
    : "#f5f7fa",

color: darkMode ? "white" : "black",
                padding: "20px",
                fontFamily: "Arial, sans-serif"
            }}
        >

            <h1
                style={{
                    textAlign: "center",
                    marginBottom: "30px",
                    fontSize: "40px",
                    fontWeight: "bold"
                }}
            >
                sFlow Monitoring Dashboard
            </h1>

            <div
    style={{
        textAlign: "center",
        marginBottom: "20px"
    }}
>
    <button
        onClick={() => setDarkMode(!darkMode)}
        style={{
            padding: "10px 20px",
            borderRadius: "10px",
            border: "none",
            cursor: "pointer",
            fontWeight: "bold"
        }}
    >
        {darkMode ? "☀️ Light Mode" : "🌙 Dark Mode"}
    </button>
</div>

            <div
    style={{
        textAlign: "center",
        marginBottom: "20px"
    }}
>

    <label
    style={{
        color: darkMode ? "white" : "#111827",
        marginRight: "10px",
        fontSize: "18px",
        fontWeight: "bold"
    }}
>
        View Mode :
    </label>

    <select
    value={viewMode}
    onChange={(e) =>
        setViewMode(e.target.value)
    }
    style={{
        padding: "8px 12px",
        borderRadius: "8px",
        border: darkMode
            ? "1px solid #3b82f6"
            : "1px solid #94a3b8",
        backgroundColor: darkMode
            ? "#0f172a"
            : "#ffffff",
        color: darkMode
            ? "white"
            : "#111827",
        fontWeight: "bold",
        cursor: "pointer"
    }}
>

        <option value="all">
            All Data
        </option>

        <option value="date">
            Date Wise
        </option>

    </select>

    {
        viewMode === "date" && (

            <input
    type="date"
    value={selectedDate}
    onChange={(e) =>
        setSelectedDate(e.target.value)
    }
    style={{
        marginLeft: "15px",
        padding: "8px",
        borderRadius: "8px",
        border: darkMode
            ? "1px solid #3b82f6"
            : "1px solid #94a3b8",
        backgroundColor: "white",
        color: "black",
        cursor: "pointer"
    }}
/>
        )
    }

</div>

            <div
    style={{
        marginBottom: "20px"
    }}
>

    <label
    style={{
        color: darkMode ? "white" : "#111827",
        marginRight: "10px",
        fontWeight: "bold"
    }}
>
        Device :
    </label>

   <select
    value={selectedDevice}
    onChange={(e) =>
        setSelectedDevice(e.target.value)
    }
    style={{
        padding: "8px 12px",
        borderRadius: "8px",
        border: darkMode
            ? "1px solid #3b82f6"
            : "1px solid #94a3b8",
        backgroundColor: darkMode
            ? "#0f172a"
            : "#ffffff",
        color: darkMode
            ? "white"
            : "#111827",
        fontWeight: "bold",
        cursor: "pointer"
    }}
>

        <option value="">
            All Devices
        </option>

        {

            devices.map(device => (

                <option
                    key={device.id}
                    value={device.id}
                >

                    {device.hostname}

                </option>

            ))

        }

    </select>

</div>

            <StatsCard darkMode={darkMode} viewMode={viewMode} selectedDate={selectedDate} selectedDevice={selectedDevice}/>

            <EventLog darkMode={darkMode}/>

            <CaptureControl darkMode={darkMode}/>

            <div
    style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        gap: "25px",
        marginBottom: "30px",
        flexWrap: "wrap"
    }}
>

    {/* DATE FILTER */}
    <div>

        <label
            style={{
                fontSize: "18px",
                fontWeight: "bold",
                marginRight: "10px"
            }}
        >
            Graph Date :
        </label>

        <input
            type="date"
            value={selectedDate}
            onChange={(e) =>
                setSelectedDate(e.target.value)
            }
            style={{
                padding: "8px",
                borderRadius: "8px",
                border: "1px solid #3b82f6"
            }}
        />

    </div>

    {/* TIME RANGE FILTER */}
    <div>

        <label
            style={{
                fontSize: "18px",
                fontWeight: "bold",
                marginRight: "10px"
            }}
        >
            Time Window :
        </label>

        <select
            value={selectedRange}
            onChange={(e) =>
                setSelectedRange(e.target.value)
            }
            style={{
                padding: "8px 12px",
                borderRadius: "8px",
                border: "1px solid #3b82f6",
                cursor: "pointer"
            }}
        >

            {/* NEW: NO FILTER OPTION */}
            <option value="">
                No Time Filter
            </option>

            <option value="1h">
                Last 1 Hour
            </option>

            <option value="6h">
                Last 6 Hours
            </option>

            <option value="12h">
                Last 12 Hours
            </option>

            <option value="24h">
                Last 24 Hours
            </option>

        </select>

    </div>

</div>


            <TrafficChart darkMode={darkMode} selectedDate={selectedDate} selectedDevice={selectedDevice} selectedRange={selectedRange}/>

            <DeltaTrafficChart darkMode={darkMode} selectedDate={selectedDate} selectedDevice={selectedDevice} selectedRange={selectedRange}/>

            <DataRate darkMode={darkMode} selectedDate={selectedDate} selectedDevice={selectedDevice} selectedRange={selectedRange}/>

            <Databps darkMode={darkMode} selectedDate={selectedDate} selectedDevice={selectedDevice} selectedRange={selectedRange}/>

            <MulticastChart darkMode={darkMode} selectedDate={selectedDate} selectedDevice={selectedDevice} selectedRange={selectedRange}/>

            <BroadcastChart darkMode={darkMode} selectedDate={selectedDate} selectedDevice={selectedDevice} selectedRange={selectedRange}/>

            <DeviceCard darkMode={darkMode} viewMode={viewMode} selectedDate={selectedDate} selectedDevice={selectedDevice}/>

            <PacketTable darkMode={darkMode} viewMode={viewMode} selectedDate={selectedDate} selectedDevice={selectedDevice}/>

        </div>

    );

}

export default App;