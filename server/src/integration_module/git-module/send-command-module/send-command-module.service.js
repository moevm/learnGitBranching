import { Injectable } from '@nestjs/common';
import base from '../../base';
import { HeadlessGit } from '../../../js/git/headless';
import { levelSequences } from '../../../levels';
import { levelsState } from '../git.service'
import Q from "q";


const expectTreeAsync = (headless, command, expectedJSON, deferred) => {
  return headless.sendCommand(command, deferred).then(function() {
    return base.compareAnswer(headless, expectedJSON);
  });
};


@Injectable()
export class SendCommandModuleService {

  async sendCommand(sendCommandDto) {
    const level = levelSequences[sendCommandDto.levelType][sendCommandDto.levelIndex]

    let headless = levelsState[level.name.en_US]
    if (!headless) {
      headless = new HeadlessGit();
      levelsState[level.name.en_US] = headless

      if (level.startTree) {
        headless.gitEngine.loadTreeFromString(level.startTree);
      }
    }

    const deferred = Q.defer();
    let res = await expectTreeAsync(headless, sendCommandDto.command, level.goalTreeString, deferred)
    // reset completed level state
    if (res) {
      levelsState[level.name.en_US] = undefined
    }
    const sentCommands = await deferred.promise
    let gitResultMessage = sentCommands.filter(el => el.attributes.result !== '').map(el => `Результат команды ${el.attributes.rawStr}:\n${el.attributes.result}`).join('\n\n')
    let levelResultMessage = res ? 'level completed' : 'not completed'

    // смотрим в логах что за результат
    console.log('Выполнен ли уровень:')
    console.log(levelResultMessage)
    // смотрим, что вывел "git"
    console.log(gitResultMessage)
    console.log('\n\n')

    return {'result': res, 'gitMessage': gitResultMessage, 'message': levelResultMessage}
  }
}
