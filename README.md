# leadpost-maker

这是一个演示用的小项目，目的是展示怎么把自己写的文章（比如 newsletter）自动改写成适合发到 Facebook 的引流帖。

写文章和发社群其实是两件事。一篇适合放在 newsletter 里的长文，直接搬到 Facebook 上往往没人看完——开头不够抓人、节奏太慢、结尾没有引导。如果每发一篇都要手动重写一遍，太累。

这个项目把改写这件事固定成一个流程：放一篇文章进 `input/`，跑一下，`output/` 里就能拿到改写好的帖子，附带三个标题选项和一个引流到 newsletter 的结尾。

整套流程包成了 Claude Code 的一个 skill，叫 `fb-maker`。

---

## 怎么用

### 一、安装 skill

把 `fb-maker.skill` 解压到 Claude Code 的 skills 目录：

```sh
unzip fb-maker.skill -d ~/.claude/skills/fb-maker
```

### 二、跑一次改写

1. 把文章原文放进 `input/<name>.md`
2. 在 Claude Code 里运行：

   ```
   /fb-maker @input/<name>.md
   ```

3. Skill 会输出三个标题选项 + 完整改写帖，并直接写入 `output/<name>.md`
4. 不满意就直接说「换读者处境型标题」「压缩到 200 字以内」之类的，它会改

### 三、目录结构

```
input/              文章原文（.md）
output/             改写后的 FB 帖（.md，文件名与 input 同名）
fb-maker.skill      打包好的 skill 文件（zip）
CLAUDE.md           项目说明（Claude Code 自动加载）
```

### 四、改写规则在哪

帖子结构、三种标题类型、结尾 callback 的句式轮换这些规则，全部写在 skill 的 `SKILL.md` 里。安装完之后可以在 `~/.claude/skills/fb-maker/SKILL.md` 看到，想改规则直接改这个文件。
