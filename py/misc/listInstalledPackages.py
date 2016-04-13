# http://stackoverflow.com/questions/739993/how-can-i-get-a-list-of-locally-installed-python-modules

import pip

packages = sorted(["%s==%s" % (el.key, el.version) for el in pip.get_installed_distributions()])
for p in packages:
	print(p)
