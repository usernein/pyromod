"use strict";
exports.id = 8614;
exports.ids = [8614];
exports.modules = {

/***/ 36500:
/***/ ((module) => {



module.exports = ebnf
ebnf.displayName = 'ebnf'
ebnf.aliases = []
function ebnf(Prism) {
  Prism.languages.ebnf = {
    comment: /\(\*[\s\S]*?\*\)/,
    string: {
      pattern: /"[^"\r\n]*"|'[^'\r\n]*'/,
      greedy: true
    },
    special: {
      pattern: /\?[^?\r\n]*\?/,
      greedy: true,
      alias: 'class-name'
    },
    definition: {
      pattern: /^([\t ]*)[a-z]\w*(?:[ \t]+[a-z]\w*)*(?=\s*=)/im,
      lookbehind: true,
      alias: ['rule', 'keyword']
    },
    rule: /\b[a-z]\w*(?:[ \t]+[a-z]\w*)*\b/i,
    punctuation: /\([:/]|[:/]\)|[.,;()[\]{}]/,
    operator: /[-=|*/!]/
  }
}


/***/ })

};
;