from flask.ext.script import Option
from .BaseCommand import BaseCommand


class Run(BaseCommand):
	"Run the Flask Builtin Server (Not for production)"

	option_list = (
		Option('--hostname', '-h', dest='hostname', default='0.0.0.0', type=str),
		Option('--port', '-p', dest='port', default=8000, type=int),
		Option('--debug', '-d', dest='debug', default=True, action='store_true'),
		Option('--config', '-c', dest='config', nargs=1, action='store', help='Provide'\
			'a configuation class defined in config.'),
	)

	def run(self, port, hostname, debug, config):
		self.app.run(debug=debug, host=hostname, port=port)
