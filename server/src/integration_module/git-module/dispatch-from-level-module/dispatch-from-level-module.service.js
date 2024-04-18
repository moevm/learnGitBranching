import { Injectable } from '@nestjs/common';
import { levelSequences } from '../../../levels';
import {HeadlessGit} from "../../../js/git/headless";
import Q from "q";
import TreeCompare from "../../../js/graph/treeCompare";
import * as axios from "axios";
import * as https from "node:https";

const _ = require('underscore');
const state = {}

@Injectable()
export class DispatchFromLevelModuleService {

  async dispatchFromLevel(dispatchFromLevelDto) {
    const levelIndex = dispatchFromLevelDto.levelIndex
    const levelType = dispatchFromLevelDto.levelType
    const userId = dispatchFromLevelDto.userId
    const strCommand = dispatchFromLevelDto.rawCommandStr
    const jwtToken = dispatchFromLevelDto.jwtToken

    const level = levelSequences[levelType][levelIndex - 1]

    let userState = state[jwtToken] ? state[jwtToken] : undefined
    if (!userState) {
      state[jwtToken] = {}
    }
    userState = state[jwtToken]

    console.log(userState)
    let levelState = userState[level.name.en_US] ? userState[level.name.en_US] : undefined
    if (!levelState) {
      state[jwtToken][level.name.en_US] = {}
    }
    levelState = state[jwtToken][level.name.en_US]
    console.log(levelState)

    let headless = levelState['level'] ? levelState['level'] : undefined
    if (!headless) {
      headless = new HeadlessGit();
      if (level.startTree) {
        headless.gitEngine.loadTreeFromString(level.startTree);
      }
    }
    state[jwtToken][level.name.en_US]['level'] = headless
    state[jwtToken][level.name.en_US]['updatedAt'] = new Date()

    // ---------------------------------------------------------
    // выводим уровень для общей информации
    // console.log(level)
    // ---------------------------------------------------------
    // выполняем команду, не забыв дождаться от неё отклика о завершении в deferred
    const deferred = Q.defer();
    headless.sendCommand(strCommand, deferred)
    const commands = await deferred.promise
    await this.sendStatSendCommand(jwtToken, dispatchFromLevelDto.headers, commands.slice(-1)[0] )
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
      await this.sendStatResolveTask(jwtToken, dispatchFromLevelDto.headers)
    }

    this.clearOldState()
    return {
      'levelComplete': res,
      'userId': userId,
      'nextLevelType': dispatchFromLevelDto.levelType,
      'nextLevelIndex': dispatchFromLevelDto.levelIndex + 1,
    }
  }

  async sendStatResolveTask(jwtToken, nginx_headers) {
    await axios.post(
      'https://python_app:8001/python_app/v1/send-stat/',
      {
        'stat_event_type': 'resolve_task',
        'jwt_token': jwtToken,
        'extra_data': {},
        'user_ip': nginx_headers['x-real-ip'],
        'user_agent': nginx_headers['user-agent'],
      },
      {
          httpsAgent: new https.Agent({
            rejectUnauthorized: false
          }),
        },
      )
  }

  async sendMark(mark, jwtToken){
    const data = {mark}

    await axios.post('https://python_app:8001/python_app/v1/send-score/', data, {
      httpsAgent: new https.Agent({
        rejectUnauthorized: false
      }),
      headers: {
        'Cookie': `${process.env.JWT_COOKIE_NAME}=${jwtToken}`,
      },
    })

  }

  clearOldState() {
    const now = new Date()
    const twoHour = 2 * 60 * 60 * 1000
    for (let jwtToken of Object.keys(state)) {
      for (let levelName of Object.keys(state[jwtToken])) {
        const dateDiffInMilliSeconds = now - state[jwtToken][levelName]['updatedAt']
        console.log(dateDiffInMilliSeconds)
        console.log(twoHour)
        if (dateDiffInMilliSeconds < twoHour) {
          continue
        }

        delete state[jwtToken][levelName]
      }
    }
  }

  async sendStatSendCommand(jwtToken, nginx_headers, command) {
    await axios.post(
      'https://python_app:8001/python_app/v1/send-stat/',
      {
        'stat_event_type': 'send_command',
        'jwt_token': jwtToken,
        'extra_data': {
          'command': JSON.parse(JSON.stringify(command)),
        },
        'user_ip': nginx_headers['x-real-ip'],
        'user_agent': nginx_headers['user-agent'],
      },
      {
        httpsAgent: new https.Agent({
          rejectUnauthorized: false
        }),
      },
    )
  }
}
