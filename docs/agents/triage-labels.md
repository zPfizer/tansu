# Triage Labels

The skills speak in terms of five canonical triage roles. This file maps those roles to the actual label strings used in this repo's issue tracker (GitHub Issues, see `issue-tracker.md`).

| Label in mattpocock/skills | Label in our tracker | Meaning                                  |
| -------------------------- | -------------------- | ---------------------------------------- |
| `needs-triage`             | `needs-triage`       | Maintainer needs to evaluate this issue  |
| `needs-info`               | `needs-info`         | Waiting on reporter for more information |
| `ready-for-agent`          | `ready-for-agent`    | Fully specified, ready for an AFK agent  |
| `ready-for-human`          | `ready-for-human`    | Requires human implementation            |
| `wontfix`                  | `wontfix`            | Will not be actioned                     |

When a skill mentions a role (e.g. "apply the AFK-ready triage label"), use the corresponding label string from this table.

Three more labels belong to Tansu. They are not triage roles:

| Label | Meaning |
| --- | --- |
| `yerel` | On an issue: the ticket needs the brain pool, `veri/`, or a real snapshot. The cloud agent skips it. Only a local session runs it. |
| `ci-kirmizi` | On a PR: CI is red. The label starts the agent again on the same branch. |
| `inceleme-gecti` | On a PR: the independent review says "geçti". With a green CI, the PR can merge. |

The role label is the triage state of an open ticket. How the labels, the assignee, the PR, and the issue state map to the old `Status:` line is in `issue-tracker.md`, section "State of a ticket".
