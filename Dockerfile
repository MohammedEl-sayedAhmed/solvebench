# Toolchain image for the polyglot runner: Python, g++ (C++17), a JDK, Node.js,
# Go, and Rust. You don't need any of these installed on the host — use ./run.sh,
# which builds this image once and runs the suite inside it against a volume mount.
FROM debian:bookworm-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        python3 \
        g++ \
        default-jdk-headless \
        nodejs \
        npm \
        golang-go \
        rustc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /repo

# Marker so run.sh / run.ps1 know they're already inside the toolchain image
# and should run natively instead of trying to launch another container.
ENV PST_IN_CONTAINER=1

# Default command runs the whole suite; ./run.sh overrides this as needed.
CMD ["python3", "run.py"]
