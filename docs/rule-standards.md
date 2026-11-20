# Rule Standards

## File naming
`<category>_<product>_<short_description>.yml`
e.g. `proc_creation_win_powershell_encoded_cmd.yml`

## Required fields
title, id (UUIDv4), status, description, references, author, date,
tags (ATT&CK tactic + technique), logsource, detection, falsepositives, level

## Status lifecycle
- experimental: passes `sigma check`
- test: validated against at least 1 true-positive sample in CI
- stable: also produces no hits on benign data

## Level guidance
- critical: near-certain compromise
- high: strong malicious signal, triage within 1h
- medium: suspicious, needs context
- low: hunting / enrichment only

## Branch naming
rule/<technique>-<name> | ci/<change> | docs/<change> | fix/<change>

## ATT&CK version
Tags follow ATT&CK v19+. Do not use attack.defense-evasion; use attack.stealth or attack.defense-impairment.
