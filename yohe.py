import sublime
import sublime_plugin
import re
import webbrowser
import os
import subprocess

class YoheCommand():

    def get_path(self, paths):
        if paths:
            return paths[0].replace('\\', '/')
        # DEV: On ST3, there is always an active view.
        #   Be sure to check that it's a file with a path (not temporary view)
        elif self.window.active_view() and self.window.active_view().file_name():
            return self.window.active_view().file_name().replace('\\', '/')
        elif self.window.folders():
            return self.window.folders()[0].replace('\\', '/')
        else:
            sublime.error_message('yoho: Unkonw Error')
            return False
    def get_git_path(self):
        git_dir = self._getSetting('git_dir');
        if(git_dir == None):
            sublime.error_message('git not found')
        return git_dir.replace('\\', '/') + '/bin/sh.exe';

    def get_vhosts(self, paths):
        apache_dir = self._getSetting('apache_dir')
        try:
            input = open(apache_dir + '\\conf\\extra\\httpd-vhosts.conf', 'r')
        except Exception:
            return sublime.error_message('apache directory not found')
        content = input.read()
        input.close()
        list = re.findall('<VirtualHost[^<#]*<', content)
        vhosts = []
        for item in list:
            arr_item = re.sub('[\n\s]+', ' ', item).split(' ')
            vhosts.append(self._getHost(arr_item))
        return vhosts

    def match_url(self, path, vhosts):
        for host in vhosts:
            if(re.search(path, host[1])):
                return host[0]
        return None

    # host format : [baseAddress, dir]
    def _getHost(self, arr):
        host = []
        for index, value in enumerate(arr):
            if(re.search('VirtualHost', value) != None):
                i = index + 1
                host.append(arr[i].replace('>', '').replace('*', '127.0.0.1'))
            if(value == 'DocumentRoot'):
                i = index + 1
                host.append(arr[i])
        return host

    def _getSetting(self, key):
        settings = sublime.load_settings('yohe.sublime-settings')
        return settings.get(key)


class OpenWebCommand(sublime_plugin.WindowCommand, YoheCommand):

    def run(self, paths=[], parameters=None):
        path = self.get_path(paths)
        vhosts = self.get_vhosts('')
        while True:
            url = self.match_url(path, vhosts)
            if(url != None):
                webbrowser.open_new('http://' + url)
                return
            path = re.sub('/[^/]*$', '',path)
            if(path.count('/') <= 1):
                break

        return sublime.error_message('vhost not found')



class OpenGitCommand(sublime_plugin.WindowCommand, YoheCommand):

    def run(self, paths=[]):
        path = self.get_path(paths).replace('\\', '/')
        git  = self.get_git_path()
        while True:
            if(os.path.isdir(path)):
                print(git + ' --login -i')
                if(subprocess.Popen(git + ' --login -i', cwd=path)):
                    return
                else:
                     return sublime.error_message('yoho: Unkonw Error')
            path = re.sub('/[^/]*$', '',path)


class OpenGitExCommand(sublime_plugin.WindowCommand, YoheCommand):

    def run(self, paths=[]):
        command = OpenGitCommand(self.window)
        command.run(paths)
        return