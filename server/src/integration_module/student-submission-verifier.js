function escapeRegExp(value) {
  return String(value).replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function getTargetId(ref) {
  if (!ref || !ref.get || !ref.get('target')) {
    return null;
  }
  return ref.get('target').get('id');
}

function verifyStudentSubmission(level, gitEngine) {
  const goal = level.virtualFileSystemGoal;
  if (!goal) {
    return {ok: true, checks: {}};
  }

  const branch = gitEngine.refs[goal.branchName];
  const remoteTrackingBranch = gitEngine.refs[`o/${goal.branchName}`];
  const mainBranch = gitEngine.refs.main;
  const originBranch = gitEngine.origin && gitEngine.origin.refs[goal.branchName];
  const studentCommitId = getTargetId(branch);
  const studentCommit = studentCommitId && gitEngine.refs[studentCommitId];
  const parentIds = studentCommit
    ? (studentCommit.get('parents') || []).map((parent) => parent.get('id'))
    : [];
  const fileSystem = gitEngine.getVirtualFileSystem();
  const fileContent = fileSystem.lastCommittedFiles[goal.filePath];
  const identityAndGroupPattern = new RegExp(
    `^\\s*${escapeRegExp(goal.fullName)}\\s*,\\s*группа\\s+\\S.*$`,
    'iu',
  );

  const checks = {
    branchExists: !!branch,
    headOnStudentBranch: getTargetId(gitEngine.HEAD) === goal.branchName,
    mainUnchanged: getTargetId(mainBranch) === goal.baseCommit,
    oneCommitFromMain: parentIds.length === 1 && parentIds[0] === goal.baseCommit,
    remoteBranchExists: !!originBranch,
    remoteBranchMatchesLocal: getTargetId(originBranch) === studentCommitId,
    trackingBranchMatchesLocal: getTargetId(remoteTrackingBranch) === studentCommitId,
    fileWasCommitted: fileSystem.lastCommittedCommit === studentCommitId,
    fileHasCorrectPath: typeof fileContent === 'string',
    fileHasIdentityAndGroup:
      typeof fileContent === 'string' && identityAndGroupPattern.test(fileContent.trim()),
    stagingIsEmpty: Object.keys(fileSystem.stagedFiles).length === 0,
    commitMessageIsCorrect:
      !!studentCommit && studentCommit.get('commitMessage') === goal.commitMessage,
  };

  return {
    ok: Object.keys(checks).every((key) => checks[key]),
    checks,
  };
}

module.exports = {
  verifyStudentSubmission,
};
