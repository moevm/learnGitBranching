import { Module } from '@nestjs/common';
import {GitModule} from "./git-module/git.module";

@Module({
  imports: [GitModule],
  controllers: [],
  providers: [],
})
export class AppModule {}
