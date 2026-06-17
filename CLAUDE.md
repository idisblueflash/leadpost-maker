# leadpost-maker

把 newsletter 文章改写成 Facebook 引流帖的工作目录。

## 目录约定

- `input/`：放 newsletter 原文 `.md`
- `output/`：放改写后的 FB 帖 `.md`，文件名与 input 同名
- `fb-maker.skill`：打包好的 Skill 文件（已安装到 `~/.claude/skills/fb-maker/`）

## 转换流程

1. 用户在 `input/<name>.md` 放入 newsletter 原文
2. 调用 `/fb-maker @input/<name>.md` 触发改写
3. Skill 输出「改写帖子 + 三个标题选项」
4. 用户确认或要求修改后，把最终结果写到 `output/<name>.md`

改写规则见 `~/.claude/skills/fb-maker/SKILL.md`。
