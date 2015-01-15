# Import Alembic command
import abc
from Command import AbstractCommand

class ImportAlembic():

	def execute(self):
		print "Executing Import Alembic"


AbstractCommand.register(ImportAlembic)