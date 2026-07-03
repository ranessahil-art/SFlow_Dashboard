from SFlow_Device import device_info
import psycopg2, requests
from datetime import datetime
from EventLogger import add_event

def insert_device():

    device = device_info

    if not device:
        return

    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        database="Sflow_db",
        user="postgres",
        password="Sahil"
    )

    cur = conn.cursor()

    # STEP 1: CHECK IF DEVICE ALREADY EXISTS
    cur.execute("""
        SELECT id FROM device
        WHERE device_ip = %s
        OR serial_number = %s
        LIMIT 1
    """, (
        device.get("device_ip"),
        device.get("serial_number")
    ))

    result = cur.fetchone()

    if result:
        # DEVICE EXISTS → reuse ID
        device_id = result[0]
        print("DEVICE ALREADY EXISTS, REUSING ID:", device_id)

    else:
        # DEVICE DOES NOT EXIST → INSERT NEW
        cur.execute("""
            INSERT INTO device
            (
                created_at,
                updated_at,

                hostname,
                location,

                device_ip,

                cpu_mac,
                vlan_mac,

                software_version,
                bootrom_version,
                hardware_version,
                cpld_version,

                serial_number,

                uptime
            )
            VALUES
            (
                %s,%s,
                %s,%s,
                %s,
                %s,%s,
                %s,%s,%s,%s,
                %s,
                %s
            )
            RETURNING id
        """,
        (
            datetime.now(),
            datetime.now(),

            device.get("hostname"),
            device.get("location"),

            device.get("device_ip"),

            device.get("cpu_mac"),
            device.get("vlan_mac"),

            device.get("software_version"),
            device.get("bootrom_version"),
            device.get("hardware_version"),
            device.get("cpld_version"),

            device.get("serial_number"),

            device.get("uptime")
        ))

        requests.post("http://10.21.1.38:8000/log_event", json={
            "severity": "Info",
            "event_type": "New Device",
            "message": f"New device {device.get('hostname')} added"
        })

        device_id = cur.fetchone()[0]
        print("NEW DEVICE INSERTED, ID:", device_id)

    conn.commit()
    cur.close()
    conn.close()

    return device_id