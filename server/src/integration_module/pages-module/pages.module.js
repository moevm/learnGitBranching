import { Module } from '@nestjs/common';
import {MainPageModuleModule} from "./main-page-module/main-page-module.module";

@Module({
  imports: [MainPageModuleModule],
  controllers: [],
  providers: [],
})
export class PagesModule {}
