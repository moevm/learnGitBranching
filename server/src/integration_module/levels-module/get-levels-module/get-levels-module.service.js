import { Injectable } from '@nestjs/common';
import { levelSequences, sequenceInfo } from '../../../levels';
import LevelStore from "../../../js/stores/LevelStore";
import {personalizeLevel} from "../../student-profile";

@Injectable()
export class GetLevelsModuleService {
  async getLevels(level_id, is_success, studentProfile) {
    const level = personalizeLevel(LevelStore.getLevel(level_id), studentProfile)
    const levelNumber = level_id.match(/\d+/g)[0]
    const levelType = level_id.match(/[a-zA-Z]+/g)[0]

    const jsonLevel = JSON.parse(JSON.stringify(level))
    const toAnalyze = jsonLevel.solutionCommand.replace(/^;|;$/g, '')

    jsonLevel.best = toAnalyze.split(';').length
    jsonLevel.levelIndex = levelNumber
    jsonLevel.levelType = levelType
    jsonLevel.isSuccess = is_success
    // The browser sends this value back with every command. It lets the
    // server detect when another Moodle launch in the same browser has
    // replaced the shared LTI cookie with a different user's session.
    jsonLevel.studentUserId = studentProfile.userId

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
