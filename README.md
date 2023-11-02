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
```

## Outputs

The following outputs are available:

```yaml
files:
  description: The SVG files that have been converted
  type: array
  items: strings
```