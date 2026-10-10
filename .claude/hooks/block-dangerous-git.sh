#!/bin/bash
# Matt Pocock git-guardrails-claude-code betiğinin Tansu uyarlaması: AGENTS.md "Git" kuralını mekanik olarak uygular.
# jq bu makinede yok; desenler ham JSON girdisinde aranır. `git push` serbesttir (iş akışı 4. adım).

INPUT=$(cat)

DANGEROUS_PATTERNS=(
  "git rebase"
  "--amend"
  "push (.* )?(--force|-f)( |\"|$)"
  "--force-with-lease"
  "reset --hard"
  "git clean -f"
  "git branch -D"
  "git checkout \.( |\"|$)"
  "git restore \.( |\"|$)"
  "git add \.( |\"|$)"
  "git add (-A|--all)( |\"|$)"
)

for pattern in "${DANGEROUS_PATTERNS[@]}"; do
  if echo "$INPUT" | grep -qE -- "$pattern"; then
    echo "BLOCKED: komut yasak desene uyuyor: '$pattern'. Tansu AGENTS.md Git kuralı buna izin vermez; dosyaları adıyla ekle." >&2
    exit 2
  fi
done

exit 0
