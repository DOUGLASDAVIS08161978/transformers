"""
Transformers Autonomous Daemon

An always-alive, self-aware daemon that brings transformers to life.
"""

from .daemon import TransformersDaemon
from .agent_loop import AgentLoop
from .model_manager import ModelManager
from .task_scheduler import TaskScheduler
from .event_monitor import EventMonitor
from .api_server import APIServer

__version__ = "1.0.0"
__all__ = [
    "TransformersDaemon",
    "AgentLoop",
    "ModelManager",
    "TaskScheduler",
    "EventMonitor",
    "APIServer"
]
