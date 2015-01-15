# Version command
import abc
from Command import AbstractCommand

class Version():

	def execute(self):
		print "Executing Version"


AbstractCommand.register(Version)