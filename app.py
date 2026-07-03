from flask import Flask, jsonify,request,Response
from flask_cors import CORS
import psycopg2, json
from EventLogger import event_logs, event_queue, add_event
from datetime import timedelta
import subprocess
import os
import sys
import signal
pyshark_process = None
postgres_process = None

app = Flask(__name__)
CORS(app)

@app.route("/start_capture", methods=["POST"])
def start_capture():

    global pyshark_process
    global postgres_process

    if pyshark_process is None or pyshark_process.poll() is not None:

        pyshark_process = subprocess.Popen(

            [
                sys.executable,
                os.path.join(
                    os.path.dirname(__file__),
                    "SFlow_Pyshark.py"
                )
            ]

        )

    if postgres_process is None or postgres_process.poll() is not None:

        postgres_process = subprocess.Popen(

            [
                sys.executable,
                os.path.join(
                    os.path.dirname(__file__),
                    "SFlow_PostgreSQL.py"
                )
            ]

        )

    return jsonify(
        {
            "message": "Packet Capture Started Successfully"
        }
    )

@app.route("/stop_capture", methods=["POST"])
def stop_capture():

    global pyshark_process
    global postgres_process

    if pyshark_process and pyshark_process.poll() is None:

        pyshark_process.terminate()

        pyshark_process = None

    if postgres_process and postgres_process.poll() is None:

        postgres_process.terminate()

        postgres_process = None

    return jsonify(
        {
            "message": "Packet Capture Stopped Successfully"
        }
    )

