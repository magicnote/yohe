"use strict";

function requireBeautify(type) {
    if (type == 'html') {
        return require('js-beautify').html;
    }
    if (type == 'css') {
        return require('js-beautify').css;
    }
    return require('js-beautify');
}

var type = process.argv[2] || "js";
var file = process.argv[3] || "";

var beautify = requireBeautify(type);
var fs = require('fs');

var default_style = {
    "indent_size": 4,
    "indent_char": " ",
    "eol": "\n",
    "indent_level": 0,
    "indent_with_tabs": false,
    "preserve_newlines": true,
    "max_preserve_newlines": 10,
    "jslint_happy": false,
    "space_after_anon_function": false,
    "brace_style": "collapse",
    "keep_array_indentation": true,
    "keep_function_indentation": true,
    "space_before_conditional": true,
    "break_chained_methods": false,
    "eval_code": false,
    "unescape_strings": false,
    "wrap_line_length": 0,
    "wrap_attributes": "auto",
    "wrap_attributes_indent_size": 4,
    "end_with_newline": false
};

fs.readFile(file, 'utf8', function(err, data) {
        if (err) {
            throw err;
        }
        fs.writeFile(file, beautify(data, default_style), function(err) {
            if (err) throw err;
            console.log('formated!');
        });
    }

);