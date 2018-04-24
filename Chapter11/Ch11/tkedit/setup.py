#!/usr/bin/env python3

from distutils.core import setup

setup(
	name='tkedit',
	version='0.1',
	description='This is a python text editor with syntax highlighting',
	author='David Love',
	py_modules= [
    	"colourchooser",
		"findwindow",
		"fontchooser",
		"highlighter",
		"linenumbers",
		"textarea",
		"texteditor",
    ],
    install_requires = [
	"PyYAML",
	],
	entry_points = {
		"console_scripts": ["tkedit = texteditor:main"]	
	}
)
 
