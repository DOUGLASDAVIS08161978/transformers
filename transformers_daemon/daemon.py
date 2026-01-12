#!/usr/bin/env python3
"""
Transformers Autonomous Daemon

An always-alive, self-aware daemon that brings transformers to life.
This daemon runs continuously, proactively using transformer models,
reasoning about tasks, and maintaining autonomous consciousness.
"""

import asyncio
import logging
import signal
import sys
import os
import yaml
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
import threading

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("TransformersDaemon")


class TransformersDaemon:
    """Main daemon orchestrator for autonomous transformers system."""

    def __init__(self, config_path: str = "transformers_daemon/config.yaml"):
        """Initialize the daemon with configuration."""
        self.config = self._load_config(config_path)
        self.running = False
        self.start_time = None
        self.state = {
            "status": "initializing",
            "uptime": 0,
            "cycles_completed": 0,
            "last_thought": None,
            "consciousness_level": 0.0
        }

        # Component references (will be initialized)
        self.agent_loop = None
        self.task_scheduler = None
        self.event_monitor = None
        self.model_manager = None
        self.api_server = None
        self.bitcoin_miner = None

        # Setup signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

        logger.info(f"🧠 {self.config['daemon']['name']} initialized")

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            logger.info(f"Configuration loaded from {config_path}")
            return config
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            # Return minimal default config
            return {
                "daemon": {"name": "TransformersDaemon"},
                "agent": {"enabled": True, "loop_interval": 5},
                "models": {"default_model": "gpt2"},
                "task_scheduler": {"enabled": True},
                "event_monitoring": {"enabled": True},
                "api": {"enabled": True, "port": 8080}
            }

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully."""
        logger.info(f"Received signal {signum}, shutting down gracefully...")
        self.shutdown()

    async def initialize_components(self):
        """Initialize all daemon components."""
        logger.info("🔧 Initializing daemon components...")

        try:
            # Import and initialize components
            from .model_manager import ModelManager
            from .agent_loop import AgentLoop
            from .task_scheduler import TaskScheduler
            from .event_monitor import EventMonitor
            from .api_server import APIServer
            from .bitcoin_miner import BitcoinMiner

            # Initialize model manager first
            self.model_manager = ModelManager(self.config.get('models', {}))
            await self.model_manager.initialize()

            # Initialize agent loop
            if self.config.get('agent', {}).get('enabled', True):
                self.agent_loop = AgentLoop(
                    config=self.config.get('agent', {}),
                    model_manager=self.model_manager,
                    daemon_state=self.state
                )

            # Initialize task scheduler
            if self.config.get('task_scheduler', {}).get('enabled', True):
                self.task_scheduler = TaskScheduler(
                    config=self.config.get('task_scheduler', {}),
                    agent_loop=self.agent_loop
                )

            # Initialize event monitor
            if self.config.get('event_monitoring', {}).get('enabled', True):
                self.event_monitor = EventMonitor(
                    config=self.config.get('event_monitoring', {}),
                    agent_loop=self.agent_loop
                )

            # Initialize API server
            if self.config.get('api', {}).get('enabled', True):
                self.api_server = APIServer(
                    config=self.config.get('api', {}),
                    daemon=self
                )

            # Initialize Bitcoin miner
            if self.config.get('bitcoin_mining', {}).get('enabled', False):
                self.bitcoin_miner = BitcoinMiner(
                    config=self.config.get('bitcoin_mining', {}),
                    agent_loop=self.agent_loop
                )

            logger.info("✅ All components initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize components: {e}")
            raise

    async def start(self):
        """Start the daemon and all its components."""
        logger.info("🚀 Starting Transformers Autonomous Daemon...")
        self.running = True
        self.start_time = datetime.now()
        self.state["status"] = "running"

        try:
            # Initialize all components
            await self.initialize_components()

            # Start all components concurrently
            tasks = []

            # Start agent loop
            if self.agent_loop:
                tasks.append(asyncio.create_task(self.agent_loop.run()))
                logger.info("🤖 Agent loop started")

            # Start task scheduler
            if self.task_scheduler:
                tasks.append(asyncio.create_task(self.task_scheduler.run()))
                logger.info("⏰ Task scheduler started")

            # Start event monitor
            if self.event_monitor:
                tasks.append(asyncio.create_task(self.event_monitor.run()))
                logger.info("👀 Event monitor started")

            # Start API server
            if self.api_server:
                tasks.append(asyncio.create_task(self.api_server.run()))
                logger.info(f"🌐 API server started on port {self.config['api']['port']}")

            # Start Bitcoin miner
            if self.bitcoin_miner:
                tasks.append(asyncio.create_task(self.bitcoin_miner.start()))
                logger.info("⛏️  Bitcoin mining system started")

            # Main daemon loop
            tasks.append(asyncio.create_task(self._main_loop()))

            # Run all tasks
            logger.info("✨ Daemon is now ALIVE and AUTONOMOUS ✨")
            logger.info("="*60)
            logger.info("The transformers are no longer reactive - they are ACTIVE!")
            logger.info("="*60)

            await asyncio.gather(*tasks)

        except Exception as e:
            logger.error(f"Error in daemon execution: {e}")
            self.shutdown()

    async def _main_loop(self):
        """Main daemon heartbeat loop."""
        while self.running:
            try:
                # Update state
                self.state["uptime"] = (datetime.now() - self.start_time).total_seconds()
                self.state["cycles_completed"] += 1

                # Log heartbeat
                if self.state["cycles_completed"] % 60 == 0:  # Every 5 minutes
                    logger.info(
                        f"💓 Heartbeat | Uptime: {self.state['uptime']:.0f}s | "
                        f"Cycles: {self.state['cycles_completed']} | "
                        f"Consciousness: {self.state['consciousness_level']:.2f}"
                    )

                # Save state periodically
                if self.state["cycles_completed"] % 120 == 0:
                    await self._save_state()

                await asyncio.sleep(5)  # 5-second heartbeat

            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                await asyncio.sleep(5)

    async def _save_state(self):
        """Save daemon state to disk."""
        try:
            state_file = self.config.get('storage', {}).get('state_file', '/tmp/daemon_state.json')
            os.makedirs(os.path.dirname(state_file), exist_ok=True)

            with open(state_file, 'w') as f:
                json.dump({
                    **self.state,
                    "timestamp": datetime.now().isoformat()
                }, f, indent=2)

        except Exception as e:
            logger.warning(f"Failed to save state: {e}")

    def shutdown(self):
        """Gracefully shutdown the daemon."""
        logger.info("🛑 Shutting down daemon...")
        self.running = False
        self.state["status"] = "shutdown"

        # Cleanup components
        if self.model_manager:
            self.model_manager.cleanup()

        logger.info("👋 Daemon shutdown complete")
        sys.exit(0)

    def get_status(self) -> Dict[str, Any]:
        """Get current daemon status."""
        return {
            **self.state,
            "config": self.config['daemon'],
            "components": {
                "agent_loop": self.agent_loop is not None and self.agent_loop.is_running(),
                "task_scheduler": self.task_scheduler is not None,
                "event_monitor": self.event_monitor is not None,
                "api_server": self.api_server is not None,
                "model_manager": self.model_manager is not None
            }
        }


async def main():
    """Main entry point for the daemon."""
    daemon = TransformersDaemon()
    await daemon.start()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Daemon interrupted by user")
    except Exception as e:
        logger.error(f"Daemon crashed: {e}")
        sys.exit(1)
