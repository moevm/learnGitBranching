import { Bind, Body, Controller, Dependencies, Post } from '@nestjs/common';
import {SendCommandModuleService} from './send-command-module.service';


@Controller()
@Dependencies(SendCommandModuleService)
export class SendCommandModuleController {
  constructor(sendCommandService) {
    this.sendCommandService = sendCommandService;
  }

  @Post('send-command')
  @Bind(Body())
  sendCommand(sendCommandDto) {
    return this.sendCommandService.sendCommand(sendCommandDto)
  }
}
