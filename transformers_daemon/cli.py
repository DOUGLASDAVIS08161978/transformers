#!/usr/bin/env python3
"""
Enhanced CLI Interface for Transformers Daemon

Command-line interface with exponential capabilities.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path
from typing import Dict, Any
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("TransformersCLI")


class TransformersCLI:
    """
    Exponentially enhanced CLI for the Transformers Daemon.

    Features:
    - run: Start daemon in foreground
    - start: Start as background service
    - stop: Stop daemon
    - status: Get comprehensive status
    - thoughts: View autonomous thoughts
    - models: List loaded models
    - mine: Control Bitcoin mining
    - interact: Send messages to daemon
    - config: Show/edit configuration
    """

    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(
            prog="transformers-daemon",
            description="🤖 Transformers Autonomous Daemon - Always-Alive AI Agent",
            epilog="Making transformers ALIVE since 2026 🚀"
        )

        # Add global options
        self.parser.add_argument(
            "-v", "--verbose",
            action="store_true",
            help="Enable verbose output"
        )

        # Subcommands
        sub = self.parser.add_subparsers(dest="command", required=True)

        # Run command
        run_parser = sub.add_parser(
            "run",
            help="Run the daemon in foreground (for testing/development)"
        )
        run_parser.add_argument(
            "--config",
            default="transformers_daemon/config.yaml",
            help="Path to config file"
        )

        # Start command
        start_parser = sub.add_parser(
            "start",
            help="Start daemon as background service"
        )

        # Stop command
        stop_parser = sub.add_parser(
            "stop",
            help="Stop the daemon gracefully"
        )

        # Status command
        status_parser = sub.add_parser(
            "status",
            help="Get comprehensive daemon status"
        )
        status_parser.add_argument(
            "--json",
            action="store_true",
            help="Output as JSON"
        )

        # Thoughts command
        thoughts_parser = sub.add_parser(
            "thoughts",
            help="View recent autonomous thoughts"
        )
        thoughts_parser.add_argument(
            "--count",
            type=int,
            default=10,
            help="Number of thoughts to display"
        )

        # Models command
        models_parser = sub.add_parser(
            "models",
            help="List loaded transformer models"
        )

        # Mine command
        mine_parser = sub.add_parser(
            "mine",
            help="Control Bitcoin mining operations"
        )
        mine_parser.add_argument(
            "action",
            choices=["status", "start", "stop", "stats"],
            help="Mining action to perform"
        )

        # Interact command
        interact_parser = sub.add_parser(
            "interact",
            help="Send a message to the daemon"
        )
        interact_parser.add_argument(
            "message",
            help="Message to send"
        )

        # Config command
        config_parser = sub.add_parser(
            "config",
            help="Show or edit configuration"
        )
        config_parser.add_argument(
            "--show",
            action="store_true",
            help="Show current configuration"
        )

        # Demo command (exponential addition!)
        demo_parser = sub.add_parser(
            "demo",
            help="🚀 Run full system demonstration"
        )
        demo_parser.add_argument(
            "--duration",
            type=int,
            default=30,
            help="Demo duration in seconds"
        )

    def run(self, argv: list[str] | None = None) -> None:
        """Main entry point."""
        args = self.parser.parse_args(argv)

        if args.verbose:
            logging.getLogger().setLevel(logging.DEBUG)

        try:
            # Route to command handlers
            if args.command == "run":
                asyncio.run(self._cmd_run(args))
            elif args.command == "start":
                asyncio.run(self._cmd_start())
            elif args.command == "stop":
                asyncio.run(self._cmd_stop())
            elif args.command == "status":
                asyncio.run(self._cmd_status(args))
            elif args.command == "thoughts":
                asyncio.run(self._cmd_thoughts(args))
            elif args.command == "models":
                asyncio.run(self._cmd_models())
            elif args.command == "mine":
                asyncio.run(self._cmd_mine(args))
            elif args.command == "interact":
                asyncio.run(self._cmd_interact(args))
            elif args.command == "config":
                self._cmd_config(args)
            elif args.command == "demo":
                asyncio.run(self._cmd_demo(args))
        except KeyboardInterrupt:
            print("\n👋 Interrupted by user")
            sys.exit(0)
        except Exception as e:
            logger.error(f"Command failed: {e}")
            sys.exit(1)

    async def _cmd_run(self, args) -> None:
        """Run daemon in foreground."""
        print("="*80)
        print("🚀 Starting Transformers Autonomous Daemon")
        print("="*80)

        from .daemon import TransformersDaemon

        daemon = TransformersDaemon(config_path=args.config)
        await daemon.start()

    async def _cmd_start(self) -> None:
        """Start daemon as background service."""
        import subprocess

        print("🚀 Starting daemon as systemd service...")
        result = subprocess.run(
            ["sudo", "systemctl", "start", "transformers-daemon"],
            capture_output=True
        )

        if result.returncode == 0:
            print("✅ Daemon started successfully")
            print("Use 'transformers-daemon status' to check status")
        else:
            print("❌ Failed to start daemon")
            print(result.stderr.decode())

    async def _cmd_stop(self) -> None:
        """Stop the daemon."""
        import requests

        print("🛑 Stopping daemon...")

        try:
            response = requests.post("http://localhost:8080/shutdown", timeout=5)
            if response.status_code == 200:
                print("✅ Daemon stopping gracefully")
            else:
                print("⚠️  Daemon may not be running")
        except requests.exceptions.ConnectionError:
            print("❌ Cannot connect to daemon")

    async def _cmd_status(self, args) -> None:
        """Get daemon status."""
        import requests

        try:
            response = requests.get("http://localhost:8080/status", timeout=5)
            if response.status_code == 200:
                data = response.json()

                if args.json:
                    print(json.dumps(data, indent=2))
                else:
                    self._print_status(data)
            else:
                print("❌ Failed to get status")
        except requests.exceptions.ConnectionError:
            print("❌ Daemon is not running")
            print("Start with: transformers-daemon run")

    def _print_status(self, data: Dict[str, Any]) -> None:
        """Pretty print status."""
        print("="*80)
        print("📊 TRANSFORMERS DAEMON STATUS")
        print("="*80)

        print(f"\n🔹 Status: {data.get('status', 'UNKNOWN').upper()}")
        print(f"🔹 Uptime: {data.get('uptime', 0):.0f} seconds")
        print(f"🔹 Cycles: {data.get('cycles_completed', 0)}")
        print(f"🔹 Consciousness Level: {data.get('consciousness_level', 0):.2%}")

        components = data.get('components', {})
        print("\n🔹 Components:")
        for name, status in components.items():
            status_icon = "✅" if status else "❌"
            print(f"   {status_icon} {name}")

        print("\n" + "="*80)

    async def _cmd_thoughts(self, args) -> None:
        """View autonomous thoughts."""
        import requests

        try:
            response = requests.get("http://localhost:8080/thoughts", timeout=5)
            if response.status_code == 200:
                data = response.json()
                thoughts = data.get('thoughts', [])

                print("="*80)
                print(f"💭 RECENT AUTONOMOUS THOUGHTS (Last {args.count})")
                print("="*80)

                for i, thought in enumerate(thoughts[-args.count:], 1):
                    print(f"\n{i}. {thought.get('thought', 'N/A')}")
                    print(f"   Cycle: {thought.get('cycle', 'N/A')} | "
                          f"Time: {thought.get('timestamp', 'N/A')}")

                print("\n" + "="*80)
            else:
                print("❌ Failed to get thoughts")
        except requests.exceptions.ConnectionError:
            print("❌ Daemon is not running")

    async def _cmd_models(self) -> None:
        """List loaded models."""
        import requests

        try:
            response = requests.get("http://localhost:8080/models", timeout=5)
            if response.status_code == 200:
                data = response.json()
                models = data.get('models', [])

                print("="*80)
                print(f"🤖 LOADED TRANSFORMER MODELS ({len(models)})")
                print("="*80)

                for model in models:
                    print(f"  • {model}")

                print("\n" + "="*80)
            else:
                print("❌ Failed to get models")
        except requests.exceptions.ConnectionError:
            print("❌ Daemon is not running")

    async def _cmd_mine(self, args) -> None:
        """Control Bitcoin mining."""
        print(f"⛏️  Mining action: {args.action}")
        print("Mining control via API (implementation depends on daemon state)")

    async def _cmd_interact(self, args) -> None:
        """Interact with daemon."""
        import requests

        try:
            response = requests.post(
                "http://localhost:8080/interact",
                json={"message": args.message},
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                print(f"💬 Daemon: {data.get('message', 'No response')}")
            else:
                print("❌ Interaction failed")
        except requests.exceptions.ConnectionError:
            print("❌ Daemon is not running")

    def _cmd_config(self, args) -> None:
        """Show/edit config."""
        config_path = Path("transformers_daemon/config.yaml")

        if args.show:
            if config_path.exists():
                with open(config_path) as f:
                    print(f.read())
            else:
                print("❌ Config file not found")
        else:
            print(f"Config location: {config_path}")

    async def _cmd_demo(self, args) -> None:
        """Run comprehensive demo."""
        print("="*80)
        print("🎬 TRANSFORMERS DAEMON DEMONSTRATION")
        print("="*80)
        print(f"Duration: {args.duration} seconds\n")

        # Import and run quick demo
        from .quick_demo import run_quick_demo
        await run_quick_demo(duration=args.duration)


def main() -> None:
    """CLI entry point."""
    TransformersCLI().run()


if __name__ == "__main__":
    main()
