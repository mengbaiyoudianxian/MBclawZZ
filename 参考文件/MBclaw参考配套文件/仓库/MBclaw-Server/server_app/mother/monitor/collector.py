from __future__ import annotations

import time

from monitor.metrics import MetricEvent


class SystemCollector:

    def collect_system(self):

        try:
            import psutil
            return [
                MetricEvent("cpu_usage", psutil.cpu_percent()),
                MetricEvent("ram_usage", psutil.virtual_memory().percent),
                MetricEvent("disk_usage", psutil.disk_usage("/").percent),
                MetricEvent("timestamp", time.time())
            ]
        except ImportError:
            return [
                MetricEvent("cpu_usage", 0),
                MetricEvent("ram_usage", 0),
                MetricEvent("timestamp", time.time())
            ]


class RuntimeCollector:

    def collect_runtime(self, runtime_state: dict):

        return [
            MetricEvent(
                name="token_usage",
                value=runtime_state.get("token_usage", 0)
            ),
            MetricEvent(
                name="api_latency",
                value=runtime_state.get("latency", 0)
            ),
            MetricEvent(
                name="queue_length",
                value=runtime_state.get("queue", 0)
            )
        ]
