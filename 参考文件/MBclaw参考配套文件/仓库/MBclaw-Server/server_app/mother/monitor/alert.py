from __future__ import annotations


class AlertManager:

    def __init__(self):

        self.thresholds = {
            "cpu_usage": 85,
            "ram_usage": 85,
            "api_latency": 2.0,
            "queue_length": 50
        }

    def check(self, events: list):

        alerts = []

        for e in events:

            threshold = self.thresholds.get(e.name)

            if threshold is None:
                continue

            if e.value > threshold:

                alerts.append({
                    "metric": e.name,
                    "value": e.value,
                    "threshold": threshold,
                    "severity": "high"
                })

        return alerts
