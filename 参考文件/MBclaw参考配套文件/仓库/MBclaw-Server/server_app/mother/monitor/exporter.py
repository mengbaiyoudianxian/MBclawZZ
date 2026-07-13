from __future__ import annotations

from monitor.metrics import MetricEvent


class PrometheusExporter:

    def format(self, events: list[MetricEvent]) -> str:

        lines = []

        for e in events:

            labels = ",".join(
                f'{k}="{v}"' for k, v in e.tags.items()
            )

            if labels:
                lines.append(f"{e.name}{{{labels}}} {e.value}")
            else:
                lines.append(f"{e.name} {e.value}")

        return "\n".join(lines)
