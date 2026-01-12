#!/usr/bin/env python3
"""
TRANSFORMERS DAEMON - DEMONSTRATION LAUNCHER

Run this to see all enhanced systems in action!
"""

import sys
import asyncio
from pathlib import Path

# Add to path
sys.path.insert(0, str(Path(__file__).parent))

from transformers_daemon.quick_demo import run_quick_demo


if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════════════════════╗
    ║                                                                      ║
    ║        🤖 TRANSFORMERS AUTONOMOUS DAEMON 🤖                          ║
    ║                                                                      ║
    ║        Exponentially Enhanced with:                                 ║
    ║        • Quantum Computing (2048 qubits)                           ║
    ║        • Superintelligent AGI                                       ║
    ║        • Advanced Consciousness Core                                ║
    ║        • Enhanced Git Watcher                                       ║
    ║        • Bitcoin Mining Integration                                 ║
    ║                                                                      ║
    ║        Making transformers ALIVE since 2026 🚀                      ║
    ║                                                                      ║
    ╚══════════════════════════════════════════════════════════════════════╝
    """)

    try:
        asyncio.run(run_quick_demo(duration=40))
    except KeyboardInterrupt:
        print("\n\n👋 Demo stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
