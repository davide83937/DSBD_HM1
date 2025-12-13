import time
import threading

class CircuitBreaker:
    def __init__(self, failure_threshold=2, recovery_timeout=15, expected_exception=Exception):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception
        self.failure_count = 0
        self.last_failure_time = None
        self.state = 'CLOSED'
        self.lock = threading.Lock()

    def call(self, func, *args, **kwargs):
        with self.lock:
            if self.state == 'OPEN':
                time_since_failure = time.time() - self.last_failure_time
                if time_since_failure > self.recovery_timeout:
                    self.state = 'HALF_OPEN'
                else:
                    print('Circuit breaker is open yet', flush=True)
                    raise CircuitBreakerOpenException("Circuit is open. Call denied.")

            try:
                result = func(*args, **kwargs)
            except self.expected_exception as e:
                self.failure_count += 1
                self.last_failure_time = time.time()
                if self.failure_count >= self.failure_threshold:
                    print('Circuit breaker is opened', flush=True)
                    self.state = 'OPEN'
                raise e
            else:
                if self.state == 'HALF_OPEN':
                    print('Circuit breaker is closed', flush=True)
                    self.state = 'CLOSED'

                    self.failure_count = 0
                return result

class CircuitBreakerOpenException(Exception):
    pass
