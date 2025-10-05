import time
from collections import deque
from threading import Lock


class RateLimiter:
    def __init__(self, max_calls: int = 5000, time_window: int = 3600):
        self.max_calls = max_calls
        self.time_window = time_window
        self.calls = deque()
        self.lock = Lock()
    
    def _clean_old_calls(self):
        current_time = time.time()
        while self.calls and current_time - self.calls[0] > self.time_window:
            self.calls.popleft()
    
    def can_make_call(self) -> bool:
        with self.lock:
            self._clean_old_calls()
            return len(self.calls) < self.max_calls
    
    def record_call(self):
        with self.lock:
            self._clean_old_calls()
            self.calls.append(time.time())
    
    def wait_if_needed(self):
        while not self.can_make_call():
            time.sleep(1)
        self.record_call()
    
    def get_remaining_calls(self) -> int:
        with self.lock:
            self._clean_old_calls()
            return self.max_calls - len(self.calls)
    
    def get_reset_time(self) -> float:
        with self.lock:
            if not self.calls:
                return 0
            return self.calls[0] + self.time_window
