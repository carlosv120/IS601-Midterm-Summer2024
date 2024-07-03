import logging
from app.commands import Command

class MenuCommand(Command):
    def __init__(self, plugins):
        self.plugins = plugins
        logging.info("MenuCommand initialized with plugins: %s", plugins)

    def execute(self):
        logging.info("MenuCommand executed successfully, displaying commands loaded")

        if not self.plugins:
            print("No plugins loaded.")
            logging.warning("No plugins loaded.")
            return

        # Print header
        print(f"{'Plugins:'}")
        print('-' * 120)

        # Print plugins in a single line
        print("  ----  ".join(self.plugins))
        print('-' * 120)


