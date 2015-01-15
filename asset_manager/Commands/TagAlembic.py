# Tag Alembic command
import abc
from Command import AbstractCommand

class TagAlembic():

	def execute(self):
		print "Executing Tag Alembic"


AbstractCommand.register(TagAlembic)