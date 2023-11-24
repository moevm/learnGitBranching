import { Injectable } from '@nestjs/common';
import base from './base';
import { HeadlessGit } from '../js/git/headless';
import { levelSequences } from '../levels';


const expectTreeAsync = (headless, command, expectedJSON) => {
  return headless.sendCommand(command).then(function() {
    return base.compareAnswer(headless, expectedJSON);
  });
};


const state = {}


@Injectable()
export class AppService {

  async sendCommand(sendCommandDto) {
    const level = levelSequences[sendCommandDto.levelType][sendCommandDto.levelIndex]

    let headless = state[level.name.en_US]
    if (!headless) {
      headless = new HeadlessGit();
      state[level.name.en_US] = headless

      if (level.startTree) {
        headless.gitEngine.loadTreeFromString(level.startTree);
      }
    }

    let res = await expectTreeAsync(headless, sendCommandDto.command, level.goalTreeString)
    if (res) {
      state[level.name.en_US] = undefined
    }

    // смотрим в логах что за результат + что за дерево получилось (изменилось ли, сохранилось ли и т.д.)
    console.log(res)
    console.log(JSON.stringify(headless.gitEngine.exportTree()))
    console.log('---------------')
    return {'result': res}
  }
}
