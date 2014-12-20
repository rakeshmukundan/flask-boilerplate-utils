"""
Generate the Security keys on the fly if they do not exist in the repo
"""
import os 

d = './Application/config/'
salt_file = os.path.realpath(os.path.join(d, './salt.key'))
security_key_file = os.path.realpath(os.path.join(d, './security.key'))

SECURITY_PASSWORD_SALT = None
SECRET_KEY = None

if os.path.isfile(salt_file):
	with open(salt_file, 'r') as f:
		SECURITY_PASSWORD_SALT = f.read().strip()
else:
	import uuid
	with open(salt_file, 'w') as f:
		SECURITY_PASSWORD_SALT = "%s%s%s" % (uuid.uuid4().hex, uuid.uuid4().hex, uuid.uuid4().hex)
		f.write(SECURITY_PASSWORD_SALT)

if os.path.isfile(security_key_file):
	with open(security_key_file, 'r') as f:
		SECRET_KEY = f.read().strip()
else:
	import uuid
	with open(security_key_file, 'w') as f:
		SECRET_KEY = "%s%s%s" % (uuid.uuid4().hex, uuid.uuid4().hex, uuid.uuid4().hex)
		f.write(SECRET_KEY)
