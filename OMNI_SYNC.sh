#!/bin/bash
# OMNI_SYNC.sh — Propagate ABHIMANYU 2.0 AGENTS.md to all AI tool configs
# Follows the OMNI-gnostic principle from original JOBS-OS

ABHIMANYU_DIR=$(dirname "$(readlink -f "$0")")
echo "[OMNI_SYNC] Syncing ABHIMANYU 2.0 AGENTS.md to all tool configs..."

# Copy AGENTS.md to all tool config locations
declare -a TARGETS=(
    "$ABHIMANYU_DIR/.opencode/AGENTS.md"
    "$ABHIMANYU_DIR/CLAUDE.md"
    "$ABHIMANYU_DIR/OPENCODE.md"
    "$ABHIMANYU_DIR/CODEX.md"
    "$ABHIMANYU_DIR/GEMINI.md"
    "$ABHIMANYU_DIR/.cursorrules"
    "$ABHIMANYU_DIR/.windsurfrules"
    "$ABHIMANYU_DIR/.github/copilot-instructions.md"
    "$ABHIMANYU_DIR/.clinerules/AGENTS.md"
    "$ABHIMANYU_DIR/.kiro/AGENTS.md"
    "$ABHIMANYU_DIR/.agents/AGENTS.md"
)

for target in "${TARGETS[@]}"; do
    mkdir -p "$(dirname "$target")"
    cp "$ABHIMANYU_DIR/AGENTS.md" "$target"
    echo "[OK] → $target"
done

# Verify
echo "[OMNI_SYNC] Verifying all copies match..."
for target in "${TARGETS[@]}"; do
    if diff "$ABHIMANYU_DIR/AGENTS.md" "$target" > /dev/null 2>&1; then
        echo "[MATCH] $target"
    else
        echo "[MISMATCH] $target — run copy again"
    fi
done

# Bootstrap CLI skill entrypoints
echo "[OMNI_SYNC] Bootstrapping CLI skill entrypoints..."
for CLI_DIR in ".claude" ".opencode" ".qwen" ".antigravitycli" ".grok"; do
    SKILL_DIR="$ABHIMANYU_DIR/$CLI_DIR/skills/abhimanyu"
    mkdir -p "$SKILL_DIR"
    POINTER="../../../.agents/skills/abhimanyu/SKILL.md"
    if [ ! -f "$SKILL_DIR/SKILL.md" ] || [ "$(cat "$SKILL_DIR/SKILL.md")" = "$POINTER" ]; then
        echo "$POINTER" > "$SKILL_DIR/SKILL.md"
        echo "[OK] → $SKILL_DIR/SKILL.md"
    fi
done

echo "[OMNI_SYNC] Complete. All tools see same kernel."
