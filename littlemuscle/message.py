from typing import Any

class Message:
    def __init__(self, time: float, next_time: float, data: Any):
        self.time = time
        self.next_time = next_time
        self.data = data


    def __format__(self, format_spec: str) -> str:
        return 'Message({}, {}, {})'.format(self.time, self.next_time, self.data)


    def __str__(self) -> str:
        return 'Message({}, {}, {})'.format(self.time, self.next_time, self.data)
