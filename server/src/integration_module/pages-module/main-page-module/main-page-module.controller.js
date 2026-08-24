import { Bind, Controller, Dependencies, Get, Req, Res } from '@nestjs/common';
import { MainPageModuleService } from './main-page-module.service';
import * as jwt from 'jsonwebtoken';
import * as axios from 'axios';

const INTRO_PAGE = `
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <title>Learn Git Branching</title>

  <style>
    * {
      box-sizing: border-box;
    }

    body {
      margin: 0;
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 24px;
      background: #202124;
      color: #ffffff;
      font-family: Arial, sans-serif;
    }

    .card {
      width: 100%;
      max-width: 680px;
      padding: 48px;
      border-radius: 16px;
      background: #303134;
      box-shadow: 0 12px 40px rgba(0, 0, 0, 0.35);
      text-align: center;
    }

    h1 {
      margin: 0 0 20px;
      color: #a6ff4d;
      font-size: 38px;
    }

    p {
      margin: 12px 0;
      color: #e8eaed;
      font-size: 18px;
      line-height: 1.6;
    }

    .status {
      display: inline-block;
      margin-top: 24px;
      padding: 10px 18px;
      border-radius: 20px;
      background: #214d25;
      color: #a6ff4d;
      font-weight: bold;
    }
  </style>
</head>

<body>
  <main class="card">
    <h1>Learn Git Branching</h1>

    <p>Интерактивный учебный инструмент для изучения Git.</p>

    <p>
      Доступ к лабораторным заданиям осуществляется через соответствующий
      элемент курса в LMS Moodle.
    </p>

    <p>
      Для начала работы откройте назначенное преподавателем задание в Moodle.
    </p>

    <div class="status">Сервис запущен</div>
  </main>
</body>
</html>
`;

@Controller()
@Dependencies(MainPageModuleService)
export class MainPageModuleController {
  constructor(mainPageModuleService) {
    this.mainPageModuleServcie = mainPageModuleService;
  }

  @Get('/intro')
  @Bind(Res())
  intro(response) {
    response.status(200).type('html').send(INTRO_PAGE);
  }

  @Get('/')
  @Bind(Req(), Res())
  async mainPage(request, response) {
    const jwtToken = request.cookies[process.env.JWT_COOKIE_NAME];

    if (!jwtToken) {
      return response.status(200).type('html').send(INTRO_PAGE);
    }

    let decoded;

    try {
      decoded = jwt.verify(jwtToken, process.env.JWT_SECRET);
    } catch (error) {
      response.clearCookie(process.env.JWT_COOKIE_NAME);
      return response.status(200).type('html').send(INTRO_PAGE);
    }

    const taskId = decoded[process.env.JWT_TASK_ID_PARAM_NAME || 'task_id'];

    let page = await this.mainPageModuleServcie.getMainPage({
      level_id: taskId,
    });

    page = page.replaceAll('build/', 'static/build/');

    response.send(page);

    await this.sendStatOpenPage(jwtToken, request.headers, taskId);
  }

  async sendStatOpenPage(jwtToken, nginxHeaders, taskId) {
    await axios.post(
      'http://lti_service/v1/send-stat/',
      {
        stat_event_type: 'open_page',
        jwt_token: jwtToken,
        extra_data: {
          task_id: taskId,
        },
        user_ip: nginxHeaders['x-real-ip'],
        user_agent: nginxHeaders['user-agent'],
      },
    );
  }
}
