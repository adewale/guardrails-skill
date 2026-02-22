# Language-Specific Defaults — Reference

This is the single source of truth for tool selection per ecosystem. The main SKILL.md
describes what each guardrail does and why. This reference specifies which tool to use
for each guardrail in each language.

Read this reference at SessionStart when discovering the project's ecosystem and existing
tooling. Use it to fill gaps — if the project has a test runner but no linter, this tells
you which linter to add.

## Tool Selection

| Concern | JS/TS | Python | Rust | Go | Java |
|---|---|---|---|---|---|
| **Testing** | | | | | |
| Test runner | Vitest / Jest | pytest | cargo test | go test | JUnit 5 |
| Property tests | fast-check | Hypothesis | proptest | rapid | jqwik |
| Mutation | Stryker | mutmut | cargo-mutants | — | pitest |
| Screenshot | Playwright | Playwright | — | — | — |
| E2E | Playwright / Cypress | Playwright | — | — | — |
| Contract | Pact | Pact | — | — | Spring Cloud Contract |
| Accessibility | axe-core / jest-axe | pa11y | — | — | — |
| Fuzz | — | Atheris | cargo-fuzz | go-fuzz / native | Jazzer |
| Performance | Benchmark.js | pytest-benchmark | criterion | go test -bench | JMH |
| **Static analysis** | | | | | |
| Linter | ESLint | Ruff | clippy | golangci-lint | Checkstyle / SpotBugs |
| Formatter | Prettier | Black / Ruff | rustfmt | gofmt | google-java-format |
| Type checker | tsc (strict: true) | mypy / pyright (strict) | (built-in) | (built-in) | (built-in) |
| Dead code | knip | vulture | (compiler warns) | deadcode | — |
| Duplicate code | jscpd | pylint (R0801) | cargo-dupes | dupl | PMD CPD |
| Complexity | eslint-plugin-complexity | ruff (McCabe) | clippy (cognitive) | gocyclo | PMD |
| **Security** | | | | | |
| SAST | Semgrep | Bandit + Semgrep | cargo-audit | gosec | CodeQL |
| Deps audit | npm audit | pip-audit | cargo audit | govulncheck | OWASP dep-check |
| Deps update | Dependabot / Renovate | Dependabot / Renovate | Dependabot / Renovate | Dependabot / Renovate | Dependabot / Renovate |
| Secrets | gitleaks | gitleaks | gitleaks | gitleaks | gitleaks |
| **Infrastructure** | | | | | |
| Coverage | v8 / istanbul | coverage.py | cargo-tarpaulin | go cover | JaCoCo |
| Pre-commit | husky + lint-staged | pre-commit | pre-commit | pre-commit | pre-commit |
| Commit lint | commitlint | commitlint | commitlint | commitlint | commitlint |

## Config File Discovery Patterns

When discovering a project's existing guardrails at SessionStart, look for these config
files by ecosystem:

| Concern | JS/TS | Python | Rust | Go | Java |
|---|---|---|---|---|---|
| Test runner | `vitest.config.ts`, `jest.config.*` | `pytest.ini`, `pyproject.toml [tool.pytest]` | `Cargo.toml [test]` | `*_test.go` files | `pom.xml`, `build.gradle` |
| Lint | `.eslintrc.*`, `eslint.config.*` | `ruff.toml`, `pyproject.toml [tool.ruff]` | `clippy.toml` | `.golangci.yml` | `checkstyle.xml` |
| Formatter | `.prettierrc.*` | `pyproject.toml [tool.black]` | `rustfmt.toml` | (gofmt has no config) | `.editorconfig` |
| Type checker | `tsconfig.json` | `mypy.ini`, `pyproject.toml [tool.mypy]` | (built-in) | (built-in) | (built-in) |
| Pre-commit | `.husky/`, `.lintstagedrc` | `.pre-commit-config.yaml` | `.pre-commit-config.yaml` | `.pre-commit-config.yaml` | `.pre-commit-config.yaml` |
| CI | `.github/workflows/`, `.gitlab-ci.yml` | `.github/workflows/`, `.gitlab-ci.yml` | `.github/workflows/` | `.github/workflows/` | `.github/workflows/`, `Jenkinsfile` |
| Coverage | `.nycrc`, `vitest.config.ts` | `.coveragerc`, `pyproject.toml [tool.coverage]` | `Cargo.toml` | (go test flags) | `jacoco.gradle`, `pom.xml` |
