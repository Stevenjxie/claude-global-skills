# -*- coding: utf-8 -*-
"""阶段A:faster-whisper 转录,分段落盘 JSON。

用法:
  python asr_dump.py <音频文件> <输出.json> [--language zh] [--prompt "领域提示词"] [--dry-run]

必须独立进程运行(勿在同进程接声纹聚类):ctranslate2 在 Windows 上进程收尾
会以退出码 9 崩溃(del model 会提前引爆)。崩溃发生在 JSON 写出之后,无害。
判断成败看 JSON 文件是否存在且日志有 [done-A],不要看退出码。
"""
import argparse
import json
import time

import av
import numpy as np

DEFAULT_PROMPT = "以下是普通话录音的整理文稿,使用规范标点。"


def decode_robust(path, rate=16000):
    """逐包解码,跳过坏包。微信导出的 m4a 首个音频包损坏,faster_whisper 自带的
    decode_audio 用生成器式解码,首包抛异常整个生成器就死了,静默返回 0 采样。"""
    container = av.open(path, metadata_errors="ignore")
    stream = container.streams.audio[0]
    resampler = av.audio.resampler.AudioResampler(format="s16", layout="mono", rate=rate)
    chunks, bad = [], 0
    for packet in container.demux(stream):
        try:
            frames = packet.decode()
        except av.error.InvalidDataError:
            bad += 1
            continue
        for f in frames:
            for rf in resampler.resample(f):
                chunks.append(rf.to_ndarray().reshape(-1))
    return np.concatenate(chunks).astype(np.float32) / 32768.0, bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("audio")
    ap.add_argument("out_json")
    ap.add_argument("--language", default="zh")
    ap.add_argument("--prompt", default=DEFAULT_PROMPT,
                    help="带规范标点的引导句;领域专有词写进去可显著减少误识别")
    ap.add_argument("--dry-run", action="store_true", help="只解码验证音频,不跑模型")
    args = ap.parse_args()

    audio, bad = decode_robust(args.audio)
    dur = len(audio) / 16000
    print(f"[info] decoded {dur:.0f}s, skipped {bad} bad packet(s)", flush=True)
    if dur < 1:
        raise SystemExit("[error] decoded audio is empty")
    if args.dry_run:
        print("[done-dry] audio decodable", flush=True)
        return

    from faster_whisper import WhisperModel
    try:
        model = WhisperModel("large-v3", device="cuda", compute_type="float16", local_files_only=True)
        print("[info] using CUDA float16", flush=True)
    except Exception as e:
        print(f"[info] CUDA unavailable ({e}), falling back to CPU int8", flush=True)
        model = WhisperModel("large-v3", device="cpu", compute_type="int8", local_files_only=True)

    t0 = time.time()
    segments, info = model.transcribe(
        audio, language=args.language, initial_prompt=args.prompt, beam_size=5,
        vad_filter=True, vad_parameters=dict(min_silence_duration_ms=500),
        word_timestamps=True, hallucination_silence_threshold=2.0,
    )
    segs = []
    for seg in segments:
        text = seg.text.strip()
        if not text:
            continue
        if segs and text == segs[-1]["text"]:  # 连续重复幻觉合并
            segs[-1]["end"] = seg.end
            continue
        segs.append({"start": seg.start, "end": seg.end, "text": text})
        if len(segs) % 200 == 0:
            print(f"[progress] ASR {seg.end:.0f}s / {dur:.0f}s", flush=True)

    with open(args.out_json, "w", encoding="utf-8") as f:
        json.dump({"duration": dur, "language": args.language, "segments": segs}, f, ensure_ascii=False)
    print(f"[done-A] {len(segs)} segments in {time.time()-t0:.0f}s -> {args.out_json}", flush=True)


main()
