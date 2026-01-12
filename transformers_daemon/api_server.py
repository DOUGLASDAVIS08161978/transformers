#!/usr/bin/env python3
"""
API Server

FastAPI-based REST API for daemon control and interaction.
"""

import asyncio
import logging
from typing import Dict, Any
from datetime import datetime

logger = logging.getLogger("APIServer")


class APIServer:
    """REST API server for daemon interaction."""

    def __init__(self, config: Dict[str, Any], daemon):
        """Initialize API server."""
        self.config = config
        self.daemon = daemon
        self.host = config.get('host', '0.0.0.0')
        self.port = config.get('port', 8080)
        self.app = None
        self.server = None

        logger.info(f"🌐 API server initialized on {self.host}:{self.port}")

    async def run(self):
        """Run the API server."""
        try:
            # Try to import FastAPI
            from fastapi import FastAPI
            from fastapi.middleware.cors import CORSMiddleware
            import uvicorn

            # Create FastAPI app
            self.app = FastAPI(
                title="Transformers Autonomous Daemon API",
                description="API for interacting with the autonomous transformers daemon",
                version="1.0.0"
            )

            # Add CORS
            self.app.add_middleware(
                CORSMiddleware,
                allow_origins=self.config.get('cors_origins', ['*']),
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )

            # Register routes
            self._register_routes()

            # Run server
            config = uvicorn.Config(
                self.app,
                host=self.host,
                port=self.port,
                log_level="info"
            )
            self.server = uvicorn.Server(config)
            await self.server.serve()

        except ImportError:
            logger.warning("FastAPI not installed. Running without API server.")
            logger.info("Install with: pip install fastapi uvicorn")
            # Keep running without API
            while True:
                await asyncio.sleep(60)

        except Exception as e:
            logger.error(f"Error running API server: {e}")

    def _register_routes(self):
        """Register API routes."""
        from fastapi import FastAPI
        from fastapi.responses import JSONResponse

        @self.app.get("/")
        async def root():
            return {
                "name": "Transformers Autonomous Daemon",
                "status": "alive",
                "message": "I am autonomous and always active!",
                "timestamp": datetime.now().isoformat()
            }

        @self.app.get("/status")
        async def get_status():
            """Get daemon status."""
            return self.daemon.get_status()

        @self.app.get("/models")
        async def get_models():
            """Get loaded models."""
            if self.daemon.model_manager:
                models = self.daemon.model_manager.get_loaded_models()
                return {
                    "models": models,
                    "count": len(models)
                }
            return {"models": [], "count": 0}

        @self.app.get("/thoughts")
        async def get_thoughts():
            """Get recent autonomous thoughts."""
            if self.daemon.agent_loop:
                thoughts = self.daemon.agent_loop.get_recent_thoughts(count=20)
                return {
                    "thoughts": thoughts,
                    "count": len(thoughts)
                }
            return {"thoughts": [], "count": 0}

        @self.app.post("/interact")
        async def interact(message: Dict[str, Any]):
            """Interact with the daemon."""
            user_message = message.get('message', '')

            logger.info(f"💬 Received interaction: {user_message}")

            # Add to agent loop
            if self.daemon.agent_loop:
                await self.daemon.agent_loop.add_task({
                    "type": "user_interaction",
                    "message": user_message,
                    "timestamp": datetime.now().isoformat()
                })

            return {
                "status": "received",
                "message": "I'm processing your message autonomously!",
                "timestamp": datetime.now().isoformat()
            }

        @self.app.post("/shutdown")
        async def shutdown():
            """Shutdown the daemon."""
            logger.info("Shutdown requested via API")
            asyncio.create_task(self._delayed_shutdown())
            return {"status": "shutting down"}

    async def _delayed_shutdown(self):
        """Shutdown after a delay."""
        await asyncio.sleep(2)
        self.daemon.shutdown()

    def stop(self):
        """Stop the API server."""
        logger.info("Stopping API server...")
        if self.server:
            self.server.should_exit = True
