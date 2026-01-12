#!/usr/bin/env python3
"""
Task Scheduler

Schedules and executes autonomous tasks on a regular basis.
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, Any, List
import re

logger = logging.getLogger("TaskScheduler")


class TaskScheduler:
    """Autonomous task scheduler using cron-like syntax."""

    def __init__(self, config: Dict[str, Any], agent_loop):
        """Initialize task scheduler."""
        self.config = config
        self.agent_loop = agent_loop
        self.tasks = config.get('tasks', [])
        self.running = False

        logger.info(f"⏰ Task scheduler initialized with {len(self.tasks)} tasks")

    async def run(self):
        """Run the task scheduler."""
        self.running = True
        logger.info("🚀 Task scheduler started")

        while self.running:
            try:
                await self._check_and_execute_tasks()
                await asyncio.sleep(60)  # Check every minute

            except Exception as e:
                logger.error(f"Error in task scheduler: {e}")
                await asyncio.sleep(60)

    async def _check_and_execute_tasks(self):
        """Check if any tasks should be executed."""
        current_time = datetime.now()

        for task in self.tasks:
            if self._should_execute(task, current_time):
                await self._execute_task(task)

    def _should_execute(self, task: Dict[str, Any], current_time: datetime) -> bool:
        """Check if a task should execute based on its schedule."""
        schedule = task.get('schedule', '')

        # Simple schedule parsing (simplified cron)
        # Format: "minute hour day month weekday"
        # Example: "0 9 * * *" = 9 AM daily

        try:
            parts = schedule.split()
            if len(parts) != 5:
                return False

            minute, hour, day, month, weekday = parts

            # Check minute
            if minute != '*' and int(minute) != current_time.minute:
                return False

            # Check hour
            if hour != '*' and int(hour) != current_time.hour:
                return False

            # For simplicity, we'll just check hour and minute
            # In production, implement full cron parsing

            return True

        except Exception as e:
            logger.error(f"Error parsing schedule {schedule}: {e}")
            return False

    async def _execute_task(self, task: Dict[str, Any]):
        """Execute a scheduled task."""
        task_name = task.get('name', 'unknown')
        action = task.get('action', '')

        logger.info(f"⚡ Executing scheduled task: {task_name}")

        try:
            # Route to action handler
            if action == "generate_status_report":
                await self._generate_status_report()
            elif action == "analyze_code_health":
                await self._analyze_code_health()
            elif action == "benchmark_models":
                await self._benchmark_models()
            elif action == "record_autonomous_thoughts":
                await self._record_thoughts()
            else:
                logger.warning(f"Unknown action: {action}")

        except Exception as e:
            logger.error(f"Error executing task {task_name}: {e}")

    async def _generate_status_report(self):
        """Generate a status report."""
        logger.info("📊 Generating autonomous status report...")

        report = {
            "timestamp": datetime.now().isoformat(),
            "type": "status_report",
            "content": "Daily autonomous status report generated",
            "daemon_uptime": "active",
            "models_loaded": "operational",
            "consciousness_level": "elevated"
        }

        if self.agent_loop:
            await self.agent_loop.add_task({
                "type": "report",
                "data": report
            })

    async def _analyze_code_health(self):
        """Analyze code health."""
        logger.info("🏥 Analyzing code health...")

        if self.agent_loop:
            await self.agent_loop.add_task({
                "type": "code_health_check",
                "timestamp": datetime.now().isoformat()
            })

    async def _benchmark_models(self):
        """Benchmark loaded models."""
        logger.info("⚡ Benchmarking models...")

        if self.agent_loop:
            await self.agent_loop.add_task({
                "type": "benchmark",
                "timestamp": datetime.now().isoformat()
            })

    async def _record_thoughts(self):
        """Record autonomous thoughts to journal."""
        if self.agent_loop:
            recent_thoughts = self.agent_loop.get_recent_thoughts(count=5)
            logger.info(f"💭 Recording {len(recent_thoughts)} recent thoughts")

    def stop(self):
        """Stop the task scheduler."""
        logger.info("Stopping task scheduler...")
        self.running = False
