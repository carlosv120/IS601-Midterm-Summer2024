import sys
from app.commands import Command
import logging

class ExitCommand(Command):
    def execute(self):
        logging.info("ExitCommand executed, exiting the application")
        sys.exit("Exiting...")