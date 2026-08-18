const startTree = {
  branches: {
    main: {target: 'C3', id: 'main', remoteTrackingBranchID: 'o/main'},
    'o/main': {target: 'C3', id: 'o/main', remoteTrackingBranchID: null},
    Romanov_Petr_lb3: {
      target: 'C2',
      id: 'Romanov_Petr_lb3',
      remoteTrackingBranchID: 'o/Romanov_Petr_lb3',
    },
    'o/Romanov_Petr_lb3': {
      target: 'C2',
      id: 'o/Romanov_Petr_lb3',
      remoteTrackingBranchID: null,
    },
    '34Rhwsdfib': {target: 'C1', id: '34Rhwsdfib', remoteTrackingBranchID: null},
    'o/Smirnova_Anna_lb3': {
      target: 'C3',
      id: 'o/Smirnova_Anna_lb3',
      remoteTrackingBranchID: null,
    },
  },
  commits: {
    C0: {parents: [], id: 'C0', rootCommit: true},
    C1: {parents: ['C0'], id: 'C1'},
    C2: {parents: ['C1'], id: 'C2'},
    C3: {parents: ['C2'], id: 'C3'},
  },
  tags: {},
  HEAD: {target: 'main', id: 'HEAD'},
  virtualFileSystem: {
    cwd: '/',
    directories: [
      '/',
      '/Romanov_Petr_lb3',
      '/Romanov_Petr_lb3/src',
      '/Smirnova_Anna_lb3',
      '/Smirnova_Anna_lb3/src',
      '/old_lab',
    ],
    files: {
      '/Romanov_Petr_lb3/src/main.c': 'printf("Romanov lab");\n',
      '/Smirnova_Anna_lb3/src/main.c': 'printf("Smirnova lab");\n',
      '/old_lab/main.c': 'printf("old");\n',
    },
    stagedFiles: {},
    lastCommittedFiles: {
      '/Romanov_Petr_lb3/src/main.c': 'printf("Romanov lab");\n',
      '/Smirnova_Anna_lb3/src/main.c': 'printf("Smirnova lab");\n',
      '/old_lab/main.c': 'printf("old");\n',
    },
    lastCommittedCommit: null,
  },
  originTree: {
    branches: {
      main: {target: 'C4', id: 'main', remoteTrackingBranchID: null},
      Romanov_Petr_lb3: {
        target: 'C2',
        id: 'Romanov_Petr_lb3',
        remoteTrackingBranchID: null,
      },
      Smirnova_Anna_lb3: {
        target: 'C3',
        id: 'Smirnova_Anna_lb3',
        remoteTrackingBranchID: null,
      },
    },
    commits: {
      C0: {parents: [], id: 'C0', rootCommit: true},
      C1: {parents: ['C0'], id: 'C1'},
      C2: {parents: ['C1'], id: 'C2'},
      C3: {parents: ['C2'], id: 'C3'},
      C4: {parents: ['C3'], id: 'C4'},
    },
    tags: {},
    HEAD: {target: 'main', id: 'HEAD'},
  },
};

const goalTree = {
  branches: {
    main: {target: 'C4', id: 'main', remoteTrackingBranchID: 'o/main'},
    'o/main': {target: 'C4', id: 'o/main', remoteTrackingBranchID: null},
    Romanov_Petr_lb3: {
      target: 'C2',
      id: 'Romanov_Petr_lb3',
      remoteTrackingBranchID: 'o/Romanov_Petr_lb3',
    },
    'o/Romanov_Petr_lb3': {
      target: 'C2',
      id: 'o/Romanov_Petr_lb3',
      remoteTrackingBranchID: null,
    },
    '34Rhwsdfib': {target: 'C1', id: '34Rhwsdfib', remoteTrackingBranchID: null},
    'o/Smirnova_Anna_lb3': {
      target: 'C3',
      id: 'o/Smirnova_Anna_lb3',
      remoteTrackingBranchID: null,
    },
    '{{STUDENT_BRANCH}}': {
      target: 'C5',
      id: '{{STUDENT_BRANCH}}',
      remoteTrackingBranchID: 'o/{{STUDENT_BRANCH}}',
    },
    'o/{{STUDENT_BRANCH}}': {
      target: 'C5',
      id: 'o/{{STUDENT_BRANCH}}',
      remoteTrackingBranchID: null,
    },
  },
  commits: {
    C0: {parents: [], id: 'C0', rootCommit: true},
    C1: {parents: ['C0'], id: 'C1'},
    C2: {parents: ['C1'], id: 'C2'},
    C3: {parents: ['C2'], id: 'C3'},
    C4: {parents: ['C3'], id: 'C4'},
    C5: {parents: ['C4'], id: 'C5'},
  },
  tags: {},
  HEAD: {target: '{{STUDENT_BRANCH}}', id: 'HEAD'},
  originTree: {
    branches: {
      main: {target: 'C4', id: 'main', remoteTrackingBranchID: null},
      Romanov_Petr_lb3: {
        target: 'C2',
        id: 'Romanov_Petr_lb3',
        remoteTrackingBranchID: null,
      },
      Smirnova_Anna_lb3: {
        target: 'C3',
        id: 'Smirnova_Anna_lb3',
        remoteTrackingBranchID: null,
      },
      '{{STUDENT_BRANCH}}': {
        target: 'C5',
        id: '{{STUDENT_BRANCH}}',
        remoteTrackingBranchID: null,
      },
    },
    commits: {
      C0: {parents: [], id: 'C0', rootCommit: true},
      C1: {parents: ['C0'], id: 'C1'},
      C2: {parents: ['C1'], id: 'C2'},
      C3: {parents: ['C2'], id: 'C3'},
      C4: {parents: ['C3'], id: 'C4'},
      C5: {parents: ['C4'], id: 'C5'},
    },
    tags: {},
    HEAD: {target: 'main', id: 'HEAD'},
  },
};

