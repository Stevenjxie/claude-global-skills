# -*- coding: utf-8 -*-
"""阶段B:说话人分离(Silero VAD + CAM++ ONNX + 谱聚类),读阶段A的 JSON,输出成品。

用法:
  python diarize.py <音频文件> <segments.json> <输出.txt> [--num-speakers N]

独立进程,不加载 ctranslate2,正常退出码为 0。
--num-speakers 可跳过自动人数估计(已知人数时更稳)。
"""
import argparse
import json
import os
import time

import av
import numpy as np
import onnxruntime as ort
import kaldi_native_fbank as knf
from sklearn.cluster import KMeans
from sklearn.preprocessing import normalize
from faster_whisper.vad import get_speech_timestamps, VadOptions

SR = 16000
WIN_FRAMES, HOP_FRAMES = 148, 75  # 1.5s 窗 / 0.75s 步进(帧移10ms)
ONNX_DEFAULT = os.path.join(os.path.dirname(__file__), "..", "models", "campplus.onnx")


def fmt(t):
    h, rem = divmod(int(t), 3600)
    m, s = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


def decode_robust(path, rate=SR):
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


def full_fbank(audio):
    opts = knf.FbankOptions()
    opts.frame_opts.samp_freq = SR
    opts.frame_opts.dither = 0.0
    opts.frame_opts.snip_edges = True
    opts.mel_opts.num_bins = 80
    fb = knf.OnlineFbank(opts)
    fb.accept_waveform(SR, audio)
    fb.input_finished()
    feats = np.empty((fb.num_frames_ready, 80), dtype=np.float32)
    for i in range(len(feats)):
        feats[i] = fb.get_frame(i)
    return feats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("audio")
    ap.add_argument("segments_json")
    ap.add_argument("out_txt")
    ap.add_argument("--onnx", default=ONNX_DEFAULT)
    ap.add_argument("--num-speakers", type=int, default=0, help="已知人数时指定,0=自动估计")
    args = ap.parse_args()

    audio, _ = decode_robust(args.audio)
    data = json.load(open(args.segments_json, encoding="utf-8"))
    segs, dur = data["segments"], data["duration"]
    print(f"[info] loaded {len(segs)} ASR segments, audio {fmt(dur)}", flush=True)

    t0 = time.time()
    speech = get_speech_timestamps(audio, VadOptions(min_silence_duration_ms=500))
    feats = full_fbank(audio)
    mask = np.zeros(len(feats), dtype=np.float32)
    for st in speech:
        mask[int(st["start"] / 160): int(st["end"] / 160)] = 1.0

    sess = ort.InferenceSession(args.onnx, providers=["CPUExecutionProvider"])
    in_name = sess.get_inputs()[0].name
    wins, centers = [], []
    for start in range(0, len(feats) - WIN_FRAMES, HOP_FRAMES):
        if mask[start:start + WIN_FRAMES].mean() < 0.5:
            continue
        w = feats[start:start + WIN_FRAMES]
        wins.append(w - w.mean(axis=0, keepdims=True))  # CAM++ 要求逐窗均值归一
        centers.append((start + WIN_FRAMES / 2) * 0.01)
    centers = np.array(centers)
    embs = np.concatenate([
        sess.run(None, {in_name: np.stack(wins[i:i + 64]).astype(np.float32)})[0]
        for i in range(0, len(wins), 64)
    ])
    print(f"[info] {len(embs)} windows embedded in {time.time()-t0:.0f}s", flush=True)

    # 谱聚类,特征值间隙自动估人数(需 threadpoolctl>=3,旧版 KMeans 会 NoneType.split 崩溃)
    E = normalize(embs)
    A = E @ E.T
    np.fill_diagonal(A, 0.0)
    thresh = np.percentile(A, 80, axis=1, keepdims=True)
    Ap = np.where(A >= thresh, A, 0.0)
    Ap = (Ap + Ap.T) / 2
    d = Ap.sum(axis=1)
    d[d == 0] = 1e-8
    Dinv = np.diag(d ** -0.5)
    L = np.eye(len(Ap)) - Dinv @ Ap @ Dinv
    eigvals, eigvecs = np.linalg.eigh(L)
    if args.num_speakers:
        k = args.num_speakers
    else:
        gaps = np.diff(eigvals[:9])
        k = int(np.argmax(gaps[1:]) + 2) if len(gaps) > 1 else 1
    print(f"[info] eigvals[:9]={np.round(eigvals[:9], 3)}, k={k}", flush=True)
    labels = KMeans(n_clusters=k, n_init=10, random_state=0).fit_predict(normalize(eigvecs[:, :k]))
    for i in range(1, len(labels) - 1):  # 平滑孤立点
        if labels[i] != labels[i - 1] and labels[i - 1] == labels[i + 1]:
            labels[i] = labels[i - 1]

    def seg_speaker(s, e):
        idx = np.where((centers >= s - 0.4) & (centers <= e + 0.4))[0]
        if len(idx) == 0:
            idx = [int(np.argmin(np.abs(centers - (s + e) / 2)))]
        return int(np.bincount(labels[idx], minlength=k).argmax())

    spk_of = [seg_speaker(s["start"], s["end"]) for s in segs]
    order, names = [], {}
    for sp in spk_of:
        if sp not in order:
            order.append(sp)
            names[sp] = "说话人" + chr(ord("A") + len(order) - 1)
    talk = {sp: 0.0 for sp in order}
    for s, sp in zip(segs, spk_of):
        talk[sp] += s["end"] - s["start"]

    turns = []
    for s, sp in zip(segs, spk_of):
        t = s["text"] if s["text"][-1] in "。!?,、;:" else s["text"] + ","
        if turns and turns[-1][3] == sp and s["start"] - turns[-1][1] < 1.5 and len(turns[-1][2]) < 300:
            turns[-1] = (turns[-1][0], s["end"], turns[-1][2] + t, sp)
        else:
            turns.append((s["start"], s["end"], t, sp))

    def polish(p):
        p = p.rstrip(",、")
        return p + "。" if p and p[-1] not in "。!?" else p

    with open(args.out_txt, "w", encoding="utf-8") as f:
        f.write(f"# 来源: {args.audio}\n# 时长: {fmt(dur)}  检测到 {k} 位说话人\n")
        for sp in order:
            f.write(f"# {names[sp]}: 发言约 {fmt(talk[sp])}\n")
        f.write("\n")
        for s, e, text, sp in turns:
            f.write(f"[{fmt(s)}] {names[sp]}:\n{polish(text)}\n\n")
    print(f"[done-B] {len(turns)} turns, {k} speakers -> {args.out_txt}", flush=True)


main()
