from flask import Flask, Response
import logging
import time

from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST


app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger(__name__)

REQUEST_COUNT = Counter(
    "flask_http_requests_total",
    "Total number of HTTP requests",
    ["method", "endpoint", "http_status"],
)

REQUEST_LATENCY = Histogram(
    "flask_http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "endpoint"],
)


@app.before_request
def before_request():
    from flask import request

    request.start_time = time.time()


@app.after_request
def after_request(response):
    from flask import request

    endpoint = request.path
    REQUEST_COUNT.labels(request.method, endpoint, response.status_code).inc()
    REQUEST_LATENCY.labels(request.method, endpoint).observe(time.time() - request.start_time)
    return response


@app.route("/")
def home():
    logger.info("Received request on home page")
    return "Hello, Monitoring!"


@app.route("/error")
def error():
    logger.error("Test error endpoint was called")
    return "Error was logged", 500


@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
