# Node Neighborhood Highlighting

## Status

- State: ready for review
- Last updated: 2026-09-03
- Maintained branch: `cjxai/dev`
- Scope: one-hop graph relationship tracing and custom model parser selection

## Behavior

Selecting a graph node highlights its directly connected neighborhood:

- direct input nodes and their edges are green;
- direct output nodes and their edges are red;
- the selected node uses a thicker blue border;
- unrelated nodes and edges keep their original style;
- selecting another node clears the previous neighborhood;
- clearing the selection clears all neighborhood highlights.

The traversal is intentionally limited to one hop. Users can follow a longer
path by selecting each adjacent node in sequence. This keeps interaction
predictable and avoids coloring an entire large graph.

Zooming, panning, edge hover, sidebars, and the existing graph layout behavior
remain unchanged. Neighborhood colors persist while the graph is zoomed.

## Parser Selection

The Python CLI and API accept an optional parser name:

```bash
netron --parser tf /path/to/model
```

```python
netron.start("/path/to/model", parser="tf")
```

The browser URL form also accepts `parser=tf`. A forced parser is the only
model factory considered for the top-level file. Unknown parser names fail
without attempting a dynamic module import.

Files without an extension are tried as TensorFlow binary protobuf before
other extensionless formats. This allows TensorFlow `GraphDef` artifacts named
`frozen_graph` to open directly. Explicit `--parser tf` also treats an
unrecognized filename extension as binary protobuf while retaining the normal
TensorFlow content checks.

## Build and Install

The maintained branch stores its custom package version in `package.json`.
Build the Python wheel from a clean `cjxai/dev` checkout:

```bash
version=$(python3 -c 'import json; print(json.load(open("package.json"))["version"])')
python3 package.py build version
mkdir -p "dist/artifacts/${version}"
python3 -m pip wheel \
  --no-deps \
  --no-build-isolation \
  --wheel-dir "dist/artifacts/${version}" \
  ./dist/pypi
(
  cd "dist/artifacts/${version}"
  sha256sum "netron-${version}-py3-none-any.whl" > SHA256SUMS
  sha256sum -c SHA256SUMS
)
```

Replace the system Python package with the verified wheel:

```bash
python3 -m pip install \
  --force-reinstall \
  --no-deps \
  "dist/artifacts/${version}/netron-${version}-py3-none-any.whl"
netron --version
```

An already-running Netron process keeps its loaded code and must be restarted
by its owner. The wheel is retained outside the task worktree at:

```text
/root/dev/agent_workspace/tmp/netron-artifacts/node-neighborhood-highlight-d07c6b3b/9.2.2+cjx.20260902.1/
```

The retained wheel SHA-256 is
`0f63c5b486074333c65310980c02b0b657da54c605e1fab189cdc249095d3894`.

## Implementation

| Area | File | Responsibility |
| --- | --- | --- |
| Python parser option | `source/__init__.py`, `source/server.py` | Exposes `--parser` and transfers the selected parser to the browser. |
| Parser routing | `source/browser.js`, `source/view.js` | Carries the parser through the load context and limits factory selection. |
| Extensionless GraphDef | `source/tf.js` | Applies TensorFlow binary protobuf detection to extensionless files. |
| Parser regressions | `test/parser.py`, `test/browser.spec.js` | Covers parser metadata, validation, forced selection, and extensionless GraphDef rendering. |
| Selection state | `source/view.js` | Finds incoming and outgoing rendered edges, applies directional classes, and clears stale highlights. |
| SVG markers | `source/grapher.js` | Defines separate arrowheads for input and output highlights. |
| Visual styles | `source/grapher.css` | Defines green input, blue selection, and red output styles for light and dark themes. |
| Browser regression | `test/browser.spec.js` | Verifies colors, edge direction, zoom persistence, and selection changes. |
| Test graph | `test/neighborhood.dot` | Provides input, output, branch, and disconnected-node coverage. |

## Validation

- ESLint passes for the modified JavaScript files.
- `git diff --check` passes.
- The 2026-08-26 focused neighborhood-highlighting Playwright test reported
  `1 passed`.
- Manual browser inspection confirms green input nodes and edges, a blue
  selected node, red output nodes and edges, unchanged disconnected nodes, and
  retained colors after zooming.
- A large TensorFlow graph with 29,454 logical nodes and 33,995 logical edges
  loads with the feature enabled. Full-graph layout time remains governed by
  Netron's existing layout implementation.
- The packaged Python build `9.2.2+cjx.20260826` renders that graph and marks
  one direct input node and edge green and one direct output node and edge red
  when selecting a node with both relationships.
- The packaged and system-installed build `9.2.2+cjx.20260902.1` accepts
  `--parser tf` and directly renders the extensionless EXP-004/A
  `frozen_graph` as a TensorFlow graph with 1,007 main-graph nodes and two
  FunctionDef graph entries.
- Full ESLint, Python syntax, Python server metadata, isolated wheel install,
  model-factory smoke, and browser rendering checks pass. The repository
  Playwright tests were not run because their pinned Chromium revision is not
  installed; browser-tool validation covered the same new loading paths.
- Zooming from `1.0x` to `1.1x` preserves the selected node and all four
  directional highlight classes.
- The earlier neighborhood validation input was normalized from a
  length-delimited GraphDef wrapper before loading. The 2026-09-02 parser
  validation instead opened the original extensionless `frozen_graph`
  directly.

## Update Log

| Date | Update |
| --- | --- |
| 2026-09-02 | Added explicit parser selection and direct TensorFlow GraphDef detection for extensionless files such as `frozen_graph`; moved the maintained custom build branch to `cjxai/dev`. |
| 2026-08-26 | Distinguished the selected node with a thicker blue border and aligned directional styles across light, dark, and nested graph views. |
| 2026-08-26 | Validated the packaged build on a large TensorFlow graph, including bidirectional coloring and zoom persistence. |
| 2026-08-26 | Allowed SemVer prerelease and build metadata in Browser and Electron version validation so custom builds such as `9.2.2+cjx.20260826` can start. |
| 2026-08-26 | Added one-hop directional highlighting, theme-aware colors, zoom persistence coverage, selection cleanup coverage, and the browser test fixture. |
