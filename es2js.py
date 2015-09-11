# -*- coding: utf-8 -*-
import sublime
import sublime_plugin
import os
try:
  import escompiler
except ImportError:
  from . import escompiler

SETTING_SHOW_ALERT = "showErrorWithWindow"

#message window
class MessageWindow:
  def __init__(self, message=''):
    self.show(message)

  def show(self, message):
    if message == '':
      return
    settings = sublime.load_settings('es2js.sublime-settings')
    project_settings = sublime.active_window().active_view().settings().get("es2js")
    if project_settings is None:
      project_settings = {}
    show_alert = project_settings.get(SETTING_SHOW_ALERT, settings.get(SETTING_SHOW_ALERT,True))

    if not show_alert:
      return

    sublime.error_message(message)


############################
##### SUBLIME COMMANDS #####
############################

#single es file
class EsToJsCommand(sublime_plugin.TextCommand):
  def run(self, text):
    l2c = escompiler.Compiler(self.view)
    resp = l2c.convertOne()
    MessageWindow(resp)


class AutoEsToJsCommand(sublime_plugin.TextCommand):
  def run(self, text):
    l2c = escompiler.Compiler(self.view)
    resp = l2c.convertOne(is_auto_save=True)
    MessageWindow(resp)


#all es files
class AllEsToJsCommand(sublime_plugin.TextCommand):
  def run(self, text):
    l2c = escompiler.Compiler(self.view)
    sublime.status_message("Compiling .es files...")
    resp = l2c.convertAll()

    if resp != "":
      MessageWindow(resp)
    else:
      sublime.message_dialog("All .es files compiled successfully")


#listener to current es file
class EsToJsSave(sublime_plugin.EventListener):
  def on_post_save(self, view):
    view.run_command("auto_es_to_js")


#change js base setting
class SetEsBaseCommand(sublime_plugin.WindowCommand):
  def run(self):
    self.window.show_input_panel("Enter Your Es Base Directory: ", '', lambda s: self.set_es_setting(s), None, None)

  def set_es_setting(self, text):
    settings_base = 'es2js.sublime-settings'

    settings = sublime.load_settings("es2js.sublime-settings")

    if os.path.isdir(text):
      settings.set("esBaseDir", text)
      sublime.save_settings(settings_base)  # have to assume this is successful...

      sublime.status_message("Es Base Directory updated")
    else:
      sublime.error_message("Entered directory does not exist")


# set the js output folder to auto
class ResetEsBaseAuto(sublime_plugin.WindowCommand):
  def run(self):
    settings_base = 'es2js.sublime-settings'

    settings = sublime.load_settings("es2js.sublime-settings")

    settings.set("outputDir", "auto")
    sublime.save_settings(settings_base)

    sublime.status_message("Output directory reset to auto")


class SetOutputDirCommand(sublime_plugin.WindowCommand):
  def run(self):
    self.window.show_input_panel("Enter JS Output Directory: ", "", lambda s: self.set_output_dir(s), None, None)

  def set_output_dir(self, text):
    settings_base = 'es2js.sublime-settings'

    settings = sublime.load_settings("es2js.sublime-settings")

    if os.path.isdir(text):
      settings.set("outputDir", text)
      sublime.save_settings(settings_base)

      sublime.status_message("Output directory updated")
    else:
      sublime.error_message("Entered directory does not exist")


#toggle minification
class toggleJsMinificationCommand(sublime_plugin.WindowCommand):
  def run(self):
    #show yes/no input
    self.window.show_quick_panel(["Minify js", "Don't minify js"], lambda s: self.set_minify_flag(s))

  def set_minify_flag(self, minify):
    minify_flag = False

    if minify == 0:
      minify_flag = True

    settings = sublime.load_settings("es2js.sublime-settings")

    if minify == -1:
      #input was cancelled, don't change
      minify_flag = settings.get("minify", True)  # existing or default

    settings.set("minify", minify_flag)
    sublime.save_settings("es2js.sublime-settings")

    sublime.status_message("Updated minify flag")
