import sublime
import sublime_plugin
import subprocess
import os.path
import re

class FilterCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.view.window().show_input_panel("Filter", "", self.end, self.filter, self.end)
		
	def filter(self, filterstr):
		self.view.unfold(sublime.Region(0, self.view.size()))
		
		regs = self.view.lines(sublime.Region(0, self.view.size()))
		r = sublime.Region(0,0)
		self.view.erase_regions("FILTER")
		finds = []
		for reg in regs:
			line = self.view.substr(reg)
			f = re.finditer(filterstr, line)

			match = False
			for a in f:
				match = True
				finds.append(sublime.Region(reg.begin() + a.start(), reg.begin() + a.end()))

			if match:
				self.view.fold(r)
				r = sublime.Region(reg.end(), reg.end())
			else:
				r = r.cover(reg)

		self.view.add_regions("FILTER", finds, "comment")

		self.view.fold(r)
		self.view.show(0)

	def end(self, arg=None):
		self.view.erase_regions("FILTER")
		self.view.unfold(sublime.Region(0, self.view.size()))

		s = 0
		sel = self.view.sel()
		if len(sel) != 0:
			self.view.show_at_center(self.view.sel()[0])
