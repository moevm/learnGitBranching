const Q = require('q');

const {HeadlessGit} = require('../../js/git/headless');
const TreeCompare = require('../../js/graph/treeCompare');
const {buildStudentProfile, personalizeLevel} = require('../../integration_module/student-profile');
const {
  verifyStudentSubmission,
} = require('../../integration_module/student-submission-verifier');
const {level: levelTemplate} = require('./studentSubmission');

function sendCommand(headless, commandText) {
  const deferred = Q.defer();
  headless.sendCommand(commandText, deferred);
  return deferred.promise.then((commands) => {
    const failedCommand = commands.find((command) => command.get('error'));
    if (failedCommand) {
      throw new Error(`${commandText}: ${failedCommand.get('result')}`);
    }
    return commands;
  });
}

describe('personalized laboratory submission level', () => {
  test('accepts the complete pull, filesystem, commit and push workflow', async () => {
    const profile = buildStudentProfile({
      user_id: '42',
      family_name: 'Иванов',
      given_name: 'Иван',
      full_name: 'Иванов Иван',
    });
    const level = personalizeLevel(levelTemplate, profile);
    const headless = new HeadlessGit();
    headless.gitEngine.loadTreeFromString(level.startTree);

    for (const command of level.solutionCommand.split(';')) {
      await sendCommand(headless, command);
    }

    expect(TreeCompare.dispatchFromLevel(level, headless.gitEngine.printTree())).toBe(true);
    expect(verifyStudentSubmission(level, headless.gitEngine)).toEqual({
      ok: true,
      checks: expect.objectContaining({
        branchExists: true,
        fileHasCorrectPath: true,
        fileHasIdentityAndGroup: true,
        commitMessageIsCorrect: true,
        remoteBranchExists: true,
      }),
    });
  });

  test('uses stable transliterated branch and directory names', () => {
    const profile = buildStudentProfile({
      user_id: '42',
      family_name: 'Смирнова',
      given_name: 'Анна',
      full_name: 'Смирнова Анна',
    });

    expect(profile.directoryName).toBe('Smirnova_Anna_lb3');
    expect(profile.branchName).toBe('Smirnova_Anna_lb3');
  });

  test('does not accept a file that skipped git add', async () => {
    const profile = buildStudentProfile({
      user_id: '42',
      family_name: 'Иванов',
      given_name: 'Иван',
      full_name: 'Иванов Иван',
    });
    const level = personalizeLevel(levelTemplate, profile);
    const headless = new HeadlessGit();
    headless.gitEngine.loadTreeFromString(level.startTree);

    const commandsWithoutAdd = level.solutionCommand
      .split(';')
      .filter((command) => !command.startsWith('git add'));
    for (const command of commandsWithoutAdd) {
      await sendCommand(headless, command);
    }

    expect(TreeCompare.dispatchFromLevel(level, headless.gitEngine.printTree())).toBe(true);
    expect(verifyStudentSubmission(level, headless.gitEngine).ok).toBe(false);
  });

  test('accepts an echo command already escaped by the browser', async () => {
    const headless = new HeadlessGit();
    await sendCommand(headless, 'mkdir work');
    await sendCommand(headless, 'cd work');
    await sendCommand(headless, 'echo "Pedro" &gt;&gt; main.c');

    expect(headless.gitEngine.virtualFileSystem.files['/work/main.c']).toBe('Pedro\n');
  });

  test('finishes an unsupported command instead of hanging', async () => {
    const headless = new HeadlessGit();
    const deferred = Q.defer();
    headless.sendCommand('definitely-not-a-command', deferred);

    const commands = await deferred.promise;
    expect(commands).toHaveLength(1);
    expect(commands[0].get('error')).toBeTruthy();
  });
});
