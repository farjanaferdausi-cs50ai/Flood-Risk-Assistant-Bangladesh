"""
Load fetched flood discharge data into BigQuery.

Prerequisites:
  1. `gcloud auth application-default login` (or a service account key)
  2. BigQuery dataset created: bq mk --dataset YOUR_PROJECT_ID:flood_risk
  3. Table created from ../schema.sql (or let load_table_from_dataframe
     auto-create it on first run, if you skip schema.sql)

Usage:
  python load_to_bigquery.py --project YOUR_GCP_PROJECT_ID
"""

import argparse
import os

import pandas as pd
from google.cloud import bigquery

from fetch_flood_data import fetch_all_districts

TABLE_ID_SUFFIX = "flood_risk.river_discharge_daily"


def load_to_bigquery(df: pd.DataFrame, project_id: str) -> None:
    client = bigquery.Client(project=project_id)
    table_id = f"{project_id}.{TABLE_ID_SUFFIX}"

    df = df.copy()
    df["date"] = pd.to_datetime(df["date"]).dt.date

    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
        schema=[
            bigquery.SchemaField("district", "STRING"),
            bigquery.SchemaField("division", "STRING"),
            bigquery.SchemaField("latitude", "FLOAT64"),
            bigquery.SchemaField("longitude", "FLOAT64"),
            bigquery.SchemaField("date", "DATE"),
            bigquery.SchemaField("river_discharge_m3s", "FLOAT64"),
        ],
    )

    load_job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    load_job.result()  # block until the job finishes

    table = client.get_table(table_id)
    print(f"Loaded {load_job.output_rows} rows into {table_id}")
    print(f"Table now has {table.num_rows} total rows")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", default=os.environ.get("GCP_PROJECT_ID"))
    args = parser.parse_args()

    if not args.project:
        raise SystemExit("Pass --project YOUR_GCP_PROJECT_ID or set GCP_PROJECT_ID")

    print("Fetching latest flood data from Open-Meteo...")
    data = fetch_all_districts()

    print("Loading into BigQuery...")
    load_to_bigquery(data, args.project)
