import { Injectable } from '@nestjs/common';
import { levelSequences } from '../../../levels';
import {HeadlessGit} from "../../../js/git/headless";
import Q from "q";
import {expectTreeAsync, compareLevelTree} from "../../base";
import {levelsState} from "../git.service";
import * as util from "../../../js/util"
import {Command} from "../../../js/models/commandModel"
import TreeCompare from "../../../js/graph/treeCompare";
import * as axios from "axios";
import * as https from "node:https";
import {env} from "../../env";

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
    const jwtToken = dispatchFromLevelDto.jwtToken

    const level = levelSequences[levelType][levelIndex - 1]
    const userState = state[userId]

    let headless = userState ? userState[level.name.en_US] : undefined
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
    // выводим дерево из решения, текущее состояние дерева для данного пользователя и результат проверки
    console.log(level.goalTreeString)
    console.log(headless.gitEngine.printTree())
    console.log(res)

    // -----------------------------------------------------------
    // возвращаем ответ

    if (res) {
      await this.sendMark(1, dispatchFromLevelDto.jwtToken)
    }

    return {
      'levelComplete': res,
      'userId': userId,
      'nextLevelType': dispatchFromLevelDto.levelType,
      'nextLevelIndex': dispatchFromLevelDto.levelIndex + 1,
    }
  }

  async sendMark(mark, jwtToken){
    const data = {mark}
    console.log('send mark')
    await axios.post('https://python_app:8001/python_app/v1/send-score/', data, {
      httpsAgent: new https.Agent({
        rejectUnauthorized: false
      }),
      headers: {
        'Cookie': `${env.JWT_COOKIE_NAME}=${jwtToken}`,
      },
    })

  }
}
