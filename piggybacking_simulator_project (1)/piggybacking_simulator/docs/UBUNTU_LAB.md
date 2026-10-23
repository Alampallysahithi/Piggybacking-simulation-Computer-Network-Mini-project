# Ubuntu/Linux Networking Lab

Install tools:

```bash
sudo apt update
sudo apt install python3 python3-venv wireshark git
```

Create environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Useful commands:

```bash
ip addr
ip route
ping 127.0.0.1
ss -lnt
ss -tn
```

Run the application and use `ss -tn` while the TCP demo is active.

For packet capture from the command line:

```bash
sudo tcpdump -i lo tcp port 50505
```
