"use strict";
exports.id = 7561;
exports.ids = [7561,3657];
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

/***/ 80963:
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {


var refractorJson = __webpack_require__(45950)
module.exports = jsonp
jsonp.displayName = 'jsonp'
jsonp.aliases = []
function jsonp(Prism) {
  Prism.register(refractorJson)
  Prism.languages.jsonp = Prism.languages.extend('json', {
    punctuation: /[{}[\]();,.]/
  })
  Prism.languages.insertBefore('jsonp', 'punctuation', {
    function: /(?!\s)[_$a-zA-Z\xA0-\uFFFF](?:(?!\s)[$\w\xA0-\uFFFF])*(?=\s*\()/
  })
}


/***/ })

};
;