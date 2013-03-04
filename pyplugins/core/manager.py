import blessings
import os
import sys

class PluginManager(object):
    def __init__(self, projectdir, plugindir, debug):
        self.projectdir = projectdir
        self.plugindir = plugindir
        self._debug = debug

        self.terminal = blessings.Terminal()

        sys.path.append(projectdir)

        self.modules = {}

        self.fromlist = [pl for pl in self.plugindir.split("/")[1:] if pl not in self.projectdir.split("/")[1:]]

    def debug(self, message):
        if self._debug:
            print self.terminal.red_on_black("[pyPlugins.PluginManager] {0}".format(self.terminal.bold(message)))

    def ignore(self, folder,s):
        if s == 1: return folder.startswith(".") or folder == "__init__.py" or not folder.endswith(".py")
        return folder.startswith(".") or folder == "__init__.py" or folder.endswith(".pyc")

    def load(self, directory, pfile):
        self.debug("Loading plugin {0}.{1}".format(directory, pfile))
        return __import__(".".join(self.fromlist + [directory,pfile]), fromlist=[pfile], level=-1)

    def load_all(self):
        self.debug("Starting to load all plugins")
        plugin_directories = [(folder, os.path.join(self.plugindir, folder)) for folder in os.listdir(self.plugindir) if not self.ignore(folder,0)]
        for directory, fullpath in plugin_directories:
            self.modules[directory] = {}
            plugin_files = [_file.strip(".py") for _file in os.listdir(fullpath) if not self.ignore(_file,1)]
            for pfile in plugin_files:
                plugin = self.load(directory, pfile)
                self.modules[directory][pfile] = plugin
        self.debug("All plugins loaded")

    def get(self, d, f):
        d = self.modules.get(d)
        if d: return d.get(f)