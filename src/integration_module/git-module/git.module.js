import { Module } from '@nestjs/common';
import {SendCommandModuleModule} from "./send-command-module/send-command-module.module";

@Module({
  imports: [SendCommandModuleModule],
  controllers: [],
  providers: [],
})
export class GitModule {}
