import wx

class Menu(wx.Menu):
	"""Manages a wx Menu.
	Create the menu with the menu title, including optional shortkey indicator (&).
	Provide all menu items as four-tuples in the following args.
	Example: (wx.ID_XXXX, "&Name", "helpString", event_callable)
	"""

	_stealthTitle = None

	def __init__(self, title, *args):
		super().__init__()
		# We don't propagate the title up to the menu itself, because that displays it at the top.
		# Instead, we carry it locally, and return it if asked via GetTitle().
		self._stealthTitle = title
		# Process each menu item, presented as a tuple in args
		for id, name, helpString, toCall in args:
			if id != wx.ID_SEPARATOR:
				thisItem = self.Append(id, name, helpString)
				if toCall is not None: #callable(toCall):
					self.Bind(wx.EVT_MENU, toCall, id=id)
			else:  # It's a separator, not a real item
				self.AppendSeparator()

	def GetTitle(self):
		"""Overrides the wx.Menu.GetTitle method.
		Because the kind of menus we prefer to use won't generally include displayed titles as their
		first "item", we don't (usually) set a title.
		But in case we did, this function checks and returns the parent class's title, if any.
		If there isn't one, it instead returns the "stealth title" that is carried in the instance.
		"""
		realTitle = super().GetTitle()
		if realTitle is not None and realTitle is not "":
			return realTitle
		else:
			return self._stealthTitle
