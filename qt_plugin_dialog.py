#  carla_plugin_dialog.py
#
#  Copyright 2024 liyang <liyang@veronica>
#

from PyQt5.QtWidgets import QMainWindow

from carla.carla_frontend import CarlaFrontendLib
from carla.carla_shared import DLL_EXTENSION


class CarlaPluginDialog():
	"""
	Plugin selection dialog from Carla felib
	(handles all supported plugins)
	"""
	_instance = None

	def __new__(cls, parent):
		if cls._instance is None:
			cls._instance = super(cls, CarlaPluginDialog).__new__(cls)
		return cls._instance

	def __init__(self, parent):
		felib_path = '/usr/local/lib/carla/libcarla_frontend.' + DLL_EXTENSION
		self._carla_felib = CarlaFrontendLib(felib_path)
		self._plugin_list_dialog = self._carla_felib.createPluginListDialog(parent, {
			'showPluginBridges': False,
			'showWineBridges': False,
			'useSystemIcons': False,
			'wineAutoPrefix': '',
			'wineExecutable': '',
			'wineFallbackPrefix': ''
		})

	def exec_dialog(self):
		"""
		Displays the plugin dialog and returns a dict containing the values essential
		for loading a plugin.
		"""
		return self._carla_felib.execPluginListDialog(self._plugin_list_dialog)



class TestWindow(QMainWindow):

	def __init__(self, options):
		super().__init__()
		self.options = options

	def showEvent(self, event):
		QTimer.singleShot(0, self.show_dialog)

	def show_dialog(self):
		self.plugin_def = CarlaPluginDialog(self).exec_dialog()
		if self.plugin_def is not None:
			if self.options.plugin_def:
				pprint({ k:self.plugin_def[k] for k in ['name', 'build', 'type', 'filename', 'label', 'uniqueId'] })
			else:
				pprint(self.plugin_def)
		self.close()



if __name__ == "__main__":
	import argparse, logging, sys
	from PyQt5.QtWidgets import QApplication
	from PyQt5.QtCore import QTimer
	from musecbox.locals import SETTINGS, STYLES
	from pprint import pprint
	p = argparse.ArgumentParser()
	p.epilog = """
	Write your help text!
	"""
	p.add_argument("--plugin-def", "-d", action="store_true", help="Spit out a plugin definition to use when coding plugins.")
	p.add_argument("--verbose", "-v", action="store_true", help="Show more detailed debug information")
	options = p.parse_args()
	logging.basicConfig(
		stream=sys.stdout,
		level=logging.DEBUG if options.verbose else logging.ERROR,
		format="[%(filename)24s:%(lineno)-4d] %(levelname)-8s %(message)s"
	)
	app = QApplication([])
	style = SETTINGS.value("style", "system")
	with open(STYLES[style], 'r') as cssfile:
		QApplication.instance().setStyleSheet(cssfile.read())
	window = TestWindow(options)
	window.show()
	app.exec()


#  end carla_plugin_dialog.py
