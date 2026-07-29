# Claude 全局 Skills 层（跨 harness 单一真值）

本仓库是 Claude Code 与 Codex 共用的全局 skill 层，两处 clone，一份真值：

| Harness | 位置 | 说明 |
|---|---|---|
| Claude Code | `~/.claude/skills/` | clone 本仓库 |
| Codex | `~/.codex/skills/` | clone 本仓库 + 少量 Codex 专属未跟踪目录（shadcn / design-md-manager / pomelox-deploy-*，见各自 `.git/info/exclude`） |

## 新机器恢复

```bash
git clone https://github.com/Stevenjxie/claude-global-skills.git ~/.claude/skills
git clone https://github.com/Stevenjxie/claude-global-skills.git ~/.codex/skills
```

## 日常同步

在任意一侧改完：

```bash
cd ~/.claude/skills   # 或 ~/.codex/skills
git add -A && git commit -m "..." && git push
# 另一侧
git pull
```

## `_tools/` — 非 skill 资产

`_tools/` 里放的**不是 skill**(没有 `SKILL.md`,不会被 skill 扫描加载),只是需要跨机器同步的小脚本。放这里纯粹因为本仓库是现成的双机同步通道。

| 文件 | 用途 |
|---|---|
| `_tools/statusline-ctx.js` | Claude Code 状态栏 + 上下文/套餐额度基线采集器。显示模型/上下文进度条/5h·7d 额度/成本,并把采样追加到 `~/.claude/context-handoff/baseline.jsonl`。本地运行,不消耗 API token,不改变任何会话行为。 |

启用方式(每台机器各配一次,`~/.claude/settings.json` 顶层加一个键):

```jsonc
"statusLine": {
  "type": "command",
  "command": "node ~/.claude/skills/_tools/statusline-ctx.js",
  "refreshInterval": 60
}
```

Windows 上若 `~` 不展开导致状态栏不出现,改成绝对路径 `node C:/Users/<用户名>/.claude/skills/_tools/statusline-ctx.js`。

采样数据是**每台机器各存各的**(写在本机 `~/.claude/context-handoff/`),分析时需合并;`rate_limits` 是账号级滚动窗口,含 claude.ai 网页端与 Cowork 的消耗。

停用:删掉 `settings.json` 的 `statusLine` 键即可,无残留。

## 入口

设计类工作统一从 `design/`（路由枢纽 v2）进入，它分流到 taste / impeccable / gsap-* / promax-design / ai-interface-design / react-native-best-practices 等。项目专属 skill（如 Cretas 的 ux-flow、e2e）留在各项目 `.claude/skills/`，不进本仓库。

**最后更新**: 2026-07-29
