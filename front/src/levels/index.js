// Each level is part of a "sequence;" levels within
// a sequence proceed in the order listed here


const {env} = require("../js/env");
const request = new XMLHttpRequest();
const url = `/get-levels/`
console.log(url)
request.open("GET", url, false);

request.send(null);

if (request.status === 200) {
  // console.log(request.responseText);
}

const res = JSON.parse(request.responseText);
exports.levelSequences = res.levelSequences;
const sequenceInfo = exports.sequenceInfo = res.sequenceInfo;

exports.getTabForSequence = function(sequenceName) {
  var info = sequenceInfo[sequenceName];
  return (info.tab) ?
    info.tab :
    'main';
};
