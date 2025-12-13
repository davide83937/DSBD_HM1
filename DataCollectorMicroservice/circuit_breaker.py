import time
import threading

class CircuitBreaker:
    def __init__(self, failure_threshold=5, recovery_timeout=30, expected_exception=Exception):
        self.failure_threshold = failure_threshold  # Threshold for failures to open the circuit
        self.recovery_timeout = recovery_timeout  # Timeout before attempting to reset the circuit
        self.expected_exception = expected_exception  # Exception type to monitor
        self.failure_count = 0  # Counter for consecutive failures
        self.last_failure_time = None  # Timestamp of the last failure
        self.state = 'CLOSED'  # Initial state of the circuit
        self.lock = threading.Lock()  # Lock to ensure thread-safe operations

    def call(self, func, *args, **kwargs):

        with self.lock:
            if self.state == 'OPEN':
                time_since_failure = time.time() - self.last_failure_time
                if time_since_failure > self.recovery_timeout:
                    self.state = 'HALF_OPEN'
                    print('Circuit breaker is halfopeneed', flush=True)
                    #raise CircuitBreakerOpenException
                else:
                    print('Circuit breaker is open yet', flush=True)
                    raise CircuitBreakerOpenException("Circuit is open. Call denied.")

            try:
                result = func(*args, **kwargs)
            except self.expected_exception as e:
                # Function raised an expected exception; increment failure count
                self.failure_count += 1
                self.last_failure_time = time.time()  # Update the last failure timestamp
                if self.failure_count >= self.failure_threshold:
                    print('Circuit breaker is opened', flush=True)
                    self.state = 'OPEN'
                raise e
            else:
                if self.state == 'HALF_OPEN':
                    print('Circuit breaker is closed', flush=True)
                    self.state = 'CLOSED'

                    self.failure_count = 0  # Reset failure count
                return result

class CircuitBreakerOpenException(Exception):
    """Custom exception raised when the circuit breaker is open."""
    pass
