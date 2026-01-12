#!/usr/bin/env python3
"""
Event Monitor

Monitors file system changes, webhooks, and external events.
"""

import asyncio
import logging
from typing import Dict, Any, List
from pathlib import Path
from datetime import datetime

logger = logging.getLogger("EventMonitor")


class EventMonitor:
    """Monitors events and triggers autonomous responses."""

    def __init__(self, config: Dict[str, Any], agent_loop):
        """Initialize event monitor."""
        self.config = config
        self.agent_loop = agent_loop
        self.running = False

        self.watch_paths = config.get('watch_paths', [])
        self.last_check = {}

        logger.info(f"👀 Event monitor initialized with {len(self.watch_paths)} watch paths")

    async def run(self):
        """Run the event monitor."""
        self.running = True
        logger.info("🚀 Event monitor started")

        # Initialize file watching
        for watch_path in self.watch_paths:
            path = watch_path.get('path', '')
            self.last_check[path] = datetime.now()

        while self.running:
            try:
                await self._check_file_changes()
                await self._check_external_events()
                await asyncio.sleep(10)  # Check every 10 seconds

            except Exception as e:
                logger.error(f"Error in event monitor: {e}")
                await asyncio.sleep(10)

    async def _check_file_changes(self):
        """Check for file system changes."""
        for watch_config in self.watch_paths:
            path = watch_config.get('path', '')
            events = watch_config.get('events', [])
            recursive = watch_config.get('recursive', True)

            try:
                # Simple file modification check
                p = Path(path)
                if p.exists() and p.is_dir():
                    # Check for recent modifications
                    await self._scan_directory(p, events, recursive)

            except Exception as e:
                logger.error(f"Error checking path {path}: {e}")

    async def _scan_directory(self, path: Path, events: List[str], recursive: bool):
        """Scan directory for changes."""
        try:
            # Get recently modified files
            recent_files = []
            pattern = "**/*" if recursive else "*"

            for file_path in path.glob(pattern):
                if file_path.is_file():
                    mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                    if mtime > self.last_check.get(str(path), datetime.min):
                        recent_files.append(file_path)

            # Update last check time
            self.last_check[str(path)] = datetime.now()

            # Trigger events for modified files
            if recent_files and self.agent_loop:
                logger.info(f"📝 Detected {len(recent_files)} changed files in {path}")

                await self.agent_loop.add_task({
                    "type": "file_change_event",
                    "path": str(path),
                    "files": [str(f) for f in recent_files[:10]],  # Limit to 10
                    "timestamp": datetime.now().isoformat()
                })

        except Exception as e:
            logger.error(f"Error scanning directory {path}: {e}")

    async def _check_external_events(self):
        """Check for external events (APIs, webhooks, etc)."""
        # This would check external APIs, GitHub webhooks, etc.
        # Simplified for this implementation
        pass

    def trigger_event(self, event_type: str, data: Dict[str, Any]):
        """Manually trigger an event."""
        logger.info(f"🎯 Event triggered: {event_type}")

        if self.agent_loop:
            asyncio.create_task(self.agent_loop.add_task({
                "type": event_type,
                "data": data,
                "timestamp": datetime.now().isoformat()
            }))

    def stop(self):
        """Stop the event monitor."""
        logger.info("Stopping event monitor...")
        self.running = False
