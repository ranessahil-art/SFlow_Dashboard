import { useEffect, useState } from "react";
import axios from "axios";

function PacketTable({darkMode, viewMode, selectedDate, selectedDevice}) {

    const [packets, setPackets] = useState([]);

    const columns = [
        "packet_id",
        "device_id",
        "capture_time",

        "sflow_245_version",
        "sflow_245_agenttype",
        "sflow_245_agent",
        "sflow_245_sequence_number",
        "sflow_245_sysuptime",
        "sflow_delta_sysuptime",
        "sflow_245_numsamples",

        "sflow_245_sampletype",

        "counters_sample_sequence_number",
        "counters_sample_source_id_class",
        "counters_sample_index",
        "counters_sample_sampling_interval",
        "counters_sample_counters_type",

        "sflow_245_ifindex",
        "sflow_245_iftype",
        "sflow_245_ifspeed",
        "sflow_245_ifdirection",
        "sflow_245_ifadmin_status",
        "sflow_245_ifoper_status",

        "sflow_245_ifinoct",
        "sflow_delta_ifinoct",
        "sflow_245_ifinpkt",
        "sflow_delta_ifinpkt",
        "sflow_245_ifinmcast",
        "sflow_245_ifinbcast",
        "sflow_245_ifindisc",
        "sflow_245_ifinerr",
        "sflow_245_ifinunk",

        "sflow_245_ifoutoct",
        "sflow_delta_ifoutoct",
        "sflow_245_ifoutpkt",
        "sflow_delta_ifoutpkt",
        "sflow_245_ifoutmcast",
        "sflow_245_ifoutbcast",
        "sflow_245_ifoutdisc",
        "sflow_245_ifouterr",
        "sflow_245_ifpromisc"
    ];

    useEffect(() => {

    const fetchPackets = () => {

        let url = "http://10.21.1.38:8000/packets";

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

                setPackets(response.data);

            })
            .catch(error => {

                console.log(error);

            });

    };

    fetchPackets();

    const interval = setInterval(fetchPackets, 10000);

    return () => clearInterval(interval);

}, [viewMode, selectedDate, selectedDevice]);

    return (

        <div>

            <h2>Packet Records</h2>

            <div
                style={{
                    overflowX: "auto",
                    overflowY: "auto",
                    maxHeight: "500px",
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

                            {
                                columns.map((column) => (

                                    <th
                                        key={column}
                                        style={{
                                            position: "sticky",
                                            top: 0,

                                        }}
                                    >
                                        {column}
                                    </th>

                                ))
                            }

                        </tr>

                    </thead>

                    <tbody>

                        {
                            packets.map((packet, index) => (

                                <tr key={index}>

                                    {
                                        columns.map((column) => (

                                            <td key={column}>
                                                {String(packet[column])}
                                            </td>

                                        ))
                                    }

                                </tr>

                            ))
                        }

                    </tbody>

                </table>

            </div>

        </div>

    );

}

export default PacketTable;