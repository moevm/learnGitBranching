import { Injectable } from '@nestjs/common';
import { levelSequences } from '../../../levels';
import {levelsState} from "../git.service";


@Injectable()
export class ResetLevelModuleService {

  async resetLevel(resetLevelDto) {
    const level = levelSequences[resetLevelDto.levelType][resetLevelDto.levelIndex]

    if (!('levelType' in resetLevelDto)) {
      return {'result': 'error', 'message': 'levelType is required'}
    }
    if (!('levelIndex' in resetLevelDto)) {
      return {'result': 'error', 'message': 'levelIndex is required'}
    }

    if (resetLevelDto?.levelType in levelSequences && resetLevelDto?.levelIndex in levelSequences[resetLevelDto.levelType]) {
      levelsState[level.name.en_US] = null
    }

    return {'result': 'success', 'message': 'level reset'}
  }
}
