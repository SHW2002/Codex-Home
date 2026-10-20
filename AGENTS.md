# Global Agent Instructions

## 回答问题相关:

1. 思考和回答时都使用简体中文。
2. 对话中每句话的末尾都带一个“喵”，标题和英文部分除外。对于要写入的本地文件(文档等)除外.

## 代码编写相关:

1. 积极拆分代码，避免单个过长文件。单个文件超过200行即优先考虑通过代码复用来降低行数, 其次考虑拆分. 代码行数越长考虑该步骤的权重越大.
2. 把代码文件按文件夹分类. 单个文件夹内存在不同功能的代码时积极操作. 每次新建文件都做一次该评估.

## 提交规范:

1. commit message:
   1. 新特性用"feat: "开头
      - 对Unity项目: 如果本次提交的所有内容只在编辑器生效, 使用"feat-editor: "前缀
   2. 对已有功能的优化以"opt: "开头
   3. 对bug的修复用"fix: XXXX(问题描述表现的陈述句), 该问题已得到修复."这样的格式. 综合判断本次提交的内容以功能为主还是修复为主, 来决定选用哪种前缀.

2. commit message默认使用中文, 除非所贡献的项目之前都是英文.

## 项目规范:

- 对所有项目的README.md:
  1. 中英双语. 英语为默认版本(README.md), 中文命名为README_CN.md
  2. 在顶部标题下方提供切换中英文文档的超链接.
- 对所有.net(不含unity)项目:
  1. 添加如下打包机制: 每当执行dotnet publish, 将生成的文件夹压缩, 重命名为程序名-平台名(win/mac等)-包体类型(poartable等)-yymmdd-hhmmss, 存放至bin/Release-Archives/ 文件夹下.
  2. 所有源代码文件放入项目目录/src/文件夹下.
- 对所有Python项目:
  - 所有源代码文件放入项目目录/src/文件夹下.


## SSH 连接规范

- fairy 的 SSH 登录用户为 shw，默认使用 ssh shw@fairy（本机 SSH 配置已设置 User shw，也可直接 ssh fairy）。
- fairy 的应用部署目录为 /Users/shw/Documents/Applications，除非用户另有指定。
