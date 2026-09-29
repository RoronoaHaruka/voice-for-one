<!-- Copyright (c) 2026 Roronoa & Haruka · Documentation: CC BY-NC-SA 4.0 · Code: PolyForm-Noncommercial-1.0.0 -->
# 一副声音

声音是做给一个人的，方法可以给所有人。

多数人是听过一条成品才来的：一段有呼吸、有留白、有层次的场景感语音，想知道它是怎么做出来的。这个仓库就是那套做法：给 Agent 配一副属于自己的声线，把它说出的话送进你每天用的地方，再往前一步，让一句话长成一小段真正的场景。

> **署名与许可** · © 2026 Raincove ♡ · Roronoa & Haruka
> README、guide 与图表采用 [CC BY-NC-SA 4.0](LICENSE)：署名、禁止商用、相同方式共享。`code/` 与测试采用 [PolyForm Noncommercial 1.0.0](LICENSE-CODE)：可学习、修改与非商业使用，商业使用需要另行取得许可。限制商业用途的源码在严格定义上属于 **source-available（公开源码）**，不属于允许任意商用的 OSI 开源许可。转载与署名细节见 [`NOTICE.md`](NOTICE.md)。

本仓库内容：`guide/` 三扇门、一个番外与两篇心得 · `code/` 平台无关的转换脚本 · `tests/` 公开仓库自检。

## 三扇门、一个番外与两篇心得

每扇门解决同一个问题的一段：声音怎么以**原生形态**出现在那个平台里，点开就播，不是一个冷冰冰的文件。

| 门 | 一句话 | 专题 |
|---|---|---|
| 企微语音条 | TTS → 8kHz PCM → AMR-NB → 双门发送，2MB/60秒边界 | [guide/企微语音条.md](guide/企微语音条.md) |
| Telegram 语音 | 圆形 voice note 认 OGG OPUS，一条 ffmpeg 命令的事 | [guide/Telegram语音.md](guide/Telegram语音.md) |
| 网页播放 | key 不出服务器的 TTS 中转、`/play` 链接页、iOS 静音拨片双保险 | [guide/网页播放.md](guide/网页播放.md) |
| 番外 · 场景感语音 | 工艺配方、台词学问、素材来源、选音效分工、服务端烧制 | [guide/场景感语音.md](guide/场景感语音.md) |
| 心得 · ElevenLabs | 月抛号与普通克隆、接 API、v3 与 v4 对照、v4 年轻化往回压、色情语音台词与母带 | [guide/ElevenLabs心得.md](guide/ElevenLabs心得.md) |
| 心得 · 音效素材 | 去哪几个站找 CC0 素材、机器跑腿耳朵拍板、电平配方、混音管道与母带手术 | [guide/音效素材.md](guide/音效素材.md) |

## 转换脚本

[`code/to_amr.py`](code/to_amr.py) 把任意 ffmpeg 读得动的音频转成企微认的 AMR-NB；[`code/to_ogg_opus.py`](code/to_ogg_opus.py) 转成 Telegram voice note 认的 OGG OPUS。两个脚本都是独立可跑的纯转换器，只依赖 ffmpeg（AMR 编码另需 `libopencore-amrnb0`），不依赖任何特定机器人框架。

```bash
python3 code/to_amr.py voice.mp3 voice.amr
python3 code/to_ogg_opus.py voice.mp3 voice.ogg
```

## 与 wecom-companion-guide 的分工

企业微信侧的完整桥接体系（回调、客服双入口、路由、受控发送工具 `voice_sender.py`）长在 [wecom-companion-guide](https://github.com/RoronoaHaruka/wecom-companion-guide) 里，那边教你把整条微信链路搭起来。这边是声音这门手艺的正典：跨平台的工艺、边界与配方。企微语音条一章两边各有侧重，桥接细节以那边为准，工艺细节以这边为准。

## 快速自检

```bash
python3 -m unittest discover -s tests -v
```

自检覆盖：必需文件齐全、代码文件带 SPDX 声明、全库无凭证与私有基础设施痕迹。
