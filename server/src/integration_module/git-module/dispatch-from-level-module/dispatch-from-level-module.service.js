import { Injectable } from '@nestjs/common';
import { levelSequences } from '../../../levels';
import {HeadlessGit} from "../../../js/git/headless";
import Q from "q";
import {expectTreeAsync, compareLevelTree} from "../../base";
import {levelsState} from "../git.service";
import * as util from "../../../js/util"
import {Command} from "../../../js/models/commandModel"
import TreeCompare from "../../../js/graph/treeCompare";


const _ = require('underscore');
const state = {}

@Injectable()
export class DispatchFromLevelModuleService {

  async dispatchFromLevel(dispatchFromLevelDto) {
    console.log(dispatchFromLevelDto)
    const levelIndex = dispatchFromLevelDto.levelIndex
    const levelType = dispatchFromLevelDto.levelType
    const userId = dispatchFromLevelDto.userId
    const strCommand = dispatchFromLevelDto.rawCommandStr

    const level = levelSequences[levelType][levelIndex]
    const userState = state[userId]

    let headless = userState ? userState[level.name.en_US] : undefined
    // console.log(headless)
    if (!headless) {
      headless = new HeadlessGit();
      if (!userState) {
        state[userId] = {}
      }
      state[userId][level.name.en_US] = headless

      if (level.startTree) {
        headless.gitEngine.loadTreeFromString(level.startTree);
      }
    }

    // ---------------------------------------------------------
    // выводим уровень для общей информации
    // console.log(level)
    // ---------------------------------------------------------
    // выполняем команду, не забыв дождаться от неё отклика о завершении в deferred
    const deferred = Q.defer();
    headless.sendCommand(strCommand, deferred)
    await deferred.promise

    // ----------------------------------------------------------
    // проверяем решенность уровня
    let current = headless.gitEngine.printTree();
    let res = await TreeCompare.dispatchFromLevel(level, current);

    // -----------------------------------------------------------
    // выводим текущее состояние дерева для данного пользователя и результат проверки
    console.log(headless.gitEngine.printTree())
    console.log(res)

    // -----------------------------------------------------------
    // возвращаем ответ

    return {
      'levelComplete': res,
      'userId': userId,
      'nextLevelType': dispatchFromLevelDto.levelType,
      'nextLevelIndex': dispatchFromLevelDto.levelIndex + 1,
    }
  }
}
