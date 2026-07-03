# Publishing checklist

Steps to take this repo public (a few are GitHub UI actions the scripts can't do).

## One-time, on GitHub

- [ ] **Settings → General → Danger Zone → Change visibility → Public**
- [ ] **Settings → Pages → Deploy from a branch → `main` / `docs`** — publishes the
      marketing site (`docs/index.html`) and animated demo at
      `https://mohammedel-sayedahmed.github.io/problem-solving-training/`
- [ ] **Settings → Features → Discussions** — enable, to gather Q&A and grow reach
- [ ] **Settings → General → Social preview** — upload a preview image
- [ ] Confirm the repo **description + topics** are set (they are, via `gh repo edit`)
- [ ] Create a few `good first issue` labelled issues to invite contributors

## Encourage forks (your outreach goal)

The README already leads with **⭐ Star + Fork** and a `Fork & make it yours`
section. Forks show up in your network graph and fork count — that's the signal
you want, so keep pointing people at **Fork**, not "Use this template".

## Before flipping to public — scan for anything private

```bash
git grep -niE 'witco|secret|token|password|@gmail|@.*\.sa' || echo "clean"
```

The CI / stars / forks badges in the README start rendering once the repo is public.

## After forking, a new owner runs

```bash
./init.sh     # clean slate + their handles
./setup.sh    # repo-local tooling
```
