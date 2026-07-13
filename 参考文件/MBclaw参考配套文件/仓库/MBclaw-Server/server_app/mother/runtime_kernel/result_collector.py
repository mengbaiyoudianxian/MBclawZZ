class ResultCollector:

    def __init__(self, memory, event_bus):

        self.memory = memory
        self.event_bus = event_bus

    def collect(self, result):

        self.memory.write(result)

        self.event_bus.emit("task_completed", result)
