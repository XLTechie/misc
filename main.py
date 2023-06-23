import os
import logging as log
from time import strftime
LOG_FILE = r"%temp%\testApp.log"

# Was artifact watcher 2
import wx
import github
import threading


class App(wx.App):
	def OnInit(self):
		self.frame = wx.Frame(None, title="Artifact Downloader")
		self.frame.Show()
		self.repository = github.Repository("XLTechie", "misc")
		self.artifacts_folder = os.path.expandvars(r"%temp%\artifacts")
		self.github_thread = threading.Thread(target=self._watch_repository)
		self.github_thread.daemon = True
		self.github_thread.start()
		return True

	def _watch_repository(self):
		while True:
			for workflow_run in self.repository.get_workflow_runs():
				for artifact in workflow_run.artifacts:
					filename = artifact.name
					filepath = os.path.join(self.artifacts_folder, filename)
					if not os.path.exists(filepath):
						artifact.download(filepath)

def main():
	app = App()
	app.MainLoop()

if __name__ == "__main__":
	try:
		log.basicConfig(level=log.INFO, filename=os.path.abspath(os.path.expandvars(LOG_FILE)), filemode="w")
		log.info("Log started at " + strftime("%x %X"))
		main()
	except Exception as e:
		log.exception("Exception occurred")
		log.info("Terminating in failure.")
	else:
		log.info("Terminating successfully.")
	finally:
		log.info("Shutting down.")
