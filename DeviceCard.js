import { useEffect, useState } from "react";
import axios from "axios";

function DeviceCard({viewMode, selectedDate, selectedDevice}) {

    const [devices, setDevices] = useState([]);

    useEffect(() => {

        const fetchDevice = () => {

           let url = "http://10.21.1.38:8000/device";

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

                    setDevices(response.data);

                })
                .catch(error => {

                    console.log(error);

                });

        };

        fetchDevice();

        const interval = setInterval(fetchDevice, 10000);

        return () => clearInterval(interval);

    }, [viewMode, selectedDate, selectedDevice]);

    if (devices.length === 0) {

        return <h2>Loading Device Data...</h2>;

    }

    return (

        <div>

            <h2>Device Information</h2>

            <div
                style={{
                    overflowX: "auto",
                    overflowY: "auto",
                    maxHeight: "400px",
                    border: "1px solid black"
                }}
            >

                <table
                    border="1"
                    cellPadding="5"
                    style={{
                        borderCollapse: "collapse",
                        whiteSpace: "nowrap",
                        minWidth: "100%"
                    }}
                >

                    <thead>

                        <tr>

                            <th>ID</th>
                            <th>Hostname</th>
                            <th>Location</th>
                            <th>Device IP</th>
                            <th>Software Version</th>
                            <th>Serial Number</th>
                            <th>Uptime</th>

                        </tr>

                    </thead>

                    <tbody>

                        {
                            devices.map((device, index) => (

                                <tr key={index}>

                                    <td>{device.id}</td>
                                    <td>{device.hostname}</td>
                                    <td>{device.location}</td>
                                    <td>{device.device_ip}</td>
                                    <td>{device.software_version}</td>
                                    <td>{device.serial_number}</td>
                                    <td>{device.uptime}</td>

                                </tr>

                            ))
                        }

                    </tbody>

                </table>

            </div>

        </div>

    );

}

export default DeviceCard;