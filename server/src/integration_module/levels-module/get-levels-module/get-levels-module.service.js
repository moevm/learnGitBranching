import { Injectable } from '@nestjs/common';
import { levelSequences, sequenceInfo } from '../../../levels';

@Injectable()
export class GetLevelsModuleService {

  async getLevels() {
    let sequences = JSON.parse(JSON.stringify(levelSequences))
    let info = JSON.parse(JSON.stringify(sequenceInfo))

    for (let sequence of Object.keys(sequences)) {
      for (let i = 0; i < sequences[sequence].length; i++) {
        let level = sequences[sequence][i]
        level.levelIndex = i
        level.levelType = sequence
      }
    }

    let res = {
      'levelSequences': sequences,
      'sequenceInfo': info,
    }

    return res
  }
}