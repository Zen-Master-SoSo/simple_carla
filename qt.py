#  simple_carla/qt.py
#
#  Copyright 2024 liyang <liyang@veronica>
#
import logging, traceback, os, sys
from qt_extras import ShutUpQT

# PyQt5 imports
from PyQt5 import uic
from PyQt5.QtCore import Qt, QObject, pyqtSignal, pyqtSlot, QTimer, QMetaObject
from PyQt5.QtWidgets import QAction, QFrame
from simple_carla import Carla, Plugin

from carla.carla_backend import (

	charPtrToString,

	# Callback action codes:
	ENGINE_CALLBACK_DEBUG,
	ENGINE_CALLBACK_PLUGIN_ADDED,
	ENGINE_CALLBACK_PLUGIN_REMOVED,
	ENGINE_CALLBACK_PLUGIN_RENAMED,
	ENGINE_CALLBACK_PLUGIN_UNAVAILABLE,
	ENGINE_CALLBACK_PARAMETER_VALUE_CHANGED,
	ENGINE_CALLBACK_PARAMETER_DEFAULT_CHANGED,
	ENGINE_CALLBACK_PARAMETER_MAPPED_CONTROL_INDEX_CHANGED,
	ENGINE_CALLBACK_PARAMETER_MIDI_CHANNEL_CHANGED,
	ENGINE_CALLBACK_OPTION_CHANGED,
	ENGINE_CALLBACK_PROGRAM_CHANGED,
	ENGINE_CALLBACK_MIDI_PROGRAM_CHANGED,
	ENGINE_CALLBACK_UI_STATE_CHANGED,
	ENGINE_CALLBACK_NOTE_ON,
	ENGINE_CALLBACK_NOTE_OFF,
	ENGINE_CALLBACK_UPDATE,
	ENGINE_CALLBACK_RELOAD_INFO,
	ENGINE_CALLBACK_RELOAD_PARAMETERS,
	ENGINE_CALLBACK_RELOAD_PROGRAMS,
	ENGINE_CALLBACK_RELOAD_ALL,
	ENGINE_CALLBACK_PATCHBAY_CLIENT_ADDED,
	ENGINE_CALLBACK_PATCHBAY_CLIENT_REMOVED,
	ENGINE_CALLBACK_PATCHBAY_CLIENT_RENAMED,
	ENGINE_CALLBACK_PATCHBAY_CLIENT_DATA_CHANGED,
	ENGINE_CALLBACK_PATCHBAY_PORT_ADDED,
	ENGINE_CALLBACK_PATCHBAY_PORT_REMOVED,
	ENGINE_CALLBACK_PATCHBAY_PORT_CHANGED,
	ENGINE_CALLBACK_PATCHBAY_CONNECTION_ADDED,
	ENGINE_CALLBACK_PATCHBAY_CONNECTION_REMOVED,
	ENGINE_CALLBACK_ENGINE_STARTED,
	ENGINE_CALLBACK_ENGINE_STOPPED,
	ENGINE_CALLBACK_PROCESS_MODE_CHANGED,
	ENGINE_CALLBACK_TRANSPORT_MODE_CHANGED,
	ENGINE_CALLBACK_BUFFER_SIZE_CHANGED,
	ENGINE_CALLBACK_SAMPLE_RATE_CHANGED,
	ENGINE_CALLBACK_CANCELABLE_ACTION,
	ENGINE_CALLBACK_PROJECT_LOAD_FINISHED,
	ENGINE_CALLBACK_NSM,
	ENGINE_CALLBACK_IDLE,
	ENGINE_CALLBACK_INFO,
	ENGINE_CALLBACK_ERROR,
	ENGINE_CALLBACK_QUIT,
	ENGINE_CALLBACK_INLINE_DISPLAY_REDRAW,
	ENGINE_CALLBACK_PATCHBAY_PORT_GROUP_ADDED,
	ENGINE_CALLBACK_PATCHBAY_PORT_GROUP_REMOVED,
	ENGINE_CALLBACK_PATCHBAY_PORT_GROUP_CHANGED,
	ENGINE_CALLBACK_PARAMETER_MAPPED_RANGE_CHANGED,
	ENGINE_CALLBACK_PATCHBAY_CLIENT_POSITION_CHANGED,

)
from carla.carla_frontend import CarlaFrontendLib
from carla.carla_shared import DLL_EXTENSION


