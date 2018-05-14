## yohe
Sublime Text 3 Plugin。


##### 为Sublime Text右侧菜单添加以下功能:

* `Open In Browser`  
   自动打开当前项目在apache中对应virtual host。
   如果设置了ServerName，优先使用ServerName访问，否则使用IP:Port形式访问。
* `Open In Git`  
   在当前目录的打开git。
* `Open In Folder`  
   在资源管理器中打开文件目录。

##### 为Sublime Text内容菜单添加以下功能:

* `Lint this php` 检查php语法错误(使用当前环境变量的php版本)
* `Formater`
	* `php`  (已整合[sublime-phpfmt]( https://github.com/nanch/sublime-phpfmt/tree/6125cf9058c0666f06ed758f0f5451996f7c7211)最后可用版本)
	* `javascript`
	* `html`
	* `css`

##### 安装
1.[download](https://github.com/magicnote/yohe/archive/master.zip)文件，打开 Sublime Text 找到 `Preferences` 菜单下的`Browse Packages...`，将下载文件解压后放入打开目录。  
2.将解压目录改名为`yohe`  
3.安装`nodejs`，并进入`yohe`目录执行`npm install`。(部分格式化功能必须)  
4.重启 Sublime Text。  
