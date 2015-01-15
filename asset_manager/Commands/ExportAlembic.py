# Export Alembic command
import abc
from Command import AbstractCommand

class ExportAlembic():

	def execute(self):
		print "Executing Export Alembic"


AbstractCommand.register(ExportAlembic)