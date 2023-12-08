import { Module } from '@nestjs/common';
import {SendCommandModuleModule} from "./send-command-module/send-command-module.module";
import {ResetLevelModuleModule} from "./reset-level-module/reset-level-module.module";

@Module({
  imports: [ResetLevelModuleModule, SendCommandModuleModule],
  controllers: [],
  providers: [],
})
export class GitModule {}
