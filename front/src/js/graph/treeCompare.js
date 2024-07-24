let _ = require('underscore');
const {env} = require("../env");

// static class...
let TreeCompare = {};

TreeCompare.dispatchFromLevel = function(levelBlob, rawCommandStr) {
  const request = new XMLHttpRequest();
  const url = `/dispatch-from-level/`
  request.open("POST", url, false);
  request.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  request.send(JSON.stringify({
    'levelType': levelBlob.levelType,
    'levelIndex': levelBlob.levelIndex,
    'userId': 1,
    'rawCommandStr': rawCommandStr,
  }));

  const res = JSON.parse(request.responseText);
  return res.levelComplete
};

TreeCompare.onlyMainCompared = function(levelBlob) {
  let getAroundLintTrue = true;
  switch (getAroundLintTrue) {
    case !!levelBlob.compareOnlyMain:
    case !!levelBlob.compareOnlyMainHashAgnostic:
    case !!levelBlob.compareOnlyMainHashAgnosticWithAsserts:
      return true;
    default:
      return false;
  }
};

TreeCompare.reduceTreeFields = function(trees) {
  let commitSaveFields = [
    'parents',
    'id',
    'rootCommit'
  ];
  let branchSaveFields = [
    'target',
    'id',
    'remoteTrackingBranchID'
  ];
  let tagSaveFields = [
    'target',
    'id'
  ];

  let commitSortFields = ['children', 'parents'];
  // for backwards compatibility, fill in some fields if missing
  let defaults = {
    remoteTrackingBranchID: null
  };
  // also fill tree-level defaults
  let treeDefaults = {
    tags: {}
  };

  trees.forEach(function(tree) {
    Object.keys(treeDefaults).forEach(function(key) {
      let val = treeDefaults[key];
      if (tree[key] === undefined) {
        tree[key] = val;
      }
    });
  });

  // this function saves only the specified fields of a tree
  let saveOnly = function(tree, treeKey, saveFields, sortFields) {
    let objects = tree[treeKey];
    Object.keys(objects).forEach(function(objKey) {
      let obj = objects[objKey];
      // our blank slate to copy over
      let blank = {};
      saveFields.forEach(function(field) {
        if (obj[field] !== undefined) {
          blank[field] = obj[field];
        } else if (defaults[field] !== undefined) {
          blank[field] = defaults[field];
        }
      });

      Object.values(sortFields || {}).forEach(function(field) {
        // also sort some fields
        if (obj[field]) {
          obj[field].sort();
          blank[field] = obj[field];
        }
      });
      tree[treeKey][objKey] = blank;
    });
  };

  trees.forEach(function(tree) {
    saveOnly(tree, 'commits', commitSaveFields, commitSortFields);
    saveOnly(tree, 'branches', branchSaveFields);
    saveOnly(tree, 'tags', tagSaveFields);

    tree.HEAD = {
      target: tree.HEAD.target,
      id: tree.HEAD.id
    };
    if (tree.originTree) {
      this.reduceTreeFields([tree.originTree]);
    }
  }, this);
};

module.exports = TreeCompare;
