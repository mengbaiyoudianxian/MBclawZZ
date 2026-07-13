from runtime_kernel.worker import Worker


class WorkerPool:

    def __init__(self, size=3):

        self.workers = [Worker() for _ in range(size)]

    def acquire(self):

        for w in self.workers:
            if w.state == "IDLE":
                return w

        return self.workers[0]  # fallback
