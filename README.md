# iperf3 LibreNMS Service Plugin

A Nagios-compatible Python plugin for **LibreNMS** designed to monitor network throughput using `iperf3`. This plugin provides real-time graphing for throughput and network health metrics like TCP Retransmissions or UDP Jitter/Loss.

## 🚀 Features

*   **Dynamic Graphing:** Provides performance data for "Received", "Sent", and a third context-aware metric (Retries for TCP, Jitter/Loss for UDP).
*   **Protocol Support:** Toggle between **TCP** (default) and **UDP** modes.
*   **Threshold Alerting:** Custom Warning and Critical thresholds (entered in Mbps) to trigger LibreNMS alerts.
*   **Directional Control:** Choose between `send` (client to server), `receive` (server to client), or `bidir` (simultaneous).
*   **Advanced Networking:** Supports target bandwidth capping and the IPv4 "Don't Fragment" (DF) bit.

## 🛠 Prerequisites

1.  **iperf3 binary:** Must be installed on the LibreNMS poller.
    `sudo apt install iperf3`
2.  **iperf3-python library:** Python wrapper for the iperf3 API.
    `pip3 install iperf3`
3.  **Target Server:** An accessible server running `iperf3 -s`.

## 📥 Installation

1.  Place the script in your LibreNMS plugins directory:
    ```bash
    cp check_iperf3.py /usr/lib/monitoring-plugins/check_iperf3.py
    chmod +x /usr/lib/monitoring-plugins/check_iperf3.py

2.  Test the script from the command line:
    ```bash
    /usr/lib/nagios/plugins/check_iperf3.py -H <server_ip> -w 750 -c 500
    ```

## 📊 LibreNMS Integration

1.  In the LibreNMS Web UI, go to **Device** -> **Services** -> **Add Service**.
2.  **Service Type:** Select `check_iperf3.py` (ensure it is in the plugins directory).
3.  **Parameters:** Add your desired flags, e.g., `-H 192.168.1.10 -u -b 1000 -w 900 -c 800`.
4.  **RRD Note:** If you change the number of metrics (e.g., switching from TCP to UDP) or change the labels, you **must** delete the existing `.rrd` file for this service to allow LibreNMS to recreate the database structure.
    *   Path: `/opt/librenms/rrd/<device_name>/services-<service_id>.rrd`

## 📖 Usage

### Arguments

| Flag | Name | Description | Default |
| :--- | :--- | :--- | :--- |
| `-H` | `--host` | **Required.** IP or Hostname of the iperf3 server. | N/A |
| `-p` | `--port` | Port of the iperf3 server. | 5201 |
| `-t` | `--time` | Duration of the test in seconds. | 10 |
| `-P` | `--parallel` | Number of parallel client streams. | 1 |
| `-d` | `--direction` | Traffic flow: `send`, `receive`, or `bidir`. | send |
| `-u` | `--udp` | Use UDP instead of TCP. | False |
| `-b` | `--bandwidth` | Target bandwidth in Mbps (Required for UDP). | N/A |
| `-D` | `--dont-fragment` | Set the IPv4 Don't Fragment (DF) bit. | False |
| `-w` | `--warning` | Warning threshold in Mbps (Alerts if below). | 750 |
| `-c` | `--critical` | Critical threshold in Mbps (Alerts if below). | 500 |
| `-m` | `--min` | Minimum value for the graph Y-axis. | 0 |
| `-M` | `--max` | Maximum value for the graph Y-axis (optional). | None |

## ⚠️ Known Limitations
The `iperf3-python` library is a wrapper for the iperf3 C library. If you receive an **UNKNOWN** status regarding `bidir` or `dont_fragment`, please ensure your Python library and system iperf3 versions are up to date.
