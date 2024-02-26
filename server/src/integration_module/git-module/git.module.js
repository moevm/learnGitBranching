import { Module } from '@nestjs/common';
import {SendCommandModuleModule} from "./send-command-module/send-command-module.module";
import {ResetLevelModuleModule} from "./reset-level-module/reset-level-module.module";
import {DispatchFromLevelModuleModule} from "./dispatch-from-level-module/dispatch-from-level-module.module";

@Module({
  imports: [ResetLevelModuleModule, SendCommandModuleModule, DispatchFromLevelModuleModule],
  controllers: [],
  providers: [],
})
export class GitModule {}
