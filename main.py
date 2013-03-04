from pyplugins.core.manager import PluginManager
import os
# requires blessings library (color)

if __name__ == "__main__":
    proj_dir = os.path.dirname(os.path.abspath(__file__))
    plug_dir = os.path.join(proj_dir, "plugins")
    manager =  PluginManager(projectdir=proj_dir, plugindir=plug_dir, debug=True)
    manager.load_all()
    print "example.constants.host = ", manager.get("example","constants").host