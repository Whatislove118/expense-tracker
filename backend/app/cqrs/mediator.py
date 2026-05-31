from typing import Any


class Mediator:
    def __init__(self) -> None:
        self._handlers: dict[type, Any] = {}

    def register(self, message_type: type, handler: Any) -> None:
        self._handlers[message_type] = handler

    async def send(self, message: Any) -> Any:
        handler = self._handlers.get(type(message))
        if handler is None:
            raise ValueError(f"No handler registered for {type(message).__name__}")
        return await handler.handle(message)
