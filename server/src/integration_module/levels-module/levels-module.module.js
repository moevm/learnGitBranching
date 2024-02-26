import { Module } from '@nestjs/common';
import {GetLevelsModuleModule} from "./get-levels-module/get-levels-module.module";


@Module({
  imports: [GetLevelsModuleModule],
})
export class LevelsModuleModule {}
