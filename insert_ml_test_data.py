import pandas as pd
import psycopg2


# -------------------------------
# Load CSV
# -------------------------------

df = pd.read_csv(
    "ml_test_dataset.csv"
)


# -------------------------------
# PostgreSQL Connection
# -------------------------------

conn = psycopg2.connect(

    host="localhost",
    database="Sflow_db",
    user="postgres",
    password="Sahil",
    port="5432"

)


cursor = conn.cursor()



# -------------------------------
# Insert Data
# -------------------------------


for index,row in df.iterrows():


    cursor.execute(

        """
        INSERT INTO ml_test_dataset
        (
        flow_duration,
        tot_fwd_pkts,
        tot_bwd_pkts,
        totlen_fwd_pkts,
        totlen_bwd_pkts,
        flow_byts_per_sec,
        flow_pkts_per_sec,
        fwd_pkts_per_sec,
        bwd_pkts_per_sec,
        actual_label
        )

        VALUES
        (
        %s,%s,%s,%s,%s,
        %s,%s,%s,%s,%s
        )

        """,

        (
            float(row["Flow_Duration"]),
            int(row["Tot_Fwd_Pkts"]),
            int(row["Tot_Bwd_Pkts"]),
            float(row["TotLen_Fwd_Pkts"]),
            float(row["TotLen_Bwd_Pkts"]),
            float(row["Flow_Byts_per_sec"]),
            float(row["Flow_Pkts_per_sec"]),
            float(row["Fwd_Pkts_per_sec"]),
            float(row["Bwd_Pkts_per_sec"]),
            int(row["Actual_Label"])
        )

    )


conn.commit()


cursor.close()

conn.close()


print("Data inserted successfully")