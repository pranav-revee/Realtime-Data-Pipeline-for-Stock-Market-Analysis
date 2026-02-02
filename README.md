
<div align="center">
  <img src="pipeline_banner.png" alt="Real-time Financial Data Pipeline" width="100%">

  # Real-Time Stock Market Data Pipeline
  
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  [![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
  [![Kafka](https://img.shields.io/badge/Apache%20Kafka-2.8-black)](https://kafka.apache.org/)
  [![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791.svg)](https://www.postgresql.org/)
  [![Cloud](https://img.shields.io/badge/Confluent%20Cloud-Stream-orange)](https://confluent.io)

  **A high-throughput, fault-tolerant streaming pipeline for ingesting, processing, and analyzing financial market data in real-time.**
</div>

---

## 🚀 Overview

This project implements an enterprise-grade ETL (Extract, Transform, Load) pipeline designed to handle high-velocity stock market data. It leverages **Apache Kafka** as the central nervous system for streaming events from **Alpha Vantage APIs** to a **PostgreSQL** data warehouse hosted on Aiven, enabling sub-second latency for financial analysis.

Key capabilities:
*   **Real-Time Ingestion**: Captures tick-level stock data (Open, High, Low, Close, Volume).
*   **Decoupled Architecture**: Uses Kafka to buffer producers from consumers, ensuring system stability during traffic spikes.
*   **Scalable Storage**: Persists structured financial data in PostgreSQL for complex analytical querying.
*   **Secure**: Implements SASL_SSL authentication for all cloud interactions.

---

## 🏗️ Architecture

```mermaid
graph LR
    API[Alpha Vantage API] -->|JSON Stream| Producer[Python Producer]
    Producer -->|Topic: topic_0| Kafka[Apache Kafka (Confluent Cloud)]
    Kafka -->|Consumer Group| Consumer[Python Consumer]
    Consumer -->|Batch Insert| DB[(PostgreSQL / Aiven)]
    
    style Kafka fill:#231F20,stroke:#fff,color:#fff
    style DB fill:#336791,stroke:#fff,color:#fff
    style Producer fill:#3776AB,stroke:#fff,color:#fff
    style Consumer fill:#3776AB,stroke:#fff,color:#fff
```

### Data Flow
1.  **Producer**: Polls the Alpha Vantage API every 5 minutes (configurable) to fetch intra-day stock time series.
2.  **Streaming**: Serializes data records and pushes them to a Kafka topic (`topic_0`) on Confluent Cloud.
3.  **Consumer**: Subscribes to the topic, deserializes messages, and performs transactional inserts into the PostgreSQL database.

---

## 🛠️ Technology Stack

*   **Language**: Python 3.10+
*   **Streaming Platform**: Apache Kafka (Managed by Confluent Cloud)
*   **Database**: PostgreSQL (Managed by Aiven)
*   **Data Source**: Alpha Vantage API
*   **Libraries**: `confluent-kafka`, `psycopg2`, `requests`

---

## ⚡ Getting Started

### Prerequisites
*   Python 3.x
*   Confluent Cloud Account (Kafka)
*   Aiven Account (PostgreSQL)
*   Alpha Vantage API Key

### Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/pranav-revee/Realtime-Data-Pipeline-for-Stock-Market-Analysis.git
    cd Realtime-Data-Pipeline-for-Stock-Market-Analysis
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Environment Setup**
    Create a `.env` file in the root directory based on `.env.example`:
    ```bash
    cp .env.example .env
    ```
    Fill in your credentials:
    ```ini
    KAFKA_BOOTSTRAP_SERVERS=your_endpoint:9092
    KAFKA_SASL_USERNAME=your_key
    KAFKA_SASL_PASSWORD=your_secret
    DB_PASSWORD=your_db_password
    ALPHA_VANTAGE_API_KEY=your_api_key
    ```

### Running the Pipeline

**1. Start the Producer**
This script will begin fetching data and writing to Kafka.
```bash
python producer.py
```

**2. Start the Consumer**
In a separate terminal, start the consumer to read from Kafka and write to the DB.
```bash
python consumer.py
```

---

## 📊 Database Schema

The pipeline automatically provisions the following schema in PostgreSQL:

| Column | Type | Description |
|--------|------|-------------|
| `id` | SERIAL | Primary Key |
| `Open` | VARCHAR | Opening price of the interval |
| `High` | VARCHAR | Highest price of the interval |
| `Low` | VARCHAR | Lowest price of the interval |
| `Close` | VARCHAR | Closing price of the interval |
| `Volume`| VARCHAR | Number of shares traded |

---

## 🔮 Future Roadmap
*   [ ] Integration with Spark Streaming for rolling window aggregations.
*   [ ] Dashboard visualization using Streamlit or Grafana.
*   [ ] Kubernetes (Helm Charts) for deployment.

---

## 📄 License
This project is licensed under the MIT License.
