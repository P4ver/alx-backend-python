#!/usr/bin/env python3
"""Async Comprehensions,"""

import asyncio
from typing import List

async_gen = __import__('0-async_generator').async_generator


async def async_comprehension() -> List[float]:
    """ Collect random numbers using async,"""
    return [i async for i in async_gen()]
