import distutils.util

def getYesNoChoice (prompt, default=None):
	if default == None:	
		prompt = prompt + (" (y/n) ")
	else:
		sDefault = str(default)
		default = distutils.util.strtobool(sDefault)
		if default == True:
			prompt = prompt + (" (Y/n) ")
		else:
			prompt = prompt + (" (y/N) ")
	choice = None
	while choice == None:
		try:
			sChoice = input(prompt)
			if sChoice == "" and default is not None:
				sChoice = str(default)
			choice = distutils.util.strtobool(sChoice)
		except ValueError:
			print("Invalid choice: " + sChoice)
	return choice	
	



