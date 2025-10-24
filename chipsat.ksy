meta:
  id: chipsat
  title: Alpha ChipSat Downlink Packet (last updated 10/24)
  endian: le
doc: https://github.com/Alpha-CubeSat/oop-chipsat-code/wiki/2.-Telemetry
seq:
  - id: lat_raw
    type: s2
  - id: long_raw
    type: s2
  - id: alt_raw
    type: u2
  - id: gyro_x_raw
    type: u1
  - id: gyro_y_raw
    type: u1
  - id: gyro_z_raw
    type: u1
  - id: accel_x_raw
    type: u1
  - id: accel_y_raw
    type: u1
  - id: accel_z_raw
    type: u1
  - id: mag_x_raw
    type: u1
  - id: mag_y_raw
    type: u1
  - id: mag_z_raw
    type: u1
  - id: temperature_raw
    type: u1
  - id: valid_uplinks
    type: b4
  - id: invalid_uplinks
    type: b4
  - id: chipsat_id
    type: b2
  - id: gps_position_valid
    type: b1
  - id: gps_altitude_valid
    type: b1
  - id: imu_valid
    type: b1
  - id: gps_on
    type: b1
  - id: l_flag
    type: b1
instances:
  latitude:
    value: lat_raw / 100.
  longitude:
    value: long_raw / 100.
  altitude:
    value: alt_raw * 10
  gyro_x:
    value: -245 + (490 / 255.0) * gyro_x_raw
  gyro_y:
    value: -245 + (490 / 255.0) * gyro_y_raw
  gyro_z:
    value: -245 + (490 / 255.0) * gyro_z_raw
  accel_x:
    value: -20 + (40 / 255.0) * accel_x_raw
  accel_y:
    value: -20 + (40 / 255.0) * accel_y_raw
  accel_z:
    value: -20 + (40 / 255.0) * accel_z_raw
  mag_x:
    value: -100 + (200 / 255.0) * mag_x_raw
  mag_y:
    value: -100 + (200 / 255.0) * mag_y_raw
  mag_z:
    value: -100 + (200 / 255.0) * mag_z_raw
  temperature:
    value: -40 + (165 / 255.0) * temperature_raw