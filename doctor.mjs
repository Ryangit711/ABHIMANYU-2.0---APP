#!/usr/bin/env node

/**
 * doctor.mjs — Setup validation for ABHIMANYU 2.0
 * Checks all prerequisites and prints a pass/fail checklist.
 */

import { execFileSync } from 'node:child_process';
import { existsSync, mkdirSync, writeFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const argv = process.argv.slice(2);
const targetIdx = argv.indexOf('--target');
const projectRoot =
  targetIdx !== -1 && argv[targetIdx + 1] ? argv[targetIdx + 1] : __dirname;
const JSON_OUT = argv.includes('--json');

// ANSI colors (only on TTY)
const isTTY = process.stdout.isTTY;
const green = (s) => isTTY ? `\x1b[32m${s}\x1b[0m` : s;
const red = (s) => isTTY ? `\x1b[31m${s}\x1b[0m` : s;
const yellow = (s) => isTTY ? `\x1b[33m${s}\x1b[0m` : s;
const dim = (s) => isTTY ? `\x1b[2m${s}\x1b[0m` : s;

function checkNodeVersion() {
  const major = parseInt(process.versions.node.split('.')[0]);
  if (major >= 18) {
    return { pass: true, label: `Node.js >= 18 (v${process.versions.node})` };
  }
  return {
    pass: false,
    label: `Node.js >= 18 (found v${process.versions.node})`,
    fix: 'Install Node.js 18 or later from https://nodejs.org',
  };
}

function checkPython() {
  try {
    const out = execFileSync('python3', ['--version'], { encoding: 'utf-8' }).trim();
    return { pass: true, label: `Python 3 (${out})` };
  } catch {
    return {
      pass: false,
      label: 'Python 3 not found',
      fix: 'Install Python 3 from https://python.org',
    };
  }
}

function checkDependencies() {
  if (existsSync(join(projectRoot, 'node_modules'))) {
    return { pass: true, label: 'npm dependencies installed' };
  }
  return {
    pass: false,
    label: 'npm dependencies not installed',
    fix: 'Run: npm install',
  };
}

function checkPythonDeps() {
  try {
    execFileSync('python3', ['-c', 'import docx'], { stdio: 'ignore' });
    return { pass: true, label: 'python-docx installed' };
  } catch {
    return {
      warn: true,
      label: 'python-docx not installed (needed for DOCX generation)',
      fix: 'Run: pip install python-docx',
    };
  }
}

function checkGit() {
  try {
    execFileSync('git', ['--version'], { stdio: 'ignore' });
    return { pass: true, label: 'git installed' };
  } catch {
    return {
      pass: false,
      label: 'git not found',
      fix: 'Install git from https://git-scm.com',
    };
  }
}

function checkAgentSkills() {
  const skillPath = join(projectRoot, '.agents', 'skills', 'abhimanyu', 'SKILL.md');
  if (existsSync(skillPath)) {
    return { pass: true, label: 'Agent skill entrypoint ready (.agents/skills/abhimanyu/SKILL.md)' };
  }
  return {
    pass: false,
    label: 'Agent skill entrypoint missing',
    fix: 'Run: node scaffolder/bin/skill-entrypoints.mjs (or re-install)',
  };
}

function checkCoreFiles() {
  const files = ['AGENTS.md', 'SKILL_REGISTRY.md', 'BIRDS_EYE.md'];
  const missing = files.filter((f) => !existsSync(join(projectRoot, f)));
  if (missing.length === 0) {
    return { pass: true, label: 'Core files present (AGENTS.md, SKILL_REGISTRY.md, BIRDS_EYE.md)' };
  }
  return {
    pass: false,
    label: `Core files missing: ${missing.join(', ')}`,
    fix: 'Ensure all repository files are present',
  };
}

function checkAutoDir(name) {
  const dirPath = join(projectRoot, name);
  if (existsSync(dirPath)) {
    return { pass: true, label: `${name}/ directory ready` };
  }
  try {
    mkdirSync(dirPath, { recursive: true });
    return { pass: true, label: `${name}/ directory ready (auto-created)` };
  } catch {
    return {
      pass: false,
      label: `${name}/ directory could not be created`,
      fix: `Run: mkdir ${name}`,
    };
  }
}

function checkPlaywright() {
  try {
    execFileSync('npx', ['playwright', '--version'], { stdio: 'ignore' });
    return { pass: true, label: 'Playwright available (for browser automation)' };
  } catch {
    return {
      warn: true,
      label: 'Playwright not installed (needed for AUTO-APPLY)',
      fix: 'Run: npx playwright install chromium',
    };
  }
}

// Single source of truth for user-layer prerequisites
const USER_LAYER_PREREQS = [
  {
    path: 'Master_Resume.md',
    fix: ['Create Master_Resume.md with your master resume in markdown'],
  },
  {
    path: 'data/jobs.json',
    fix: ['Run: echo \'{"applied":[],"pipeline":[]}\' > data/jobs.json'],
  },
];

function prereqPresent(root, path) {
  return existsSync(join(root, ...path.split('/')));
}

function checkPrereq({ path, fix }) {
  if (prereqPresent(projectRoot, path)) {
    return { pass: true, label: `${path} found` };
  }
  return { pass: false, label: `${path} not found`, fix };
}

// Onboarding state for --json mode
function onboardingState() {
  const missing = USER_LAYER_PREREQS
    .filter(({ path }) => !prereqPresent(projectRoot, path))
    .map(({ path }) => path);
  return { onboardingNeeded: missing.length > 0, missing };
}

async function main() {
  console.log('\nABHIMANYU 2.0 doctor');
  console.log('====================\n');

  // Re-implement checkSkills without require
  const { readdirSync } = await import('node:fs');
  const skillsDir = join(projectRoot, 'skills');
  let skillsCheck;
  if (!existsSync(skillsDir)) {
    skillsCheck = { pass: false, label: 'skills/ directory not found', fix: 'Ensure the repository is fully cloned' };
  } else {
    const entries = readdirSync(skillsDir);
    if (entries.length >= 20) {
      skillsCheck = { pass: true, label: `Skills directory ready (${entries.length} skills)` };
    } else {
      skillsCheck = { warn: true, label: `Skills directory has only ${entries.length} entries (expected 27)`, fix: 'Ensure the repository is fully cloned' };
    }
  }

  const checks = [
    checkNodeVersion(),
    checkPython(),
    checkGit(),
    checkDependencies(),
    checkPythonDeps(),
    checkAgentSkills(),
    checkCoreFiles(),
    skillsCheck,
    checkPlaywright(),
    ...USER_LAYER_PREREQS.map(checkPrereq),
    checkAutoDir('data'),
  ];

  let failures = 0;
  let warnings = 0;

  for (const result of checks) {
    const fixes = Array.isArray(result.fix) ? result.fix : result.fix ? [result.fix] : [];
    if (result.warn) {
      warnings++;
      console.log(`${yellow('⚠')} ${result.label}`);
      for (const hint of fixes) {
        console.log(`  ${dim('→ ' + hint)}`);
      }
    } else if (result.pass) {
      console.log(`${green('✓')} ${result.label}`);
    } else {
      failures++;
      console.log(`${red('✗')} ${result.label}`);
      for (const hint of fixes) {
        console.log(`  ${dim('→ ' + hint)}`);
      }
    }
  }

  console.log('');
  if (failures > 0) {
    console.log(`Result: ${failures} issue${failures === 1 ? '' : 's'} found. Fix them and run \`npm run doctor\` again.`);
    process.exit(1);
  } else {
    const warnNote = warnings > 0 ? ` (${warnings} warning${warnings === 1 ? '' : 's'} — see above)` : '';
    console.log(`Result: All checks passed${warnNote}. You're ready to go!`);
    console.log('');
    console.log('Next: open your AI coding tool (claude, opencode, codex) and issue FETCH or SHOOT.');
    process.exit(0);
  }
}

if (JSON_OUT) {
  console.log(JSON.stringify(onboardingState()));
  process.exit(0);
} else {
  main().catch((err) => {
    console.error('doctor.mjs failed:', err.message);
    process.exit(1);
  });
}
