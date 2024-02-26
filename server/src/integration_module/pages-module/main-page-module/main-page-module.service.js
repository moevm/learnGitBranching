import {Injectable, HttpException, NotFoundException, StreamableFile} from '@nestjs/common';
import { readFileSync } from 'fs'
import * as path from "node:path";

@Injectable()
export class MainPageModuleService {

  async getMainPage(mainPageDto) {
    if (!mainPageDto.level_id) {
      throw new NotFoundException()
    }

    const filename = path.resolve(process.cwd(), 'src/dist/index.html');
    // console.log(readFileSync(filename, 'utf8'))
    return readFileSync(filename, 'utf8');
  }
}
