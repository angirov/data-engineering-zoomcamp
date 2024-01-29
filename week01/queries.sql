select max(trip_distance)
from green
where lpep_pickup_datetime >= '2019-09-26 00:00:00' and
lpep_pickup_datetime <= '2019-09-26 23:59:59';