import { Controller, Dependencies, Get } from '@nestjs/common';
import {GetLevelsModuleService} from "./get-levels-module.service";


@Controller()
@Dependencies(GetLevelsModuleService)
export class GetLevelsModuleController {
  constructor(getLevelsService) {
    this.getLevelsService = getLevelsService;
  }

  @Get('get-levels')
  getLevels() {
    return this.getLevelsService.getLevels()
  }
}
