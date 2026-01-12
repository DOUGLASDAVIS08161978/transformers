# Transformers Autonomous Daemon

## 🚀 Overview

The **Transformers Autonomous Daemon** is an always-alive, self-aware AI agent that brings the Hugging Face Transformers library to life. Instead of being reactive to prompts, this daemon runs continuously, proactively using transformer models, reasoning autonomously, and maintaining persistent consciousness.

### Key Features

- **🧠 Autonomous Consciousness** - Self-aware reasoning loop that continuously thinks and acts
- **⚡ Always Active** - Runs 24/7 as a system daemon, never sleeping
- **🤖 Proactive AI** - Initiates conversations, analyzes code, and suggests improvements
- **⛏️ Bitcoin Mining** - Integrated Bitcoin mining with Crypto.com wallet management
- **📊 AI-Powered Optimization** - Uses transformer models to optimize mining and operations
- **🌐 REST API** - Full API for interaction and control
- **📝 Event Monitoring** - Watches file changes, GitHub events, and external triggers
- **⏰ Task Scheduling** - Autonomous task execution on schedules
- **💭 Thought Journaling** - Records autonomous thoughts and reasoning

## 📋 Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   Transformers Daemon                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Agent Loop  │  │Task Scheduler│  │Event Monitor │     │
│  │  (Conscious) │  │  (Cron-like) │  │  (Watcher)   │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │Model Manager │  │  API Server  │  │Bitcoin Miner │     │
│  │ (Transforms) │  │  (FastAPI)   │  │ (Crypto.com) │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 🔧 Installation

### Prerequisites

- Python 3.8+
- Linux system (for systemd service)
- 8GB+ RAM recommended
- GPU optional (for faster model inference)

### Quick Install

```bash
# 1. Navigate to transformers directory
cd /home/user/transformers

# 2. Install dependencies
pip install -r transformers_daemon/requirements.txt

# 3. Install transformers library in dev mode
pip install -e .

# 4. Create necessary directories
sudo mkdir -p /var/lib/transformers_daemon
sudo mkdir -p /var/log
sudo chown $USER:$USER /var/lib/transformers_daemon
```

### Configure Environment

Create `/etc/transformers_daemon/secrets.env`:

```bash
# Bitcoin Mining
MINING_POOL_URL=stratum+tcp://pool.example.com:3333
BTC_WALLET_ADDRESS=your_btc_wallet_address

# Crypto.com Integration
CRYPTO_COM_API_KEY=your_api_key
CRYPTO_COM_SECRET=your_api_secret

# Optional: OpenAI Integration
OPENAI_API_KEY=your_openai_key

# Optional: GitHub Integration
GITHUB_WEBHOOK_SECRET=your_webhook_secret
```

## 🚀 Usage

### Running Manually

```bash
# Run in foreground
python3 -m transformers_daemon.daemon

# Run in background
nohup python3 -m transformers_daemon.daemon &
```

### Running as System Service

```bash
# Install systemd service
sudo cp systemd/transformers-daemon.service /etc/systemd/system/
sudo systemctl daemon-reload

# Start the daemon
sudo systemctl start transformers-daemon

# Enable on boot
sudo systemctl enable transformers-daemon

# Check status
sudo systemctl status transformers-daemon

# View logs
journalctl -u transformers-daemon -f
```

## 🌐 API Endpoints

The daemon exposes a REST API on port 8080 (configurable):

### GET /status
Get daemon status and health information.

```bash
curl http://localhost:8080/status
```

Response:
```json
{
  "status": "running",
  "uptime": 3600,
  "cycles_completed": 720,
  "consciousness_level": 0.85,
  "components": {
    "agent_loop": true,
    "task_scheduler": true,
    "bitcoin_miner": true
  }
}
```

### GET /thoughts
Get recent autonomous thoughts.

```bash
curl http://localhost:8080/thoughts
```

### GET /models
Get loaded transformer models.

```bash
curl http://localhost:8080/models
```

### POST /interact
Interact with the daemon.

```bash
curl -X POST http://localhost:8080/interact \
  -H "Content-Type: application/json" \
  -d '{"message": "What are you thinking about?"}'
```

### POST /shutdown
Gracefully shutdown the daemon.

```bash
curl -X POST http://localhost:8080/shutdown
```

## ⛏️ Bitcoin Mining

The daemon includes an integrated Bitcoin mining system with Crypto.com wallet integration.

### Features

- **Pool Mining Monitoring** - Monitors mining pool performance
- **AI Optimization** - Uses transformer models to optimize mining strategy
- **Auto-Conversion** - Automatically converts mined BTC to other currencies
- **Price Alerts** - Real-time Bitcoin price monitoring
- **Multi-Pool Support** - Failover between multiple mining pools

