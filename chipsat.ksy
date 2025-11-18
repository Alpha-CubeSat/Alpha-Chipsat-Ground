meta:
  id: chipsat
  title: Alpha ChipSat Downlink Packet (last updated 11/11)
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
  latitude_deg:
    value: lat_raw / 100.
  longitude_deg:
    value: long_raw / 100.
  altitude_m:
    value: alt_raw * 10
  gyro_x_dps:
    value: -245 + (490 / 255.0) * gyro_x_raw
  gyro_y_dps:
    value: -245 + (490 / 255.0) * gyro_y_raw
  gyro_z_dps:
    value: -245 + (490 / 255.0) * gyro_z_raw
  accel_x_g:
    value: -20 + (40 / 255.0) * accel_x_raw
  accel_y_g:
    value: -20 + (40 / 255.0) * accel_y_raw
  accel_z_g:
    value: -20 + (40 / 255.0) * accel_z_raw
  mag_x_ut:
    value: -100 + (200 / 255.0) * mag_x_raw
  mag_y_ut:
    value: -100 + (200 / 255.0) * mag_y_raw
  mag_z_ut:
    value: -100 + (200 / 255.0) * mag_z_raw
  temperature_c:
    value: -40 + (165 / 255.0) * temperature_raw