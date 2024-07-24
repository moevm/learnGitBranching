import { Bind, Body, Controller, Dependencies, Get, Req, Res } from '@nestjs/common';
import {MainPageModuleService} from "./main-page-module.service";
import {env} from "../../env";
import * as jwt from "jsonwebtoken";
import * as axios from "axios";
import https from "node:https";


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
    const jwt_token = request.cookies[process.env.JWT_COOKIE_NAME]
    const decoded = jwt.verify(jwt_token, process.env.JWT_SECRET)
    const task_id = decoded[process.env.JWT_TASK_ID_PARAM_NAME]
    console.log(task_id)
    let res = await this.mainPageModuleServcie.getMainPage({'level_id': task_id})
    res = res.replaceAll('build/', 'static/build/')

    response.send(res)

    await this.sendStatOpenPage(jwt_token, request.headers, task_id)
  }

  async sendStatOpenPage(jwtToken, nginx_headers, taskId) {
    await axios.post(
      'http://lti_service/v1/send-stat/',
      {
        'stat_event_type': 'open_page',
        'jwt_token': jwtToken,
        'extra_data': {
          'task_id': taskId,
        },
        'user_ip': nginx_headers['x-real-ip'],
        'user_agent': nginx_headers['user-agent'],
      },
    )
  }
}
