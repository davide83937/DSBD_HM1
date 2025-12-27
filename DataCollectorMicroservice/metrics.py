import prometheus_client


# Definiamo la metrica Gauge
FLIGHTS_DOWNLOAD_DATA = prometheus_client.Gauge(
    'datacollector_download_data',
    'Tempo di download',
    ['service', 'node', 'resource'],
)

NUM_FLIGHTS_DOWNLOADED = prometheus_client.Counter(
    'datacollector_num_flights_downloaded',
    'Numero di voli scaricati',
    ['service', 'node', 'resource'],
)

