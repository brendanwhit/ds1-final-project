SELECT
mytable.id AS id,
mytable.name AS name,
mytable.state AS state,
mytable.distance_in_km AS dist,
(ghcn_tmax.value / 10.0) AS tmax,
ghcn_tmax.sflag AS tmax_sflag,
(ghcn_tmin.value / 10.0) AS tmin,
ghcn_tmin.sflag AS tmin_sflag,
IF(ghcn_prcp.value = 99.99, 0, ghcn_prcp.value) AS prcp,
ghcn_prcp.sflag AS prcp_sflag,
ghcn_tmax.date AS date
FROM
final_stations.ARI_station AS mytable
JOIN (
  SELECT
    ghcn.id as id,
    ghcn.value as value,
    ghcn.date as date,
    ghcn.sflag as sflag
  FROM
    `bigquery-public-data.ghcn_d.ghcnd_*` AS ghcn
  WHERE ghcn.qflag IS NULL
  AND _TABLE_SUFFIX = '2018'
  AND ghcn.element = 'TMAX'
  AND ghcn.value IS NOT NULL
  AND EXTRACT(MONTH FROM ghcn.date) >= 3
  AND EXTRACT(MONTH FROM ghcn.date) <=10) AS ghcn_tmax
ON ghcn_tmax.id = mytable.id
JOIN (
  SELECT
    ghcn.id as id,
    ghcn.value as value,
    ghcn.date as date,
    ghcn.sflag as sflag
  FROM
    `bigquery-public-data.ghcn_d.ghcnd_*` AS ghcn
  WHERE ghcn.qflag IS NULL
  AND _TABLE_SUFFIX = '2018'
  AND ghcn.element = 'TMIN'
  AND ghcn.value IS NOT NULL
  AND EXTRACT(MONTH FROM ghcn.date) >= 3
  AND EXTRACT(MONTH FROM ghcn.date) <=10) AS ghcn_tmin
ON
  ghcn_tmin.id = mytable.id AND ghcn_tmin.date = ghcn_tmax.date
JOIN (
  SELECT
    ghcn.id as id,
    ghcn.value as value,
    ghcn.date as date,
    ghcn.sflag as sflag
  FROM
    `bigquery-public-data.ghcn_d.ghcnd_*` AS ghcn
  WHERE ghcn.qflag IS NULL
  AND _TABLE_SUFFIX = '2018'
  AND ghcn.element = 'PRCP'
  AND ghcn.value IS NOT NULL
  AND EXTRACT(MONTH FROM ghcn.date) >= 3
  AND EXTRACT(MONTH FROM ghcn.date) <=10) AS ghcn_prcp
ON
  ghcn_prcp.id = mytable.id AND ghcn_prcp.date = ghcn_tmax.date
ORDER BY
dist, date