const instructions = {
  childViews: [
    {
      type: 'ModalAlert',
      options: {
        markdowns: [
          '## Загрузка лабораторной работы в общий репозиторий',
          '',
          'В репозитории уже есть ветки и каталоги других студентов. Локальная ветка `main` отстаёт от `origin/main` на один коммит.',
          '',
          '> Перед началом работы получите актуальное состояние ветки `main`.',
          '',
          '> Создайте отдельную ветку `{{STUDENT_BRANCH}}` от обновлённой `main`. Ветка `main` не должна содержать коммит вашей лабораторной.',
          '',
          '> Создайте каталог `{{STUDENT_DIR}}/src` и файл `{{STUDENT_DIR}}/src/main.c`.',
          '',
          '> В файл одной командой `echo` запишите строку `{{FULL_NAME}}, группа <ваша группа>`.',
          '',
          '> Добавьте файл в staging area, создайте коммит с сообщением `{{STUDENT_DIR}}: lab 3` и отправьте свою ветку в `origin`.',
        ],
      },
    },
    {
      type: 'ModalAlert',
      options: {
        markdowns: [
          '## Команды виртуальной файловой системы',
          '',
          'В этом задании файловая система учебная: команды не выполняются на сервере и не создают настоящие файлы.',
          '',
          '- `ls` — показать содержимое текущего каталога;',
          '- `pwd` — показать текущий каталог;',
          '- `mkdir ИМЯ` — создать один каталог;',
          '- `cd ПУТЬ` — перейти в каталог; поддерживаются `..` и относительные пути;',
          '- `echo "ТЕКСТ" >> ПУТЬ` — создать файл или дописать в него строку;',
          '- `git add ПУТЬ` или `git add .` — добавить виртуальные файлы в staging area.',
          '',
          'Проверяется не список введённых команд, а итог: основание ветки, точные имена ветки и файла, содержимое `main.c`, staging, сообщение коммита и наличие ветки в `origin`.',
        ],
      },
    },
  ],
};

exports.level = {
  name: {
    en_US: 'Lab 3 submission',
    ru_RU: 'Загрузка лабораторной работы № 3',
  },
  startTree: JSON.stringify(startTree),
  goalTreeString: JSON.stringify(goalTree),
  solutionCommand: [
    'git pull origin main',
    'git checkout -b {{STUDENT_BRANCH}}',
    'mkdir {{STUDENT_DIR}}',
    'cd {{STUDENT_DIR}}',
    'mkdir src',
    'cd src',
    'echo "{{FULL_NAME}}, группа ИКТ-301" >> main.c',
    'git add main.c',
    'git commit -m "{{STUDENT_DIR}}: lab 3"',
    'git push origin {{STUDENT_BRANCH}}',
  ].join(';'),
  hint: {
    en_US: 'Use `objective` to reopen the assignment requirements.',
    ru_RU: 'Введите `objective`, чтобы снова открыть требования. Для самопроверки доступны `pwd` и `ls`.',
  },
  startDialog: {
    en_US: instructions,
    ru_RU: instructions,
  },
  virtualFileSystemGoal: {
    branchName: '{{STUDENT_BRANCH}}',
    baseCommit: 'C4',
    filePath: '/{{STUDENT_DIR}}/src/main.c',
    fullName: '{{FULL_NAME}}',
    commitMessage: '{{STUDENT_DIR}}: lab 3',
  },
};
