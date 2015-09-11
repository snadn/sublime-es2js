# sublime-es2js

just copy form https://github.com/timdouglas/sublime-less2css and replace less,css to es,js for use babel transform

# sublime-less2css

Sublime Text 2 and 3 Plugin to compile less files to css on save. Requires lessc installed on PATH.


# Features

 * Automatically compile less -> css on save when editing a .less file in sublime
 * Reports compilation errors
 * Compile all less files in a directory to css files

NB This plugin requires lessc to be in your execution path

# Installation

## Install The Plugin

Either clone into your sublime packages directory, or just use [Package Control](https://github.com/wbond/sublime_package_control/)

## Install Requirements

Es2Js requires lessc to compile less to css.

### Mac OS X / Linux(Ubuntu/Debian…)

1. Install [NodeJS](http://nodejs.org) (you may need nodejs-legacy - see [issue #23](https://github.com/timdouglas/sublime-less2css/issues/23))
2. Install npm([NodeJS Package Manager](https://npmjs.org/doc/README.html))
3. Install less

	    npm install less -gd

4. Optional: To use minification you will need a minifier. Install less-plugin-clean-css or similar.

        npm install -g less-plugin-clean-css

5. Optional: To use autoprefix. Install [less-plugin-autoprefix](https://github.com/less/less-plugin-autoprefix).

        npm install -g less-plugin-autoprefix


### Windows

1. Clone [less.js-windows](https://github.com/duncansmart/less.js-windows)
2. Add the path of your less.js-windows to PATH environment variable([How to?](http://msdn.microsoft.com/en-us/library/ee537574.aspx)).

[中文版详细安装教程](http://fdream.net/blog/article/783.aspx)

# Configuration
less2css can be configured on two levels. There are the user settings which you can access through `Preferences\Package Settings\less2css`. These are your global settings. Below you will find a description for all the various settings. The second level where you can configure less2css is at the project level. If you have a Sublime Text project file, it has the extension `.sublime-project`, you can override your user settings for just that project. This will be described at the end of this chapter.

### autoCompile
The allowed values are `true` and `false`. When this setting is set to `true` the plugin will compile your LESS file each time you save it (otherwise you can compile from Sublime's "Tools" > "Es > Js" > "Compile this file to css" menu item).

### createJsSourceMaps
When `true` a css source map will be generated.

### lessBaseDir
This folder is only used when compiling all LESS files at once through *Tools \ Es>Js \ Compile all less in less base directory to css*. This can be an absolute path or a relative path. A relative path is useful when your projects always use the same structure, like a folder named `less` to keep all your LESS files in. When compiling all files at once it will also process all subfolders under the base folder.

### lesscCommand
This setting can be used to specify a different compiler. When it is left empty the default compiler, named *lessc*, will be used.

### ignorePrefixedFiles
The allowed values are `true` and `false`. When this setting is `true` the plugin will not compile files whose file name start with an underscore (`_`) when:

- saving and `autoCompile` set to `true`
- building all LESS files through *Tools \ Es>Js \ Compile all less in less base directory to css*.

You can still compile the file through *Tools \ Es>Js \ Compile this less file to css* or the appropriate shortcut.

### main_file
When you specify a main file only this file will get compiled when you save any LESS file. This is especially useful if you have one LESS file which imports all your other LESS files. Please note that this setting is only used when compiling a single LESS file and not when compiling all LESS files in the LESS base folder through *Tools \ Es>Js \ Compile all less in less base directory to css*. *Note: If your main file imports other files, the other files must be in the same folder for less2css to automatically compile your main file when editing an imported file.*

### minify
Default: True
The allowed values are `true`/`false` or a string which passes a minification option to lessc (e.g. `--clean-css`).
When this setting is set to `true` the LESS compiler will be instructed to create a minified CSS file. The recommended less minifier is `npm install -g less-plugin-clean-css` which is a required dependancy when `minify=true`.

### minName
When the minify setting is set to `true` the LESS compiler will add `.min` to the created minified version of the css files: `default.less` would be compiled to the minified `default.min.css`.

### outputDir
Use this setting to specify the folder where the CSS files will be placed. The following values are supported:

* Empty string or `./`
Use an empty string or `./` to have the CSS file stored in the same folder as the LESS file.

* Absolute path
Specify an absolute path to the directory where the CSS file should be stored, eg. `/home/user/projects/site/assets/css`

* Relative path
Specify a partial path to the directory where the CSS should be stored, eg. `./css`. This will store the CSS files in a folder CSS in the root of the project.

### `auto` setting
If you set the `outputDir` to `auto`, the plugin will try to automatically determine the folder where the CSS should be compiled to. It works best when you compile a single css file that imports other CSS files. If you work with multiple CSS files within one project that get compiled seperately, consider using the [`shadow`](#shadow-setting) setting instead.

The `auto` setting recognizes the following project setups:

  - When your LESS files are stored directly in a folder called `css\less` (and not in any subfolders) the compiled CSS files will be placed in the `css` folder.

		[project]
		    |- [css]
		    |---- [less]
		    |-------- site.less

  Will result in the following after compilation:

		[project]
		    |- [css]
		    |---- [less]
		    |-------- site.less
		    |---- site.css

  - When your LESS files are stored in a folder called `less` and its parent folder has a subfolder named `css` the compiled CSS files will be placed in the `css` folder.

		[project]
		    |- [css]
		    |- [less]
		    |---- site.less

  Will result in the following after compilation:

		[project]
		    |- [css]
		    |---- site.css
		    |- [less]
		    |---- site.less

  - If neither of the two cases above have been met the CSS file will be stored in the same folder as the LESS file is in.

### `shadow` setting

Use this setting to compile a complete `less` folder into a shadow `css` folder. It is expected your LESS files are stored in a folder named `less`. Within this folder you are free to create any number of subfolder to organise your LESS files. When you compile a single file or all files through the menu command, the string `less` will be replaced with `css` in the file path. For example, if you have this file structure:

	[project]
	    |- [less]
	    |---- [global]
	    |-------- global.less
	    |---- [elements]
	    |-------- header.less
	    |---- site.less

It will generate the same structure, only with css as its root folder like:

	[project]
	    |- [css]
	    |---- [global]
	    |-------- global.css
	    |---- [elements]
	    |-------- header.css
	    |---- site.css
	    |- [less]
	    |---- [global]
	    |-------- global.less
	    |---- [elements]
	    |-------- header.less
	    |---- site.less

### outputFile
When you specify an output file, this will be the file name used to compile **all** LESS files to. The content of the file will be overwritten after each compile. When you build all LESS file in the LESS base folder through *Tools \ Es>Js \ Compile all less in less base directory to css* you will only have the CSS of the last compiled file! Assign an empty string to have each LESS file compiled to its CSS counterpart, ie: site.less will become site.css.

### showErrorWithWindow
Set to `true` to see parse errors in a pop up window

### autoprefix
Set to `true` to add prefixes to css after conversion from less

# Project settings
You can use the configuration settings that are described above and apply them to just the project you are working on. In order to do this you need to manually alter the `.sublime-project` file. A default project file looks like this:

	{
		"folders":
		[
			{
				"path": "<path_to_project_folder"
			}
		]
	}

You can add the less2css settings like this:

	{
		"folders":
		[
			{
				"path": "<path_to_project_folder"
			}
		],
		"settings":
		{
			"less2css":
			{
				"autoCompile": false,
				"minify": false
			}
		}
	}

Now the user settings `autoCompile` and `minify` will be overriden by the project setting.
