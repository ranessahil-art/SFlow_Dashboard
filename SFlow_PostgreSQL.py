import asyncio

asyncio.set_event_loop(asyncio.new_event_loop())

import pyshark
import psycopg2
import requests
import joblib
import pandas as pd
import os

from datetime import datetime
from collections import deque

from Sflow_Device_SQL import insert_device
from EventLogger import add_event

# --------------------------------------------------
# PostgreSQL Connection
# --------------------------------------------------

conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="Sflow_db",
    user="postgres",
    password="Sahil"
)

cur = conn.cursor()

# --------------------------------------------------
# Machine Learning
# --------------------------------------------------


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "ML_DDOS_Project",
    "Models",
    "ddos_final_model.pkl"
)

model = joblib.load(MODEL_PATH)

model = joblib.load(MODEL_PATH)

print("Random Forest Model Loaded Successfully")

WINDOW_SIZE = 5

ml_buffer = deque(maxlen=WINDOW_SIZE)

last_prediction = 0


# --------------------------------------------------
# Helper Function
# --------------------------------------------------

def get_field(pkt, field):
    try:

        value = pkt.sflow.get_field_value(field)

        if value is None or value == "":
            return None

        return value

    except:
        return None


# --------------------------------------------------
# PyShark Configuration
# --------------------------------------------------

INTERFACE = "Ethernet"

SFLOW_PORT = 6343

capture = pyshark.LiveCapture(
    interface=INTERFACE,
    bpf_filter=f"udp port {SFLOW_PORT}"
)

print(f"Listening for sFlow packets on UDP port {SFLOW_PORT}...")
print(f"Interface : {INTERFACE}")

requests.post("http://10.21.1.38:8000/log_event", json={
    "severity": "Info",
    "event_type": "Packet Processing",
    "message": "sFlow packet capturing started"
})

# --------------------------------------------------
# Main Loop
# --------------------------------------------------

