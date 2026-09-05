-- BigQuery schema for the Flood Risk Assistant.
-- First create the dataset (once): bq mk --dataset YOUR_PROJECT_ID:flood_risk
-- Then run this to create the table.

CREATE TABLE IF NOT EXISTS `flood_risk.river_discharge_daily` (
  district STRING NOT NULL,
  division STRING,
  latitude FLOAT64,
  longitude FLOAT64,
  date DATE NOT NULL,
  river_discharge_m3s FLOAT64,
  ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
)
PARTITION BY date
CLUSTER BY district;
