// Each level is part of a "sequence;" levels within
// a sequence proceed in the order listed here


const request = new XMLHttpRequest();
request.open("GET", "http://localhost:3000/get-levels/", false);

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
