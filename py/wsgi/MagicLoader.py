from importlib.machinery import FileFinder
from importlib.machinery import SourceFileLoader
import os.path

def loadModule (path):
	folder = os.path.dirname(path)
	filename = os.path.basename(path)
	(moduleName, dot, extension) = filename.rpartition(filename)
	loaderArgs = (SourceFileLoader, [dot+extension])
	finder = FileFinder(folder, loaderArgs)
	spec = finder.find_spec(moduleName)
	module = importlib.util.module_from_spec(spec)
	loader = spec.loader
	module.moduleSpec = spec
	module.exec = lambda: loader.exec_module(module)
	return module


# from importlib.abc import ExecutionLoader
# from importlib.machinery import SourceFileLoader
# import abc
# 
# class MagicLoader (ExecutionLoader):
# 	def __init__ (self, fullname, path):
# 		self.dlg = SourceFileLoader(fullname, path)
# 		pass
# 
# 	def get_code (self, fullname):
# 		return dlg.get_code(fullname)
# 	
# 	def get_filename (self, fullname):
# 		return dlg.get_filename(fullname)
# 
# 	def get_source (self, fullname):
# 		return dlg.get_source(fullname)
 

# ExecutionLoader.register(MagicLoader)

# if __name__ == '__main__':
	# loader = MagicLoader('fullname', 'path')
	# loader = SourceFileLoader('TestModule', 'TestModule.py')
	#for s in sorted(dir(loader)):
	#	print(s)
	#m = 
	#pass
