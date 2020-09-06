# Cishe

**Client Information System for HelloEdu.**

<div>
  <a href="https://github.com/ace-han/cishe/actions?query=workflow%3ACI">
    <img src="https://img.shields.io/github/workflow/status/ace-han/cishe/CI/master?logo=github" alt="GitHub Workflow Status (branch)">
  </a>
  <a href="https://codecov.io/gh/ace-han/cishe">
    <img src="https://img.shields.io/codecov/c/gh/ace-han/cishe?logo=codecov" alt="Coverage">
  </a>
  <a href="https://github.com/python/black">
    <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black">
  </a>
</div>

# Database setup

```shell

CREATE USER `cishe`@`localhost` IDENTIFIED BY 'cishe';
# for regular db use
CREATE DATABASE `cishe` CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
GRANT ALL ON `cishe`.* TO `cishe`@`localhost`;
# for test db use
CREATE DATABASE `test_cishe` CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
GRANT ALL ON `test_cishe`.* TO `cishe`@`localhost`;

FLUSH PRIVILEGES;
```
