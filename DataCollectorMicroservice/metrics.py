import prometheus_client

# ... (altri import esistenti)

# Definiamo la metrica Gauge
FLIGHTS_DOWNLOAD_TIME = prometheus_client.Gauge(
    'datacollector_download_time',
    'Tempo di download',
    ['service', 'resource'],

)


