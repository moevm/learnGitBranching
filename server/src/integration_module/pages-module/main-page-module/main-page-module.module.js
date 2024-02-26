import { Module } from '@nestjs/common';
import {MainPageModuleController} from "./main-page-module.controller";
import {MainPageModuleService} from "./main-page-module.service";

@Module({
  controllers: [MainPageModuleController],
  providers: [MainPageModuleService],
})
export class MainPageModuleModule {}
