import wx

from file import file
from constants import titles

class MainFrame(wx.Frame):
	"""The primary program frame. This is the base for the main program window. Virtual singleton."""

	def __init__(self):
		super().__init__(
			None,
			style=wx.DEFAULT_FRAME_STYLE,
			title=titles.displayName
		)
		# FixMe: this can max and restore
		self.Maximize()

	def OnClose(self, evt):
		"""It's all ending. I can feel it slipping away...
		But what if the user hasn't saved yet?
		"""
		if evt.CanVeto():
			if wx.MessageBox("The file has not been saved... continue closing?", "Please confirm", wx.ICON_QUESTION | wx.YES_NO) != wx.YES:
				evt.Veto()
				return
		self.Destroy()  # you may also do:  event.Skip()
		#with wx.MessageDialog(self, message="Are you sure you want to quit?", caption="No, wait!", style=wx.YES_NO, pos=wx.DefaultPosition) as dlg:
			#resp = dlg.ShowModal()
		#if resp == wx.ID_YES:
			#evt.Skip()
		#else:
			#evt.Veto()
