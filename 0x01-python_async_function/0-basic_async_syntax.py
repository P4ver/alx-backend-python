#!/usr/bin/env python3
""" My first async program """
import random
import asyncio


async def wait_random(max_delay: int = 10) -> float:
    """async program returns a float number
        with a random wait delay,
    """

    random_v = random.uniform(0, max_delay)
    await asyncio.sleep(random_v)
    return random_v
