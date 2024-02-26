import { Module } from '@nestjs/common';
import {ResetLevelModuleService} from './reset-level-module.service';
import { ResetLevelModuleController } from './reset-level-module.controller';

@Module({
  controllers: [ResetLevelModuleController],
  providers: [ResetLevelModuleService],
})
export class ResetLevelModuleModule {}