for pkt in capture.sniff_continuously():

    try:

        capture_time = datetime.now()

        print("\n" + "=" * 100)
        print("sFlow Packet Received")
        print("=" * 100)

        print("Time :", capture_time)

        if hasattr(pkt, "sflow"):

            version = get_field(pkt, "sflow_245_version")
            agenttype = get_field(pkt, "sflow_245_agenttype")
            agent = get_field(pkt, "sflow_245_agent")
            sequence = get_field(pkt, "sflow_245_sequence_number")
            sysuptime = get_field(pkt, "sflow_245_sysuptime")
            numsamples = get_field(pkt, "sflow_245_numsamples")

            sampletype = get_field(pkt, "sflow_245_sampletype")

            counter_seq = get_field(pkt, "counters_sample_sequence_number")
            source_class = get_field(pkt, "counters_sample_source_id_class")
            counter_index = get_field(pkt, "counters_sample_index")
            sampling_interval = get_field(pkt, "counters_sample_sampling_interval")
            counter_type = get_field(pkt, "counters_sample_counters_type")

            ifindex = get_field(pkt, "sflow_245_ifindex")
            iftype = get_field(pkt, "sflow_245_iftype")
            ifspeed = get_field(pkt, "sflow_245_ifspeed")
            ifdirection = get_field(pkt, "sflow_245_ifdirection")
            ifadmin = get_field(pkt, "sflow_245_ifadmin_status")
            ifoper = get_field(pkt, "sflow_245_ifoper_status")

            ifinoct = get_field(pkt, "sflow_245_ifinoct")
            ifinpkt = get_field(pkt, "sflow_245_ifinpkt")
            ifinmcast = get_field(pkt, "sflow_245_ifinmcast")
            ifinbcast = get_field(pkt, "sflow_245_ifinbcast")
            ifindisc = get_field(pkt, "sflow_245_ifindisc")
            ifinerr = get_field(pkt, "sflow_245_ifinerr")
            ifinunk = get_field(pkt, "sflow_245_ifinunk")

            ifoutoct = get_field(pkt, "sflow_245_ifoutoct")
            ifoutpkt = get_field(pkt, "sflow_245_ifoutpkt")
            ifoutmcast = get_field(pkt, "sflow_245_ifoutmcast")
            ifoutbcast = get_field(pkt, "sflow_245_ifoutbcast")
            ifoutdisc = get_field(pkt, "sflow_245_ifoutdisc")
            ifouterr = get_field(pkt, "sflow_245_ifouterr")
            ifpromisc = get_field(pkt, "sflow_245_ifpromisc")

            # ----------------------------------------------
            # Delta Calculations
            # ----------------------------------------------

            delta_sysuptime = None
            delta_ifinoct = None
            delta_ifinpkt = None
            delta_ifoutoct = None
            delta_ifoutpkt = None

            device_id = insert_device()

            cur.execute(
                """
                SELECT
                    sflow_245_sysuptime,
                    sflow_245_ifinoct,
                    sflow_245_ifinpkt,
                    sflow_245_ifoutoct,
                    sflow_245_ifoutpkt
                FROM sflow_packets
                WHERE device_id = %s
                ORDER BY packet_id DESC
                """,
                (device_id,)
            )

            previous = cur.fetchone()
            restart_detected = False

            if previous:

                try:

                    previous_sysuptime = int(previous[0])
                    current_sysuptime = int(sysuptime)

                    if current_sysuptime < previous_sysuptime:
                        restart_detected = True

                        requests.post(
                            "http://10.21.1.38:8000/log_event",
                            json={
                                "severity": "Warning",
                                "event_type": "Device Restart",
                                "message": "Switch restarted. New baseline created."
                            }
                        )

                except:
                    pass


            if previous:

                try:
                    delta_sysuptime = int(sysuptime) - int(previous[0])

                except:
                    pass

                try:

                    if restart_detected:

                        delta_ifinoct = None

                    else:

                        delta_ifinoct = int(ifinoct) - int(previous[1])

                except:
                    pass
                if (
                        delta_ifinoct is not None and
                        delta_ifinoct > 1000000
                ):
                    requests.post("http://10.21.1.38:8000/log_event", json={
                        "Critical",
                        "High Traffic",
                        f"High input traffic detected ({delta_ifinoct} octets)."
                    })

                try:

                    if restart_detected:

                        delta_ifinpkt = None

                    else:

                        delta_ifinpkt = int(ifinpkt) - int(previous[2])

                except:
                    pass

                try:

                    if restart_detected:

                        delta_ifoutoct = None

                    else:

                        delta_ifoutoct = int(ifoutoct) - int(previous[3])

                except:
                    pass

                if (
                        delta_ifoutoct is not None and
                        delta_ifoutoct > 1000000
                ):
                    requests.post("http://10.21.1.38:8000/log_event", json={
                        "Critical",
                        "High Traffic",
                        f"High output traffic detected ({delta_ifinoct} octets)."
                    })

                try:

                    if restart_detected:

                        delta_ifoutpkt = None

                    else:

                        delta_ifoutpkt = int(ifoutpkt) - int(previous[4])

                except:
                    pass

            # --------------------------------------------------
            # Build ML Feature Vector
            # --------------------------------------------------

            ml_sample = None

            if (

                    delta_sysuptime is not None and
                    delta_sysuptime > 0 and

                    delta_ifinoct is not None and
                    delta_ifinpkt is not None and

                    delta_ifoutoct is not None and
                    delta_ifoutpkt is not None

            ):

                # Convert milliseconds to seconds
                duration_seconds = delta_sysuptime / 1000.0

                ml_sample = {

                    "Flow Duration": duration_seconds,

                    "Tot Fwd Pkts": delta_ifinpkt,
                    "Tot Bwd Pkts": delta_ifoutpkt,

                    "TotLen Fwd Pkts": delta_ifinoct,
                    "TotLen Bwd Pkts": delta_ifoutoct,

                    "Flow Byts/s":
                        (delta_ifinoct + delta_ifoutoct) / duration_seconds,

                    "Flow Pkts/s":
                        (delta_ifinpkt + delta_ifoutpkt) / duration_seconds,

                    "Fwd Pkts/s":
                        delta_ifinpkt / duration_seconds,

                    "Bwd Pkts/s":
                        delta_ifoutpkt / duration_seconds

                }

                print("\nML FEATURES")

                for key, value in ml_sample.items():
                    print(f"{key:20} : {value}")

                # ------------------------------------
                # Store sample in rolling buffer
                # ------------------------------------

                ml_buffer.append(ml_sample)

                print(f"\nWindow Buffer : {len(ml_buffer)}/{WINDOW_SIZE}")

                if len(ml_buffer) < WINDOW_SIZE:

                    print("Waiting for enough samples...\n")

                else:

                    print("Window Ready!")

                    # ----------------------------------
                    # Convert window to DataFrame
                    # ----------------------------------

                    window_df = pd.DataFrame(ml_buffer)

                    print("\n========== WINDOW CONTENT ==========")
                    print(window_df)
                    print("====================================")

                    # ----------------------------------
                    # Compute average feature values
                    # ----------------------------------

                    final_features = pd.DataFrame([

                        window_df.mean()

                    ])

                    print("\n========== WINDOW MEAN ==========")
                    print(final_features)
                    print("=================================")

                    # ----------------------------------
                    # Prediction
                    # ----------------------------------

                    prediction = model.predict(final_features)[0]

                    probability = model.predict_proba(final_features)[0]

                    confidence = max(probability) * 100

                    # ----------------------------------
                    # Display Result
                    # ----------------------------------

                    print("\n========== ML RESULT ==========")



                    if prediction == 0:

                        print(f"Prediction : BENIGN")
                        print(f"Confidence : {confidence:.2f}%")

                        last_prediction = 0


                    else:

                        print(f"Prediction : DDOS")
                        print(f"Confidence : {confidence:.2f}%")

                        # Generate alert only once
                        if last_prediction == 0 and confidence >= 90:

                            try:

                                requests.post(
                                    "http://10.21.1.38:8000/log_event",
                                    json={
                                        "severity": "Critical",
                                        "event_type": "ML DDoS Detection",
                                        "message":
                                            f"Random Forest detected DDoS ({confidence:.2f}% confidence)"
                                    }
                                )

                                print("ML DDoS Event Sent To Dashboard")

                            except Exception as e:

                                print("Event Logging Failed:", e)

                        last_prediction = 1

                    print("===============================\n")

            print("NEW INSERT BLOCK RUNNING")
            cur.execute(
                """
                INSERT INTO sflow_packets
                (
                    device_id,
                    capture_time,

                    sflow_245_version,
                    sflow_245_agenttype,
                    sflow_245_agent,
                    sflow_245_sequence_number,
                    sflow_245_sysuptime,
                    sflow_delta_sysuptime,
                    sflow_245_numsamples,

                    sflow_245_sampletype,

                    counters_sample_sequence_number,
                    counters_sample_source_id_class,
                    counters_sample_index,
                    counters_sample_sampling_interval,
                    counters_sample_counters_type,

                    sflow_245_ifindex,
                    sflow_245_iftype,
                    sflow_245_ifspeed,
                    sflow_245_ifdirection,
                    sflow_245_ifadmin_status,
                    sflow_245_ifoper_status,

                    sflow_245_ifinoct,
                    sflow_delta_ifinoct,
                    sflow_245_ifinpkt,
                    sflow_delta_ifinpkt,
                    sflow_245_ifinmcast,
                    sflow_245_ifinbcast,
                    sflow_245_ifindisc,
                    sflow_245_ifinerr,
                    sflow_245_ifinunk,

                    sflow_245_ifoutoct,
                    sflow_delta_ifoutoct,
                    sflow_245_ifoutpkt,
                    sflow_delta_ifoutpkt,

                    sflow_245_ifoutmcast,
                    sflow_245_ifoutbcast,
                    sflow_245_ifoutdisc,
                    sflow_245_ifouterr,
                    sflow_245_ifpromisc
                )
                VALUES
                (
                %s,
                %s,

                %s,%s,%s,%s,%s,%s,%s,

                %s,

                %s,%s,%s,%s,%s,

                %s,%s,%s,%s,%s,%s,

                %s,%s,%s,%s,%s,%s,%s,%s,%s,

                %s,%s,%s,%s,%s,%s,%s,%s,%s
                )
                """,
                (
                    device_id,
                    capture_time,

                    version,
                    agenttype,
                    agent,
                    sequence,
                    sysuptime,
                    delta_sysuptime,
                    numsamples,

                    sampletype,

                    counter_seq,
                    source_class,
                    counter_index,
                    sampling_interval,
                    counter_type,

                    ifindex,
                    iftype,
                    ifspeed,
                    ifdirection,
                    ifadmin,
                    ifoper,

                    ifinoct,
                    delta_ifinoct,
                    ifinpkt,
                    delta_ifinpkt,
                    ifinmcast,
                    ifinbcast,
                    ifindisc,
                    ifinerr,
                    ifinunk,

                    ifoutoct,
                    delta_ifoutoct,
                    ifoutpkt,
                    delta_ifoutpkt,
                    ifoutmcast,
                    ifoutbcast,
                    ifoutdisc,
                    ifouterr,
                    ifpromisc
                )
            )

            conn.commit()

            print("DATABASE INSERT SUCCESS")
            print("Stored Successfully in PostgreSQL")

    except Exception as e:

        print("\n" + "=" * 60)
        print("ERROR DETECTED")
        print("=" * 60)

        print("Exception :", repr(e))