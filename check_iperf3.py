#!/usr/bin/env python3
import iperf3
import argparse
import sys

def run_iperf_test(server_ip, duration, port, streams, direction, is_udp, bandwidth_mbps, dont_fragment, warn_mbps, crit_mbps, min_val, max_mbps):
    client = iperf3.Client()
    
    # --- iPerf3 Settings ---
    client.server_hostname = server_ip
    client.duration = duration
    client.port = port
    client.num_streams = streams

    # --- Direction ---
    if direction == "receive":
        client.reverse = True
    elif direction == "bidir":
        if hasattr(client, 'bidir'):
            client.bidir = True
        else:
            print("IPERF3 UNKNOWN - Your iperf3-python library version lacks 'bidir' support. | Received_bps=0;;;; Sent_bps=0;;;;")
            sys.exit(3)

    # --- Protocol & Bandwidth ---
    if is_udp:
        client.protocol = 'udp'
        
    if bandwidth_mbps:
        # Different versions of the library use slightly different names for target bandwidth
        if hasattr(client, 'bandwidth'):
            client.bandwidth = bandwidth_mbps * 1_000_000
        elif hasattr(client, 'bitrate'):
            client.bitrate = bandwidth_mbps * 1_000_000

    # --- Don't Fragment ---
    if dont_fragment:
        if hasattr(client, 'dont_fragment'):
            client.dont_fragment = True
        else:
            print("IPERF3 UNKNOWN - Your iperf3-python library version lacks 'dont_fragment' support. | Received_bps=0;;;; Sent_bps=0;;;;")
            sys.exit(3)

    # --- Threshold Math ---
    warn_bps = warn_mbps * 1_000_000
    crit_bps = crit_mbps * 1_000_000
    max_str = f"{max_mbps * 1_000_000}" if max_mbps is not None else ""

    try:
        result = client.run()
    except Exception as e:
        print(f"IPERF3 CRITICAL - Failed to connect to {server_ip} | Received_bps=0;{warn_bps};{crit_bps};{min_val};{max_str} Sent_bps=0;{warn_bps};{crit_bps};{min_val};{max_str}")
        sys.exit(2)

    if result.error:
        print(f"IPERF3 WARNING - {result.error} | Received_bps=0;{warn_bps};{crit_bps};{min_val};{max_str} Sent_bps=0;{warn_bps};{crit_bps};{min_val};{max_str}")
        sys.exit(1)
    else:
        # Pulling the standard data
        sent = result.sent_bps
        received = result.received_bps
        
        # Dynamically change the 3rd graph metric based on the protocol used
        if is_udp:
            # Using getattr() as a safe fallback just in case
            jitter = getattr(result, 'jitter_ms', 0)
            loss = getattr(result, 'lost_percent', 0)
            perf_data = f"Received_bps={received:.2f};{warn_bps};{crit_bps};{min_val};{max_str} Sent_bps={sent:.2f};{warn_bps};{crit_bps};{min_val};{max_str} Jitter_ms={jitter:.2f};;;; Loss_Percent={loss:.2f};;;;"
            extra_msg = f"Jitter: {jitter:.2f}ms, Loss: {loss:.2f}%"
        else:
            retries = getattr(result, 'retransmits', 0)
            perf_data = f"Received_bps={received:.2f};{warn_bps};{crit_bps};{min_val};{max_str} Sent_bps={sent:.2f};{warn_bps};{crit_bps};{min_val};{max_str} Retries={retries};;;;"
            extra_msg = f"Retries: {retries}"

        # Alert Logic
        if received < crit_bps:
            print(f"IPERF3 CRITICAL - Received dropped to {received / 1_000_000:.2f} Mbps ({extra_msg}) | {perf_data}")
            sys.exit(2)
        elif received < warn_bps:
            print(f"IPERF3 WARNING - Received dropped to {received / 1_000_000:.2f} Mbps ({extra_msg}) | {perf_data}")
            sys.exit(1)
        else:
            print(f"IPERF3 OK - Received: {received / 1_000_000:.2f} Mbps, Sent: {sent / 1_000_000:.2f} Mbps, {extra_msg} | {perf_data}")
            sys.exit(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LibreNMS iperf3 Service Check")
    
    iperf_group = parser.add_argument_group('iPerf3 Settings')
    iperf_group.add_argument("-H", "--host", required=True, help="Target iperf3 server IP")
    iperf_group.add_argument("-p", "--port", type=int, default=5201, help="Target port (default: 5201)")
    iperf_group.add_argument("-t", "--time", type=int, default=10, help="Test duration in seconds (default: 10)")
    iperf_group.add_argument("-P", "--parallel", type=int, default=1, help="Number of parallel client streams")
    
    # New Protocol & Control Flags
    iperf_group.add_argument("-d", "--direction", choices=["send", "receive", "bidir"], default="send", help="Traffic direction (default: send)")
    iperf_group.add_argument("-u", "--udp", action="store_true", help="Use UDP instead of TCP")
    iperf_group.add_argument("-b", "--bandwidth", type=int, help="Target bandwidth in Mbps (Highly recommended for UDP)")
    iperf_group.add_argument("-D", "--dont-fragment", action="store_true", help="Set the IPv4 Don't Fragment (DF) bit")

    alert_group = parser.add_argument_group('Alert Thresholds & Graph Limits (in Mbps)')
    alert_group.add_argument("-w", "--warning", type=int, default=750, help="Warning threshold in Mbps (default: 750)")
    alert_group.add_argument("-c", "--critical", type=int, default=500, help="Critical threshold in Mbps (default: 500)")
    alert_group.add_argument("-m", "--min", type=int, default=0, help="Minimum value for the graph (default: 0)")
    alert_group.add_argument("-M", "--max", type=int, help="Maximum value for the graph in Mbps (optional)")
    
    args = parser.parse_args()
    
    run_iperf_test(args.host, args.time, args.port, args.parallel, args.direction, args.udp, args.bandwidth, args.dont_fragment, args.warning, args.critical, args.min, args.max)
