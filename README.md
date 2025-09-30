# Actum — AI Compliance Engine

**AI Compliance Engine:** policy tags, risk labels, blocking for sensitive patterns (e.g., biometric ID), and an immutable audit trail mapped to the EU AI Act.

## Quick Start

```bash
# Clone and setup
git clone <repo-url>
cd Actum

# Start the full stack
docker-compose up -d postgres minio redis

# Access the services
# Admin UI: http://localhost:3000
# API Docs: http://localhost:8000/docs
# Database: localhost:5432

# Backend development
cd backend
uv venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
uv pip install -r requirements.txt
uvicorn main:app --reload

# Frontend development
cd frontend
npm install
npm run dev

```

## Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Admin UI      │    │   API Gateway   │    │  Policy Engine  │
│   (React)       │◄──►│   (FastAPI)     │◄──►│   (Rules + ML)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                       │
                                ▼                       ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │  Audit Trail    │    │ Pattern Detector│
                       │  (Postgres)     │    │ (Regex + NER)   │
                       └─────────────────┘    └─────────────────┘
```

## Core Features

- **Content Intake API** — Accept text, metadata, and optional file/image
- **Policy Engine** — Rule-based + ML risk classifier with EU AI Act compliance
- **Pattern Detector** — Regex + keyword detection for biometric terms, face detection
- **Enforcement Actions** — Block, redact, or attach restrictions
- **Immutable Audit Trail** — Append-only event store with HMAC signatures
- **Admin UI** — Policy management, audit viewer, demo scenarios

## EU AI Act Compliance

- **Prohibited Practices Detection** — Blocks biometric ID & scraping
- **Risk Classification** — Maps to unacceptable/high/limited/minimal risk levels
- **Record-Keeping** — Tamper-evident audit trail with policy versions
- **Enforcement Ready** — Exportable evidence for auditors

## Demo Scenarios

1. **Biometric Intent Blocking** — Text with facial recognition intent → blocked
2. **Image Face Detection** — Upload image with face → flagged/blocked
3. **High-Risk Classification** — CV screening tool → additional controls required

## Development

```bash
# Backend development
cd backend
uv venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
uv pip install -r requirements.txt
uvicorn main:app --reload

# Frontend development
cd frontend
npm install
npm run dev
```


