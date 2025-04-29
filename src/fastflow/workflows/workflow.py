import functools
from typing import Callable, List, Optional

from .consumer_activity import ConsumerActivity
from .producer_activity import ProducerActivity
from .task_activity import TaskActivity


class Workflow:
    __slots__ = [
        "_name",
        "_inputs",
        "_activities",
    ]

    def __init__(self, name: str):
        self._name = name
        self._inputs = []
        self._activities = []

    @property
    def name(self):
        return self._name

    @property
    def inputs(self):
        return self._inputs

    @property
    def activities(self):
        return self._activities

    def input(self):
        def decorator(func):
            @functools.wraps(func)
            async def wrapper(val: str):
                result = await func(val)
                return result

            self._inputs.append(wrapper)
            return wrapper

        return decorator

    def producer(
        self,
        topic: str,
        *,
        after: List[Callable] = [],
    ):
        def decorator(func):
            @functools.wraps(func)
            async def wrapper():
                return await func()

            activity = ProducerActivity(
                wrapper,
                topic,
                after=after,
            )
            self._activities.append(activity)
            return wrapper

        return decorator

    def consumer(
        self,
        topic: str,
        *,
        after: List[Callable] = [],
        offset: Optional[int | Callable] = None,
    ):
        def decorator(func):
            @functools.wraps(func)
            async def wrapper():
                return await func()

            activity = ConsumerActivity(
                wrapper,
                topic,
                offset=offset,
                after=after,
            )
            self._activities.append(activity)
            return wrapper

        return decorator

    def task(
        self,
        after: Optional[List[Callable]] = None,
    ):
        def decorator(func):
            @functools.wraps(func)
            async def wrapper():
                return await func()

            # self._activities.append(wrapper)
            activity = TaskActivity(
                wrapper,
                after=after,
            )
            self._activities.append(activity)
            return wrapper

        return decorator
