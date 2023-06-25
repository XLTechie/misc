import os
import wx
import github
import yaml

filename = os.path.expandvars(r"%temp%\testAppConfig.yaml")

class ConfigDialog(wx.Dialog):

	def __init__(self, parent):
		super().__init__(parent, title="Configuration Dialog")

		self.token_text_ctrl = wx.TextCtrl(self, value="")

		self.repos = []
		for i in range(5):
			repo_text_ctrl = wx.TextCtrl(self, value="")
			refresh_time_text_ctrl = wx.TextCtrl(self, value="")
			target_folder_text_ctrl = wx.TextCtrl(self, value="")
			self.repos.append((repo_text_ctrl, refresh_time_text_ctrl, target_folder_text_ctrl))

		button_box = wx.BoxSizer(wx.HORIZONTAL)
		save_button = wx.Button(self, label="Save")
		cancel_button = wx.Button(self, label="Cancel")
		button_box.Add(save_button)
		button_box.Add(cancel_button)

		main_sizer = wx.BoxSizer(wx.VERTICAL)
		main_sizer.Add(wx.StaticText(self, label="Token:"))
		main_sizer.Add(self.token_text_ctrl, 1, wx.EXPAND)
		main_sizer.Add(wx.StaticText(self, label="Repos:"))
		for repo, refresh_time, target_folder in self.repos:
			main_sizer.Add(repo, 1, wx.EXPAND)
			main_sizer.Add(refresh_time, 1, wx.EXPAND)
			main_sizer.Add(target_folder, 1, wx.EXPAND)
		main_sizer.Add(button_box, 0, wx.ALIGN_RIGHT)

		self.list_ctrl = wx.ListCtrl(self, wx.ID_ANY, style=wx.LC_REPORT)
		self.list_ctrl.InsertColumn(0, "Name")
		self.list_ctrl.InsertColumn(1, "Value")

		self.SetSizer(main_sizer)

		save_button.Bind(wx.EVT_BUTTON, self.on_save)
		cancel_button.Bind(wx.EVT_BUTTON, self.on_cancel)

	def on_save(self, event):
		config = {
			"token": self.token_text_ctrl.GetValue(),
			"repos": [
				(repo.GetValue(), refresh_time.GetValue(), target_folder.GetValue())
				for repo, refresh_time, target_folder in self.repos
			]
		}
		with open(filename, "w") as f:
			yaml.dump(config, f, default_flow_style=False)
		self.Close()

	def on_cancel(self, event):
		self.Close()

	def on_load(self, event):
		with open(filename, "r") as f:
			config = yaml.safe_load(f)
		self.token_text_ctrl.SetValue(config["token"])
		for repo, refresh_time, target_folder in config["repos"]:
			self.repos[i][0].SetValue(repo)
			self.repos[i][1].SetValue(refresh_time)
			self.repos[i][2].SetValue(target_folder)

def main():
	app = wx.App()
	dialog = ConfigDialog(None)
	dialog.Show()
	app.MainLoop()
