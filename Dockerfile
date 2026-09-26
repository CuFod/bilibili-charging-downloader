# B站充电视频下载器 - Linux Docker (Unraid兼容)
# BBDownNext 固定到包含 Cookie 覆盖修复的提交，避免上游行为漂移。
ARG BBDOWNNEXT_COMMIT=d3dc234225fa0012a3f3911f4457da11d486d93f

FROM mcr.microsoft.com/dotnet/sdk:10.0 AS bbdown-builder
ARG TARGETARCH
ARG BBDOWNNEXT_COMMIT
RUN apt-get update && apt-get install -y --no-install-recommends git ca-certificates \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /src
RUN set -eux; \
    git clone --filter=blob:none https://github.com/KaiHuaDou/BBDownNext.git BBDownNext; \
    cd BBDownNext; \
    git checkout --detach "$BBDOWNNEXT_COMMIT"; \
    case "$TARGETARCH" in \
      amd64) rid=linux-x64 ;; \
      arm64) rid=linux-arm64 ;; \
      *) echo "unsupported arch: $TARGETARCH"; exit 1 ;; \
    esac; \
    dotnet publish BBDown/BBDown.csproj -r "$rid" -c Release -o /out \
      -p:PublishAot=false -p:SelfContained=true -p:PublishSingleFile=false; \
    test -x /out/BBDown

FROM python:3.10-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=bbdown-builder /out /opt/bbdown
ENV PATH="/opt/bbdown:${PATH}"

COPY server/requirements.txt /app/server/requirements.txt
RUN pip install --no-cache-dir -r /app/server/requirements.txt

COPY server/ /app/server/
COPY web/dist/ /app/web/dist/

ENV BILI_CONFIG_DIR=/config
ENV BILI_DOWNLOAD_DIR=/downloads

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

EXPOSE 8000

VOLUME ["/config", "/downloads"]

ENTRYPOINT ["/app/entrypoint.sh"]
