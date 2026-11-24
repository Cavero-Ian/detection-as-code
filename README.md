[![detection-ci](https://github.com/Cavero-Ian/detection-as-code/actions/workflows/ci.yml/badge.svg)](https://github.com/Cavero-Ian/detection-as-code/actions/workflows/ci.yml)

# detection-as-code

Sigma detection rules managed like software: version-controlled, validated in CI,
and converted automatically to SIEM queries.

## Pipeline
| Stage | Tool | Purpose |
|---|---|---|
| Lint | `yamllint` | YAML syntax |
| Validate | `sigma check` | Rule validity + ATT&CK v19 tag validation |
| Convert | `sigma convert` | Splunk SPL / SPL2 queries, published as CI artifacts |
| Test | Chainsaw 2.18.0 | True-positive and negative tests on self-generated Sysmon telemetry (`tests/cases.yml`) |

Every change reaches `main` only through a pull request with passing checks (branch ruleset).

## Rules
| Rule | ATT&CK | Level | Status |
|---|---|---|---|
| PowerShell Execution With Encoded Command | T1059.001, T1027 | medium | test |

## Notable decisions
- **ATT&CK v19:** Defense Evasion was split into Stealth (TA0005) and Defense Impairment (TA0112); the CI validator rejects outdated tactic tags.
- **Pinned dependencies** (pySigma 2.1.0): an upstream release broke the Kusto backend during development, so exact versions are pinned for reproducible CI.
- **Splunk only for now:** Elastic and KQL backends are pending pySigma 2.x compatibility.

## Roadmap
- [x] True-positive and negative testing against self-generated Sysmon telemetry (EVTX)
- [ ] ATT&CK Navigator coverage layer generated in CI
- [ ] 15+ rules across Execution, Persistence, Credential Access and Stealth
- [ ] Elastic / KQL conversion once backends support pySigma 2.x

## Repository layout
    rules/      Sigma rules, organized by log source
    docs/       Rule standards and conventions
    .github/    CI workflow