# SVG dark-mode action

Add style to SVG(s) to invert colours based on `prefers-color-scheme`.

Basically adds the following CSS to the SVG:

```css
@media (prefers-color-scheme: dark) {
    svg {
        filter: invert(100%)
    }
}
```

## Options

The following options are available:

```yaml
inputs:
  description: "SVG files to convert"
  required: true
  type: array
  items: string
excluded:
  description: "Glob(s) to exclude from matching the inputs"
  required: false
  type: array
  items: string
include-hidden:
  description: "Also match hidden files and directories (starting with a '.') with wildcards such as '*' and '**', for both inputs and excluded"
  required: false
  type: boolean
  default: false
```

A glob that matches nothing is a warning, not an error. Files that are already converted are left as they are, so the task can run again.

## Outputs

The following outputs are available:

```yaml
files:
  description: The SVG files that have been converted
  type: array
  items: string
```

- `files`: the converted files, relative to the working directory and always with `/` (also on Windows).

## Releases

Releases are automated with [semantic-release](https://semantic-release.gitbook.io/). Pull requests are squash merged, so the PR title becomes the commit on `main` and must follow [Conventional Commits](https://www.conventionalcommits.org/) (checked on every PR):

| PR title | Release |
|----------|---------|
| `fix: ...`, `perf: ...` | patch (1.2.3 → 1.2.4) |
| `feat: ...` | minor (1.2.3 → 1.3.0) |
| `!` after the type (e.g. `feat!: ...`, `refactor!: ...`) or a `BREAKING CHANGE:` footer | major (1.2.3 → 2.0.0) |
| `docs:`, `chore:`, `ci:`, `build:`, `refactor:`, `test:`, `style:`, `revert:` | no release |

On every merge to `main` the next version is determined, tagged (`vX.Y.Z`) and a GitHub release is created. The major tag (e.g. `v1`) is moved to the new release, so `uses: svg-darkmode@v1` always gets the newest 1.x version.

Because the major tag moves, `git pull` in an existing clone can fail with `! [rejected] v1 -> v1 (would clobber existing tag)`. Update the tags once with `git fetch --tags --force` and pull again.
