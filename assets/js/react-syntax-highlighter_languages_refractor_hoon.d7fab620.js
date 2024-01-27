"use strict";
exports.id = 9426;
exports.ids = [9426];
exports.modules = {

/***/ 60591:
/***/ ((module) => {



module.exports = hoon
hoon.displayName = 'hoon'
hoon.aliases = []
function hoon(Prism) {
  Prism.languages.hoon = {
    comment: {
      pattern: /::.*/,
      greedy: true
    },
    string: {
      pattern: /"[^"]*"|'[^']*'/,
      greedy: true
    },
    constant: /%(?:\.[ny]|[\w-]+)/,
    'class-name': /@(?:[a-z0-9-]*[a-z0-9])?|\*/i,
    function: /(?:\+[-+] {2})?(?:[a-z](?:[a-z0-9-]*[a-z0-9])?)/,
    keyword:
      /\.[\^\+\*=\?]|![><:\.=\?!]|=[>|:,\.\-\^<+;/~\*\?]|\?[>|:\.\-\^<\+&~=@!]|\|[\$_%:\.\-\^~\*=@\?]|\+[|\$\+\*]|:[_\-\^\+~\*]|%[_:\.\-\^\+~\*=]|\^[|:\.\-\+&~\*=\?]|\$[|_%:<>\-\^&~@=\?]|;[:<\+;\/~\*=]|~[>|\$_%<\+\/&=\?!]|--|==/
  }
}


/***/ })

};
;