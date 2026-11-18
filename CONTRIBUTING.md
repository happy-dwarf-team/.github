# Contributing

Thanks for helping. This is the default guide for Happy Dwarf Team
repositories; when a repository has its own `CONTRIBUTING.md`, that one wins.

## Issues

Search the open issues first, then use the repository's issue forms. Include
the version you use, the game version and the steps that show the problem.
Security problems go through private reporting, see
[SECURITY.md](SECURITY.md).

## Pull requests

- Every change goes to `main` through a pull request, one topic per pull
  request. For a larger change, open an issue first so we can agree on the
  approach.
- Pull requests are **squash-merged**: the title becomes the commit on `main`.
  Titles follow [Conventional Commits](https://www.conventionalcommits.org/),
  `<type>(<optional scope>): <summary in the imperative, lowercase, no period>`,
  for example `fix: keep the speed after loading a save`. Common types are
  `feat`, `fix`, `perf`, `docs`, `build`, `ci`, `refactor`, `test` and `chore`.
- Show what the change does in the description's Evidence section, and say
  what you tested and what you could not test.

## Evidence

Every pull request has an `## Evidence` section that shows what it changes, so
a reviewer sees the effect without checking out the branch. The `pr-evidence`
check fails a pull request whose section is missing or empty.

A change of existing behaviour shows **before and after** in the same
conditions: the same view, save, input or command, on `main` and on your
branch. Something new shows **what it adds**. Pick the form by where the change
is seen:

- **By a person** (the game, a UI, a website, a Workshop page): screenshots.
  For movement, an interaction or a flow of several steps, also a short
  recording (5–30 s).
- **An API, CLI, config or file format:** the API itself (signatures,
  parameters, defaults, errors) and one real call or command with its output.
- **Logs or files the program writes:** the relevant lines before and after, as
  text.
- **Speed or memory:** the measurement before and after, with its conditions.
- **No visible effect** (a fix inside, a refactor): the cases, as input, result
  on `main` and result on your branch, and the test that fails on `main` and
  passes on your branch. A refactor shows that the results stay the same.
- **Docs or CI:** a screenshot of the rendered page, or the link to the run that
  shows the new behaviour.

Say what produced each piece (build, game version, mods, command). If some
evidence cannot be made, say what is missing and why.

Drag images and videos into the description box, or attach them from the
command line: `gh pr create --attach ./after.png` (also `gh pr edit` and
`gh pr comment`), with `![After](./after.png)` in the body where it should
appear. In a public repository the files are public: crop out private paths and
other people's names.

By contributing you agree that your work is released under the repository's
license and that you follow the [code of conduct](CODE_OF_CONDUCT.md).
