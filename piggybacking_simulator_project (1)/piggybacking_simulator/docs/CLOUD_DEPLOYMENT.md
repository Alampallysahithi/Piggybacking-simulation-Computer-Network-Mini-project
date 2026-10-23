# Cloud Extension

The core project runs locally. For the cloud extension, deploy the Streamlit application on a Linux VM/container.

General steps:
1. Create an Ubuntu VM on AWS, Azure or Google Cloud.
2. Install Python and Git.
3. Clone the GitHub repository.
4. Create a virtual environment.
5. Install requirements.
6. Run Streamlit on port 8501.
7. Restrict firewall rules to the required source IPs.
8. For production, place the app behind HTTPS/reverse proxy.

Do not expose the TCP demo port 50505 publicly; it is intended for localhost testing.
