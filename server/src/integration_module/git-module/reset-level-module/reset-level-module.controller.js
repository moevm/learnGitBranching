import { Bind, Body, Controller, Dependencies, Post } from '@nestjs/common';
import {ResetLevelModuleService} from './reset-level-module.service';


@Controller()
@Dependencies(ResetLevelModuleService)
export class ResetLevelModuleController {
  constructor(resetLevelService) {
    this.resetLevelService = resetLevelService;
  }

  @Post('reset-level')
  @Bind(Body())
  resetLevel(resetLevelDto) {
    return this.resetLevelService.resetLevel(resetLevelDto)
  }
}
