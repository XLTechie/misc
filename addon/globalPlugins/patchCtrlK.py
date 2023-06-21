import wx
import threading

import ui
import globalCommands
import globalPluginHandler
from scriptHandler import script

import addonHandler
addonHandler.initTranslation()

class ResizableTextDialog(wx.Dialog):
	def __init__(self, parent, text, title):
		super().__init__(parent, -1, title, size=(300, 200))
		self.textCtrl = wx.TextCtrl(self, -1, text, style=wx.TE_MULTILINE)
		self.closeButton = wx.Button(self, wx.ID_CLOSE, "&Close")
		self.copyButton = wx.Button(self, wx.ID_ANY, "Cop&y")
		self.Bind(wx.EVT_SIZE, self.onResize)
		self.Bind(wx.EVT_BUTTON, self.onClose, self.closeButton)
		self.Bind(wx.EVT_BUTTON, self.onCopy, self.copyButton)

	def onResize(self, evt) -> None:
		self.textCtrl.SetSize(self.GetClientSize())

	def onClose(self, evt) -> None:
		self.Destroy()

	def onCopy(self, evt) -> None:
		wx.TheClipboard.SetData(wx.TextDataObject(self.textCtrl.GetValue()))
		# Translators: Message spoken to confirm that the URL was copied to the clipboard.
		ui.message(_("URL copied to clipboard."))


class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	def __init__(self, *args, **kwargs):
		# Patch Ctrl+K behavior
		self.oldScript = globalCommands.script_reportLinkDestinationInWindow
		def replacement_script_reportLinkDestinationInWindow
