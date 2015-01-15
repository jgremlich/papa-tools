# Checkin command
import abc
from Command import AbstractCommand

class Checkin():

	def execute(self):
		print "Executing Checkin"


AbstractCommand.register(Checkin)