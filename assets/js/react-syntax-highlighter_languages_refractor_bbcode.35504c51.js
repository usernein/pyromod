"use strict";
exports.id = 7250;
exports.ids = [7250];
exports.modules = {

/***/ 62260:
/***/ ((module) => {



module.exports = bbcode
bbcode.displayName = 'bbcode'
bbcode.aliases = ['shortcode']
function bbcode(Prism) {
  Prism.languages.bbcode = {
    tag: {
      pattern:
        /\[\/?[^\s=\]]+(?:\s*=\s*(?:"[^"]*"|'[^']*'|[^\s'"\]=]+))?(?:\s+[^\s=\]]+\s*=\s*(?:"[^"]*"|'[^']*'|[^\s'"\]=]+))*\s*\]/,
      inside: {
        tag: {
          pattern: /^\[\/?[^\s=\]]+/,
          inside: {
            punctuation: /^\[\/?/
          }
        },
        'attr-value': {
          pattern: /=\s*(?:"[^"]*"|'[^']*'|[^\s'"\]=]+)/,
          inside: {
            punctuation: [
              /^=/,
              {
                pattern: /^(\s*)["']|["']$/,
                lookbehind: true
              }
            ]
          }
        },
        punctuation: /\]/,
        'attr-name': /[^\s=\]]+/
      }
    }
  }
  Prism.languages.shortcode = Prism.languages.bbcode
}


/***/ })

};
;