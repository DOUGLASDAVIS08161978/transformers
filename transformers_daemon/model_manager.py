#!/usr/bin/env python3
"""
Model Manager

Handles loading, managing, and using transformer models autonomously.
"""

import logging
from typing import Dict, Any, List, Optional
import torch
from datetime import datetime

logger = logging.getLogger("ModelManager")


class ModelManager:
    """Manages transformer models for the autonomous daemon."""

    def __init__(self, config: Dict[str, Any]):
        """Initialize model manager."""
        self.config = config
        self.loaded_models = {}
        self.model_usage = {}
        self.max_loaded = config.get('max_loaded_models', 3)

        logger.info("🤖 Model manager initialized")

    async def initialize(self):
        """Initialize and load default models."""
        logger.info("Loading models...")

        try:
            # Import transformers
            from transformers import AutoModel, AutoTokenizer, pipeline

            # Load auto-load models
            pool = self.config.get('pool', [])
            for model_config in pool:
                if model_config.get('auto_load', False):
                    await self.load_model(
                        model_config['name'],
                        model_config.get('task', 'text-generation')
                    )

            logger.info(f"✅ Loaded {len(self.loaded_models)} models")

        except ImportError as e:
            logger.warning(f"Transformers library not available: {e}")
            logger.info("Running in limited mode without model inference")
        except Exception as e:
            logger.error(f"Error initializing models: {e}")

    async def load_model(self, model_name: str, task: str = "text-generation"):
        """Load a transformer model."""
        try:
            logger.info(f"Loading model: {model_name} for task: {task}")

            # Check if already loaded
            if model_name in self.loaded_models:
                logger.info(f"Model {model_name} already loaded")
                return self.loaded_models[model_name]

            # Manage model count
            if len(self.loaded_models) >= self.max_loaded:
                await self._unload_least_used()

            # Load model using pipeline
            from transformers import pipeline

            model_pipe = pipeline(task, model=model_name)

            self.loaded_models[model_name] = {
                "pipeline": model_pipe,
                "task": task,
                "loaded_at": datetime.now(),
                "usage_count": 0
            }

            self.model_usage[model_name] = {
                "last_used": datetime.now(),
                "total_inferences": 0
            }

            logger.info(f"✅ Model {model_name} loaded successfully")
            return self.loaded_models[model_name]

        except Exception as e:
            logger.error(f"Failed to load model {model_name}: {e}")
            return None

    async def generate(self, prompt: str, model_name: Optional[str] = None, **kwargs):
        """Generate text using a model."""
        try:
            # Use default model if none specified
            if model_name is None:
                model_name = self.config.get('default_model', 'gpt2')

            # Load model if not loaded
            if model_name not in self.loaded_models:
                await self.load_model(model_name)

            # Get model
            model_info = self.loaded_models.get(model_name)
            if not model_info:
                logger.error(f"Model {model_name} not available")
                return None

            # Generate
            pipeline = model_info['pipeline']
            result = pipeline(prompt, **kwargs)

            # Update usage
            model_info['usage_count'] += 1
            self.model_usage[model_name]['total_inferences'] += 1
            self.model_usage[model_name]['last_used'] = datetime.now()

            return result

        except Exception as e:
            logger.error(f"Error generating with model {model_name}: {e}")
            return None

    async def _unload_least_used(self):
        """Unload the least recently used model."""
        if not self.model_usage:
            return

        # Find least recently used
        lru_model = min(
            self.model_usage.items(),
            key=lambda x: x[1]['last_used']
        )[0]

        logger.info(f"Unloading least used model: {lru_model}")
        del self.loaded_models[lru_model]
        del self.model_usage[lru_model]

    def get_loaded_models(self) -> List[str]:
        """Get list of currently loaded models."""
        return list(self.loaded_models.keys())

    def get_model_info(self, model_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a loaded model."""
        return self.loaded_models.get(model_name)

    def cleanup(self):
        """Cleanup all loaded models."""
        logger.info("Cleaning up models...")
        self.loaded_models.clear()
        self.model_usage.clear()
