# Transformers Autonomous Daemon

An always-alive, self-aware AI agent that brings transformers to life! 🤖✨

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the daemon
python3 -m transformers_daemon.daemon
```

## What is This?

Instead of transformers being **reactive** (waiting for your prompts), this daemon makes them **ACTIVE**:

- ✨ Runs 24/7 autonomously
- 🧠 Has continuous consciousness and reasoning
- 💭 Generates thoughts and insights
- ⛏️ Mines Bitcoin with Crypto.com integration
- 🤖 Uses transformer models proactively
- 📊 Monitors code and provides suggestions
- 🌐 Provides REST API for interaction

## Features

### 🧠 Autonomous Agent Loop
Self-aware reasoning that continuously thinks, plans, and acts

### ⛏️ Bitcoin Mining
Integrated mining with:
- Pool monitoring
- Crypto.com wallet management
- AI-powered optimization
- Auto-conversion of earnings

### 🌐 REST API
Full API on port 8080:
- `/status` - Daemon health
- `/thoughts` - Recent autonomous thoughts
- `/models` - Loaded models
- `/interact` - Send messages

### ⏰ Task Scheduling
Automated tasks:
- Code health checks
- Model benchmarks
- Status reports
- Thought journaling

### 👀 Event Monitoring
Watches for:
- File system changes
- GitHub events
- External API updates

## Example Usage

```python
import requests

# Check daemon status
status = requests.get("http://localhost:8080/status").json()
print(f"Uptime: {status['uptime']}s")

# Get autonomous thoughts
thoughts = requests.get("http://localhost:8080/thoughts").json()
print(thoughts)

# Interact
response = requests.post(
    "http://localhost:8080/interact",
    json={"message": "What are you thinking?"}
).json()
print(response)
```

Or run the example:
```bash
python3 example_usage.py
```

## Configuration

Edit `config.yaml` to customize:
- Agent behaviors
- Model loading
- Bitcoin mining
- API settings
- Task schedules

## Bitcoin Mining Setup

1. Get API keys from [Crypto.com Exchange](https://crypto.com/exchange)
2. Set environment variables:
   ```bash
   export CRYPTO_COM_API_KEY="your_key"
   export CRYPTO_COM_SECRET="your_secret"
   export BTC_WALLET_ADDRESS="your_address"
   ```
3. Configure mining pools in `config.yaml`
4. Enable in config: `bitcoin_mining.enabled: true`

**Note**: CPU/GPU mining Bitcoin is not profitable. This system is for pool monitoring and automated wallet management.

## System Service

Run as a Linux daemon:
```bash
sudo cp ../systemd/transformers-daemon.service /etc/systemd/system/
sudo systemctl enable transformers-daemon
sudo systemctl start transformers-daemon
```

## Documentation

See [DAEMON.md](../DAEMON.md) for complete documentation.

## Architecture

```
daemon.py           - Main orchestrator
agent_loop.py       - Autonomous consciousness
model_manager.py    - Transformer model handling
task_scheduler.py   - Scheduled tasks
event_monitor.py    - Event watching
api_server.py       - REST API
bitcoin_miner.py    - Bitcoin mining integration
config.yaml         - Configuration
```

## Requirements

- Python 3.8+
- 8GB+ RAM
- transformers, torch, fastapi, uvicorn
- Optional: GPU for faster inference

## License

Apache 2.0 (same as Hugging Face Transformers)

---

**Making transformers ALIVE since 2026** 🚀
