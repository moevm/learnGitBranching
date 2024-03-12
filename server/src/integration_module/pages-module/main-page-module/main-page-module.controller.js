import { Bind, Body, Controller, Dependencies, Get, Req, Res } from '@nestjs/common';
import {MainPageModuleService} from "./main-page-module.service";
import {env} from "../../env";
import * as jwt from "jsonwebtoken";


@Controller()
@Dependencies(MainPageModuleService)
export class MainPageModuleController {
  constructor(mainPageModuleService) {
    this.mainPageModuleServcie = mainPageModuleService;
  }

  @Get('/')
  @Bind(Req(), Res())
  async resetLevel(request, response) {
    console.log(request.cookies)
    const jwt_token = request.cookies[env.JWT_COOKIE_NAME]
    const decoded = jwt.verify(jwt_token, env.JWT_SECRET)
    const task_id = decoded[env.JWT_TASK_ID_PARAM_NAME]
    console.log(task_id)
    let res = await this.mainPageModuleServcie.getMainPage({'level_id': task_id})
    res = res.replaceAll('build/', 'static/build/')

    response.send(res)
  }
}
