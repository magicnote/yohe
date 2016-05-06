import sublime
import sublime_plugin
import re
import webbrowser
import os
import sys
import subprocess
import codecs


PLUGIN_DIR = os.path.dirname(os.path.realpath(__file__))


class unit():

    def save_in_file_cache(buff):
        temp_file_name = '.__Cache__'
        temp_file_path = PLUGIN_DIR + '/' + temp_file_name
        try:
            output =  open(temp_file_path, mode='w', encoding='utf-8')
            output.write(buff)
            output.close()
            return temp_file_path;
        except Exception:
            sublime.error_message('cache write failed')


    def read_file(filePath,errMessages):
        try:
            input =  open(filePath, mode='r', encoding='utf-8')
            content = input.read()
            input.close()
            return content
        except Exception:
            sublime.error_message(errMessages)

    def get_setting(key):
        settings = sublime.load_settings('yohe.sublime-settings')
        return settings.get(key)


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
        git_dir = unit.get_setting('git_dir');
        if(git_dir == None):
            sublime.error_message('git not found')
        return git_dir.replace('\\', '/') + '/bin/sh.exe';

    def get_vhosts(self, paths):
        apache_dir = unit.get_setting('apache_dir')
        content = unit.read_file(apache_dir + '\\conf\\extra\\httpd-vhosts.conf',
            'apache directory not found')
        list = re.findall('<VirtualHost[^<#]*<', content)
        vhosts = []
        for item in list:
            arr_item = re.sub('[\n\s]+', ' ', item).split(' ')
            vhosts.append(self._get_vhost(arr_item))
        return vhosts

    def match_url(self, path, vhosts):
        for host in vhosts:
            if(re.search(path, host['root'])):
                return host['ServerName'] if 'ServerName' in host else host['ip']
        return None

    # vhost format : [baseAddress, dir]
    def _get_vhost(self, arr):
        host = {}
        #arr data fomrat : ['key', 'value', 'key', 'value']
        for index, value in enumerate(arr):
            i = index + 1
            if(re.search('ServerName', value) != None):
                host['ServerName']= arr[i];
            if(re.search('VirtualHost', value) != None):
                host['ip'] = arr[i].replace('>', '').replace('*', '127.0.0.1');
            if(value == 'DocumentRoot'):
                host['root'] = arr[i];
        return host


class OpenWebCommand(sublime_plugin.WindowCommand, YoheCommand):

    def run(self, paths=[], parameters=None):
        path = self.get_path(paths)
        vhosts = self.get_vhosts('')
   
        while True:
            url = self.match_url(path, vhosts)
            if(url != None):
                return webbrowser.open_new('http://' + url)
            path = os.path.dirname(path)
            if(path.count('/') <= 1):
                break
        return sublime.error_message('vhost not found')

class OpenGitCommand(sublime_plugin.WindowCommand, YoheCommand):

    def run(self, paths=[]):
        path = self.get_path(paths).replace('\\', '/')
        git  = self.get_git_path()
        if(not os.path.isdir(path)):
            path = os.path.dirname(path)
        if(not subprocess.Popen(git + ' --login -i', cwd=path)):
            return sublime.error_message('yoho: Unkonw Error')

class OpenGitExCommand(sublime_plugin.WindowCommand, YoheCommand):

    def run(self, paths=[]):
        command = OpenGitCommand(self.window)
        command.run(paths)

class OpenFolderCommand(sublime_plugin.WindowCommand, YoheCommand):

    def run(self, paths=[]):
        path = self.get_path(paths).replace('\\', '/')
        if(not os.path.isdir(path)):
            path = os.path.dirname(path)
        os.startfile(path)

class FormaterCommand(sublime_plugin.TextCommand, YoheCommand):
    def run(self, edit, **args):
        type =args['type'];
        if (type == 'html' or type == 'js' or type == 'css'):
            entire_buffer_region = sublime.Region(0, self.view.size())
            cache_file_path = unit.save_in_file_cache(self.view.substr(entire_buffer_region))
            nodejs_dir = unit.get_setting('nodejs_dir')

            cmd = [nodejs_dir + '/node', PLUGIN_DIR + '/js-beautify.js', type, cache_file_path]
            subprocess.call(cmd)

            cache = unit.read_file(cache_file_path, 'cache read failed');
            os.remove(cache_file_path)
            self.view.replace(edit, entire_buffer_region, cache)
        elif(type == 'php'):
             self.view.run_command('fmt_now')
