from logging import StreamHandler, INFO, Logger, Formatter
from nguyenpanda.swan import random_color_text, red, green, misty_rose, gray

class CustomLogger(Logger):
    def __init__(self, name: str, color_function=random_color_text):
        super().__init__(name)
        self.setLevel(INFO)
        stream_handler = StreamHandler()
        stream_handler.setFormatter(Formatter('%(asctime)s - %(message)s'))
        self.addHandler(stream_handler)

        self.color_function = color_function

    def info(self, msg):
        msg = f"{self.color_function('Node ' + self.name)} - {green('INFO')}: {gray(msg)}"
        super().info(msg)

    def error(self, msg):
        msg = f"{self.color_function('Node ' + self.name)} - {red('ERROR')}: {misty_rose(msg)}"
        super().error(msg)