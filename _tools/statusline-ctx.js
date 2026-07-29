#!/usr/bin/env node
/**
 * statusline-ctx.js — 只读上下文/额度基线采集器 + 状态栏渲染
 *
 * 装它的唯一目的: 采集 rate_limits 与上下文体积的时间序列, 用于回答
 * "长 session 到底烧掉多少套餐额度" —— 这个数据本机此前从未被记录过。
 *
 * 它不改变任何会话行为: 不 block、不注入上下文、不触发 compact、不建 session。
 * statusLine 在本地运行, 官方明确 "does not consume API tokens"。
 *
 * 失败策略: 全程 fail-silent。解析不了就打印空行, 采样出错不影响渲染。
 *
 * 产物:
 *   ~/.claude/context-handoff/baseline.jsonl        追加式采样记录
 *   ~/.claude/context-handoff/<session_id>.json     上次采样标记(去重用)
 *
 * 卸载: 删 settings.json 的 "statusLine" 键即可, 无残留影响。
 */

'use strict';

const fs = require('fs');
const os = require('os');
const path = require('path');

const DIR = path.join(os.homedir(), '.claude', 'context-handoff');
const BASELINE = path.join(DIR, 'baseline.jsonl');
const SAMPLE_MIN_INTERVAL_MS = 120000; // 无变化时最多每 2 分钟记一条

// ---------- stdin ----------
let buf = '';
process.stdin.setEncoding('utf8');
process.stdin.on('data', (d) => { buf += d; });
process.stdin.on('end', () => {
  let s;
  try { s = JSON.parse(buf); } catch { process.stdout.write(''); return; }
  let line;
  try { line = render(s); } catch { line = ''; }
  process.stdout.write(line);
  try { sample(s); } catch { /* 采样失败绝不影响状态栏 */ }
});

// ---------- 派生量 ----------
function derive(s) {
  const cw = s.context_window || {};
  const cu = cw.current_usage || null;
  const windowSize = cw.context_window_size || null;

  // 官方公式: used_percentage 只算输入侧三项, 不含 output
  const usedTokens = cu
    ? (cu.input_tokens || 0) + (cu.cache_creation_input_tokens || 0) + (cu.cache_read_input_tokens || 0)
    : null;

  // 优先用官方预计算值; 它为 null 时(会话早期 / compact 直后)才自算
  const usedPct = (typeof cw.used_percentage === 'number')
    ? cw.used_percentage
    : (usedTokens != null && windowSize ? (usedTokens / windowSize) * 100 : null);

  const rl = s.rate_limits || {};
  return {
    windowSize,
    usedTokens,
    usedPct,
    cur: cu,
    rl5: (rl.five_hour && typeof rl.five_hour.used_percentage === 'number') ? rl.five_hour.used_percentage : null,
    rl7: (rl.seven_day && typeof rl.seven_day.used_percentage === 'number') ? rl.seven_day.used_percentage : null,
    rl5Reset: (rl.five_hour && rl.five_hour.resets_at) || null,
    rl7Reset: (rl.seven_day && rl.seven_day.resets_at) || null,
  };
}

// ---------- 渲染 ----------
const RESET = '[0m';
const DIM = '[2m';
const GREEN = '[32m';
const YELLOW = '[33m';
const RED = '[31m';

function heat(pct) {
  if (pct == null) return DIM;
  if (pct >= 85) return RED;
  if (pct >= 60) return YELLOW;
  return GREEN;
}

function bar(pct, width) {
  if (pct == null) return DIM + '·'.repeat(width) + RESET;
  const filled = Math.max(0, Math.min(width, Math.round((pct / 100) * width)));
  return heat(pct) + '▓'.repeat(filled) + RESET + DIM + '░'.repeat(width - filled) + RESET;
}

function human(n) {
  if (n == null) return '?';
  if (n >= 1000000) return (n / 1000000).toFixed(2).replace(/\.?0+$/, '') + 'M';
  if (n >= 1000) return Math.round(n / 1000) + 'k';
  return String(n);
}

function hms(ms) {
  if (!ms) return null;
  const m = Math.floor(ms / 60000);
  return m >= 60 ? `${Math.floor(m / 60)}h${String(m % 60).padStart(2, '0')}m` : `${m}m`;
}