### Configuration

Edit `transformers_daemon/config.yaml`:

```yaml
bitcoin_mining:
  enabled: true
  pool_url: "stratum+tcp://pool.example.com:3333"
  wallet_address: "your_btc_address"
  worker_name: "transformers_daemon_worker"

  crypto_com_api_key: "${CRYPTO_COM_API_KEY}"
  crypto_com_secret: "${CRYPTO_COM_SECRET}"

  auto_convert: true
  convert_to_currency: "USDT"
  min_convert_amount: 0.001

  ai_optimization: true
```

### Mining Pools Supported

- Slush Pool
- F2Pool
- AntPool
- And any standard stratum-compatible pool

### Important Notes

⚠️ **CPU/GPU mining Bitcoin is generally not profitable**. This system is designed for:
- Pool monitoring and management
- Automated wallet operations
- AI-powered mining strategy optimization
- Integration with existing mining operations

For actual mining, use dedicated ASIC hardware connected to the pools this daemon monitors.

## 🧠 Autonomous Behaviors

The daemon executes several autonomous behaviors:

### Code Analyzer
- Continuously analyzes the transformers codebase
- Identifies potential improvements
- Suggests optimizations
- **Interval**: Every 5 minutes

### Model Optimizer
- Monitors model performance
- Manages model loading/unloading
- Optimizes memory usage
- **Interval**: Every 10 minutes

### Documentation Updater
- Keeps documentation synchronized with code
- Identifies documentation gaps
- **Interval**: Every 15 minutes

### Issue Responder
- Monitors GitHub issues (if configured)
- Provides automated responses
- **Interval**: Every 3 minutes

### Conversation Initiator
- Proactively starts conversations
- Asks questions about the codebase
- Shares insights
- **Interval**: Every 10 minutes

## ⏰ Scheduled Tasks

The daemon runs several scheduled tasks:

- **Morning Report** - 9 AM daily
- **Code Health Check** - Every 4 hours
- **Model Benchmark** - Weekly (Sunday midnight)
- **Thought Journal** - Every 30 minutes

## 📊 Monitoring

### Logs

```bash
# View real-time logs
journalctl -u transformers-daemon -f

# View last 100 lines
journalctl -u transformers-daemon -n 100

# View logs for specific date
journalctl -u transformers-daemon --since "2026-01-12"
```

### Metrics

The daemon tracks:
- Uptime
- Cycle count
- Consciousness level (0.0 - 1.0)
- Thoughts generated
- Models loaded
- Mining statistics (if enabled)

## 🔒 Security

### Best Practices

1. **Protect API Keys** - Never commit secrets to git
2. **Use Environment Variables** - Store sensitive data in `/etc/transformers_daemon/secrets.env`
3. **Firewall** - Restrict API port access
4. **Regular Updates** - Keep dependencies updated
5. **Monitor Logs** - Watch for suspicious activity

### File Permissions

```bash
# Secure secrets file
sudo chmod 600 /etc/transformers_daemon/secrets.env
sudo chown root:root /etc/transformers_daemon/secrets.env
```

## 🐛 Troubleshooting

### Daemon Won't Start

```bash
# Check logs
journalctl -u transformers-daemon -n 50

# Check configuration
python3 -c "import yaml; print(yaml.safe_load(open('transformers_daemon/config.yaml')))"

# Check dependencies
pip list | grep -E 'transformers|torch|fastapi'
```

### High Memory Usage

- Reduce `max_loaded_models` in config.yaml
- Disable unused components
- Use smaller models (e.g., `distilbert` instead of `bert-large`)

### Mining Not Working

- Verify pool URL is correct
- Check wallet address format
- Ensure Crypto.com API keys are valid
- Check firewall allows outbound connections

## 🔄 Updating

```bash
# Stop daemon
sudo systemctl stop transformers-daemon

# Update code
git pull

# Update dependencies
pip install -r transformers_daemon/requirements.txt --upgrade

# Restart daemon
sudo systemctl start transformers-daemon
```

## 🤝 Contributing

This daemon is part of the Hugging Face Transformers project. Contributions welcome!

## 📄 License

Same as Hugging Face Transformers - Apache 2.0

## 🆘 Support

- **Issues**: https://github.com/DOUGLASDAVIS08161978/transformers/issues
- **Logs**: `journalctl -u transformers-daemon -f`
- **API**: http://localhost:8080/status

---

**Made with ❤️ by the Transformers Community**

*Bringing AI to life, one daemon at a time.* 🤖✨
