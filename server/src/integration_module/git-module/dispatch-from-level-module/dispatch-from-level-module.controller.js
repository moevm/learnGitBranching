import { Bind, Body, Controller, Dependencies, Post } from '@nestjs/common';
import {DispatchFromLevelModuleService} from "./dispatch-from-level-module.service";


@Controller()
@Dependencies(DispatchFromLevelModuleService)
export class DispatchFromLevelModuleController {
  constructor(dispatchFromLevelService) {
    this.dispatchFromLevelService = dispatchFromLevelService;
  }

  @Post('dispatch-from-level')
  @Bind(Body())
  resetLevel(dispatchFromLevelDto) {
    console.log(dispatchFromLevelDto)
    return this.dispatchFromLevelService.dispatchFromLevel(dispatchFromLevelDto)
  }
}
