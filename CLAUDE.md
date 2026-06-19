# leadpost-maker

把 newsletter 文章改写成 Facebook 引流帖的工作目录。

## 目录约定

- `input/`：放 newsletter 原文 `.md`
- `output/`：放改写后的 FB 帖 `.md`，文件名与 input 同名
- `.claude/skills/leadpost/`：工作流 Skill，编排「指派文章 → 改写 → 落盘」整条流程
- `.claude/skills/fb-maker/`：改写引擎 Skill，定义改写规则

## 两个 Skill 的分工

- **leadpost**（工作流）：负责流程编排——确定要处理的文章、调用改写、把成品写入 `output/<同名>.md`、回报并接收修改指令。
- **fb-maker**（引擎）：负责改写规则——三段式结构、三种标题、结尾 callback 句式轮换、改写原则。leadpost 第 2 步会读取并委托给它。

## 转换流程

1. 用户在 `input/<name>.md` 放入 newsletter 原文（或直接粘贴原文）
2. 调用 `/leadpost`（指明文件或说「转最新那篇」）触发整条流程
3. leadpost 委托 fb-maker 改写，输出「三个标题选项 + 完整帖子」
4. 改写完直接写入 `output/<name>.md`（不等确认），用户可继续提修改指令

改写规则见 `.claude/skills/fb-maker/SKILL.md`，流程编排见 `.claude/skills/leadpost/SKILL.md`。
