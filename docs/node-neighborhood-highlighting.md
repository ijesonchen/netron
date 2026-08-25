# Node Neighborhood Highlighting

## Status

- State: ready for review
- Last updated: 2026-08-26
- Scope: one-hop graph relationship tracing

## Behavior

Selecting a graph node highlights its directly connected neighborhood:

- direct input nodes and their edges are green;
- direct output nodes and their edges are red;
- the selected node keeps Netron's existing selection style;
- unrelated nodes and edges keep their original style;
- selecting another node clears the previous neighborhood;
- clearing the selection clears all neighborhood highlights.

The traversal is intentionally limited to one hop. Users can follow a longer
path by selecting each adjacent node in sequence. This keeps interaction
predictable and avoids coloring an entire large graph.

Zooming, panning, edge hover, sidebars, and the existing graph layout behavior
remain unchanged. Neighborhood colors persist while the graph is zoomed.

## Implementation

| Area | File | Responsibility |
| --- | --- | --- |
| Selection state | `source/view.js` | Finds incoming and outgoing rendered edges, applies directional classes, and clears stale highlights. |
| SVG markers | `source/grapher.js` | Defines separate arrowheads for input and output highlights. |
| Visual styles | `source/grapher.css` | Defines green input and red output styles for light and dark themes. |
| Browser regression | `test/browser.spec.js` | Verifies colors, edge direction, zoom persistence, and selection changes. |
| Test graph | `test/neighborhood.dot` | Provides input, output, branch, and disconnected-node coverage. |

## Validation

- ESLint passes for the modified JavaScript files.
- `git diff --check` passes.
- The focused Playwright browser test reports `1 passed`.
- Manual browser inspection confirms green input nodes and edges, red output
  nodes and edges, unchanged disconnected nodes, and retained colors after
  zooming.
- A large TensorFlow graph with 29,454 logical nodes and 33,995 logical edges
  loads with the feature enabled. Full-graph layout time remains governed by
  Netron's existing layout implementation.

## Update Log

| Date | Update |
| --- | --- |
| 2026-08-26 | Allowed SemVer prerelease and build metadata in Browser and Electron version validation so custom builds such as `9.2.2+cjx.20260826` can start. |
| 2026-08-26 | Added one-hop directional highlighting, theme-aware colors, zoom persistence coverage, selection cleanup coverage, and the browser test fixture. |
