// https://github.com/pkra/mathjax-node-page
// https://github.com/mathjax/MathJax-node
// https://github.com/mathjax/mathjax-node-cli/

// a simple TeX-input example
var mjAPI = require("mathjax-node");
var fs = require("fs");
var path = require("path");
const jsdom = require("jsdom");
const { JSDOM } = jsdom;


mjAPI.config({
  MathJax: {
    // traditional MathJax configuration
  },
  displayErrors: true,
  displayMessages: true
});
mjAPI.start();

var filename = "C:\\Users\\jh\\Documents\\GIT\\jehtech\\src\\html\\mathsy_stuff\\math_revision.html"
const input = fs.readFileSync(filename);

var mjpage = require('mathjax-node-page');
mjpage(input, {format: ["TeX"]}, {svg: true}, function(output) {
    console.log(output); // resulting HTML string
});

process.exit(); // TEST

// https://a3nm.net/blog/selfhost_mathjax.html
//<p><span class="math-tex">\(x = {-b \pm \sqrt{b^2-4ac} \over 2a}\)</span></p>
/// node C:\Users\jh\node_modules\mathjax-node-page\bin\mjpage < "html\mathsy_stuff\math_revision.html" > wow.html