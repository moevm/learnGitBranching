import {Bind, Controller, Dependencies, Get, Req} from '@nestjs/common';
import {GetLevelsModuleService} from "./get-levels-module.service";
import {env} from "../../env";
import * as jwt from 'jsonwebtoken'


@Controller()
@Dependencies(GetLevelsModuleService)
export class GetLevelsModuleController {
  constructor(getLevelsService) {
    this.getLevelsService = getLevelsService;
  }

  @Get('get-levels')
  @Bind(Req())
  getLevels(request) {
    const jwt_token = request.cookies[process.env.JWT_COOKIE_NAME]
    const decoded = jwt.verify(jwt_token, process.env.JWT_SECRET)

    const task_id = decoded['task_id']
    const is_success = decoded[process.env.JWT_IS_SUCCESS_PARAM_NAME]

    return this.getLevelsService.getLevels(task_id, is_success)
  }
}
