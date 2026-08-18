import {Bind, Body, Controller, Dependencies, Post, Req} from '@nestjs/common';
import {DispatchFromLevelModuleService} from "./dispatch-from-level-module.service";
import {env} from "../../env";
import * as jwt from "jsonwebtoken";
import {buildStudentProfile} from "../../student-profile";


@Controller()
@Dependencies(DispatchFromLevelModuleService)
export class DispatchFromLevelModuleController {
  constructor(dispatchFromLevelService) {
    this.dispatchFromLevelService = dispatchFromLevelService;
  }

  @Post('dispatch-from-level')
  @Bind(Req(), Body())
  resetLevel(request, dispatchFromLevelDto) {
    const jwt_token = request.cookies[process.env.JWT_COOKIE_NAME]
    const decoded = jwt.verify(jwt_token, process.env.JWT_SECRET)
    const task_id = decoded['task_id']
    const authenticatedUserId = String(decoded[process.env.JWT_USER_ID_PARAM_NAME])
    const loadedUserId = String(dispatchFromLevelDto.userId || '')

    // LTI authentication is stored in one cookie for the application domain.
    // Opening another Moodle user in the same browser replaces that cookie.
    // Do not replay commands from an already-open level under the new user.
    if (loadedUserId && loadedUserId !== authenticatedUserId) {
      return {
        levelComplete: false,
        sessionMismatch: true,
      }
    }

    const levelNumber = task_id.match(/\d+/g)[0]
    const levelType = task_id.match(/[a-zA-Z]+/g)[0]
    const headers = request.headers

    dispatchFromLevelDto.levelIndex = levelNumber
    dispatchFromLevelDto.levelType = levelType
    dispatchFromLevelDto.userId = authenticatedUserId
    dispatchFromLevelDto.studentProfile = buildStudentProfile(decoded)
    dispatchFromLevelDto.jwtToken = jwt_token
    dispatchFromLevelDto.headers = headers

    return this.dispatchFromLevelService.dispatchFromLevel(dispatchFromLevelDto)
  }
}
