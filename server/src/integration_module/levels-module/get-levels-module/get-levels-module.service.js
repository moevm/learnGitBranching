import { Injectable } from '@nestjs/common';
import { levelSequences, sequenceInfo } from '../../../levels';
import LevelStore from "../../../js/stores/LevelStore";

@Injectable()
export class GetLevelsModuleService {
  async getLevels(level_id, is_success) {
    const level = LevelStore.getLevel(level_id)
    const levelNumber = level_id.match(/\d+/g)[0]
    const levelType = level_id.match(/[a-zA-Z]+/g)[0]

    const jsonLevel = JSON.parse(JSON.stringify(level))
    const toAnalyze = jsonLevel.solutionCommand.replace(/^;|;$/g, '')

    jsonLevel.best = toAnalyze.split(';').length
    jsonLevel.levelIndex = levelNumber
    jsonLevel.levelType = levelType
    jsonLevel.isSuccess = is_success

    // delete jsonLevel.goalTreeString
    delete jsonLevel.solutionCommand

    let res = {
      'levelSequences': {},
      'sequenceInfo': {}
    }

    res['levelSequences']['intro'] = [jsonLevel]

    let info = JSON.parse(JSON.stringify(sequenceInfo))
    console.log(levelType)
    console.log(levelNumber)

    res['sequenceInfo']['intro'] = info[levelType]

    return res
  }
}