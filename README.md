# YAKt Yet Another KRaft (Kafka Raft)

## KRaft Architecture
![image](https://github.com/user-attachments/assets/525a8802-7eed-46fd-8433-14e463335b17)



* KRaft is a event based, distributed metadata management system that was written to replace Zookeeper in the ecosystem of Kafka.
* It uses Raft as an underlying consensus algorithm to do log replication and manage consistency of state.
* It is a protocol introduced in Kafka for managing the replication and consensus of Kafka broker metadata.
* 

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

KRaft is a protocol and feature set introduced in the realm of distributed systems, particularly within the context of Apache Kafka. Apache Kafka is an open-source distributed streaming platform widely used for building real-time data pipelines and streaming applications. KRaft specifically addresses the management of metadata and the consensus protocol within Kafka clusters.

## Features

1. Durability:

    KRaft aims to enhance the durability of Kafka clusters. It provides a more robust mechanism for managing metadata and handling failures,
    ensuring data consistency and reliability.
   
2. Consensus Protocol:

    KRaft uses a consensus protocol, which is similar to the Raft consensus algorithm. This protocol ensures that all nodes in the Kafka cluster agree on the current state and leadership,            contributing to a more resilient and fault-tolerant system.
   
3. ZooKeeper Replacement:

    KRaft replaces the traditional reliance on Apache ZooKeeper for managing metadata and leader election. This reduction of external dependencies simplifies the overall Kafka architecture.

4. Scalability:

    KRaft is designed to support larger Kafka deployments, allowing clusters to handle a higher number of partitions and brokers. This scalability is crucial for organizations with growing data      processing needs.
   
5. Simplified Architecture:

    By eliminating the need for ZooKeeper, KRaft simplifies the architecture of Kafka clusters. This results in a more self-contained and streamlined system.
   
6. Leader Election:

    KRaft manages leader election for partitions through the consensus protocol. This ensures that there is a single leader for each partition, facilitating efficient data processing.

7. Incremental Migration:

    Existing Kafka users can migrate to KRaft incrementally. The transition involves upgrading brokers and updating configurations without requiring a complete overhaul of the existing Kafka         deployment.

8. Improved Recovery:

    KRaft is designed to improve recovery processes in the event of node failures or other disruptions. The consensus protocol helps maintain data integrity during such scenarios.

9. Log Replication:
    
    KRaft ensures consistent metadata changes through fault-tolerant log replication across all cluster nodes.

10. Fault Tolerance:
    
    KRaft handles node failures gracefully, maintaining cluster operation with leader election and ensuring uninterrupted data consistency.


## Project Structure

| File / Directory | Purpose |
|---|---|
| `flask_http_server.py` | Main entry point — Flask HTTP server exposing the KRaft metadata API; owns the Raft node lifecycle |
| `raft/raft.py` | Core Raft consensus node (leader election, log replication, heartbeats) over ZeroMQ PUB/SUB |
| `raft/protocol.py` | Raft message types (`RequestVote`, `AppendEntries`, `ClientRequest`, etc.) with JSON serialisation |
| `raft/interface.py` | ZeroMQ transport — `Talker` (publisher) and `Listener` (subscriber) as separate processes |
| `raft/__init__.py` | Exports `RaftNode` |
| `client/client_1.py` | Register a broker record |
| `client/client_2.py` | Create a topic record |
| `client/client_3.py` | Create a partition record |
| `client/client_4.py` | Register a producer ID record |
| `client/client_broker_mgmt.py` | Broker management heartbeat (fetch metadata diff since offset) |
| `client/client_client_mgmt.py` | Client management fetch (topics/partitions/brokers since offset) |
| `client/client_remove.py` | Remove a Raft node from the cluster |
| `client/new_node_client.py` | Add a new Raft node to the running cluster |

## Getting Started

### Prerequisites

- **Python 3.12** (tested on 3.12.9)
- **pyenv** (recommended) or any Python 3.12 environment manager
- **pyzmq** requires libzmq — on macOS install via Homebrew: `brew install zeromq`

### Installation

```bash
# 1. Clone the repo
git clone https://github.com/chandanamulagund/YAKt-Yet-Another_KRaft.git
cd YAKt-Yet-Another_KRaft

# 2. Create and activate a pyenv virtualenv
pyenv virtualenv 3.12.9 yakt-env
pyenv local yakt-env

# 3. Install dependencies
pip install --upgrade pip
pip install "flask>=3.1,<4" "pyzmq>=26,<28" "requests>=2.32,<3" "future>=1.0,<2"
```

### Running the server

```bash
# Start the Flask server (runs on localhost:5000)
python flask_http_server.py
```

In a separate terminal, bootstrap the Raft cluster by hitting the root route once:

```bash
curl http://localhost:5000/
```

This starts 4 Raft nodes (node0–node3) bound to `127.0.0.1` on ports 5564–5567, runs an initial leader election, and returns `before_first_request` when the bootstrap is complete.

### Running the clients

With the server running, open another terminal (with `yakt-env` active) and run each client:

```bash
# Register a broker
python client/client_1.py

# Create a topic
python client/client_2.py

# Create a partition
python client/client_3.py

# Register a producer ID
python client/client_4.py

# Broker management heartbeat (fetch metadata diff since a given offset)
python client/client_broker_mgmt.py

# Client management fetch (topics, partitions, broker info since offset)
python client/client_client_mgmt.py
```

### API endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/register-broker-record` | Register a broker |
| `GET` | `/api/register-broker-record` | List all active brokers |
| `GET` | `/api/register-broker-record/<id>` | Get broker by ID |
| `POST` | `/api/topic-record` | Create a topic |
| `GET` | `/api/topic-record/<name>` | Get topic by name |
| `POST` | `/api/partition-record` | Create a partition |
| `POST` | `/api/producer-id-record` | Register a producer ID |
| `POST` | `/api/broker-registration-change` | Update broker info |
| `DELETE` | `/api/register-broker-record/<id>` | Unregister a broker |
| `POST` | `/api/broker-mgmt` | Broker heartbeat — returns metadata diff since offset |
| `POST` | `/api/client-mgmt` | Client fetch — returns topics/partitions/brokers since offset |
| `POST` | `/api/new_node` | Add a Raft node to the running cluster |
| `POST` | `/api/remove_node` | Remove a Raft node from the running cluster |
| `GET` | `/api/get-records-from-nodes` | Inspect the last committed log entry of a named node |

### Known issues in the current baseline

> Full details with exact error output and root causes are tracked in [`bugs.md`](bugs.md).

| Bug | Description | Fixed in |
|-----|-------------|----------|
| BUG-001 | Raft election livelock — nodes loop as candidates, no leader elected | Phase 1 |
| BUG-002 | HTTP API bypasses Raft entirely; returns 200 while silently not replicating | Phase 1 + 2 |
| BUG-003 | Flask `debug=True` reloader forks process; Raft nodes start in wrong process → `IndexError` | Phase 0 workaround (`FLASK_DEBUG=0`) / Phase 3 proper fix |
| BUG-004 | Hardcoded LAN IP `192.168.136.128` in server and clients | Phase 0 |
| BUG-005 | `node_records()` crashes with `UnboundLocalError` on unknown node name | Phase 3 |
| BUG-006 | Python 2 compat shims (`future`/`past`) imported unnecessarily on Python 3.12 | Phase 0 |

## License

This project is licensed under the [MIT License](LICENSE).

---

*Originally developed as a Big Data course project (UE21CS343AB2) at PES University. Modernised and extended by [Chandana S M](https://github.com/chandanamulagund).*
