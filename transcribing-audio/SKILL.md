---
name: transcribing-audio
description: Use when 用户要求转录音频/录音转文字/语音转录/字幕/会议记录/说话人分离/分辨谁在说话, 处理微信语音导出的 m4a, 或提到 whisper/transcribe/diarization/speaker labels。本机已有完整验证过的本地管线,勿从零搭建。
---

# 本地音频转录 + 说话人分离

## 概览

本机已验证的两阶段管线:faster-whisper large-v3(转文字)→ Silero VAD + CAM++ ONNX + 谱聚类(分说话人)。所有模型已在本地,无需联网下载。**用 scripts/ 里的现成脚本,不要重写。**

## 快速开始

```powershell
$env:KMP_DUPLICATE_LIB_OK = "TRUE"   # Anaconda 必需,否则 libiomp5md.dll 重复加载直接退出
$sk = "C:\Users\Steve\.claude\skills\transcribing-audio\scripts"

# 阶段A:转录(GPU 约 1/5 实时;后台运行,长音频勿前台等待)
python "$sk\asr_dump.py" <音频> <segments.json> --prompt "以下是普通话会议录音的整理文稿,使用规范标点。内容涉及<领域词1、领域词2>。"

# 阶段B:说话人分离(约每小时音频 2 分钟;只要转录不要分人就跳过此步,直接用 JSON)
python "$sk\diarize.py" <音频> <segments.json> <输出.txt>
```

## 铁律

1. **两阶段必须是两个进程**。ctranslate2 在 Windows 上进程收尾必崩(退出码 9);同进程里 `del model` 会把崩溃提前引爆,丢掉整个后半段。
2. **判断成败看产物,不看退出码**。日志有 `[done-A]`/`[done-B]` 且输出文件存在 = 成功;退出码 9 出现在 `[done-*]` 之后 = 无害的收尾崩溃。
3. **segments.json 是缓存**。换聚类参数、指定人数、改输出格式都只重跑阶段B(几十秒),绝不重跑转录。

## 故障速查

| 症状 | 原因与处置 |
|------|-----------|
| 转出 0 段 / duration=0 且无报错 | 音频首包损坏(微信 m4a 常见)。脚本已内置逐包解码,若绕过脚本直接 `model.transcribe(路径)` 就会踩此坑 |
| `OMP: Error #15` 立即退出 | 没设 `KMP_DUPLICATE_LIB_OK=TRUE` |
| KMeans 报 `NoneType ... split` | threadpoolctl<3 与新 MKL 的已知 bug,`pip install -U threadpoolctl` |
| 模型文件缺失 | 走 ModelScope,**不要走 HuggingFace**(本机 HF 下载确定性损坏,详见记忆 hf-download-broken-use-modelscope) |
| 退出码 9 | 见铁律 2,先查产物再下结论 |

## 调优要点

- **领域词进 `--prompt`**:能显著减少专有名词误识别(如 POS系统、堂食),但同一个词可能换着错法出现,产出后仍需抽查残留错词
- **已知人数**:`--num-speakers N` 比自动估计稳
- **精度后手**:换 ERes2NetV2(ModelScope,同接口 80 维 fbank 进/192 维出)替换 models/campplus.onnx;抢话重叠段归属不准是方案固有局限
- **说话人命名**:用户告知身份后对输出做批量替换(说话人A → 张总)
