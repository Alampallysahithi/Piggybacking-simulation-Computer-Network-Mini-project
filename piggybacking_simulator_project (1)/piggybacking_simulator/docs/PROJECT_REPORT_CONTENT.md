# Project Report Content

## 1. Title
Efficient Frame Communication Using Piggybacking

## 2. Problem Statement
Separate acknowledgements create additional communication overhead. This project develops a simulator to demonstrate how acknowledgements can be attached to outgoing data frames and compares the resulting communication efficiency.

## 3. Objectives
- Understand ACK-based communication.
- Understand piggybacking in the Data Link Layer.
- Simulate two-way communication.
- Compare frame count and byte overhead.
- Visualize communication.
- Store and analyze simulation results.
- Capture a real TCP socket exchange using Wireshark.

## 4. Modules
1. Simulation Engine
2. Piggybacking Logic
3. Streamlit Visualization
4. SQLite History
5. TCP Socket Demonstration
6. Wireshark Packet Analysis
7. Cisco Packet Tracer Network Lab
8. Git/GitHub version control

## 5. Expected Result
When both endpoints have data to exchange, piggybacking should reduce the number of separate ACK transmissions and improve bandwidth utilization. When the receiver has no outgoing data, an ACK may still need to be sent separately after the waiting period.

## 6. Future Scope
- Add configurable frame loss and retransmission.
- Add propagation/transmission delay.
- Add CRC/error detection.
- Add Go-Back-N and Selective Repeat comparison.
- Add GNS3/EVE-NG topology integration.
- Deploy Streamlit on a cloud VM or Streamlit-compatible hosting service.
