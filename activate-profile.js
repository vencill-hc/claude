#!/usr/bin/env node

/**
 * Claude Profile Activator
 * Adapted from https://github.com/TysonHeim/Claude-Profile-Switching
 *
 * Adaptations for this repo:
 *   - Sources live in skills/, agents/, commands/ (not skills-repo/ etc)
 *   - ALWAYS_ON_AGENTS empty by default
 *
 * Usage:
 *   node activate-profile.js [profile1] [profile2] ...
 *   node activate-profile.js --list
 *   node activate-profile.js --show
 */

const fs = require('fs');
const path = require('path');

const colors = {
  reset: '\x1b[0m',
  blue: '\x1b[34m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  red: '\x1b[31m',
  dim: '\x1b[2m',
};

const repoDir = __dirname;
const profilesDir = path.join(repoDir, 'profiles');
const mcpConfigsDir = path.join(repoDir, 'mcp-configs');

const claudeDir = path.join(require('os').homedir(), '.claude');
const targetDirs = {
  skills: path.join(claudeDir, 'skills'),
  agents: path.join(claudeDir, 'agents'),
  commands: path.join(claudeDir, 'commands'),
};

const SYMLINK_TYPES = ['skills', 'agents', 'commands'];

// Repo source dirs (not "<type>-repo/" — we use bare names)
const sourceDirs = {
  skills: path.join(repoDir, 'skills'),
  agents: path.join(repoDir, 'agents'),
  commands: path.join(repoDir, 'commands'),
};

const ALWAYS_ON_AGENTS = [];

function print(message, color = 'reset') {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

function ensureDir(dirPath) {
  if (!fs.existsSync(dirPath)) {
    fs.mkdirSync(dirPath, { recursive: true });
  }
}

function getAvailableProfiles() {
  if (!fs.existsSync(profilesDir)) return [];
  return fs.readdirSync(profilesDir, { withFileTypes: true })
    .filter(e => e.isDirectory() && !e.name.startsWith('.'))
    .map(e => e.name);
}

function getProfileEntries(profileName, type) {
  const dir = path.join(profilesDir, profileName, type);
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir, { withFileTypes: true })
    .filter(e => !e.name.startsWith('.'))
    .map(e => e.name);
}

function getProfileMcpServers(profileName) {
  const mcpFile = path.join(profilesDir, profileName, 'mcp-servers.json');
  if (!fs.existsSync(mcpFile)) return [];
  try {
    return JSON.parse(fs.readFileSync(mcpFile, 'utf-8'));
  } catch {
    print(`  Warning: Invalid mcp-servers.json in profile '${profileName}'`, 'yellow');
    return [];
  }
}

function clearSymlinks(dir) {
  ensureDir(dir);
  for (const entry of fs.readdirSync(dir)) {
    if (entry.startsWith('.')) continue;
    const full = path.join(dir, entry);
    if (fs.lstatSync(full).isSymbolicLink()) {
      fs.unlinkSync(full);
    }
  }
}

function createSymlink(target, linkPath) {
  try {
    if (fs.existsSync(linkPath) || fs.lstatSync(linkPath).isSymbolicLink()) {
      fs.unlinkSync(linkPath);
    }
  } catch { /* doesn't exist, fine */ }

  const relativePath = path.relative(path.dirname(linkPath), target);
  try {
    fs.symlinkSync(relativePath, linkPath, 'junction');
    return true;
  } catch {
    try {
      const stat = fs.statSync(target);
      if (stat.isDirectory()) {
        fs.cpSync(target, linkPath, { recursive: true });
      } else {
        fs.copyFileSync(target, linkPath);
      }
      return true;
    } catch (err) {
      print(`  Failed to link ${path.basename(linkPath)}: ${err.message}`, 'yellow');
      return false;
    }
  }
}

function activateSymlinks(profileName, type) {
  const entries = getProfileEntries(profileName, type);
  let count = 0;
  for (const entry of entries) {
    const source = path.join(profilesDir, profileName, type, entry);
    const realSource = fs.realpathSync(source);
    const target = path.join(targetDirs[type], entry);
    if (createSymlink(realSource, target)) {
      print(`  + ${type}/${entry}`, 'reset');
      count++;
    }
  }
  return count;
}

function loadMcpFragment(serverName) {
  const fragPath = path.join(mcpConfigsDir, `${serverName}.json`);
  if (!fs.existsSync(fragPath)) {
    print(`  Warning: MCP config '${serverName}.json' not found`, 'yellow');
    return null;
  }
  try {
    return JSON.parse(fs.readFileSync(fragPath, 'utf-8'));
  } catch (err) {
    print(`  Warning: Invalid JSON in '${serverName}.json': ${err.message}`, 'yellow');
    return null;
  }
}

function activateMcp(profileNames) {
  const allServers = new Set();
  for (const profile of profileNames) {
    for (const server of getProfileMcpServers(profile)) {
      allServers.add(server);
    }
  }

  if (allServers.size === 0) return 0;

  const merged = { mcpServers: {} };
  let count = 0;

  for (const serverName of allServers) {
    const fragment = loadMcpFragment(serverName);
    if (fragment) {
      Object.assign(merged.mcpServers, fragment);
      print(`  + mcp/${serverName}`, 'reset');
      count++;
    }
  }

  if (count > 0) {
    const outputPath = path.join(process.cwd(), '.mcp.json');
    fs.writeFileSync(outputPath, JSON.stringify(merged, null, 2) + '\n');
    print(`  Wrote ${outputPath}`, 'dim');
  }

  return count;
}

function getCurrentState() {
  const state = {};
  for (const type of SYMLINK_TYPES) {
    const dir = targetDirs[type];
    state[type] = [];
    if (!fs.existsSync(dir)) continue;
    for (const entry of fs.readdirSync(dir)) {
      if (entry.startsWith('.')) continue;
      const full = path.join(dir, entry);
      if (fs.lstatSync(full).isSymbolicLink()) {
        state[type].push(entry);
      }
    }
  }
  return state;
}

function ensureAlwaysOnAgents() {
  let added = 0;
  for (const name of ALWAYS_ON_AGENTS) {
    const target = path.join(targetDirs.agents, name);
    if (fs.existsSync(target)) continue;
    const source = path.join(sourceDirs.agents, name);
    if (createSymlink(source, target)) {
      print(`  + agents/${name} (always-on)`, 'dim');
      added++;
    }
  }
  return added;
}

function cmdList() {
  print('\n=== Available Profiles ===\n', 'blue');
  const profiles = getAvailableProfiles();
  if (profiles.length === 0) {
    print('No profiles found in profiles/', 'yellow');
    return;
  }
  print('Profile              Skills  Agents  Commands  MCP Servers', 'reset');
  print('─'.repeat(65), 'reset');
  for (const profile of profiles) {
    const skills = getProfileEntries(profile, 'skills').length;
    const agents = getProfileEntries(profile, 'agents').length;
    const commands = getProfileEntries(profile, 'commands').length;
    const mcp = getProfileMcpServers(profile).length;
    const row = [
      profile.padEnd(20),
      String(skills).padEnd(8),
      String(agents).padEnd(8),
      String(commands).padEnd(10),
      String(mcp),
    ].join('');
    print(row, 'reset');
  }
  print(`\nTotal profiles: ${profiles.length}`, 'dim');
  print('');
}

function cmdShow() {
  print('\n=== Current Activation ===\n', 'blue');
  const state = getCurrentState();
  let total = 0;
  for (const type of SYMLINK_TYPES) {
    const items = state[type];
    if (items.length === 0) continue;
    print(`${type} (${items.length}):`, 'green');
    for (const item of items) {
      print(`  ${item}`, 'reset');
    }
    total += items.length;
    print('');
  }
  if (total === 0) {
    print('No resources currently activated', 'yellow');
    print('To activate: node activate-profile.js <profile1> [profile2] ...', 'reset');
  } else {
    print(`Total active resources: ${total}`, 'blue');
  }
  print('');
}

function cmdActivate(profileNames) {
  print('\n=== Claude Profile Activator ===\n', 'blue');
  for (const name of profileNames) {
    if (!fs.existsSync(path.join(profilesDir, name))) {
      print(`Profile '${name}' not found`, 'red');
      print(`Available: ${getAvailableProfiles().join(', ')}`, 'dim');
      process.exit(1);
    }
  }
  for (const type of SYMLINK_TYPES) {
    print(`Clearing ${type}...`, 'dim');
    clearSymlinks(targetDirs[type]);
  }
  print('');
  const counts = { skills: 0, agents: 0, commands: 0, mcp: 0 };
  for (const name of profileNames) {
    print(`Profile: ${name}`, 'green');
    for (const type of SYMLINK_TYPES) {
      counts[type] += activateSymlinks(name, type);
    }
  }
  counts.mcp = activateMcp(profileNames);
  counts.agents += ensureAlwaysOnAgents();
  print('');
  const parts = [];
  if (counts.skills) parts.push(`${counts.skills} skills`);
  if (counts.agents) parts.push(`${counts.agents} agents`);
  if (counts.commands) parts.push(`${counts.commands} commands`);
  if (counts.mcp) parts.push(`${counts.mcp} MCP servers`);
  const total = Object.values(counts).reduce((a, b) => a + b, 0);
  print(`Activated ${total} resources (${parts.join(', ')}) from ${profileNames.length} profile(s)`, 'green');
  print(`Profiles: ${profileNames.join(', ')}`, 'dim');
  print('');

  // Write active-profiles state file for statusline display
  try {
    fs.writeFileSync(path.join(claudeDir, '.active-profiles'), profileNames.join(' ') + '\n');
  } catch (err) {
    print(`  (could not write .active-profiles: ${err.message})`, 'dim');
  }
}

function cmdUsage() {
  print('\n=== Claude Profile Activator ===', 'blue');
  print('Manages Claude Code skills, agents, commands, and MCP configs via profiles.', 'reset');
  print('');
  print('Usage:', 'reset');
  print('  node activate-profile.js <profile1> [profile2] ...', 'reset');
  print('  node activate-profile.js --list    List all profiles', 'reset');
  print('  node activate-profile.js --show    Show current activation', 'reset');
  print('');
  const profiles = getAvailableProfiles();
  if (profiles.length > 0) {
    print('Available profiles:', 'yellow');
    for (const p of profiles) {
      const s = getProfileEntries(p, 'skills').length;
      const a = getProfileEntries(p, 'agents').length;
      const c = getProfileEntries(p, 'commands').length;
      print(`  ${p} (${s} skills, ${a} agents, ${c} commands)`, 'reset');
    }
    print('');
  }
}

function main() {
  const args = process.argv.slice(2);
  if (args.includes('--list') || args.includes('-l')) cmdList();
  else if (args.includes('--show') || args.includes('-s')) cmdShow();
  else if (args.length === 0) cmdUsage();
  else cmdActivate(args);
}

if (require.main === module) main();

module.exports = { getAvailableProfiles, getCurrentState };
