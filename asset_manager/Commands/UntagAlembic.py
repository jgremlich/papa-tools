# Untag Alembic command
import abc
from Command import AbstractCommand

class UntagAlembic():

	def execute(self):
		print "Executing Untag Alembic"


AbstractCommand.register(UntagAlembic)