"""
Tools for the Flood Risk Assistant agent (Cloud Run deployment version).

Same district-relative risk logic as the local app/tools.py, adapted to read
the GCP project ID from an environment variable instead of an explicit
configure_project() call — Cloud Run deployment only ever imports this
module, it never calls a setup function first.
"""

import os

from google.cloud import bigquery


def _project_id() -> str:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise RuntimeError(
            "GOOGLE_CLOUD_PROJECT environment variable is not set. "
            "Cloud Run sets this automatically; for local runs, export it "
            "yourself before starting the agent."
        )
    return project_id


def check_flood_risk(district: str) -> dict:
    """Check current flood risk for a Bangladeshi district.

    Compares the district's most recent river discharge reading against that
    SAME district's own trailing-365-day 75th and 90th percentile discharge.

    Args:
        district: District name, e.g. "Sirajganj", "Dhaka", "Sylhet".

    Returns:
        A dict with: district, latest_date, latest_discharge_m3s, risk_level
        ("normal", "elevated", or "high"), p75_m3s, p90_m3s. If the district
        has no data yet, risk_level is "unknown" and a `note` explains why.
    """
    project_id = _project_id()
    client = bigquery.Client(project=project_id)

    query = f"""
        WITH baseline AS (
          SELECT
            district,
            date,
            river_discharge_m3s,
            PERCENTILE_CONT(river_discharge_m3s, 0.75)
              OVER (PARTITION BY district) AS p75_m3s,
            PERCENTILE_CONT(river_discharge_m3s, 0.90)
              OVER (PARTITION BY district) AS p90_m3s
          FROM `{project_id}.flood_risk.river_discharge_daily`
          WHERE district = @district
            AND date >= DATE_SUB(CURRENT_DATE(), INTERVAL 365 DAY)
        )
        SELECT *
        FROM baseline
        ORDER BY date DESC
        LIMIT 1
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[bigquery.ScalarQueryParameter("district", "STRING", district)]
    )
    rows = list(client.query(query, job_config=job_config).result())

    if not rows:
        return {
            "district": district,
            "risk_level": "unknown",
            "note": (
                f"No discharge data found for '{district}'. Either it hasn't "
                "been ingested yet or the name doesn't match — call "
                "list_covered_districts to check."
            ),
        }

    row = rows[0]
    latest = row["river_discharge_m3s"]
    p75, p90 = row["p75_m3s"], row["p90_m3s"]

    if latest >= p90:
        risk_level = "high"
    elif latest >= p75:
        risk_level = "elevated"
    else:
        risk_level = "normal"

    return {
        "district": district,
        "latest_date": row["date"].isoformat(),
        "latest_discharge_m3s": round(latest, 1),
        "risk_level": risk_level,
        "p75_m3s": round(p75, 1),
        "p90_m3s": round(p90, 1),
    }


def list_covered_districts() -> dict:
    """List districts currently covered by the flood dataset.

    Returns:
        dict with a "districts" list. Use this before check_flood_risk if
        you're unsure whether a district is covered yet.
    """
    project_id = _project_id()
    client = bigquery.Client(project=project_id)
    query = f"""
        SELECT DISTINCT district, division
        FROM `{project_id}.flood_risk.river_discharge_daily`
        ORDER BY district
    """
    rows = list(client.query(query).result())
    return {"districts": [{"district": r["district"], "division": r["division"]} for r in rows]}
