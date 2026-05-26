# The Bistro Critic
### Hybrid Sentiment Analysis Engine & High-Concurrency MLOps Pipeline

[![Go Version](https://img.shields.io/badge/Go-1.23%2B-00ADD8?style=flat-for-grid&logo=go)](https://go.dev)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-FF6F00?style=flat-for-grid&logo=tensorflow)](https://tensorflow.org)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=flat-for-grid&logo=react)](https://react.dev)
[![MongoDB](https://img.shields.io/badge/MongoDB-NoSQL-47A248?style=flat-for-grid&logo=mongodb)](https://mongodb.com)
[![Docker](https://img.shields.io/badge/Docker-Orchestration-2496ED?style=flat-for-grid&logo=docker)](https://docker.com)

A high-performance, containerized monorepo architecture built to process and evaluate culinary text reviews in real-time. By pairing **Go** at the edge layer with **Python (TensorFlow/Keras)** at the inference layer, this platform demonstrates production-grade distributed design, strict environment isolation, and non-blocking asynchronous data persistence.

---

## 🏛️ Architectural Overview

Rather than running an isolated, stateless Machine Learning script, this platform simulates a real-world, high-traffic food delivery infrastructure (e.g., iFood or UberEats). 


### 🛰️ Distributed Topology
1. **Frontend Core (React 18 / Vite):** A modern, responsive user interface styled with a premium culinary **Crimson** scheme. Captures text reviews and dynamically renders real-time semantic results.
2. **API Border Gateway (Go 1.23 / Gin):** The battle-hardened reverse proxy and ingestion engine. It handles high-concurrency client demands, processes structural cross-origin resource sharing (CORS) rules, and isolates the heavy inference engine from raw internet exposure.
3. **Inference Node (Python 3.12 / FastAPI):** Serving a Neural Network trained using TensorFlow and Keras. 
4. **Data Persistence (MongoDB NoSQL Cluster):** Operates as the foundation for modern **MLOps / Data Drift logging**.

---

## 🔬 Core ML & MLOps Infrastructure

### 1. Unified Brain Encapsulation
To completely eliminate pipeline "skid" (where the production backend cleans text differently than the Jupyter research notebook), the preprocessing tokenization rules are natively compiled inside the neural model layout:
* **`layers.TextVectorization`** is injected directly as the first input sequence stage inside the `tf.keras.Sequential` architecture.
* The internal structure utilizes an advanced `Embedding` layer combined with a `GlobalAveragePooling1D` setup and custom `Dropout` boundaries to ensure optimized CPU inference on cloud infrastructure.
* **Artifact Mappings:** Labels are mapped using Scikit-Learn's `LabelEncoder` and serialised via `joblib` into a lightweight companion payload (`label_encoder.pkl`).

### 2. Non-Blocking Async Ingestion
When a client sends a text review, every millisecond matters. The Go Gateway leverages **Go routines** to handle data persistence asynchronously. The incoming request immediately shoots an HTTP handshake to the TensorFlow engine to calculate the sentiment score, while a decoupled background threat writes the data to MongoDB:

``` go
// Asynchronous MLOps logging thread inside Go Gateway
go func(text string, res MLResponse) {
    dbCtx, dbCancel := context.WithTimeout(context.Background(), 2*time.Second)
    defer dbCancel()

    document := bson.M{
        "review_text":     text,
        "prediction_code": res.PredictionCode,
        "sentiment":       res.Sentiment,
        "confidence":      res.Confidence,
        "created_at":      time.Now(),
    }
    _, _ = mongoCollection.InsertOne(dbCtx, document)
}(textClean, mlResponse)
```

# 📂 Repository Layout (Monorepo)
```
nlp_restaurant_review/
├── docker-compose.yml              # Multi-container orchestration & isolated networks
├── .gitignore                      # Flawless production Git exclusion matrix
├── gateway-service-go/             # High-Performance API Gateway Service
│   ├── Dockerfile                  # Multi-stage optimized builder (Alpine native)
│   ├── main.go                     # Reverse proxy, CORS handler & Async Mongo worker
│   ├── go.mod                      # Locked Gin framework & driver configurations
│   └── go.sum
├── ml-service-python/              # TensorFlow Inference Microservice
│   ├── Dockerfile                  # Slim Python layout optimized for heavy tensors
│   ├── main.py                     # FastAPI server exposing POST /v1/predict
│   ├── requirements.txt            # Frozen scientific dependencies
│   ├── modelo_sentimento.keras     # Compiled neural network model
│   └── label_encoder.pkl           # Exported target categorical mapper
├── restaurant-review-front/        # Responsive Web Interface
│   ├── Dockerfile                  # Hot-reloading development environment container
│   ├── src/
│   │   ├── App.jsx                 # Core interface script with dynamic card feedback
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
└── notebooks/                      # Scientific R&D Sandbox
    ├── p1.ipynb                    # Jupyter Notebook with Matplotlib/Seaborn analytics
    └── Restaurant_Reviews.tsv      # Root dataset source records
```
---
# 🛠️ DevOps & Containerization Practices

## Multi-Stage Builds (Go)

To prevent bloated production imagery, the Go Gateway uses a split Docker architecture. A heavy golang:1.23-alpine image is spun up purely to build the static compiled application binary. The final runtime layer is then stripped down and injected into a bare alpine:3.20 canvas, reducing the container fingerprint down to just a few megabytes.

---
# 🌐 Network Isolation
All microservices are bound together inside an explicit, isolated internal network bridge (restaurant-network). Services resolve each other natively via internal Docker DNS matching their service definitions, protecting internal backends from external port exposure.

---

# 🚀 Local Deployment Guide

## Prerequisites
* Windows with WSL2 or native Linux
* Docker Desktop configured with WSL2 distribution integration enabled.

1. Boot up the entire Cluster.
Clone this repository, navigate to the monorepo root folder where your docker-compose.yml lives, and run the following orchestration command:
```
Bash

docker compose up --build
```
This single instruction automatically handles the following sequence under the hood:
* Installs the isolated framework environments.
* Compiles the static Go execution binary.
* Sets up the NoSQL volume mounts for data persistence.
* Mounts active workspace volumes for the React frontend to support hot-reloading.

2. Verify Database Connection
Keep an eye on the running logs. The Go microservice will print a confirmation message as soon as it secures its internal bridge link to the database container:
```
Plaintext

[gateway_service_go] Successfully connected to MongoDB!
```

3. Run the Web Interface
Open your browser on your host operating system and navigate to:
```
Plaintext

http://localhost:5173
```

Type any review text in English (e.g., "The food was absolutely amazing, but the service was a bit slow.") and watch the pipeline orchestrate the request through Go, Python, and MongoDB instantly.

---

# 📈 MLOps Feedback Loop & Future Enhancements

Because the platform actively tracks live system queries inside MongoDB, we have a continuous feedback channel ready to fight Data Drift.

When predictions return low confidence levels (near the $50\% - 60\%$ range), those text strings are automatically logged to the collection database. In future sprints, this allows an ML Engineer to draw these live entries back into the notebooks/p1.ipynb workspace, re-evaluate boundaries, swap the current average pooling structure with a Bidirectional LSTM/GRU layer or a Hugging Face DistilBERT Transformer, and update the .keras model asset without breaking any downstream system configurations.