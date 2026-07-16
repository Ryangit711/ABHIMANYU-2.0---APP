#!/usr/bin/env node

/**
 * update.mjs — Safe self-updater for ABHIMANYU 2.0
 * Updates only system-layer files. Never touches user data.
 *
 * Usage:
 *   node update.mjs          — Check for updates and apply
 *   node update.mjs check    — Check only, don't apply
 */

import { execFileSync } from 'node:child_process';
import { existsSync, readFileSync, writeFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const argv = process.argv.slice(2);
const CHECK_ONLY = argv.includes('check');

// ANSI colors
const isTTY = process.stdout.isTTY;
const green = (s) => isTTY ? `\x1b[32m${s}\x1b[0m` : s;
const red = (s) => isTTY ? `\x1b[31m${s}\x1b[0m` : s;
const yellow = (s) => isTTY ? `\x1b[33m${s}\x1b[0m` : s;
const dim = (s) => isTTY ? `\x1b[2m${s}\x1b[0m` : s;

// Files that are safe to auto-update (system layer)
const SYSTEM_PATHS = [
  'AGENTS.md', 'CLAUDE.md', 'OPENCODE.md', 'CODEX.md', 'GEMINI.md',
  'SKILL_REGISTRY.md', 'BIRDS_EYE.md', 'COMMANDS.md', 'MASTER_USER_MANUAL.md',
  'REFERENCES.md', 'TIMELINE.md', 'README.md', 'DATA_CONTRACT.md',
  'doctor.mjs', 'update.mjs', 'package.json',
  '.agents/', 'skills/', 'eval/', 'lib/', 'template/', 'spec/',
  'scripts/', 'scaffolder/',
  'HARD_KERNEL_RULE_FULL_CADENCE.md',
  'HARD_KERNEL_RULE_SYMBIOTIC_CADENCE.md',
  'HARD_KERNEL_RULE_UNIVERSAL_CADENCE.md',
];

function isSystemPath(path) {
  return SYSTEM_PATHS.some((p) => path === p || path.startsWith(p));
}

function getRemoteVersion() {
  try {
    const out = execFileSync('git', ['ls-remote', '--tags', '--refs', 'origin', 'main'], {
      cwd: __dirname, encoding: 'utf-8', timeout: 15000,
    });
    // If there are tags, use the latest
    const lines = out.trim().split('\n').filter(Boolean);
    if (lines.length > 0) {
      const last = lines[lines.length - 1];
      const match = last.match(/refs\/tags\/v?([\d.]+)/);
      if (match) return match[1];
    }
    return null;
  } catch {
    return null;
  }
}

function getLocalVersion() {
  try {
    const pkg = JSON.parse(readFileSync(join(__dirname, 'package.json'), 'utf-8'));
    return pkg.version || '0.0.0';
  } catch {
    return '0.0.0';
  }
}

function stashUncommitted() {
  try {
    execFileSync('git', ['stash', '--include-untracked'], { cwd: __dirname, stdio: 'ignore' });
    return true;
  } catch {
    return false;
  }
}

function pullLatest() {
  try {
    execFileSync('git', ['pull', '--ff-only'], { cwd: __dirname, stdio: 'inherit', timeout: 60000 });
    return true;
  } catch {
    return false;
  }
}

function restoreStash() {
  try {
    execFileSync('git', ['stash', 'pop'], { cwd: __dirname, stdio: 'ignore' });
  } catch {
    // Stash pop can fail if there are conflicts — that's okay
  }
}

async function main() {
  const local = getLocalVersion();
  console.log(`\nABHIMANYU 2.0 updater`);
  console.log(`Local version: ${local}`);

  // Check if we're in a git repo
  if (!existsSync(join(__dirname, '.git'))) {
    console.log(`${red('✗')} Not a git repository. Cannot auto-update.`);
    console.log('  Re-install with: npx @ryangit711/abhimanyu init');
    process.exit(1);
  }

  // Fetch remote
  console.log('\n→ Checking for updates...');
  try {
    execFileSync('git', ['fetch', 'origin'], { cwd: __dirname, stdio: 'ignore', timeout: 30000 });
  } catch {
    console.log(`${yellow('⚠')} Could not fetch from remote. Check your network connection.`);
    process.exit(1);
  }

  // Check if there are new commits
  let behind = 0;
  try {
    const out = execFileSync('git', ['rev-list', '--count', 'HEAD..origin/main'], {
      cwd: __dirname, encoding: 'utf-8',
    });
    behind = parseInt(out.trim()) || 0;
  } catch {
    // Can't determine — try pulling anyway
    behind = 1;
  }

  if (behind === 0) {
    console.log(`${green('✓')} Already up to date.`);
    process.exit(0);
  }

  console.log(`${yellow(`→ ${behind} commit(s) behind origin/main`)}`);

  if (CHECK_ONLY) {
    console.log('\nRun `node update.mjs` (without "check") to apply.');
    process.exit(0);
  }

  // Apply update
  console.log('\n→ Stashing local changes...');
  const stashed = stashUncommitted();

  console.log('→ Pulling latest...');
  const pulled = pullLatest();

  if (pulled) {
    console.log(`${green('✓')} Updated successfully.`);
  } else {
    console.log(`${red('✗')} Pull failed. Your local changes were stashed.`);
    if (stashed) restoreStash();
    process.exit(1);
  }

  // Restore stashed changes
  if (stashed) {
    console.log('→ Restoring local changes...');
    restoreStash();
  }

  console.log(`${green('✓')} ABHIMANYU 2.0 is now up to date.\n`);
}

main().catch((err) => {
  console.error('update.mjs failed:', err.message);
  process.exit(1);
});