class CarlaQt(Carla, QObject):

	sig_PortsChanged = pyqtSignal()
	sig_PluginRemoved = pyqtSignal(QObject)
	sig_LastPluginRemoved = pyqtSignal()
	sig_EngineStarted = pyqtSignal(int, int, int, int, float, str)
	sig_EngineStopped = pyqtSignal()
	sig_ProcessModeChanged = pyqtSignal(int)
	sig_TransportModeChanged = pyqtSignal(int, str)
	sig_BufferSizeChanged = pyqtSignal(int)
	sig_SampleRateChanged = pyqtSignal(float)
	sig_CancelableAction = pyqtSignal(int, bool, str)
	sig_Info = pyqtSignal(str)
	sig_Error = pyqtSignal(str)
	sig_Quit = pyqtSignal()
	sig_ApplicationError = pyqtSignal(str, str, str, int)


	def __init__(self, client_name):
		QObject.__init__(self)
		Carla.__init__(self, client_name)

	# -----------------------------
	# Engine callback
	# -----------------------------

	def engine_callback(self, handle, action, plugin_id, value_1, value_2, value_3, float_val, string_val):

		string_val = charPtrToString(string_val)

		try:

			if action == ENGINE_CALLBACK_INLINE_DISPLAY_REDRAW:
				return self.cb_InlineDisplayRedraw(plugin_id)

			if action == ENGINE_CALLBACK_DEBUG:
				return self.cb_Debug(plugin_id, value_1, value_2, value_3, float_val, string_val)

			if action == ENGINE_CALLBACK_PLUGIN_ADDED:
				return self.cb_PluginAdded(plugin_id, value_1, string_val)

			if action == ENGINE_CALLBACK_PLUGIN_REMOVED:
				return self.cb_PluginRemoved(plugin_id)

			if action == ENGINE_CALLBACK_PLUGIN_RENAMED:
				return self.cb_PluginRenamed(plugin_id, string_val)

			if action == ENGINE_CALLBACK_PLUGIN_UNAVAILABLE:
				return self.cb_PluginUnavailable(plugin_id, string_val)

			if action == ENGINE_CALLBACK_PARAMETER_VALUE_CHANGED:
				return self.cb_ParameterValueChanged(plugin_id, value_1, float_val)

			if action == ENGINE_CALLBACK_PARAMETER_DEFAULT_CHANGED:
				return self.cb_ParameterDefaultChanged(plugin_id, value_1, float_val)

			if action == ENGINE_CALLBACK_PARAMETER_MAPPED_CONTROL_INDEX_CHANGED:
				return self.cb_ParameterMappedControlIndexChanged(plugin_id, value_1, value_2)

			if action == ENGINE_CALLBACK_PARAMETER_MAPPED_RANGE_CHANGED:
				minimum, maximum = (float(v) for v in string_val.split(":", 2))
				return self.cb_ParameterMappedRangeChanged(plugin_id, value_1, minimum, maximum)

			if action == ENGINE_CALLBACK_PARAMETER_MIDI_CHANNEL_CHANGED:
				return self.cb_ParameterMidiChannelChanged(plugin_id, value_1, value_2)

			if action == ENGINE_CALLBACK_PROGRAM_CHANGED:
				return self.cb_ProgramChanged(plugin_id, value_1)

			if action == ENGINE_CALLBACK_MIDI_PROGRAM_CHANGED:
				return self.cb_MidiProgramChanged(plugin_id, value_1)

			if action == ENGINE_CALLBACK_OPTION_CHANGED:
				return self.cb_OptionChanged(plugin_id, value_1, bool(value_2))

			if action == ENGINE_CALLBACK_UI_STATE_CHANGED:
				return self.cb_UiStateChanged(plugin_id, value_1)

			if action == ENGINE_CALLBACK_NOTE_ON:
				return self.cb_NoteOn(plugin_id, value_1, value_2, value_3)

			if action == ENGINE_CALLBACK_NOTE_OFF:
				return self.cb_NoteOff(plugin_id, value_1, value_2)

			if action == ENGINE_CALLBACK_UPDATE:
				return self.cb_Update(plugin_id)

			if action == ENGINE_CALLBACK_RELOAD_INFO:
				return self.cb_ReloadInfo(plugin_id)

			if action == ENGINE_CALLBACK_RELOAD_PARAMETERS:
				return self.cb_ReloadParameters(plugin_id)

			if action == ENGINE_CALLBACK_RELOAD_PROGRAMS:
				return self.cb_ReloadPrograms(plugin_id)

			if action == ENGINE_CALLBACK_RELOAD_ALL:
				return self.cb_ReloadAll(plugin_id)

			if action == ENGINE_CALLBACK_PATCHBAY_CLIENT_ADDED:
				return self.cb_PatchbayClientAdded(plugin_id, value_1, value_2, string_val)

			if action == ENGINE_CALLBACK_PATCHBAY_CLIENT_REMOVED:
				return self.cb_PatchbayClientRemoved(plugin_id)

			if action == ENGINE_CALLBACK_PATCHBAY_CLIENT_RENAMED:
				return self.cb_PatchbayClientRenamed(plugin_id, string_val)

			if action == ENGINE_CALLBACK_PATCHBAY_CLIENT_DATA_CHANGED:
				return self.cb_PatchbayClientDataChanged(plugin_id, value_1, value_2)

			if action == ENGINE_CALLBACK_PATCHBAY_CLIENT_POSITION_CHANGED:
				return self.cb_PatchbayClientPositionChanged(plugin_id, value_1, value_2, value_3, int(round(float_val)))

			if action == ENGINE_CALLBACK_PATCHBAY_PORT_ADDED:
				return self.cb_PatchbayPortAdded(plugin_id, value_1, value_2, value_3, string_val)

			if action == ENGINE_CALLBACK_PATCHBAY_PORT_REMOVED:
				return self.cb_PatchbayPortRemoved(plugin_id, value_1)

			if action == ENGINE_CALLBACK_PATCHBAY_PORT_CHANGED:
				return self.cb_PatchbayPortChanged(plugin_id, value_1, value_2, value_3, string_val)

			if action == ENGINE_CALLBACK_PATCHBAY_PORT_GROUP_ADDED:
				return self.cb_PatchbayPortGroupAdded(plugin_id, value_1, value_2, string_val)

			if action == ENGINE_CALLBACK_PATCHBAY_PORT_GROUP_REMOVED:
				return self.cb_PatchbayPortGroupRemoved(plugin_id, value_1)

			if action == ENGINE_CALLBACK_PATCHBAY_PORT_GROUP_CHANGED:
				return self.cb_PatchbayPortGroupChanged(plugin_id, value_1, value_2, string_val)

			if action == ENGINE_CALLBACK_PATCHBAY_CONNECTION_ADDED:
				client_out_id, port_out_id, client_in_id, port_in_id = [int(i) for i in string_val.split(":")]
				return self.cb_PatchbayConnectionAdded(plugin_id, client_out_id, port_out_id, client_in_id, port_in_id)

			if action == ENGINE_CALLBACK_PATCHBAY_CONNECTION_REMOVED:
				return self.cb_PatchbayConnectionRemoved(plugin_id, value_1, value_2)

			if action == ENGINE_CALLBACK_ENGINE_STARTED:
				self.processMode = value_1
				self.transportMode = value_2
				return self.sig_EngineStarted.emit(plugin_id, value_1, value_2, value_3, float_val, string_val)

			if action == ENGINE_CALLBACK_ENGINE_STOPPED:
				return self.sig_EngineStopped.emit()

			if action == ENGINE_CALLBACK_PROCESS_MODE_CHANGED:
				self.processMode = value_1
				return self.sig_ProcessModeChanged.emit(value_1)

			if action == ENGINE_CALLBACK_TRANSPORT_MODE_CHANGED:
				self.transportMode = value_1
				self.transportExtra = string_val
				return self.sig_TransportModeChanged.emit(value_1, string_val)

			if action == ENGINE_CALLBACK_BUFFER_SIZE_CHANGED:
				return self.sig_BufferSizeChanged.emit(value_1)

			if action == ENGINE_CALLBACK_SAMPLE_RATE_CHANGED:
				return self.sig_SampleRateChanged.emit(float_val)

			if action == ENGINE_CALLBACK_CANCELABLE_ACTION:
				return self.sig_CancelableAction.emit(plugin_id, bool(value_1 != 0), string_val)

			if action == ENGINE_CALLBACK_PROJECT_LOAD_FINISHED:
				return

			if action == ENGINE_CALLBACK_NSM:
				return

			if action == ENGINE_CALLBACK_IDLE:
				return

			if action == ENGINE_CALLBACK_INFO:
				return self.sig_Info.emit(string_val)

			if action == ENGINE_CALLBACK_ERROR:
				return self.sig_Error.emit(string_val)

			if action == ENGINE_CALLBACK_QUIT:
				return self.sig_Quit.emit()

			logging.warning("Unhandled action %d" % action)

		except Exception as e:
			print(traceback.format_exc())
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			self.sig_ApplicationError.emit(exc_type.__name__, str(e), fname, exc_tb.tb_lineno)

	# -----------------------------
	# Helper functions for callbacks
	# which vary depending on Qt or Not-Qt
	# -----------------------------

	def _alert_ports_changed(self):
		self.sig_PortsChanged.emit()

	def _alert_plugin_removed(self, plugin):
		self.sig_PluginRemoved.emit(plugin)

	def _alert_last_plugin_removed(self):
		self.sig_LastPluginRemoved.emit()




