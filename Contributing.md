# Contributing

Hey, genuinely appreciate you being here.

Sample Pack Assembler started as a personal tool that I cleaned up and put out publicly because I thought other producers might find it useful. It is not a big open source project with a team behind it, so contributions work a little differently here. Read through this before you open anything and we will both save time.

---

## What is actually welcome

**Bug reports:** if something crashes, behaves weirdly or spits out output that makes no sense, open an issue. Tell me your OS, your Python version, what you did and what happened. The more specific you are, the faster it gets looked at. Screenshots help a lot.

**Feature requests:** if you have an idea that would make the tool genuinely more useful for producers, open an issue and walk me through the use case. Not everything will get built but everything gets read. Some of the best features in tools like this came from people just describing how they actually work.

**Typos and small documentation fixes:** if something in the README or the CHANGELOG is wrong or unclear, just open a PR directly. No need to discuss a two-word fix first.

---

## What will get closed

Pull requests that pull in new dependencies beyond `pywebview` without any prior conversation. The whole point of this project is that you run one file with one install command. That simplicity is intentional.

Pull requests that restyle the themes. The aesthetics are deliberate and I am not looking to redesign them by committee.

Anything that tries to turn this into a library, an importable module or something that runs headless. That is a different project.

---

## How to open a pull request

Open an issue first unless it is a typo. Get a quick thumbs up on the direction, then fork, branch off `main`, make your changes and open the PR with a short description of what changed and why. Keep the commits clean, one logical change per commit, no "wip" or "final final" in the history please.

---

## Code style

There is no linter set up. Just match whatever the file you are editing is already doing: 4-space indentation, names that actually describe what a variable holds, and comments only when the code genuinely needs explanation rather than as narration of what is already obvious.

---

## One last thing

Anything you submit will fall under the same restrictive license as the rest of the project. If that does not work for you, totally fine, just do not contribute. No hard feelings at all.

Thanks again for being interested enough to read this far.
