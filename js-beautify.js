var beautify = require('js-beautify').js_beautify,
  fs = require('fs');

var file = process.argv[2] || "";


fs.readFile(file, 'utf8', function(err, data) {
  if (err) {
    throw err;
  }
  fs.writeFile(file, beautify(data, {
    indent_size: 2
  }), function(err) {
    if (err) throw err;
    console.log('formated!');
  });
});