<!-- Copyright (c) 2026 Roronoa & Haruka · Documentation licensed CC BY-NC-SA 4.0 -->
# Telegram 语音

> © 2026 Raincove ♡ · Roronoa & Haruka · 文档 [CC BY-NC-SA 4.0](../LICENSE) · 代码 [PolyForm Noncommercial 1.0.0](../LICENSE-CODE)
>
> 让 Bot 发出的声音显示成 Telegram 的**圆形 voice note**：带波形条、点开即播、语音专属的那种气泡。关键只有一件事：编码。

## 先看结论

- 走 Bot API 的 `sendVoice`。想让声音**稳定**显示成圆形 voice note，编码用 **OGG 容器 + OPUS 编码**；官方文档的字面口径更宽（也列了 MP3/M4A），但实测里其他格式常被客户端降级成音频文件或文档附件，波形条也不齐。OGG OPUS 是唯一不翻车的选择。
- 转码一条 ffmpeg 命令就够，没有企微那样的编码器缺失问题。
- 边界比企微宽裕得多：Bot 上传上限 50MB，voice note 没有 60 秒一类的硬时长墙。批量试听小样首选这扇门（见[番外 · 场景感语音](场景感语音.md)的渠道建议）。

```text
一句话文本 ─ TTS ─> MP3/WAV ─ ffmpeg(libopus, 48kHz, 单声道) ─> voice.ogg
                                                                    │
POST /bot<token>/sendVoice  (multipart: chat_id, voice=@voice.ogg) ─┘
                                    ▼
                        圆形 voice note，带波形条
```

## 转码参数

```bash
ffmpeg -i voice.mp3 -c:a libopus -b:a 32k -ar 48000 -ac 1 voice.ogg
```

48kHz 是 OPUS 的原生采样率；人声 32k 码率足够，音乐类内容再往上加；voice note 用单声道。本仓库 [`../code/to_ogg_opus.py`](../code/to_ogg_opus.py) 是这条命令的带校验封装。

## 发送

```bash
curl -s -F chat_id=<CHAT_ID> -F voice=@voice.ogg -F caption="一句可选的说明" \
  "https://api.telegram.org/bot<BOT_TOKEN>/sendVoice"
```

`duration` 参数可选，客户端通常自己读得出；`caption` 会显示在语音条下方，批量发送编号小样时用它标序号最顺手。发普通音频（显示成音乐播放器样式、保留文件名）用 `sendAudio`，发原样文件用 `sendDocument`；三种形态按用途选，别都挤在 `sendVoice` 上。

## 验证清单

- [ ] Bot 发出的语音在手机客户端显示为圆形 voice note，带波形条。
- [ ] 同一文件走 `sendAudio` 与 `sendVoice` 显示形态不同（前者音乐样式，后者语音样式），确认自己拿到的是想要的那种。
- [ ] 转码后的 `.ogg` 用 `ffprobe` 看得到 `opus` 编码与 48000 Hz。

## 官方接口索引

- `sendVoice`：<https://core.telegram.org/bots/api#sendvoice>
- `sendAudio`：<https://core.telegram.org/bots/api#sendaudio>

以 Telegram Bot API 当前文档为准。
