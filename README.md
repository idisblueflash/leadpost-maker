# leadpost-maker

把 newsletter 文章改写成 Facebook 引流帖的工作目录，配套一个 Claude Code skill `fb-maker`。

## 目录结构

```
input/              newsletter 原文（.md）
output/             改写后的 FB 帖（.md，文件名与 input 同名）
fb-maker.skill      打包好的 skill 文件（zip）
CLAUDE.md           项目说明（Claude Code 自动加载）
```

## 安装 skill

把 `fb-maker.skill` 解压到 Claude Code 的 skills 目录：

```sh
unzip fb-maker.skill -d ~/.claude/skills/fb-maker
```

## 使用流程

1. 把 newsletter 原文放进 `input/<name>.md`
2. 在 Claude Code 里运行：

   ```
   /fb-maker @input/<name>.md
   ```

3. Skill 会输出三个标题选项 + 完整改写帖，并直接写入 `output/<name>.md`
4. 不满意可以直接指挥修改，比如「换读者处境型标题」「压缩到 200 字以内」

## 改写规则

帖子结构、标题类型、callback 句式轮换等细节，全部写在 skill 的 `SKILL.md` 里（安装后位于 `~/.claude/skills/fb-maker/SKILL.md`）。
