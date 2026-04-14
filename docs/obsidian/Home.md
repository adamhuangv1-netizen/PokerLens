---
tags: [home]
---

# PokerLens Knowledge Base

> **Setup:** Install [Dataview](https://github.com/blacksmithgu/obsidian-dataview) via Obsidian's community plugin browser (Settings → Community plugins → Browse → search "Dataview") to enable the live queries below.

---

## Open Decisions

```dataview
table date, modules from "Decisions"
where status = "open"
sort date desc
```

## Recent Sessions

```dataview
table date, modules from "Sessions"
sort date desc
limit 7
```

---

## Modules

[[Architecture/Modules/Capture|Capture]] · [[Architecture/Modules/Recognition|Recognition]] · [[Architecture/Modules/Engine|Engine]] · [[Architecture/Modules/Overlay|Overlay]] · [[Architecture/Modules/Tracking|Tracking]]

---

## Quick Links

- [[Architecture/Overview|System Overview]]
- [[Roadmap/Backlog|Backlog]]
- [[Roadmap/Milestones|Milestones]]
- [[Reference/Dependencies|Dependencies]]
- [[Reference/Glossary|Glossary]]
