# Toolchain image for the polyglot runner: Python, g++ (C++17), and a JDK.
# You don't need any of these installed on the host — use ./run.sh, which
# builds this image once and runs the suite inside it against a volume mount.
FROM debian:bookworm-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        python3 \
        g++ \
        default-jdk-headless \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /repo

# Default command runs the whole suite; ./run.sh overrides this as needed.
CMD ["python3", "run.py"]
