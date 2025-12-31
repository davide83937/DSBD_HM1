import prometheus_client
from flask import Flask
from UserManagerMicroservice import app
import metrics

appl = Flask(__name__)
appl.register_blueprint(app)

if __name__ == "__main__":
    prometheus_client.start_http_server(9999)
    metrics.LOGIN_LATENCY.labels(service='usermanager', node=metrics.NODE_NAME, resource='login_latency').set(0)
    metrics.LOGIN_COUNTER.labels(service='usermanager', node=metrics.NODE_NAME, resource='login_counter').inc(0)
    appl.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)

