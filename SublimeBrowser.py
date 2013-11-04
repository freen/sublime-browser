import urllib2
import threading

import sublime
import sublime_plugin

from bs4 import BeautifulSoup


class PromptSublimeBrowserCommand(sublime_plugin.WindowCommand):

    def run(self):
        self.window.show_input_panel("Enter URL", "http://", self.on_done, None, None)

    def on_done(self, text):
        view = self.window.new_file()
        view.run_command("sublime_browser", {"url": text})


class SublimeBrowserCommand(sublime_plugin.TextCommand):

    def run(self, edit, url):
        request = SublimeBrowserRequest(url, self.view, edit);
        request.run()


class SublimeBrowserRequest(threading.Thread):
    def __init__(self, url, view, edit, timeout = 30):
        self.url = url
        self.view = view
        self.edit = edit
        self.timeout = timeout
        threading.Thread.__init__(self)

    def run(self):
        try:
            request = urllib2.Request(self.url, None, headers={"User-Agent": "Sublime Browser"})
            http_file = urllib2.urlopen(request, timeout=self.timeout)
            data = http_file.read()
            soup = BeautifulSoup(data)
            # title = str(soup.find('title').string)
            # body = str(soup.find('body').string)
            # page = title + "\n\n" + body;
            # self.view.insert(self.edit, 0, page)
            self.view.insert(self.edit, 0, data)
            return
        except (urllib2.HTTPError) as (e):
            err = '%s: HTTP error %s' % (__name__, str(e.code))
        except (urllib2.URLError) as (e):
            err = '%s: URL error %s' % (__name__, str(e.reason))
        sublime.error_message(err)