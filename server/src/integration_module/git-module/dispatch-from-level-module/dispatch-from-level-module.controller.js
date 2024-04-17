import {Bind, Body, Controller, Dependencies, Post, Req} from '@nestjs/common';
import {DispatchFromLevelModuleService} from "./dispatch-from-level-module.service";
import {env} from "../../env";
import * as jwt from "jsonwebtoken";


@Controller()
@Dependencies(DispatchFromLevelModuleService)
export class DispatchFromLevelModuleController {
  constructor(dispatchFromLevelService) {
    this.dispatchFromLevelService = dispatchFromLevelService;
  }

  @Post('dispatch-from-level')
  @Bind(Req(), Body())
  resetLevel(request, dispatchFromLevelDto) {
    const jwt_token = request.cookies[env.JWT_COOKIE_NAME]
    const decoded = jwt.verify(jwt_token, env.JWT_SECRET)
    const task_id = decoded[env.JWT_TASK_ID_PARAM_NAME]
    const levelNumber = task_id.match(/\d+/g)[0]
    const levelType = task_id.match(/[a-zA-Z]+/g)[0]

    dispatchFromLevelDto.levelIndex = levelNumber
    dispatchFromLevelDto.levelType = levelType
    dispatchFromLevelDto.userId = decoded[env.JWT_USER_ID_PARAM_NAME]
    dispatchFromLevelDto.jwtToken = jwt_token

    return this.dispatchFromLevelService.dispatchFromLevel(dispatchFromLevelDto)
  }
}
