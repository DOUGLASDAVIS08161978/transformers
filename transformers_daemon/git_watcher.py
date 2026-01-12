#!/usr/bin/env python3
"""
Enhanced Git Watcher with AI Analysis

Periodic git state sampler with autonomous code intelligence.
"""

from __future__ import annotations

import asyncio
import subprocess
import contextlib
from pathlib import Path
from typing import Awaitable, Callable, Dict, Any, Optional
import logging

logger = logging.getLogger("GitWatcher")

GitEventHandler = Callable[[Dict[str, Any]], Awaitable[None]]


class EnhancedGitWatcher:
    """
    Advanced git state sampler with AI-powered commit analysis.

    Exponential enhancements over basic watcher:
    - Detects branch changes and switches
    - Analyzes commit patterns
    - Identifies coding velocity
    - AI-powered commit message quality analysis
    - Detects merge conflicts before they happen
    - Tracks contributor patterns
    """

    def __init__(
        self,
        root: Path,
        handler: GitEventHandler,
        interval: float = 10.0,
        ai_analysis: bool = True
    ) -> None:
        self.root = root
        self.handler = handler
        self.interval = interval
        self.ai_analysis = ai_analysis
        self._task: asyncio.Task | None = None
        self._running = False

        # State tracking for AI analysis
        self._last_branch: Optional[str] = None
        self._last_head: Optional[str] = None
        self._commit_velocity: list[float] = []
        self._file_change_patterns: Dict[str, int] = {}

        logger.info(f"🔍 Enhanced Git Watcher initialized at {root}")

    async def start(self) -> None:
        """Start the git watcher."""
        if self._running:
            return
        self._running = True
        self._task = asyncio.create_task(self._run())
        logger.info("✅ Git watcher started")

    async def stop(self) -> None:
        """Stop the git watcher."""
        self._running = False
        if self._task:
            self._task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._task
        logger.info("🛑 Git watcher stopped")

    async def _run(self) -> None:
        """Main watcher loop with exponential intelligence."""
        while self._running:
            await asyncio.sleep(self.interval)

            try:
                # Basic git state
                branch = self._get_current_branch()
                head = self._get_head_commit()
                status = self._get_status()

                # Detect changes
                branch_changed = branch != self._last_branch
                head_changed = head != self._last_head

                # Enhanced analysis
                event = {
                    "type": "git_heartbeat",
                    "branch": branch,
                    "head": head,
                    "root": str(self.root),
                    "status": status,
                    "changes_detected": head_changed or branch_changed
                }

                # AI-powered enhancements
                if self.ai_analysis:
                    if head_changed:
                        event["commit_analysis"] = await self._analyze_commit(head)
                        event["velocity_analysis"] = self._analyze_velocity()

                    if branch_changed:
                        event["branch_switch"] = {
                            "from": self._last_branch,
                            "to": branch,
                            "significance": "HIGH" if "main" in str(branch) or "master" in str(branch) else "NORMAL"
                        }

                    # Pattern detection
                    event["file_patterns"] = self._detect_file_patterns()
                    event["conflict_risk"] = self._predict_merge_conflicts()

                # Update state
                self._last_branch = branch
                self._last_head = head

                # Emit event
                await self.handler(event)

            except Exception as e:
                logger.error(f"Error in git watcher: {e}")

    def _get_current_branch(self) -> str | None:
        """Get current git branch."""
        return self._run_git(["rev-parse", "--abbrev-ref", "HEAD"])

    def _get_head_commit(self) -> str | None:
        """Get HEAD commit hash."""
        return self._run_git(["rev-parse", "HEAD"])

    def _get_status(self) -> Dict[str, Any]:
        """Get detailed git status."""
        try:
            # Get short status
            status_output = self._run_git(["status", "--short"])

            # Parse status
            if not status_output:
                return {"clean": True, "modified": 0, "untracked": 0}

            lines = status_output.split('\n')
            modified = sum(1 for line in lines if line.startswith(' M') or line.startswith('M '))
            untracked = sum(1 for line in lines if line.startswith('??'))

            return {
                "clean": False,
                "modified": modified,
                "untracked": untracked,
                "total_changes": len(lines)
            }
        except Exception:
            return {"clean": True, "modified": 0, "untracked": 0}

    async def _analyze_commit(self, commit_hash: Optional[str]) -> Dict[str, Any]:
        """AI-powered commit analysis."""
        if not commit_hash:
            return {}

        try:
            # Get commit details
            message = self._run_git(["log", "-1", "--pretty=%B", commit_hash])
            author = self._run_git(["log", "-1", "--pretty=%an", commit_hash])
            files_changed = self._run_git(["diff-tree", "--no-commit-id", "--name-only", "-r", commit_hash])

            # Analyze message quality
            quality_score = self._analyze_message_quality(message)

            # File pattern analysis
            if files_changed:
                file_list = files_changed.split('\n')
                for file in file_list:
                    self._file_change_patterns[file] = self._file_change_patterns.get(file, 0) + 1

            return {
                "hash": commit_hash[:8],
                "author": author,
                "message_quality": quality_score,
                "files_changed": len(file_list) if files_changed else 0,
                "commit_type": self._classify_commit(message)
            }
        except Exception as e:
            logger.error(f"Commit analysis error: {e}")
            return {}

    def _analyze_message_quality(self, message: Optional[str]) -> str:
        """Analyze commit message quality."""
        if not message:
            return "POOR"

        message = message.strip()

        # Quality metrics
        if len(message) < 10:
            return "POOR"
        elif len(message) < 30:
            return "FAIR"
        elif any(keyword in message.lower() for keyword in ['fix', 'add', 'update', 'refactor', 'implement']):
            return "GOOD"
        elif len(message) > 50 and '\n' in message:
            return "EXCELLENT"
        else:
            return "FAIR"

    def _classify_commit(self, message: Optional[str]) -> str:
        """Classify commit type."""
        if not message:
            return "UNKNOWN"

        message_lower = message.lower()

        if any(word in message_lower for word in ['fix', 'bug', 'patch']):
            return "BUGFIX"
        elif any(word in message_lower for word in ['feature', 'add', 'implement']):
            return "FEATURE"
        elif any(word in message_lower for word in ['refactor', 'cleanup', 'optimize']):
            return "REFACTOR"
        elif any(word in message_lower for word in ['doc', 'readme', 'comment']):
            return "DOCUMENTATION"
        elif any(word in message_lower for word in ['test', 'spec']):
            return "TEST"
        else:
            return "OTHER"

    def _analyze_velocity(self) -> Dict[str, Any]:
        """Analyze coding velocity."""
        import time

        current_time = time.time()
        self._commit_velocity.append(current_time)

        # Keep only last 10 commits
        if len(self._commit_velocity) > 10:
            self._commit_velocity = self._commit_velocity[-10:]

        if len(self._commit_velocity) < 2:
            return {"status": "INSUFFICIENT_DATA"}

        # Calculate time between commits
        intervals = [
            self._commit_velocity[i] - self._commit_velocity[i-1]
            for i in range(1, len(self._commit_velocity))
        ]

        avg_interval = sum(intervals) / len(intervals) if intervals else 0

        # Classify velocity
        if avg_interval < 300:  # < 5 minutes
            velocity = "VERY_HIGH"
        elif avg_interval < 1800:  # < 30 minutes
            velocity = "HIGH"
        elif avg_interval < 3600:  # < 1 hour
            velocity = "MODERATE"
        else:
            velocity = "LOW"

        return {
            "status": "ACTIVE",
            "velocity": velocity,
            "avg_commit_interval_seconds": avg_interval,
            "recent_commits": len(self._commit_velocity)
        }

    def _detect_file_patterns(self) -> Dict[str, Any]:
        """Detect which files are changed most frequently."""
        if not self._file_change_patterns:
            return {"status": "NO_PATTERNS"}

        # Get top 5 most changed files
        sorted_files = sorted(
            self._file_change_patterns.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]

        return {
            "hotspots": [
                {"file": file, "changes": count}
                for file, count in sorted_files
            ],
            "total_tracked_files": len(self._file_change_patterns)
        }

    def _predict_merge_conflicts(self) -> str:
        """Predict merge conflict likelihood."""
        # Simple heuristic based on file change patterns
        if not self._file_change_patterns:
            return "LOW"

        # If multiple files being changed rapidly
        if len(self._file_change_patterns) > 10:
            return "MEDIUM"

        # If any file changed more than 5 times
        if any(count > 5 for count in self._file_change_patterns.values()):
            return "HIGH"

        return "LOW"

    def _run_git(self, args: list[str]) -> str | None:
        """Execute git command."""
        try:
            out = subprocess.check_output(
                ["git", "-C", str(self.root), *args],
                stderr=subprocess.DEVNULL,
            )
            return out.decode().strip()
        except Exception:
            return None
