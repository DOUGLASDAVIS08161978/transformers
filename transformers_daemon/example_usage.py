#!/usr/bin/env python3
"""
Example: How to use the Transformers Autonomous Daemon

This script demonstrates how to interact with the daemon
both programmatically and via the API.
"""

import asyncio
import requests
import time


def check_daemon_status():
    """Check if daemon is running."""
    try:
        response = requests.get("http://localhost:8080/status", timeout=5)
        if response.status_code == 200:
            print("✅ Daemon is running!")
            print(f"Status: {response.json()}")
            return True
        else:
            print("❌ Daemon is not responding correctly")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to daemon. Is it running?")
        print("Start with: python3 -m transformers_daemon.daemon")
        return False


def get_daemon_thoughts():
    """Get recent autonomous thoughts."""
    try:
        response = requests.get("http://localhost:8080/thoughts", timeout=5)
        if response.status_code == 200:
            data = response.json()
            thoughts = data.get('thoughts', [])
            print(f"\n💭 Recent Thoughts ({len(thoughts)}):")
            for i, thought in enumerate(thoughts[-5:], 1):
                print(f"{i}. {thought.get('thought', 'N/A')}")
        else:
            print("Failed to get thoughts")
    except Exception as e:
        print(f"Error getting thoughts: {e}")


def get_loaded_models():
    """Get currently loaded models."""
    try:
        response = requests.get("http://localhost:8080/models", timeout=5)
        if response.status_code == 200:
            data = response.json()
            models = data.get('models', [])
            print(f"\n🤖 Loaded Models ({len(models)}):")
            for model in models:
                print(f"  - {model}")
        else:
            print("Failed to get models")
    except Exception as e:
        print(f"Error getting models: {e}")


def interact_with_daemon(message: str):
    """Send a message to the daemon."""
    try:
        response = requests.post(
            "http://localhost:8080/interact",
            json={"message": message},
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            print(f"\n💬 Daemon Response:")
            print(f"  {data.get('message', 'No response')}")
        else:
            print("Failed to interact with daemon")
    except Exception as e:
        print(f"Error interacting with daemon: {e}")


def monitor_daemon(duration_seconds: int = 30):
    """Monitor daemon for a period of time."""
    print(f"\n👀 Monitoring daemon for {duration_seconds} seconds...")
    print("Press Ctrl+C to stop\n")

    start_time = time.time()
    try:
        while time.time() - start_time < duration_seconds:
            response = requests.get("http://localhost:8080/status", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"⏱️  Uptime: {data.get('uptime', 0):.0f}s | "
                      f"Cycles: {data.get('cycles_completed', 0)} | "
                      f"Consciousness: {data.get('consciousness_level', 0):.2f}")
            time.sleep(5)
    except KeyboardInterrupt:
        print("\nMonitoring stopped")


def main():
    """Main example function."""
    print("="*60)
    print("Transformers Autonomous Daemon - Example Usage")
    print("="*60)

    # Check if daemon is running
    if not check_daemon_status():
        return

    # Get current status
    print("\n" + "="*60)
    print("DAEMON INFORMATION")
    print("="*60)

    get_loaded_models()
    get_daemon_thoughts()

    # Interact with daemon
    print("\n" + "="*60)
    print("INTERACTION")
    print("="*60)

    interact_with_daemon("Hello! What are you working on?")

    # Monitor for a short time
    print("\n" + "="*60)
    print("MONITORING")
    print("="*60)

    monitor_daemon(duration_seconds=20)

    print("\n" + "="*60)
    print("Example complete!")
    print("="*60)


if __name__ == "__main__":
    main()
