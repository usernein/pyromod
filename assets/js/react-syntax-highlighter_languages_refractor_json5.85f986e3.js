"use strict";
exports.id = 2180;
exports.ids = [2180,3657];
exports.modules = {

/***/ 45950:
/***/ ((module) => {



module.exports = json
json.displayName = 'json'
json.aliases = ['webmanifest']
function json(Prism) {
  // https://www.json.org/json-en.html
  Prism.languages.json = {
    property: {
      pattern: /(^|[^\\])"(?:\\.|[^\\"\r\n])*"(?=\s*:)/,
      lookbehind: true,
      greedy: true
    },
    string: {
      pattern: /(^|[^\\])"(?:\\.|[^\\"\r\n])*"(?!\s*:)/,
      lookbehind: true,
      greedy: true
    },
    comment: {
      pattern: /\/\/.*|\/\*[\s\S]*?(?:\*\/|$)/,
      greedy: true
    },
    number: /-?\b\d+(?:\.\d+)?(?:e[+-]?\d+)?\b/i,
    punctuation: /[{}[\],]/,
    operator: /:/,
    boolean: /\b(?:false|true)\b/,
    null: {
      pattern: /\bnull\b/,
      alias: 'keyword'
    }
  }
  Prism.languages.webmanifest = Prism.languages.json
}


/***/ }),

/***/ 50235:
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {


var refractorJson = __webpack_require__(45950)
module.exports = json5
json5.displayName = 'json5'
json5.aliases = []
function json5(Prism) {
  Prism.register(refractorJson)
  ;(function (Prism) {
    var string = /("|')(?:\\(?:\r\n?|\n|.)|(?!\1)[^\\\r\n])*\1/
    Prism.languages.json5 = Prism.languages.extend('json', {
      property: [
        {
          pattern: RegExp(string.source + '(?=\\s*:)'),
          greedy: true
        },
        {
          pattern:
            /(?!\s)[_$a-zA-Z\xA0-\uFFFF](?:(?!\s)[$\w\xA0-\uFFFF])*(?=\s*:)/,
          alias: 'unquoted'
        }
      ],
      string: {
        pattern: string,
        greedy: true
      },
      number:
        /[+-]?\b(?:NaN|Infinity|0x[a-fA-F\d]+)\b|[+-]?(?:\b\d+(?:\.\d*)?|\B\.\d+)(?:[eE][+-]?\d+\b)?/
    })
  })(Prism)
}


/***/ })

};
;