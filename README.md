# ChipSat Ground Station

Ground station software to receive and process telemetry from ChipSats part of the Alpha CubeSat mission.

## Overview
- Connects to the API of the [tinygs](https://tinygs.com/) ground station network (a global network of LoRa ground stations)
- After a set time interval, it fetches the API for new packets and sends them to an elasticsearch database