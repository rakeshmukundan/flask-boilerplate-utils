from .PyMakeManager import Target
import os


class StandardVirtualEnvTarget(Target):
	depends = ('requirements.txt',)
	output = './.venv/setup'
	sh_build_commands = (
		'./.venv/bin/pip3 install -r requirements.txt --upgrade',
		)
	def py_build_commands(self):
		if not os.path.exists('./.venv'):
			os.system('virtualenv ./.venv -p /usr/bin/python3',)

	

class StandardMySQLDBTarget(Target):
	echo = True

	sh_clean_commands = (
		'echo "DROP DATABASE IF EXISTS {DB_DATABASE};" | mysql -u {DB_USERNAME}',)
	
	sh_build_commands = (
		'./.venv/bin/pip3 install -r requirements-mysql.txt --upgrade',
		'echo "CREATE DATABASE IF NOT EXISTS {DB_DATABASE}" | mysql -u {DB_USERNAME}',)

	depends = ('requirements-mysql.txt',)
	output = './.venv/db'


class StandardRegenerateTarget(Target):
	echo = False
	always_build = True
	depends = ('requirements.txt',)
	

	sh_build_commands = ('./util/compile.sh ./Application/static/css > /dev/null',
						 './util/regenerate.sh ./Application/models Model > /dev/null',
						 './util/regenerate.sh ./Application/views View > /dev/null')
	

class StandardSQLiteTarget(Target):
	sh_clean_commands = ('rm -rf ./Application/{DB_BASE}.db',)


class StandardTestTarget(Target):
	depends = ()
