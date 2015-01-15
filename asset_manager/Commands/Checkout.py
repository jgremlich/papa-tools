# Checkout command
import abc
from Command import AbstractCommand

class Checkout():

	def execute(self):
		print "Executing Checkout"


AbstractCommand.register(Checkout)

if __name__ == '__main__':
	Checkout().execute()
	print 'Subclass:', issubclass(Checkout, AbstractCommand)
	print 'Instance:', isinstance(Checkout(), AbstractCommand)