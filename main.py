# Version 3
import wx
import requests
import os
import sqlite3


class ArtifactDownloader(wx.Frame):

    def __init__(self):
        super().__init__(None, title="Artifact Downloader")

        self.config = None

        self.repo_url = ""
        self.artifact_folder = ""
        self.refresh_frequency = 10000

        self.Bind(wx.EVT_TIMER, self.on_timer)

        self.timer = wx.Timer(self)
        self.timer.Start(self.refresh_frequency)

        self.Show()

    def on_timer(self, event):
        if self.config is None:
            self.config_dialog()

        with sqlite3.connect("config.db") as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM config")
            rows = cursor.fetchall()

            for row in rows:
                repo_url = row[0]
                artifact_folder = row[1]
                refresh_frequency = row[2]

                if self.timer.IsRunning():
                    wx.Button(self, label="Stop", id=wx.ID_STOP).Bind(wx.EVT_BUTTON, self.on_stop_monitoring)
                else:
                    wx.Button(self, label="Start", id=wx.ID_START).Bind(wx.EVT_BUTTON, self.on_start_monitoring)

    def config_dialog(self):
        dialog = wx.Dialog(self, title="Configuration")
        dialog.SetSize((300, 200))

        repo_url = wx.TextCtrl(dialog)
        artifact_folder = wx.TextCtrl(dialog)
        refresh_frequency = wx.TextCtrl(dialog)
        wx.Button(dialog, label="Save", id=wx.ID_SAVE).Bind(wx.EVT_BUTTON, self.on_config_save)

        wx.BoxSizer(wx.VERTICAL).Add(repo_url)
        wx.BoxSizer(wx.VERTICAL).Add(artifact_folder)
        wx.BoxSizer(wx.VERTICAL).Add(refresh_frequency)

        dialog.ShowModal()

    def on_config_save(self, event):
        self.config = {
            "repo_url": repo_url.GetValue(),
            "artifact_folder": artifact_folder.GetValue(),
            "refresh_frequency": int(refresh_frequency.GetValue()),
        }

        with sqlite3.connect("config.db") as db:
            cursor = db.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS config (repo_url TEXT, artifact_folder TEXT, refresh_frequency INTEGER)")
            cursor.execute("INSERT INTO config VALUES (?, ?, ?)", (self.config["repo_url"], self.config["artifact_folder"], self.config["refresh_frequency"]))

    def on_start_monitoring(self, event):
        self.timer.Start(self.refresh_frequency)

    def on_stop_monitoring(self, event):
        self.timer.Stop()


if __name__ == "__main__":
    app = wx.App()
    downloader = ArtifactDownloader()
    app.MainLoop()
    input("Press enter to exit.")
