import { Module } from '@nestjs/common';
import {GitModule} from "./git-module/git.module";
import {LevelsModuleModule} from "./levels-module/levels-module.module";
import { ServeStaticModule } from '@nestjs/serve-static';
import { join } from 'path';
import {PagesModule} from "./pages-module/pages.module";


const staticModule = ServeStaticModule.forRoot({
  rootPath: join(__dirname, '..', 'dist'),
  serveRoot: '/static',
})


@Module({
  imports: [
    GitModule,
    LevelsModuleModule,
    PagesModule,
    staticModule,
  ],
  controllers: [],
  providers: [],
})
export class AppModule {}
