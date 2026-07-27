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

## 入口

设计类工作统一从 `design/`（路由枢纽 v2）进入，它分流到 taste / impeccable / gsap-* / promax-design / ai-interface-design / react-native-best-practices 等。项目专属 skill（如 Cretas 的 ux-flow、e2e）留在各项目 `.claude/skills/`，不进本仓库。

**最后更新**: 2026-07-28
