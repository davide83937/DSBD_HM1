import prometheus_client

LOGIN_LATENCY = prometheus_client.Gauge(
    'usermanager_login_response_time_seconds',
    'Tempo di risposta ultima richiesta di login',
    ['service', 'node', 'resource'])


LOGIN_COUNTER = prometheus_client.Counter(
    'usermanager_login_attempts_total',
    'Numero totale di tentativi di login',
    ['service', 'node', 'resource'] # status può essere 'success' o 'failure'
)