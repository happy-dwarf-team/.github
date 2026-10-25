# Happy Dwarf Team .github: repository rules

- Organization profile ([profile/README.md](profile/README.md)) and the default community
  health files (`CONTRIBUTING.md`, `SECURITY.md`, `SUPPORT.md`, `CODE_OF_CONDUCT.md`). Every
  organization repository without its own copy shows these, so a change here reaches all of
  them; check which repositories have their own copy before changing one.
- `tools/` holds the social preview and Workshop thumbnail generators; their READMEs say how
  to run them. [docs/workshop-pages.md](docs/workshop-pages.md) describes the Workshop
  pages.
- English. Do not imply affiliation with Paradox Interactive.
- The agent owns the pull request flow: it works on a branch with Conventional Commits,
  pushes it and opens the PR as a draft. Once ready (green CI, the change tested as above,
  no blocking review findings, not put on hold by the user) it marks the PR ready and
  squash-merges it; GitHub does not allow auto-merge on a draft. Pull requests from other
  contributors get a review and a recommendation; the maintainer decides on merging them.
  Do not bypass CI or branch protection, and do not change repository settings beyond what
  auto-merge needs.
