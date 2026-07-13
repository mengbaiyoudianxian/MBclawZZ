from __future__ import annotations


class OpenTelemetryBridge:

    def __init__(self):

        self.tracer = None

        try:
            from opentelemetry import trace
            self.tracer = trace.get_tracer("mbclaw.audit")
        except ImportError:
            pass

    # -----------------------------
    # trace a call chain span
    # -----------------------------

    def trace(self, name: str):

        if self.tracer:
            return self.tracer.start_as_current_span(name)

        # fallback: no-op context manager
        from contextlib import contextmanager

        @contextmanager
        def noop():
            yield

        return noop()