function render(s) {
  const d = derive(s);
  const parts1 = [];

  const model = (s.model && s.model.display_name) || '?';
  // display_name 可能已含窗口信息(如 "Opus 5 (1M context)"), 避免重复
  const winRedundant = /\b1m\b|context/i.test(model);
  const win = winRedundant ? '' : (d.windowSize === 1000000 ? '1M' : d.windowSize ? human(d.windowSize) : '');
  const effort = (s.effort && s.effort.level) || null;
  parts1.push(`${DIM}${model}${win ? ' ' + win : ''}${effort ? ' · ' + effort : ''}${RESET}`);

  const pctTxt = d.usedPct == null ? ' -- ' : `${String(Math.floor(d.usedPct)).padStart(2)}%`;
  parts1.push(`${bar(d.usedPct, 10)} ${heat(d.usedPct)}${pctTxt}${RESET}` +
    (d.usedTokens != null ? ` ${DIM}${human(d.usedTokens)}${RESET}` : ''));

  const parts2 = [];
  if (d.rl5 != null) parts2.push(`${DIM}5h${RESET} ${heat(d.rl5)}${d.rl5.toFixed(0)}%${RESET}`);
  if (d.rl7 != null) parts2.push(`${DIM}7d${RESET} ${heat(d.rl7)}${d.rl7.toFixed(0)}%${RESET}`);
  if (d.rl5 == null && d.rl7 == null) parts2.push(`${DIM}额度 --${RESET}`);

  const cost = s.cost || {};
  if (typeof cost.total_cost_usd === 'number') parts2.push(`${DIM}$${cost.total_cost_usd.toFixed(2)}${RESET}`);
  const dur = hms(cost.total_duration_ms);
  if (dur) parts2.push(`${DIM}${dur}${RESET}`);

  return parts1.join('  ') + '\n' + parts2.join(` ${DIM}·${RESET} `);
}

// ---------- 采样 ----------
function statePath(sid) {
  return path.join(DIR, String(sid).replace(/[^A-Za-z0-9_-]/g, '_') + '.json');
}

function sample(s) {
  const sid = s.session_id;
  if (!sid) return;
  const d = derive(s);

  // 没有任何可采的量就别写
  if (d.usedTokens == null && d.rl5 == null && d.rl7 == null) return;

  fs.mkdirSync(DIR, { recursive: true });

  const sp = statePath(sid);
  let prev = null;
  try { prev = JSON.parse(fs.readFileSync(sp, 'utf8')); } catch { /* 首次 */ }

  const now = Date.now();
  const rlChanged = prev && (prev.rl5 !== d.rl5 || prev.rl7 !== d.rl7);
  const elapsed = prev ? now - prev.ts : Infinity;
  if (prev && !rlChanged && elapsed < SAMPLE_MIN_INTERVAL_MS) return;

  // 上下文体积相对上次骤降 >50% ⇒ 极可能刚发生 compaction。
  // statusLine 拿不到 compact 事件, 这是纯观测推断, 仅供事后分析, 不驱动任何行为。
  const ctxDrop = !!(prev && prev.usedTokens && d.usedTokens != null &&
    d.usedTokens < prev.usedTokens * 0.5);

  const cost = s.cost || {};
  const rec = {
    ts: now,
    iso: new Date(now).toISOString(),
    session_id: sid,
    version: s.version || null,
    model_id: (s.model && s.model.id) || null,
    effort: (s.effort && s.effort.level) || null,
    window_size: d.windowSize,
    used_tokens: d.usedTokens,
    used_pct: d.usedPct == null ? null : Number(d.usedPct.toFixed(2)),
    input_tokens: d.cur ? d.cur.input_tokens : null,
    cache_creation_input_tokens: d.cur ? d.cur.cache_creation_input_tokens : null,
    cache_read_input_tokens: d.cur ? d.cur.cache_read_input_tokens : null,
    output_tokens: d.cur ? d.cur.output_tokens : null,
    rl_5h_pct: d.rl5,
    rl_7d_pct: d.rl7,
    rl_5h_resets_at: d.rl5Reset,
    rl_7d_resets_at: d.rl7Reset,
    cost_usd: typeof cost.total_cost_usd === 'number' ? cost.total_cost_usd : null,
    duration_ms: cost.total_duration_ms || null,
    api_duration_ms: cost.total_api_duration_ms || null,
    lines_added: cost.total_lines_added || null,
    lines_removed: cost.total_lines_removed || null,
    ctx_drop: ctxDrop,
    cwd: s.cwd || null,
  };

  fs.appendFileSync(BASELINE, JSON.stringify(rec) + '\n', 'utf8');

  // 状态标记原子替换 —— statusLine 脚本随时可能被新触发腰斩
  const tmp = sp + '.' + process.pid + '.tmp';
  fs.writeFileSync(tmp, JSON.stringify({
    ts: now, rl5: d.rl5, rl7: d.rl7, usedTokens: d.usedTokens,
  }), 'utf8');
  fs.renameSync(tmp, sp);
}
