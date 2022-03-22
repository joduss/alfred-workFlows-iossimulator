import json
import sys
from json import JSONEncoder
from os import environ
from typing import Any

from core.biplist.biplist import readPlist, writePlist

class ItemMod:
	  Cmd, Ctrl, Alt, Shift, Fn = ('cmd', 'ctrl', 'alt', 'shift', 'fn')

class Item:
	def __init__(self, title, subtitle="", icon=None, arg=None, autocomplete=None, valid=False, uid=None, modifierSubtitles=None):
		self.title = title
		self.subtitle = subtitle
		self.icon = icon
		self.arg = arg
		self.autocomplete = autocomplete
		self.valid = valid
		self.uid = uid
		self.modifierSubtitles = modifierSubtitles if modifierSubtitles is not None else {}
		self.mods = {}

		mods = (ItemMod.Cmd, ItemMod.Ctrl, ItemMod.Alt, ItemMod.Shift, ItemMod.Fn)

		for mod in mods:
			if mod in self.modifierSubtitles:
				self.mods[mod] = ItemModEntry(valid=self.valid, subtitle=self.modifierSubtitles[mod])

	def to_dict(self):
		return json.dumps(self, default=lambda o: o.__dict__)

	@staticmethod
	def generate_output(items):
		item_json = ItemJSONEncoder().encode({"items" : items})

		sys.stdout.write(item_json)
		sys.stdout.flush()


class ItemModEntry:
	def __init__(self, valid=False, arg: str or None=None, subtitle: str or None=None):
		self.valid = valid
		self.arg = arg
		self.subtitle = subtitle


class ItemJSONEncoder(JSONEncoder):

	def default(self, o: Any) -> Any:
		if isinstance(o, ItemModEntry) or isinstance(o, Item):
			return o.__dict__
		else:
			return o


def set_variable(name, value):
	info = readPlist('info.plist')
	# Set a variable
	info['variables'][name] = value

	# Save changes
	writePlist(info, 'info.plist')

def get_variable(name):
	if name in environ:
		return environ[name]
	else:
		return None