@app.route("/device")
def get_device():
    selected_date = request.args.get("date")

    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        database="Sflow_db",
        user="postgres",
        password="Sahil"
    )

    cur = conn.cursor()

    if selected_date:

        cur.execute("""
            SELECT DISTINCT d.*
            FROM device d
            JOIN sflow_packets p
                ON d.id = p.device_id
            WHERE DATE(p.capture_time) = %s
            ORDER BY d.id ASC
        """, (selected_date,))


    else:

        cur.execute("""
                  SELECT DISTINCT d.*
                  FROM device d
                  JOIN sflow_packets p
                      ON d.id = p.device_id
                  ORDER BY d.id ASC
              """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    data = []

    for row in rows:
        data.append({
            "id": str(row[0]),
            "hostname": str(row[3]),
            "location": str(row[4]),
            "device_ip": str(row[5]),
            "software_version": str(row[8]),
            "serial_number": str(row[12]),
            "uptime": str(row[13])
        })

    return jsonify(data)

@app.route("/devices_list")
def get_devices_list():

    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        database="Sflow_db",
        user="postgres",
        password="Sahil"
    )

    cur = conn.cursor()

    cur.execute("""
        SELECT
            id,
            hostname
        FROM device
        ORDER BY hostname ASC
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    data = []

    for row in rows:

        data.append(
            {
                "id": row[0],
                "hostname": row[1]
            }
        )

    return jsonify(data)

@app.route("/traffic")
def get_traffic():

    selected_date = request.args.get("date")
    selected_range = request.args.get("range")
    if selected_range in [None, "", "undefined"]:
        selected_range = None

    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        database="Sflow_db",
        user="postgres",
        password="Sahil"
    )

    cur = conn.cursor()

    if selected_date:

        cur.execute(
            """
            SELECT
                capture_time,
                sflow_245_ifinoct,
                sflow_245_ifoutoct
            FROM sflow_packets
            WHERE DATE(capture_time) = %s
            ORDER BY packet_id ASC
            """,
            (selected_date,)
        )

    else:

        cur.execute(
            """
            SELECT
                capture_time,
                sflow_245_ifinoct,
                sflow_245_ifoutoct
            FROM sflow_packets
            ORDER BY packet_id ASC
            """
        )

    rows = cur.fetchall()

    start_time = None

    if selected_range and len(rows) > 0:

        latest_time = rows[-1][0]

        if selected_range == "1h":

            start_time = latest_time - timedelta(hours=1)

        elif selected_range == "6h":

            start_time = latest_time - timedelta(hours=6)

        elif selected_range == "12h":

            start_time = latest_time - timedelta(hours=12)

        elif selected_range == "24h":

            start_time = latest_time - timedelta(hours=24)

        rows = [

            row

            for row in rows

            if row[0] >= start_time

        ]

    traffic_data = []

    for row in rows:

        traffic_data.append(
            {
                "capture_time": str(row[0]),
                "ifinoct": row[1],
                "ifoutoct": row[2]
            }
        )

    cur.close()
    conn.close()

    return jsonify(traffic_data)

@app.route("/delta_traffic")
def get_delta_traffic():

    selected_date = request.args.get("date")
    selected_range = request.args.get("range")
    if selected_range in [None, "", "undefined"]:
        selected_range = None

    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        database="Sflow_db",
        user="postgres",
        password="Sahil"
    )

    cur = conn.cursor()

    if selected_date:

        cur.execute(
            """
            SELECT
                capture_time,
                sflow_delta_ifinoct,
                sflow_delta_ifoutoct
            FROM sflow_packets
            WHERE DATE(capture_time) = %s
            AND sflow_delta_ifinoct IS NOT NULL
            AND sflow_delta_ifoutoct IS NOT NULL
            ORDER BY packet_id ASC
            """,
            (selected_date,)
        )

    else:

        cur.execute(
            """
            SELECT
                capture_time,
                sflow_delta_ifinoct,
                sflow_delta_ifoutoct
            FROM sflow_packets
            WHERE sflow_delta_ifinoct IS NOT NULL
            AND sflow_delta_ifoutoct IS NOT NULL
            ORDER BY capture_time ASC
            """
        )

    rows = cur.fetchall()

    start_time = None

    if selected_range and len(rows) > 0:

        latest_time = rows[-1][0]

        if selected_range == "1h":

            start_time = latest_time - timedelta(hours=1)

        elif selected_range == "6h":

            start_time = latest_time - timedelta(hours=6)

        elif selected_range == "12h":

            start_time = latest_time - timedelta(hours=12)

        elif selected_range == "24h":

            start_time = latest_time - timedelta(hours=24)

        rows = [

            row

            for row in rows

            if row[0] >= start_time

        ]

    data = []

    for row in rows:

        data.append(
            {
                "capture_time": str(row[0]),
                "delta_ifinoct": row[1],
                "delta_ifoutoct": row[2]
            }
        )

    cur.close()
    conn.close()

    return jsonify(data)

@app.route("/data_bits")
def get_data_bits():
    selected_date = request.args.get("date")
    selected_range = request.args.get("range")
    if selected_range in [None, "", "undefined"]:
        selected_range = None

    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        database="Sflow_db",
        user="postgres",
        password="Sahil"
    )

    cur = conn.cursor()

    if selected_date:

        cur.execute(
            """
            SELECT
                capture_time,
                sflow_245_ifinoct,
                sflow_245_ifoutoct
            FROM sflow_packets
            WHERE DATE(capture_time) = %s
            ORDER BY packet_id ASC
            """,
            (selected_date,)
        )

    else:

        cur.execute(
            """
            SELECT
                capture_time,
                sflow_245_ifinoct,
                sflow_245_ifoutoct
            FROM sflow_packets
            ORDER BY packet_id ASC
            """
        )

    rows = cur.fetchall()

    start_time = None
    if selected_range and len(rows) > 0:

        latest_time = rows[-1][0]

        if selected_range == "1h":

            start_time = latest_time - timedelta(hours=1)

        elif selected_range == "6h":

            start_time = latest_time - timedelta(hours=6)

        elif selected_range == "12h":

            start_time = latest_time - timedelta(hours=12)

        elif selected_range == "24h":

            start_time = latest_time - timedelta(hours=24)

        rows = [

            row

            for row in rows

            if row[0] >= start_time

        ]


    data = []

    previous_time = None
    previous_ifinoct = None
    previous_ifoutoct = None
    start_time = None

    for row in rows:

        current_time = row[0]
        if start_time is None:
            start_time = current_time

        elapsed_seconds = (
                current_time - start_time
        ).total_seconds()
        current_ifinoct = row[1]
        current_ifoutoct = row[2]

        if current_ifinoct is None or current_ifoutoct is None:
            continue

        if previous_time is None:

                input_bits = current_ifinoct * 8
                output_bits = current_ifoutoct * 8

                data.append(
                    {
                        "capture_time": current_time.strftime("%Y-%m-%d %H:%M:%S"),
                        "input_bits": round(input_bits, 2),
                        "output_bits": round(output_bits, 2)
                    }
                )

        else:

                time_difference = (
                        current_time - previous_time
                ).total_seconds()

                if time_difference > 0:

                    delta_in = current_ifinoct - previous_ifinoct
                    delta_out = current_ifoutoct - previous_ifoutoct

                    if delta_in >= 0 and delta_out >= 0:
                        input_bits = delta_in * 8
                        output_bits = delta_out * 8

                        data.append(
                            {
                                "capture_time": current_time.strftime("%Y-%m-%d %H:%M:%S"),
                                "input_bits": round(input_bits, 2),
                                "output_bits": round(output_bits, 2)
                            }
                        )


        previous_time = current_time
        previous_ifinoct = current_ifinoct
        previous_ifoutoct = current_ifoutoct

    cur.close()
    conn.close()

    return jsonify(data)

@app.route("/data_bps")
def get_data_bps():

    selected_date = request.args.get("date")
    selected_range = request.args.get("range")
    if selected_range in [None, "", "undefined"]:
        selected_range = None

    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        database="Sflow_db",
        user="postgres",
        password="Sahil"
    )

    cur = conn.cursor()

    if selected_date:

        cur.execute(
            """
            SELECT
                capture_time,
                sflow_245_ifinoct,
                sflow_245_ifoutoct
            FROM sflow_packets
            WHERE DATE(capture_time) = %s
            ORDER BY packet_id ASC
            """,
            (selected_date,)
        )

    else:

        cur.execute(
            """
            SELECT
                capture_time,
                sflow_245_ifinoct,
                sflow_245_ifoutoct
            FROM sflow_packets
            ORDER BY packet_id ASC
            """
        )

    rows = cur.fetchall()

    start_time = None
    if selected_range and len(rows) > 0:

        latest_time = rows[-1][0]

        if selected_range == "1h":

            start_time = latest_time - timedelta(hours=1)

        elif selected_range == "6h":

            start_time = latest_time - timedelta(hours=6)

        elif selected_range == "12h":

            start_time = latest_time - timedelta(hours=12)

        elif selected_range == "24h":

            start_time = latest_time - timedelta(hours=24)

        rows = [

            row

            for row in rows

            if row[0] >= start_time

        ]

    data = []

    previous_time = None
    previous_ifinoct = None
    previous_ifoutoct = None

    for row in rows:

        current_time = row[0]
        current_ifinoct = row[1]
        current_ifoutoct = row[2]

        if (
            current_ifinoct is None or
            current_ifoutoct is None
        ):
            continue

        # First packet becomes the baseline
        if previous_time is None:

            previous_time = current_time
            previous_ifinoct = current_ifinoct
            previous_ifoutoct = current_ifoutoct

            continue

        time_difference = (
            current_time - previous_time
        ).total_seconds()

        if time_difference <= 0:

            previous_time = current_time
            previous_ifinoct = current_ifinoct
            previous_ifoutoct = current_ifoutoct

            continue

        delta_in = current_ifinoct - previous_ifinoct
        delta_out = current_ifoutoct - previous_ifoutoct

        # Ignore counter reset
        if delta_in < 0 or delta_out < 0:

            previous_time = current_time
            previous_ifinoct = current_ifinoct
            previous_ifoutoct = current_ifoutoct

            continue

        input_bps = (delta_in * 8) / time_difference
        output_bps = (delta_out * 8) / time_difference

        data.append({

            "capture_time": current_time.strftime("%Y-%m-%d %H:%M:%S"),

            "input_bps": round(input_bps, 2),

            "output_bps": round(output_bps, 2)

        })

        previous_time = current_time
        previous_ifinoct = current_ifinoct
        previous_ifoutoct = current_ifoutoct

    cur.close()
    conn.close()

    return jsonify(data)



@app.route("/multicast")
def get_multicast():

    selected_date = request.args.get("date")
    selected_range = request.args.get("range")
    if selected_range in [None, "", "undefined"]:
        selected_range = None

    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        database="Sflow_db",
        user="postgres",
        password="Sahil"
    )

    cur = conn.cursor()

    if selected_date:

        cur.execute(
            """
            SELECT
                capture_time,
                sflow_245_ifinmcast,
                sflow_245_ifoutmcast
            FROM sflow_packets
            WHERE DATE(capture_time) = %s
            ORDER BY packet_id ASC
            """,
            (selected_date,)
        )

    else:

        cur.execute(
            """
            SELECT
                capture_time,
                sflow_245_ifinmcast,
                sflow_245_ifoutmcast
            FROM sflow_packets
            ORDER BY packet_id ASC
            """
        )

    rows = cur.fetchall()
    start_time = None
    if selected_range and len(rows) > 0:

        latest_time = rows[-1][0]

        if selected_range == "1h":

            start_time = latest_time - timedelta(hours=1)

        elif selected_range == "6h":

            start_time = latest_time - timedelta(hours=6)

        elif selected_range == "12h":

            start_time = latest_time - timedelta(hours=12)

        elif selected_range == "24h":

            start_time = latest_time - timedelta(hours=24)

        rows = [

            row

            for row in rows

            if row[0] >= start_time

        ]

    data = []

    previous_in = None
    previous_out = None

    for row in rows:

        current_time = row[0]
        current_in = row[1]
        current_out = row[2]

        if current_in is None or current_out is None:
            continue

        if previous_in is not None and previous_out is not None:

            delta_in = current_in - previous_in
            delta_out = current_out - previous_out

            if delta_in >= 0 and delta_out >= 0:

                data.append(
                    {
                        "capture_time": str(current_time),
                        "input_mcast": delta_in,
                        "output_mcast": delta_out
                    }
                )

        previous_in = current_in
        previous_out = current_out

    cur.close()
    conn.close()

    return jsonify(data)

@app.route("/broadcast")
def get_broadcast():

    selected_date = request.args.get("date")
    selected_range = request.args.get("range")
    if selected_range in [None, "", "undefined"]:
        selected_range = None

    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        database="Sflow_db",
        user="postgres",
        password="Sahil"
    )

    cur = conn.cursor()

    if selected_date:

        cur.execute(
            """
            SELECT
                capture_time,
                sflow_245_ifinbcast,
                sflow_245_ifoutbcast
            FROM sflow_packets
            WHERE DATE(capture_time) = %s
            ORDER BY packet_id ASC
            """,
            (selected_date,)
        )

    else:

        cur.execute(
            """
            SELECT
                capture_time,
                sflow_245_ifinbcast,
                sflow_245_ifoutbcast
            FROM sflow_packets
            ORDER BY packet_id ASC
            """
        )

    rows = cur.fetchall()
    start_time = None
    if selected_range and len(rows) > 0:

        latest_time = rows[-1][0]

        if selected_range == "1h":

            start_time = latest_time - timedelta(hours=1)

        elif selected_range == "6h":

            start_time = latest_time - timedelta(hours=6)

        elif selected_range == "12h":

            start_time = latest_time - timedelta(hours=12)

        elif selected_range == "24h":

            start_time = latest_time - timedelta(hours=24)

        rows = [

            row

            for row in rows

            if row[0] >= start_time

        ]

    data = []

    previous_in = None
    previous_out = None

    for row in rows:

        current_time = row[0]
        current_in = row[1]
        current_out = row[2]

        if current_in is None or current_out is None:
            continue

        if previous_in is not None and previous_out is not None:

            delta_in = current_in - previous_in
            delta_out = current_out - previous_out

            if delta_in >= 0 and delta_out >= 0:

                data.append(
                    {
                        "capture_time": str(current_time),
                        "input_bcast": delta_in,
                        "output_bcast": delta_out
                    }
                )

        previous_in = current_in
        previous_out = current_out

    cur.close()
    conn.close()

    return jsonify(data)

@app.route("/packets")
def get_packets():
    selected_date = request.args.get("date")

    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        database="Sflow_db",
        user="postgres",
        password="Sahil"
    )

    cur = conn.cursor()

    if selected_date:

        cur.execute("""
            SELECT *
            FROM sflow_packets
            WHERE DATE(capture_time) = %s
            ORDER BY packet_id ASC
        """, (selected_date,))

    else:

        cur.execute("""
            SELECT *
            FROM sflow_packets
            ORDER BY packet_id ASC
        """)

    rows = cur.fetchall()

    columns = [
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
    ]

    data = []

    for row in rows:

        row_dict = {}

        for column, value in zip(columns, row):

            row_dict[column] = str(value)

        data.append(row_dict)

    cur.close()
    conn.close()

    return jsonify(data)

@app.route("/stats")
def get_stats():
    selected_date = request.args.get("date")

    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        database="Sflow_db",
        user="postgres",
        password="Sahil"
    )

    cur = conn.cursor()

    if selected_date:

        cur.execute("""
            SELECT COUNT(packet_id)
            FROM sflow_packets
            WHERE DATE(capture_time) = %s
        """, (selected_date,))

    else:

        cur.execute("""
            SELECT COUNT(packet_id)
            FROM sflow_packets
        """)
    total_packets = cur.fetchone()[0]

    if selected_date:

        cur.execute("""
            SELECT AVG(sflow_245_ifinoct)
            FROM sflow_packets
            WHERE DATE(capture_time) = %s
            AND sflow_245_ifinoct IS NOT NULL
        """, (selected_date,))

    else:

        cur.execute("""
            SELECT AVG(sflow_245_ifinoct)
            FROM sflow_packets
            WHERE sflow_245_ifinoct IS NOT NULL
        """)
    avg_ifinoct = cur.fetchone()[0]

    if selected_date:

        cur.execute("""
            SELECT AVG(sflow_245_ifoutoct)
            FROM sflow_packets
            WHERE DATE(capture_time) = %s
            AND sflow_245_ifoutoct IS NOT NULL
        """, (selected_date,))

    else:

        cur.execute("""
            SELECT AVG(sflow_245_ifoutoct)
            FROM sflow_packets
            WHERE sflow_245_ifoutoct IS NOT NULL
        """)
    avg_ifoutoct = cur.fetchone()[0]

    if selected_date:

        cur.execute("""
            SELECT AVG(sflow_delta_ifinoct)
            FROM sflow_packets
            WHERE DATE(capture_time) = %s
            AND sflow_delta_ifinoct IS NOT NULL
        """, (selected_date,))

    else:

        cur.execute("""
            SELECT AVG(sflow_delta_ifinoct)
            FROM sflow_packets
            WHERE sflow_delta_ifinoct IS NOT NULL
        """)
    avg_delta_ifinoct = cur.fetchone()[0]

    if selected_date:

        cur.execute("""
            SELECT AVG(sflow_delta_ifoutoct)
            FROM sflow_packets
            WHERE DATE(capture_time) = %s
            AND sflow_delta_ifoutoct IS NOT NULL
        """, (selected_date,))

    else:

        cur.execute("""
            SELECT AVG(sflow_delta_ifoutoct)
            FROM sflow_packets
            WHERE sflow_delta_ifoutoct IS NOT NULL
        """)
    avg_delta_ifoutoct = cur.fetchone()[0]

    cur.close()
    conn.close()

    return jsonify({

        "total_packets": total_packets,

        "avg_ifinoct": round(avg_ifinoct, 2) if avg_ifinoct else 0,
        "avg_ifoutoct": round(avg_ifoutoct, 2) if avg_ifoutoct else 0,
        "avg_delta_ifinoct": round(avg_delta_ifinoct, 2) if avg_delta_ifinoct else 0,
        "avg_delta_ifoutoct": round(avg_delta_ifoutoct, 2) if avg_delta_ifoutoct else 0

    })

@app.route("/events")
def get_events():

    return jsonify(event_logs)

@app.route("/log_event", methods=["GET","POST"])
def log_event():

    data = request.json

    add_event(
        data.get("severity", "Info"),
        data.get("event_type", "General"),
        data.get("message", "No message")
    )

    return {"status": "ok"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)