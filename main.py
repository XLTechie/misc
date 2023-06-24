import wx
import configobj
import github

class MainFrame(wx.Frame):

    def __init__(self):
        super().__init__(None, title="Github OAuth")
        self.config = configobj.ConfigObj("config.ini", defaults={"access_token": ""})

        if not self.config.has_section("config"):
            self._show_login_dialog()
        else:
            self._show_token_dialog(self.config["access_token"])

    def _show_login_dialog(self):
        dialog = wx.Dialog(self, title="Login to GitHub")
        text_ctrl_username = wx.TextCtrl(dialog)
        text_ctrl_password = wx.TextCtrl(dialog, style=wx.TE_PASSWORD)

        button_login = wx.Button(dialog, label="Login")
        button_cancel = wx.Button(dialog, label="Cancel")

        button_login.Bind(wx.EVT_BUTTON, lambda event: self._on_login(text_ctrl_username, text_ctrl_password))
        button_cancel.Bind(wx.EVT_BUTTON, lambda event: dialog.Close())

        layout = wx.BoxLayout(dialog, wx.VERTICAL)
        layout.Add(wx.StaticText(dialog, label="Username:"))
        layout.Add(text_ctrl_username, proportion=1)
        layout.Add(wx.StaticText(dialog, label="Password:"))
        layout.Add(text_ctrl_password, proportion=1)
        layout.Add(button_login, flag=wx.BOTTOM, border=10)
        layout.Add(button_cancel, flag=wx.BOTTOM, border=10)

        dialog.ShowModal()

    def _on_login(self, text_ctrl_username, text_ctrl_password):
        client = github.Github(username=text_ctrl_username.GetValue(), password=text_ctrl_password.GetValue())
        try:
            client.get_user()
        except github.UnknownObjectException:
            wx.MessageBox("Invalid username or password", "Error", wx.OK | wx.ICON_ERROR)
            return

        token = client.get_token()
        self.config["access_token"] = token
        self.config.write()
        self._show_token_dialog(token)

    def _show_token_dialog(self, token):
        dialog = wx.Dialog(self, title="Access Token")
        text_ctrl = wx.TextCtrl(dialog, value=token)

        button_ok = wx.Button(dialog, label="OK")
        button_cancel = wx.Button(dialog, label="Cancel")

        button_ok.Bind(wx.EVT_BUTTON, lambda event: dialog.Close())
        button_cancel.Bind(wx.EVT_BUTTON, lambda event: dialog.Close())

        layout = wx.BoxLayout(dialog, wx.VERTICAL)
        layout.Add(text_ctrl, proportion=1)
        layout.Add(button_ok, flag=wx.BOTTOM, border=10)
        layout.Add(button_cancel, flag=wx.BOTTOM, border=10)

        dialog.ShowModal()
 
def main():
    app = wx.App()
    frame = MainFrame()
    frame.Show()
    app.MainLoop()
