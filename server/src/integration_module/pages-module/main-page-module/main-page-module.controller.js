import { Bind, Body, Controller, Dependencies, Get, Req, Res } from '@nestjs/common';
import {MainPageModuleService} from "./main-page-module.service";


@Controller()
@Dependencies(MainPageModuleService)
export class MainPageModuleController {
  constructor(mainPageModuleService) {
    this.mainPageModuleServcie = mainPageModuleService;
  }

  @Get('/')
  @Bind(Req(), Res())
  async resetLevel(request, response) {
    console.log(request.query)

    let res = await this.mainPageModuleServcie.getMainPage(request.query)
    res = res.replaceAll('build/', 'static/build/')

    response.send(res)
  }
}
