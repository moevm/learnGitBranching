import { Module } from '@nestjs/common';
import {DispatchFromLevelModuleService} from './dispatch-from-level-module.service';
import {DispatchFromLevelModuleController} from "./dispatch-from-level-module.controller";

@Module({
  controllers: [DispatchFromLevelModuleController],
  providers: [DispatchFromLevelModuleService],
})
export class DispatchFromLevelModuleModule {}
