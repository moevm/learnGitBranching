import * as dotenv from 'dotenv'
import * as fs from "node:fs";
import * as path from "node:path";



export let env = null
fs.readFile(path.join(__dirname, '../../.env'), 'utf8', (err, data) => {
  if (err) {
    console.log(err)
  }

  env = dotenv.parse(data)
})
