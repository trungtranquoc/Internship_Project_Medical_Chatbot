from logging import StreamHandler, INFO, Logger, Formatter
from nguyenpanda.swan import red, green, yellow, blue

class CustomLogger(Logger):
    def __init__(self, name: str):
        super().__init__(name)
        self.setLevel(INFO)
        stream_handler = StreamHandler()
        stream_handler.setFormatter(Formatter('%(asctime)s - %(message)s'))
        self.addHandler(stream_handler)

    def info(self, msg):
        msg = f"{blue('Node ' + self.name)} - {green('INFO')}: {msg}"
        super().info(msg)

    def error(self, msg):
        msg = f"{blue('Node ' + self.name)} - {red('ERROR')}: {msg}"
        super().error(msg)