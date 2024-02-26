import { Module } from '@nestjs/common';
import {GetLevelsModuleController} from "./get-levels-module.controller";
import {GetLevelsModuleService} from "./get-levels-module.service";

@Module({
  controllers: [GetLevelsModuleController],
  providers: [GetLevelsModuleService],
})
export class GetLevelsModuleModule {}
