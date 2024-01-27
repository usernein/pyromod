"use strict";
exports.id = 8497;
exports.ids = [8497];
exports.modules = {

/***/ 15958:
/***/ ((module) => {



module.exports = bnf
bnf.displayName = 'bnf'
bnf.aliases = ['rbnf']
function bnf(Prism) {
  Prism.languages.bnf = {
    string: {
      pattern: /"[^\r\n"]*"|'[^\r\n']*'/
    },
    definition: {
      pattern: /<[^<>\r\n\t]+>(?=\s*::=)/,
      alias: ['rule', 'keyword'],
      inside: {
        punctuation: /^<|>$/
      }
    },
    rule: {
      pattern: /<[^<>\r\n\t]+>/,
      inside: {
        punctuation: /^<|>$/
      }
    },
    operator: /::=|[|()[\]{}*+?]|\.{3}/
  }
  Prism.languages.rbnf = Prism.languages.bnf
}


/***/ })

};
;