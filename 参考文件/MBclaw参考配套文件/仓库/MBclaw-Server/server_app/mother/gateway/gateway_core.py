from gateway.normalizer import MessageNormalizer
from gateway.session import SessionManager
from gateway.dispatcher import Dispatcher
from gateway.connection import ConnectionManager


class Gateway:

    def __init__(self, planner, worker, governor):

        self.normalizer = MessageNormalizer()
        self.sessions = SessionManager()
        self.connections = ConnectionManager()

        self.dispatcher = Dispatcher(planner, worker, governor)

    # -----------------------------
    # main entry
    # -----------------------------

    def receive(self, raw: dict, source: str):

        msg = self.normalizer.normalize(raw, source)

        self.sessions.append(msg)

        result = self.dispatcher.dispatch(msg)

        return result
