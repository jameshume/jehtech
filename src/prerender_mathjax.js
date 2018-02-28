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
var html = fs.readFile(filename, (err, data) => {
    var document = new JSDOM(data).window.document;
    console.log("Rendering:", filename);

    mjAPI.typeset({
        html: document.body.innerHTML,
        singleDollars: true,
        renderer: "CommonHTML",
        inputs: ["TeX"],
        //xmlns:"svg",
        svg:true
      },
      function (result) {
        console.log(result);
        if (!result.errors) {
          console.log("FINE");
          console.log(result.html);
          console.log(result.svg);
        }
        else {console.log("ERRORS"); }
    });
});