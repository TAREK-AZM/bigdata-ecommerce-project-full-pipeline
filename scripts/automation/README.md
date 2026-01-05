# 🚀 Automation Scripts (WSL)

This directory contains bash scripts to automate the e-commerce analytics pipeline for WSL environments.

## Quick Start (WSL/Linux)

### 1. First Time Setup
```bash
./scripts/automation/setup.sh
```
This will:
- Start all Docker containers
- Install dependencies
- Fix permissions
- Create Kafka topic

### 2. Start Everything
```bash
./scripts/automation/start-all.sh
```
This will start:
- Dashboard (http://localhost:5000)
- Spark Consumer
- Kafka Producer

### 3. Stop Everything
```bash
./scripts/automation/stop-all.sh
```

## Individual Scripts

### Setup
```bash
./scripts/automation/setup.sh
```
Sets up the infrastructure (run once)

### Start Producer
```bash
./scripts/automation/start-producer.sh
```
Starts the e-commerce transaction generator

### Start Consumer
```bash
./scripts/automation/start-consumer.sh
```
Starts Spark Streaming consumer

### Run Analysis
```bash
./scripts/automation/run-analysis.sh
```
Runs batch analysis and generates report

## Workflow

1. **First time:** Run `./scripts/automation/setup.sh`
2. **Start pipeline:** Run `./scripts/automation/start-all.sh`
3. **Wait 2-3 minutes** for data collection
4. **View dashboard:** Open http://localhost:5000
5. **Run analysis:** Run `./scripts/automation/run-analysis.sh`
6. **Stop:** Run `./scripts/automation/stop-all.sh`

## Manual Execution

If you prefer to run components manually in separate terminals:

**Terminal 1 - Producer:**
```bash
./scripts/automation/start-producer.sh
```

**Terminal 2 - Consumer:**
```bash
./scripts/automation/start-consumer.sh
```

**Terminal 3 - Dashboard:**
```bash
docker-compose up dashboard
```

Then access the dashboard at http://localhost:5000

## Troubleshooting

### Permission denied?
Make scripts executable:
```bash
chmod +x scripts/automation/*.sh
```

### Docker not found?
Ensure Docker is installed and running in WSL:
```bash
docker --version
docker-compose --version
```

### Containers not starting?
Check Docker service:
```bash
sudo service docker status
sudo service docker start
```
