"use strict";
exports.id = 2526;
exports.ids = [2526];
exports.modules = {

/***/ 78090:
/***/ ((module) => {



module.exports = csv
csv.displayName = 'csv'
csv.aliases = []
function csv(Prism) {
  // https://tools.ietf.org/html/rfc4180
  Prism.languages.csv = {
    value: /[^\r\n,"]+|"(?:[^"]|"")*"(?!")/,
    punctuation: /,/
  }
}


/***/ })

};
;