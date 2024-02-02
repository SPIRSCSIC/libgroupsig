FROM ubuntu:jammy
RUN apt update && apt install -y --no-install-recommends build-essential gdb cmake vim libgmp-dev libssl-dev git ca-certificates && apt clean && apt autoremove -y
WORKDIR /mnt
