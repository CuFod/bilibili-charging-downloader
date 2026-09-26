# 第三方组件声明 (Third-Party Notices)

本项目分发时（Windows/Linux 安装包、Docker 镜像）包含以下第三方组件：

## BBDownNext

- **用途**: B站视频下载/解析引擎
- **来源**: https://github.com/KaiHuaDou/BBDownNext
- **固定提交**: `d3dc234225fa0012a3f3911f4457da11d486d93f`（包含命令行 Cookie 被续期逻辑覆盖的修复）
- **许可证**: MIT License
- **说明**: BBDownNext 基于 nilaoda/BBDown 衍生，版权与许可证信息以其仓库声明为准

> MIT License 全文见 https://github.com/KaiHuaDou/BBDownNext/blob/main/LICENSE

## ffmpeg

- **用途**: 音视频流合并封装 (BBDown 调用)
- **来源**: https://ffmpeg.org （Windows 构建来自 https://www.gyan.dev/ffmpeg/builds/,Linux 构建来自 https://github.com/BtbN/FFmpeg-Builds)
- **许可证**: LGPL v2.1+ / GPL v2+（依构建配置）
- ffmpeg 源代码可从上述官网获取

## 其他（运行时依赖，随包分发）

| 组件 | 许可证 | 链接 |
|---|---|---|
| Python | PSF License | https://python.org |
| FastAPI | MIT | https://fastapi.tiangolo.com |
| Uvicorn | BSD-3 | https://www.uvicorn.org |
| React | MIT | https://react.dev |
| Ant Design | MIT | https://ant.design |
| Vite | MIT | https://vitejs.dev |
