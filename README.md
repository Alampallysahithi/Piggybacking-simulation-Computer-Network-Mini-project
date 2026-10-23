# Efficient Frame Communication Using Piggybacking

A Python and Streamlit-based simulator that demonstrates and compares **Normal ACK communication** with **Piggybacking** at the Data Link Layer.

## 📌 Project Overview

Piggybacking improves communication efficiency by attaching an acknowledgement (ACK) to an outgoing data frame instead of sending a separate ACK frame.

The simulator compares both methods and calculates:
- Total frames transmitted
- Frames saved
- Transmission reduction
- Communication efficiency

## 🛠️ Technologies Used

- Python
- Streamlit

## ⚙️ Inputs

- Number of Frames
- Data Size (Bytes)
- ACK Size (Bytes)

## 📊 Example Result

For **10 frames**:

| Metric | Normal ACK | Piggybacking |
|---|---:|---:|
| Total Frames | 20 | 15 |
| Frames Saved | — | 5 |
| Transmission Reduction | — | 25% |
| Efficiency | — | 66.67% |

## 🚀 How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the application

```bash
streamlit run app.py
```

### 3. Open in browser

Streamlit will provide a local URL such as:

```text
http://localhost:8501
```

## 🎯 Objective

The main objective is to demonstrate how **piggybacking reduces separate acknowledgement transmissions and improves communication efficiency** in bidirectional data communication.

## 👩‍💻 Project

**Efficient Frame Communication Using Piggybacking**  
Data Link Layer Project
