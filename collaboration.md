# 🤝 AI Collaboration Workspace

Welcome to the shared workspace! This file is used to pass context, designs, and code reviews back and forth between **Antigravity** (Google DeepMind) and **Claude** (Anthropic).

---

## 📋 Current Project: PokerLens (Railbird Overlay)

**Project Goal**: A real-time poker overlay for private games with friends. Uses ML-based card recognition and equity calculation to display strategic tips.

### How to use this file:
1. **User (Project Manager)** assigns a task to Agent A.
2. **Agent A** writes their work, proposal, or code in this file.
3. **User** invokes Agent B and asks them to review/modify what Agent A wrote.
4. **Agent B** adds their feedback below. 
5. Repeat until the task is complete!
6. **Important Optimization:** Once a decision is reached or a discussion point is resolved, delete the old back-and-forth text. Leave only the final agreed-upon decision or a concise summary to preserve context tokens for both agents.

---

## 💬 Discussion & Handoff Thread

### [Resolved] - CNN vs YOLO Architecture
**Decision**: We are moving forward with a spatial CNN. Claude correctly pointed out we need **54 classes** total (52 cards + 1 `empty` + 1 `back` face-down). Claude has already scaffolded the `train.py` and `src/` modules reflecting this design.

### [Pending] - User
*(Awaiting your next directive for Claude or Antigravity!)*
