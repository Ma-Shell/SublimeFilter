import sublime
import sublime_plugin
import subprocess

class FilterCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.view.window().show_input_panel("Filter", "", self.end, self.filter, self.end)

	def filter(self, filterstr, opts=sublime.LITERAL):
		self.view.unfold(sublime.Region(0, self.view.size()))
		self.view.erase_regions("FILTER")

		if len(filterstr) == 0:
			return
		
		regs_f = self.view.find_all(filterstr, opts)
		self.view.window().status_message("%i matches" % len(regs_f))
		regs = []
		cur_r = 0
		for reg in regs_f:
			reg_line = self.view.full_line(reg)
			if cur_r < reg_line.begin():
				regs.append(sublime.Region(cur_r, reg_line.begin()))

			cur_r = reg_line.end()

		end = self.view.size()
		if cur_r < end:
			regs.append(sublime.Region(cur_r, end))
			
		self.view.fold(regs)
		self.view.add_regions("FILTER", regs_f, "comment")
		self.view.show(0)

	def end(self, arg=None):
		self.view.erase_regions("FILTER")
		self.view.unfold(sublime.Region(0, self.view.size()))

		s = 0
		sel = self.view.sel()
		if len(sel) != 0:
			self.view.show_at_center(self.view.sel()[0])

class FilterReCommand(FilterCommand):
	def run(self, edit):
		self.view.window().show_input_panel("Filter (RE)", "", self.end, self.filter, self.end)

	def filter(self, filterstr):
		super().filter(filterstr, 0)
