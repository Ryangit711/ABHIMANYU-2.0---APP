#!/usr/bin/env node
// ABHIMANYU 2.0 scaffolder — one-command install.
// Clones the repo and installs dependencies.
import { execFileSync } from "node:child_process";
import { existsSync, readdirSync } from "node:fs";
import { join, delimiter } from "node:path";
import { ensureSkillEntrypoints } from "./skill-entrypoints.mjs";

const REPO = "https://github.com/Ryangit711/ABHIMANYU-2.0---APP.git";
const NPM = process.platform === "win32" ? "npm.cmd" : "npm";

const SUPPORTED_CLIS = [
  { name: "Claude Code", cmd: "claude" },
  { name: "OpenCode", cmd: "opencode" },
  { name: "Codex", cmd: "codex" },
  { name: "Gemini CLI", cmd: "gemini" },
  { name: "Qwen Code", cmd: "qwen" },
  { name: "GitHub Copilot CLI", cmd: "copilot" },
  { name: "Grok Build CLI", cmd: "grok" },
];

const USAGE = `abhimanyu — set up an AI job search workspace.

Usage:
  npx @ryangit711/abhimanyu init [folder]    Create a new workspace (default: ./ABHIMANYU-2.0)

After setup, open your AI coding tool inside the folder and issue commands like FETCH or SHOOT.
Docs: https://github.com/Ryangit711/ABHIMANYU-2.0---APP`;

function die(msg) {
  console.error(`\n✗ ${msg}\n`);
  process.exit(1);
}

function has(cmd, arg = "--version") {
  try {
    execFileSync(cmd, [arg], { stdio: "ignore" });
    return true;
  } catch {
    return false;
  }
}

function onPath(cmd) {
  const exts = process.platform === "win32" ? (process.env.PATHEXT || ".EXE;.CMD;.BAT").split(";") : [""];
  for (const dir of (process.env.PATH || "").split(delimiter)) {
    if (!dir) continue;
    for (const ext of exts) {
      try {
        if (existsSync(join(dir, cmd + ext))) return true;
      } catch {}
    }
  }
  return false;
}

function detectClis() {
  return SUPPORTED_CLIS.filter((c) => onPath(c.cmd));
}

async function main() {
  const [cmd, dirArg] = process.argv.slice(2);

  if (!cmd || cmd === "-h" || cmd === "--help") {
    console.log(USAGE);
    process.exit(cmd ? 0 : 1);
  }
  if (cmd !== "init") die(`Unknown command "${cmd}".\n${USAGE}`);

  const target = dirArg || "ABHIMANYU-2.0";
  if (existsSync(target) && readdirSync(target).length > 0) {
    die(`Target folder "${target}" already exists and is not empty. Pick another name.`);
  }
  if (!has("git")) die("git is required but was not found on PATH. Install git and try again.");

  const isAbsolute = target.startsWith("/") || /^[A-Za-z]:/.test(target);
  const display = isAbsolute ? target : `./${target}`;

  // 1. Clone the repo.
  console.log(`\n→ Cloning ABHIMANYU 2.0 into ${display} ...`);
  const cloneArgs = ["clone", "--depth=1", REPO, target];
  try {
    execFileSync("git", cloneArgs, { stdio: "inherit" });
  } catch {
    die("git clone failed. Check your network connection and try again.");
  }

  // 2. Install npm dependencies.
  console.log("\n→ Installing dependencies (npm install) ...");
  try {
    execFileSync(NPM, ["install"], { cwd: target, stdio: "inherit" });
  } catch {
    console.warn('\n! npm install failed — you can re-run it manually later with "npm install".');
  }

  // 2b. Bootstrap CLI skill entrypoints.
  const bootstrapped = ensureSkillEntrypoints(target);
  if (bootstrapped.length > 0) {
    console.log(`\n→ Bootstrapped ${bootstrapped.length} CLI skill entrypoint(s) for this workspace`);
  }

  // 3. Next steps.
  console.log(`\n✓ ABHIMANYU 2.0 is ready in ${display}\n`);
  console.log("Next steps:");
  console.log(`  1. cd ${target}`);

  const detected = detectClis();
  if (detected.length === 1) {
    console.log(`  2. Open your workspace:  ${detected[0].cmd}   (${detected[0].name} detected)`);
  } else if (detected.length > 1) {
    console.log(`  2. Open your workspace with any of:  ${detected.map((c) => c.cmd).join(", ")}   (detected)`);
  } else {
    console.log(`  2. Open your AI coding tool here, e.g.:  ${SUPPORTED_CLIS.map((c) => c.cmd).join(", ")}`);
  }

  console.log("\nOn first launch, the agent will walk you through setup — your profile and target roles — just by chatting.");
  console.log("\nABHIMANYU 2.0 is AI-agnostic — Claude Code, OpenCode, Codex, Gemini CLI, Copilot, and Grok all work.");
  console.log("\nOptional (for browser automation):");
  console.log("  npx playwright install chromium\n");
}

main().catch((err) => die(err?.message || String(err)));
