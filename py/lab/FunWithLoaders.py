from importlib.machinery import FileFinder
from importlib.machinery import SourceFileLoader
import importlib.util
import inspect
import os.path


def execModule (module):
	attrs1 = set(dir(module))
	module.exec()
	attrs2 = set(dir(module))
	newAttrs = [el for el in attrs2 if el not in attrs1 and el != '__builtins__']
	args = {}
	for attr in newAttrs:
		val = getattr(module, attr)
		if not inspect.isfunction(val) and not inspect.isclass(val):
			args[attr] = getattr(module, attr)
	return args

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

# loaders = [(SourceFileLoader, '*.py')]
# loaders = (SourceFileLoader, ['.py'])
# finder = FileFinder('/tmp/modules/', loaders)
# spec = finder.find_spec('TestModule')
# print(sorted(dir(spec)))
# print('spec={}'.format(spec))
# spec = finder.find_spec('TestModule.py')
# print('spec={}'.format(spec))
# module = spec.loader.create_module(spec)
# module = importlib.util.module_from_spec(spec)
# print('module={}'.format(module))
# print(sorted(dir(module)))
# spec.loader.exec_module(module)
# print(sorted(dir(module)))

path = '/tmp/modules/TestModule.py'
module = loadModule(path)
# loader.exec_module(module)
args = execModule(module)
print(" -- Done with exec() --")
print(args)
