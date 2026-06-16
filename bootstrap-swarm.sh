#!/usr/bin/env bash
# Bootstrap SwarmForge into this project.
# Run once on a machine with tmux + Babashka installed.
# Requires: zsh, git, tmux, bb (Babashka)
#
# Usage: bash bootstrap-swarm.sh

set -euo pipefail

BRANCH=four-pack
SWARM_ARCHIVE="https://github.com/unclebob/swarm-forge/archive/refs/heads/${BRANCH}.tar.gz"

echo "Downloading SwarmForge (${BRANCH})..."
curl -L "$SWARM_ARCHIVE" | tar -xz --strip-components=1

echo "Done. Run: ./swarm"
