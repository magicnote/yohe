import sublime
import sublime_plugin
import re
import webbrowser


class YoheCommand():

    def get_path(self, paths):
        if paths:
            return paths[0]
        # DEV: On ST3, there is always an active view.
        #   Be sure to check that it's a file with a path (not temporary view)
        elif self.window.active_view() and self.window.active_view().file_name():
            return self.window.active_view().file_name()
        elif self.window.folders():
            return self.window.folders()[0]
        else:
            sublime.error_message('yoho: Unkonw Error')
            return False

    def get_vhosts(self, paths):
        apache_dir = self._getSetting('apache_dir')
        try:
            input = open(apache_dir+'\\conf\\extra\\httpd-vhosts.conf', 'r')
        except Exception:
            return sublime.error_message('apache directory not found')
        content = input.read()
        input.close()
        list = re.findall('<VirtualHost[^<#]*<', content)
        vhosts = []
        for item in list:
            arr_item = re.sub("[\n\s]+", " ", item).split(' ')
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


class yoho_openCommand(sublime_plugin.WindowCommand, YoheCommand):

    def run(self, paths=[], parameters=None):
        path = self.get_path(paths).replace('\\', '/')
        vhosts = self.get_vhosts('')
        url = self.match_url(path, vhosts)
        if(url == None):
            return sublime.error_message('vhost not found')
        webbrowser.open_new("http://" + url)
