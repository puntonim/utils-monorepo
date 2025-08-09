from datetime import datetime, timezone


class Car:
    def start(self):
        # Let's suppose that this method connects to the local process (that controls
        #  the car engine) via a local socket and it sends the signal to start the engine.
        # Then it returns the start time.
        return datetime.now(tz=timezone.utc)
