from flask.ext.script import Option
from .BaseCommand import BaseCommand

class Host(BaseCommand):
	"""
	Run a Web Server for Hosting using meinheld.
	"""

	option_list = (
		Option('--hostname', '-h', dest='hostname', default='0.0.0.0', type=str),
		Option('--port', '-p', dest='port', default=8000, type=int),
	)
	def run(self, port, hostname):
		from meinheld import server, patch
		patch.patch_all()
		print(" - Running Hosting Server using Meinheld")
		print(" - http://%s:%s/" % (hostname, port))
		server.listen((hostname, port))
		server.run(self.app)

