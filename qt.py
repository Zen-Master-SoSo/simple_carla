#  simple_carla/qt.py
#
#  Copyright 2024 liyang <liyang@veronica>
#
import logging, traceback, os, sys

# PyQt5 imports
from PyQt5.QtCore import QObject, pyqtSignal
from simple_carla import _SimpleCarla, Plugin, PatchbayClient, PatchbayPort, carla_paths
binpath, respath = carla_paths()
sys.path.append(respath)

from carla_backend import (

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


class CarlaQt(_SimpleCarla, QObject):

	sig_patchbay_client_added = pyqtSignal(PatchbayClient)
	sig_patchbay_client_removed = pyqtSignal(PatchbayClient)
	sig_patchbay_port_added = pyqtSignal(PatchbayPort)
	sig_patchbay_port_removed = pyqtSignal(PatchbayPort)
	sig_plugin_removed = pyqtSignal(QObject)
	sig_last_plugin_removed = pyqtSignal()
	sig_engine_started = pyqtSignal(int, int, int, int, float, str)
	sig_engine_stopped = pyqtSignal()
	sig_process_mode_changed = pyqtSignal(int)
	sig_transport_mode_changed = pyqtSignal(int, str)
	sig_buffer_size_changed = pyqtSignal(int)
	sig_sample_rate_changed = pyqtSignal(float)
	sig_cancelable_action = pyqtSignal(int, bool, str)
	sig_info = pyqtSignal(str)
	sig_error = pyqtSignal(str)
	sig_quit = pyqtSignal()
	sig_application_error = pyqtSignal(str, str, str, int)


	def __init__(self, client_name):
		QObject.__init__(self)
		_SimpleCarla.__init__(self, client_name)

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
				return self.sig_engine_started.emit(plugin_id, value_1, value_2, value_3, float_val, string_val)

			if action == ENGINE_CALLBACK_ENGINE_STOPPED:
				return self.sig_engine_stopped.emit()

			if action == ENGINE_CALLBACK_PROCESS_MODE_CHANGED:
				self.processMode = value_1
				return self.sig_process_mode_changed.emit(value_1)

			if action == ENGINE_CALLBACK_TRANSPORT_MODE_CHANGED:
				self.transportMode = value_1
				self.transportExtra = string_val
				return self.sig_transport_mode_changed.emit(value_1, string_val)

			if action == ENGINE_CALLBACK_BUFFER_SIZE_CHANGED:
				return self.sig_buffer_size_changed.emit(value_1)

			if action == ENGINE_CALLBACK_SAMPLE_RATE_CHANGED:
				return self.sig_sample_rate_changed.emit(float_val)

			if action == ENGINE_CALLBACK_CANCELABLE_ACTION:
				return self.sig_cancelable_action.emit(plugin_id, bool(value_1 != 0), string_val)

			if action == ENGINE_CALLBACK_PROJECT_LOAD_FINISHED:
				return

			if action == ENGINE_CALLBACK_NSM:
				return

			if action == ENGINE_CALLBACK_IDLE:
				return

			if action == ENGINE_CALLBACK_INFO:
				return self.sig_info.emit(string_val)

			if action == ENGINE_CALLBACK_ERROR:
				return self.sig_error.emit(string_val)

			if action == ENGINE_CALLBACK_QUIT:
				return self.sig_quit.emit()

			logging.warning('Unhandled action %d', action)

		except Exception as e:
			print(traceback.format_exc())
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			self.sig_application_error.emit(exc_type.__name__, str(e), fname, exc_tb.tb_lineno)

	# -----------------------------
	# Helper functions for callbacks
	# which vary depending on Qt or Not-Qt
	# -----------------------------

	def _alert_client_added(self, client):
		self.sig_patchbay_client_added.emit(client)

	def _alert_client_removed(self, client):
		self.sig_patchbay_client_removed.emit(client)

	def _alert_port_added(self, port):
		self.sig_patchbay_port_added.emit(port)

	def _alert_port_removed(self, port):
		self.sig_patchbay_port_removed.emit(port)

	def _alert_plugin_removed(self, plugin):
		self.sig_plugin_removed.emit(plugin)

	def _alert_last_plugin_removed(self):
		self.sig_last_plugin_removed.emit()



class QtPlugin(Plugin, QObject):
	"""
	This is an abstract class which inherits from QObject, for use by plugins which
	have no direct user-interface, (i.e. track & channel filter instantiated by a
	TrackWidget). (Qt does not allow inheriting from multiple classes which
	extend QObject)

	To use:
		plugin = QtPlugin(plugin_def)
		plugin.sig_ready.connect(self.plugin_ready)
		plugin.add_to_carla()
	"""

	sig_ready		= pyqtSignal(int)
	sig_removed 	= pyqtSignal(int)

	def __init__(self, plugin_def=None, saved_state=None):
		QObject.__init__(self)
		Plugin.__init__(self, plugin_def, saved_state)

	def ready(self):
		"""
		Called after post_embed_init() and all ports ready
		"""
		logging.debug('%s ready', self)
		self.sig_ready.emit(self.plugin_id)

	def got_removed(self):
		if self.original_plugin_name in self.moniker_counts:
			self.moniker_counts[self.original_plugin_name] -= 1
		else:
			logging.warning('%s original_plugin_name not in moniker_counts', self)
		self.sig_removed.emit(self.plugin_id)



#  end simple_carla/qt.py
