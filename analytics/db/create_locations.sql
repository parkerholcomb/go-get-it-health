CREATE EXTERNAL TABLE IF NOT EXISTS vax_tx.supply (
  `name` string,
  `type` string,
  `tsa` string,
  `street` string,
  `city` string,
  `county` string,
  `address` string,
  `zip` string,
  `latitude` double,
  `longitude` double,
  `pfizer_available` int,
  `pfizer_available2` int,
  `moderna_available` int,
  `moderna_available2` int,
  `vaccines_available` int,
  `vaccines_available2` int,
  `total_available` int,
  `total_shipped` int,
  `publicphone` string,
  `website` string,
  `last_update_vac` date,
  `last_update_time_vac` string
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'
WITH SERDEPROPERTIES (
  'serialization.format' = ',',
  'field.delim' = ','
) LOCATION 's3://vax-tx/'
TBLPROPERTIES (
  'has_encrypted_data'='false',
  'skip.header.line.count'='1'
);


