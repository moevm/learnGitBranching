import { Module } from '@nestjs/common';
import {SendCommandModuleService} from './send-command-module.service';
import { SendCommandModuleController } from './send-command-module.controller';

@Module({
  controllers: [SendCommandModuleController],
  providers: [SendCommandModuleService],
})
export class SendCommandModuleModule {}