class QtPlugin(Plugin, QObject):
	"""
	This is an abstract class which inherits from QObject, for use by plugins which
	have no direct user-interface, (i.e. track & channel filter instantiated by a
	TrackWidget). (Qt does not allow inheriting from multiple classes which
	extend QObject)
	"""

	sig_Ready					= pyqtSignal(int)
	sig_Removed 				= pyqtSignal(int)

	def __init__(self, plugin_def, saved_state=None):
		QObject.__init__(self)
		Plugin.__init__(self, plugin_def, saved_state)

	def ready(self):
		"""
		Called after post_embed_init() and all ports ready
		"""
		logging.debug(f"{self} ready")
		self.sig_Ready.emit(self.plugin_id)

	def got_removed(self):
		if self.original_plugin_name in self.moniker_counts:
			self.moniker_counts[self.original_plugin_name] -= 1
		else:
			logging.warning(f"{self} original_plugin_name not in moniker_counts")
		self.sig_Removed.emit(self.plugin_id)


class QtWidgetPlugin(Plugin, QFrame):

	has_user_interface = True

	def __init__(self, parent, plugin_def, ui_filename, saved_state=None):
		QFrame.__init__(self, parent)
		Plugin.__init__(self, plugin_def, saved_state)
		with ShutUpQT():
			uic.loadUi(ui_filename, self)

		self.setFixedHeight(self.fixed_height)
		self.setFixedWidth(self.fixed_width)

		self.generic_dialog = None
		self.prefer_generic_dialog = False

		self.b_name.autoFit()
		self.b_name.setText(self.moniker)
		self.b_name.toggled.connect(self.show_plugin_dialog)
		self.b_name.setContextMenuPolicy(Qt.ActionsContextMenu)

		action = QAction('Rename', self)
		action.triggered.connect(self.action_rename)
		self.b_name.addAction(action)

		action = QAction('Prefer generic interface', self)
		action.setCheckable(True)
		action.triggered.connect(self.action_prefer_generic)
		self.b_name.addAction(action)

		# Vol & dry/wet dependent on plugin:
		if self.can_volume:
			self.b_volume.clicked.connect(self.b_volume_clicked)
		else:
			for obj_name in ["label_1", "b_volume", "sld_volume"]:
				getattr(self, obj_name).setEnabled(False)
		if self.can_drywet:
			self.b_wet.clicked.connect(self.b_wet_clicked)
		else:
			for obj_name in ["label_2", "b_wet", "sld_wet"]:
				getattr(self, obj_name).setEnabled(False)

	def finalize_init(self):
		# Stero / mono output peak meter (sets "_update_peak_meter" func):
		if self._audio_out_count > 0:
			if self._audio_out_count > 1:
				peak_out = StereoPeakMeter(self)
				self._update_peak_meter = self._update_peak_stereo
			else:
				peak_out = MonoPeakMeter(self)
				self._update_peak_meter = self._update_peak_mono
			self.lo_meter.replaceWidget(self.peak_out, peak_out)
			self.peak_out.deleteLater()
			self.peak_out = peak_out
		super().finalize_init()

	@pyqtSlot()
	def action_rename(self):
		new_name, ok = QInputDialog.getText(self, 'Rename plugin', 'Enter a name for this plugin', text=self.moniker)
		if ok:
			self.moniker = new_name

	@pyqtSlot(bool)
	def action_prefer_generic(self, checked):
		self.prefer_generic_dialog = checked

	def _update_peak_meter(self):
		pass

	def _update_peak_stereo(self):
		self.peak_out.setValues(
			CarlaQt.instance.get_output_peak_value(self.plugin_id, True),
			CarlaQt.instance.get_output_peak_value(self.plugin_id, False)
		)

	def _update_peak_mono(self):
		self.peak_out.setValue(CarlaQt.instance.get_output_peak_value(self.plugin_id, True))

	def idle_fast(self):
		self._update_peak_meter()

	def inline_display_redraw(self):
		retval = CarlaQt.instance.render_inline_display(self.plugin_id, self.fixed_width, self.fixed_height)

	@pyqtSlot(bool)
	def show_plugin_dialog(self, state):
		if state:
			if self.prefer_generic_dialog or not self.has_custom_ui:
				if self.generic_dialog is None:
					self.generic_dialog = PluginDialog(self)
					self.generic_dialog.sig_Closed.connect(self.generic_dialog_closed)
				self.generic_dialog.show()
			else:
				CarlaQt.instance.show_custom_ui(self.plugin_id, state)
		else:
			if not self.generic_dialog is None:
				self.generic_dialog.hide()

	@pyqtSlot()
	def generic_dialog_closed(self):
		with SigBlock(self.b_name):
			self.b_name.setChecked(False)

	def ui_state_changed(self, state):
		if state == 0:
			self.b_name.setChecked(False)
		else:
			self.b_name.setChecked(True)
			if state == -1:
				logging.debug("SETTING has_custom_ui = False")
				self.has_custom_ui = False

	@pyqtSlot()
	def b_volume_clicked(self):
		self.volume = 0

	@pyqtSlot()
	def b_wet_clicked(self):
		self.dry_wet = 0



class CarlaPluginDialog():
	"""
	Plugin selection dialog from Carla felib
	(handles all supported plugins)
	"""
	_instance = None

	def __new__(cls, parent):
		if cls._instance is None:
			cls._instance = super().__new__(cls)
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



#  end simple_carla/qt.py
