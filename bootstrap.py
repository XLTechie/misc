try:

	import os
	import sys
	import logging
	from time import strftime

	LOG_FILE = r"%temp%\testApp.log"
	logging.basicConfig(stream=sys.stdout, level=logging.INFO)
	#logging.basicConfig(level=logging.INFO, filename=os.path.abspath(os.path.expandvars(LOG_FILE)), filemode="w")
	#logging.info("Log started at " + strftime("%x %X"))

	if __name__ == "__main__":
		import main
		main.main()

except Exception as e:
	logging.exception("An exception occurred")
	logging.info("Terminating in failure.")
else:
	logging.info("Terminating successfully.")
finally:
	input("Press enter to shutdown.")
	logging.info("Shutting down.")
