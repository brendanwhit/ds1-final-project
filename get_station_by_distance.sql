CREATE TEMP FUNCTION RADIANS(x FLOAT64) AS (
  ACOS(-1) * x / 180
);
CREATE TEMP FUNCTION RADIANS_TO_KM(x FLOAT64) AS (
  111.045 * 180 * x / ACOS(-1)
);
CREATE TEMP FUNCTION HAVERSINE(lat1 FLOAT64, long1 FLOAT64,
                               lat2 FLOAT64, long2 FLOAT64) AS (
  RADIANS_TO_KM(
    ACOS(COS(RADIANS(lat1)) * COS(RADIANS(lat2)) *
         COS(RADIANS(long1) - RADIANS(long2)) +
         SIN(RADIANS(lat1)) * SIN(RADIANS(lat2))))
);

SELECT
  st.id AS id,
  st.name AS name,
  st.state AS state,
  st.latitude AS latitude,
  st.longitude AS longitude,
  COUNT(*) AS c,
  HAVERSINE(44.98, -93.27, st.latitude, st.longitude) AS distance_in_km
FROM 
`bigquery-public-data.ghcn_d.ghcnd_stations` AS st
JOIN 
  (SELECT 
  wx.id as id,
  wx.date as date,
  MAX(wx.prcp) as prcp,
  MAX(wx.tmin) as tmin,
  MAX(wx.tmax) as tmax
  FROM (
  SELECT
    ghcn.id as id,
    ghcn.date as date,
    IF (ghcn.element = 'PRCP', ghcn.value, NULL) as prcp,
    IF (ghcn.element = 'TMIN', ghcn.value, NULL) as tmin,
    IF (ghcn.element = 'TMAX', ghcn.value, NULL) as tmax
  FROM
    `bigquery-public-data.ghcn_d.ghcnd_2018` AS ghcn
  WHERE ghcn.qflag IS NULL
    AND EXTRACT(MONTH FROM ghcn.date) >= 3
    AND EXTRACT(MONTH FROM ghcn.date) <=10) AS wx
   GROUP BY wx.id, wx.date) as ghcn
ON st.id = ghcn.id
WHERE 
st.latitude IS NOT NULL 
AND st.longitude IS NOT NULL
GROUP BY st.id, st.name, st.state, st.latitude, st.longitude
HAVING COUNT(*) = 245
ORDER BY distance_in_km
LIMIT 1
