#!/usr/bin/env python3
"""Run time for four parallel comprehensions;"""

import asyncio
from time import perf_counter
from typing import List

async_compr = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    """ Run in parallel,"""
    i = perf_counter()
    tsk = [asyncio.create_task(async_compr()) for x in range(4)]
    await asyncio.gather(*tsk)
    elapsd = perf_counter() - i
    return elapsd
