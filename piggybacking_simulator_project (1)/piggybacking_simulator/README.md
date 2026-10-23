# Efficient Frame Communication Using Piggybacking

A Data Link Layer project that compares normal ACK-based communication with piggybacking.

## Technology mapping

| Category | Technology used |
|---|---|
| Network Simulation | Cisco Packet Tracer (topology/config), GNS3/EVE-NG optional |
| Programming | Python |
| Network Programming | Python TCP sockets |
| Packet Analysis | Wireshark |
| Linux Networking | Ubuntu/Linux CLI |
| Visualization | Streamlit |
| Database | SQLite |
| Cloud Extension | AWS / Azure / Google Cloud deployment |
| Version Control | Git / GitHub |

## Main features

1. Simulate A→B and B→A data frames.
2. Compare separate ACKs with DATA+ACK piggybacking.
3. Calculate total frames, total bytes, ACK overhead and bandwidth saved.
4. Show an interactive timeline and bar chart.
5. Store simulation history in SQLite.
6. Send a real localhost TCP message for Wireshark capture.
7. Includes Cisco IOS configuration and Wireshark filter examples.

## Run on Windows / Ubuntu

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Ubuntu:
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

Open the URL shown by Streamlit, normally http://localhost:8501.

## Wireshark demonstration

Run the app and click **Send TCP Demo**. In Wireshark, capture on the loopback interface and use:

```
tcp.port == 50505
```

You can inspect TCP SYN, SYN-ACK, ACK, PSH/data and connection termination.

## Cisco Packet Tracer

Use `network/packet_tracer_topology.txt` as the lab plan. Packet Tracer is used to demonstrate the network path, while the Python simulator demonstrates the Data Link Layer ACK/piggyback logic.

## Academic point

Piggybacking is useful when the receiver also has data to send. The ACK is attached to the outgoing data frame instead of being sent as a separate frame. If there is no outgoing data within the waiting period, the ACK is sent separately.

## Important note

This is an educational simulation. Real TCP uses cumulative ACKs, delayed ACKs and its own transport-layer mechanisms; the application models the Data Link Layer concept requested by the project.
