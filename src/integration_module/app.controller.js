import { Bind, Body, Controller, Dependencies, Post } from '@nestjs/common';
import { AppService } from './app.service';


@Controller()
@Dependencies(AppService)
export class AppController {
  constructor(appService) {
    this.appService = appService;
  }

  @Post('send-command')
  @Bind(Body())
  sendCommand(sendCommandDto) {
    return this.appService.sendCommand(sendCommandDto)
  }
}
