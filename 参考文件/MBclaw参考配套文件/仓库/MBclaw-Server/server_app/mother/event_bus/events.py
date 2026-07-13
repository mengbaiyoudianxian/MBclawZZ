from event_bus.types import Event


class Events:

    # Task lifecycle

    @staticmethod
    def task_created(task):

        return Event(
            type="task.created",
            payload=task.__dict__,
            task_id=task.id,
            source_module="runtime_kernel"
        )

    @staticmethod
    def task_started(task):

        return Event(
            type="task.started",
            payload=task.__dict__,
            task_id=task.id,
            source_module="runtime_kernel"
        )

    @staticmethod
    def task_completed(result, task_id):

        return Event(
            type="task.completed",
            payload=result,
            task_id=task_id,
            source_module="worker"
        )

    @staticmethod
    def task_failed(error, task_id):

        return Event(
            type="task.failed",
            payload={"error": str(error)},
            task_id=task_id,
            source_module="worker"
        )

    # Tool events

    @staticmethod
    def tool_called(tool_name, payload, task_id):

        return Event(
            type="tool.called",
            payload={
                "tool": tool_name,
                "input": payload
            },
            task_id=task_id,
            source_module="tool_executor"
        )

    @staticmethod
    def tool_completed(result, task_id):

        return Event(
            type="tool.completed",
            payload=result,
            task_id=task_id,
            source_module="tool_executor"
        )

    # Memory events

    @staticmethod
    def memory_written(record, task_id):

        return Event(
            type="memory.written",
            payload=record,
            task_id=task_id,
            source_module="memory"
        )

    # Evolution events

    @staticmethod
    def evolution_suggested(suggestion):

        return Event(
            type="evolution.suggested",
            payload=suggestion,
            source_module="evolution_engine"
        )
