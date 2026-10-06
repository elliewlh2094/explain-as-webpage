# Pictorial Figures

A pictorial figure draws a concrete object, a body, or a container, so the reader sees *where* the parts are: what goes in which layer of a backpack, where the water of the body is, what a game object holds. Use it when position or containment carries the meaning. For causes, flows, and steps, use a mechanism figure (`svg-recipes.md`).

The object can be the real thing (a backpack) or a metaphor for an abstract one (a jar for a game object). A metaphor needs one sentence in the paragraph that says where it stops holding (`../explain-as-webpage/references/writing-rules.md` § Reader).

## Rules for every pictorial figure

These rules come from test drawings; each one prevents a failure that was seen.

- **Build the object from simple shapes**: rounded rectangles, circles, ellipses, and paths with straight lines and `Q` curves. Do not trace a detailed outline by hand: the shapes drift and the object looks broken. The label, not the detail, tells the reader what the object is.
- **Drawing left, notes right.** Put the object at x = 10–380 and the notes at x ≥ 430. Each note is one leader: a `pin` (r = 3) on the part, a horizontal `lead` line to x = 420, and the text at x = 430 (a bold line, and an `sm` line 20px below). Keep notes at least 40px apart vertically, one note per part, and never let two leaders cross.
- **Every `id` stays inside the figure's own `<svg><defs>`** and starts with the figure number (`f2-…`). A `clipPath` in the page's shared, hidden `<svg>` works in the browser, but the figure-only screenshot commands hide that block, and Chrome then ignores the clip: the drawing disappears.
- **Colours:** the outline is `outline` (text colour). A part that is a key concept takes its concept class (`box c1`, `area c1`); other parts are `box` or `box muted`. Semantic colours (`bad`, `good`, `warn`) only mark a problem or a fix, as in any figure.
- **Scale:** a drawing is a schematic. The caption says "示意，不按比例" / "Schematic, not to scale", unless the sizes come from data (then give the source, as for any number).
- **Icons** may label a part (`icons.md`), but the object itself is drawn, not an icon.
- **Notes stay in the figure.** The paragraph points to a part and says what to notice; it does not restate the notes (`../explain-as-webpage/references/writing-rules.md` § Figures and text, *Do not repeat the figure in the text*).
- **Check the screenshot for text on shapes.** The text bounds of a figure can be inside the canvas and still cover a shape or a line. Only the figure screenshot (`SKILL.md` § Self-check) shows this; move the label or shorten it.

## Recipe P1 — Layered container

A container cut open to show its layers: what goes where, and why. Clip the layers to the container's shape, then draw the outline on top.

```html
<figure id="fig-1">
<svg viewBox="0 0 720 380" role="img" aria-label="A backpack cut open in three layers: daily items on top, heavy items in the middle against the back, light bulky items at the bottom.">
  <defs><clipPath id="f1-body"><rect x="140" y="70" width="220" height="290" rx="30"/></clipPath></defs>
  <path class="outline" d="M225 54 Q250 22 275 54"/>
  <path class="box muted" d="M150 76 Q250 34 350 76 Z"/>
  <rect class="box muted" x="110" y="230" width="40" height="100" rx="10"/>
  <g clip-path="url(#f1-body)">
    <rect class="box c1" x="140" y="70" width="220" height="80"/>
    <rect class="box c2" x="140" y="150" width="220" height="110"/>
    <rect class="box c3" x="140" y="260" width="220" height="100"/>
  </g>
  <rect class="outline" x="140" y="70" width="220" height="290" rx="30"/>
  <text x="250" y="106" text-anchor="middle" class="b">Daily items</text><text x="250" y="126" text-anchor="middle" class="sm">torch, whistle, ID</text>
  <text x="250" y="201" text-anchor="middle" class="b">Heavy items</text><text x="250" y="221" text-anchor="middle" class="sm">water, canned food</text>
  <text x="250" y="306" text-anchor="middle" class="b">Light, bulky</text><text x="250" y="326" text-anchor="middle" class="sm">clothes, blanket</text>
  <text x="110" y="350" text-anchor="middle" class="sm">pocket</text>
  <circle class="pin" cx="340" cy="110" r="3"/><line class="lead" x1="340" y1="110" x2="420" y2="110"/>
  <text x="430" y="106" class="b">Top</text><text x="430" y="126" class="sm">used most; no digging</text>
  <circle class="pin" cx="340" cy="205" r="3"/><line class="lead" x1="340" y1="205" x2="420" y2="205"/>
  <text x="430" y="201" class="b">Middle, against the back</text><text x="430" y="221" class="sm">keeps the weight close to the body</text>
  <circle class="pin" cx="340" cy="310" r="3"/><line class="lead" x1="340" y1="310" x2="420" y2="310"/>
  <text x="430" y="306" class="b">Bottom</text><text x="430" y="326" class="sm">light items fill the base</text>
</svg>
<figcaption>Figure 1. Daily items on top, heavy items in the middle against the back, light items at the bottom. Schematic, not to scale.</figcaption>
</figure>
```

- 2–4 layers. A layer's height can follow a real share (and then says so); otherwise make the layers about equal.
- Other containers use the same steps: a cup (a path with straight sides), a cell (an ellipse), a building (a rectangle with a roof path).

### P1 with actors and flow arrows

When the question asks both where things sit and who reads or writes them, draw the actors outside the container and connect them to the layers with arrows. The arrows show the direction in which information moves. The notes about each layer go inside the layer, not on leader lines.

```html
<figure id="fig-4">
<svg viewBox="0 0 720 360" role="img" aria-label="A git repo folder in three layers: schema, wiki, and raw sources. On the left, the LLM follows the schema, reads the raw sources, and writes the wiki. On the right, you read the wiki, pick the raw sources, and revise the schema with the LLM.">
  <defs><clipPath id="f4-body"><rect x="240" y="60" width="240" height="280" rx="10"/></clipPath></defs>
  <path class="outline" d="M250 60 V46 Q250 36 260 36 H330 L346 60"/><text x="260" y="53" class="sm">git repo</text>
  <g clip-path="url(#f4-body)">
    <rect class="box c3" x="240" y="60" width="240" height="60"/>
    <rect class="box c1" x="240" y="120" width="240" height="130"/>
    <rect class="box c2" x="240" y="250" width="240" height="90"/>
  </g>
  <rect class="outline" x="240" y="60" width="240" height="280" rx="10"/>
  <text x="360" y="86" text-anchor="middle" class="b c3">schema</text><text x="360" y="106" text-anchor="middle" class="sm">CLAUDE.md / AGENTS.md</text>
  <text x="360" y="156" text-anchor="middle" class="b c1">wiki</text><text x="360" y="176" text-anchor="middle" class="sm">summary, entity, concept pages</text>
  <text x="360" y="196" text-anchor="middle" class="sm">index.md, log.md</text><text x="360" y="226" text-anchor="middle" class="sm">written only by the LLM</text>
  <text x="360" y="281" text-anchor="middle" class="b c2">raw/ sources</text><text x="360" y="301" text-anchor="middle" class="sm">articles, papers, images, data</text>
  <text x="360" y="321" text-anchor="middle" class="sm">read only; the source of truth</text>
  <rect class="box" x="10" y="150" width="120" height="60" rx="6"/>
  <text x="70" y="176" text-anchor="middle" class="b">LLM</text><text x="70" y="196" text-anchor="middle" class="sm">follows schema</text>
  <path class="line" d="M240 90 H70 V148" marker-end="url(#arr)"/><text x="155" y="82" text-anchor="middle" class="sm">rules</text>
  <path class="line" d="M240 300 H70 V212" marker-end="url(#arr)"/><text x="155" y="292" text-anchor="middle" class="sm">reads</text>
  <line class="line" x1="130" y1="180" x2="238" y2="180" marker-end="url(#arr)"/><text x="184" y="172" text-anchor="middle" class="sm">writes</text>
  <rect class="box" x="590" y="150" width="120" height="60" rx="6"/>
  <text x="650" y="176" text-anchor="middle" class="b">You</text><text x="650" y="196" text-anchor="middle" class="sm">pick, ask, judge</text>
  <line class="line" x1="480" y1="180" x2="588" y2="180" marker-end="url(#arr)"/><text x="534" y="172" text-anchor="middle" class="sm">reads</text>
  <path class="line" d="M650 212 V300 H482" marker-end="url(#arr)"/><text x="566" y="292" text-anchor="middle" class="sm">picks sources</text>
  <path class="line" d="M650 148 V90 H482" marker-end="url(#arr)"/><text x="566" y="82" text-anchor="middle" class="sm">revises with the LLM</text>
</svg>
<figcaption>Figure 4. Information flows from the raw sources through the LLM into the wiki and on to you; the only arrow into the wiki comes from the LLM. Folder names are illustrative.</figcaption>
</figure>
```

- The container keeps the P1 coordinates, moved to x = 240–480; one actor box (120 × 60) on each side at x = 10 and x = 590.
- At most 3 arrows per side. Route them so they never cross: the top one leaves above the actor, the middle one is straight, the bottom one leaves below.
- Each arrow ends at a layer edge and has one verb in `sm` above its horizontal part.
- The paragraph says which arrows to compare ("only one arrow reaches the wiki"), not what each arrow says.

## Recipe P2 — Silhouette with leaders

A figure of a person (or an animal, a vehicle) with a filled region and notes. Define the shapes once in `<defs>` and draw them three times:

1. `<use class="edge">`: every shape with a thick outline;
2. `<use class="shape">`: the same shapes filled, without outline. This covers the inner lines where shapes overlap, so only the outer edge of the whole figure stays;
3. `<use class="area">` clipped by a rectangle: the filled region (a level, a zone).

```html
<figure id="fig-2">
<svg viewBox="0 0 720 400" role="img" aria-label="A person filled with water to about 60 percent of the height; a bar splits the body water into intracellular fluid, about two thirds, and interstitial fluid and plasma, about one third.">
  <defs>
    <g id="f2-person">
      <circle cx="150" cy="60" r="28"/><rect x="105" y="95" width="90" height="150" rx="20"/>
      <rect x="78" y="100" width="24" height="135" rx="12"/><rect x="198" y="100" width="24" height="135" rx="12"/>
      <rect x="108" y="230" width="38" height="150" rx="16"/><rect x="154" y="230" width="38" height="150" rx="16"/>
    </g>
    <clipPath id="f2-level"><rect x="70" y="170" width="160" height="220"/></clipPath>
  </defs>
  <use href="#f2-person" class="edge"/>
  <use href="#f2-person" class="shape"/>
  <use href="#f2-person" class="area" clip-path="url(#f2-level)"/>
  <line class="line dash" x1="70" y1="170" x2="250" y2="170"/>
  <text x="260" y="166" class="b">Body water ≈ 60%</text><text x="260" y="186" class="sm">of body weight (adult)</text>
  <path class="lead" d="M440 110 V100 H610 V110"/><text x="525" y="92" text-anchor="middle" class="sm">2/3 of body water</text>
  <path class="lead" d="M610 110 V100 H700 V110"/><text x="655" y="92" text-anchor="middle" class="sm">1/3</text>
  <rect class="box c1" x="440" y="120" width="170" height="60"/>
  <rect class="box c2" x="610" y="120" width="70" height="60"/>
  <rect class="box c3" x="680" y="120" width="20" height="60"/>
  <text x="525" y="146" text-anchor="middle" class="b">Intracellular</text><text x="525" y="166" text-anchor="middle" class="sm">≈ 40% of weight</text>
  <circle class="pin" cx="645" cy="150" r="3"/><line class="lead" x1="645" y1="150" x2="645" y2="220"/>
  <text x="645" y="240" text-anchor="middle" class="b">Interstitial</text><text x="645" y="260" text-anchor="middle" class="sm">≈ 15%</text>
  <circle class="pin" cx="690" cy="150" r="3"/><line class="lead" x1="690" y1="150" x2="690" y2="290"/>
  <text x="700" y="310" text-anchor="end" class="b">Plasma</text><text x="700" y="330" text-anchor="end" class="sm">≈ 5%</text>
  <path class="line dash" d="M230 320 H525 V184" marker-end="url(#arr)"/>
  <text x="380" y="312" text-anchor="middle" class="sm">split the 60%</text>
</svg>
<figcaption>Figure 2. Most of the body's water is inside the cells; the plasma in the blood vessels is a small part. Schematic; shares are textbook approximations.</figcaption>
</figure>
```

- The clip rectangle sets the level: here its top is at y = 170, about 60% of the figure's height (y = 32 to 380).
- Here the notes sit on a bar to the right instead of single leaders, because the three parts are shares of one whole. The bar widths follow the shares (2/3, 1/4 and 3/4 of the remaining 1/3, rounded to the 10px grid).
- The figure has no face, hands, or clothes. A person drawn from rounded rectangles reads like a mannequin; that is enough for an explainer and stays stable.

## Recipe P3 — Object and its parts

An object drawn as a container with labelled parts inside, for "what is it made of" questions. A metaphor fits here: a jar is a game object, the things in it are its components.

```html
<figure id="fig-3">
<svg viewBox="0 0 720 380" role="img" aria-label="A jar stands for a GameObject: the lid holds its name; inside are a Transform, a Mesh Renderer, a Box Collider, and a script, each with one job.">
  <rect class="box muted" x="160" y="40" width="180" height="30" rx="6"/>
  <text x="250" y="60" text-anchor="middle" class="b">GameObject: Player</text>
  <path class="outline" d="M170 70 V90 Q120 90 120 130 V330 Q120 360 150 360 H350 Q380 360 380 330 V130 Q380 90 330 90 V70"/>
  <rect class="box" x="150" y="120" width="200" height="44" rx="6"/>
  <use href="#i-move-3d" class="icon" x="162" y="132" width="20" height="20"/><text x="194" y="147" class="b">Transform</text>
  <rect class="box" x="150" y="174" width="200" height="44" rx="6"/>
  <use href="#i-eye" class="icon" x="162" y="186" width="20" height="20"/><text x="194" y="201" class="b">Mesh Renderer</text>
  <rect class="box" x="150" y="228" width="200" height="44" rx="6"/>
  <use href="#i-square-dashed" class="icon" x="162" y="240" width="20" height="20"/><text x="194" y="255" class="b">Box Collider</text>
  <rect class="box c1" x="150" y="282" width="200" height="44" rx="6"/>
  <use href="#i-file-code" class="icon c1" x="162" y="294" width="20" height="20"/><text x="194" y="309" class="b c1">PlayerMove.cs</text>
  <circle class="pin" cx="340" cy="55" r="3"/><line class="lead" x1="340" y1="55" x2="420" y2="55"/>
  <text x="430" y="59" class="sm">name, tag, layer (the lid)</text>
  <circle class="pin" cx="340" cy="142" r="3"/><line class="lead" x1="340" y1="142" x2="420" y2="142"/>
  <text x="430" y="146" class="sm">position, rotation, scale</text>
  <circle class="pin" cx="340" cy="196" r="3"/><line class="lead" x1="340" y1="196" x2="420" y2="196"/>
  <text x="430" y="200" class="sm">draws the mesh on screen</text>
  <circle class="pin" cx="340" cy="250" r="3"/><line class="lead" x1="340" y1="250" x2="420" y2="250"/>
  <text x="430" y="254" class="sm">gives the collision shape</text>
  <circle class="pin" cx="340" cy="304" r="3"/><line class="lead" x1="340" y1="304" x2="420" y2="304"/>
  <text x="430" y="308" class="sm">your script: the behaviour</text>
</svg>
<figcaption>Figure 3. A GameObject is an empty, named jar; what it can do depends on the components put into it.</figcaption>
</figure>
```

- Part boxes are 200 × 44 with 10px between them; at most 5 parts. With more, group them, or use summary cards (`cards.md`).
- Single-line notes (`sm` only) are enough when the part's label already names it.
- The icons need their symbols on the page: run the copy command in `icons.md`.

## Recipe P4 — Interface layout

A software window drawn as a container: its panels as rectangles in their real positions, and the user's action as one dashed arrow. Use it for "which panel does what" and "where do I drag this" questions.

```html
<figure id="fig-5">
<svg viewBox="0 0 720 360" role="img" aria-label="The Unity editor: Hierarchy on the left lists the objects in the scene, the Scene and Game view in the middle shows the result, the Inspector on the right shows the components of the selected object, and Project at the bottom holds the files. A dashed arrow drags bird.png from Project into the Sprite field in the Inspector.">
  <rect class="box muted" x="10" y="20" width="700" height="30" rx="4"/>
  <path class="box good" d="M352 28 L366 35 L352 42 Z"/><text x="380" y="40" class="sm">Play: test the game</text>
  <rect class="box" x="10" y="50" width="160" height="200"/>
  <text x="20" y="72" class="b">Hierarchy</text><text x="20" y="92" class="sm">objects in the scene</text>
  <text x="30" y="122" class="sm">Main Camera</text><text x="30" y="144" class="b c1">bird</text>
  <rect class="box" x="170" y="50" width="360" height="200"/>
  <text x="180" y="72" class="b">Scene / Game View</text><text x="180" y="92" class="sm">editing view / what the camera sees</text>
  <circle class="area c1" cx="350" cy="170" r="22"/>
  <rect class="box" x="530" y="50" width="180" height="290"/>
  <text x="540" y="72" class="b">Inspector</text><text x="540" y="92" class="sm">the selected object</text>
  <text x="540" y="122" class="b c1">bird</text>
  <rect class="box c2" x="540" y="134" width="160" height="30" rx="4"/><text x="550" y="154" class="sm">Transform</text>
  <rect class="box c2" x="540" y="172" width="160" height="56" rx="4"/><text x="550" y="192" class="sm">Sprite Renderer</text>
  <rect class="box muted" x="550" y="200" width="140" height="20" rx="3"/><text x="556" y="215" class="sm">Sprite: bird</text>
  <text x="540" y="256" class="sm">+ Add Component</text>
  <rect class="box" x="10" y="250" width="520" height="90"/>
  <text x="20" y="272" class="b">Project</text><text x="20" y="292" class="sm">every file: images, sounds, scripts, fonts</text>
  <use href="#i-image" class="icon" x="30" y="304" width="20" height="20"/><text x="56" y="320" class="sm">bird.png</text>
  <path class="line dash" d="M60 328 H480 Q510 328 510 298 V210 H548" marker-end="url(#arr)"/>
  <text x="340" y="320" text-anchor="middle" class="sm">drag into the Sprite field</text>
</svg>
<figcaption>Figure 5. Each panel does one job: Project holds files, Hierarchy lists objects, the Inspector changes the selected one, and the view shows the result. Schematic layout, not a screenshot.</figcaption>
</figure>
```

- Put each panel's name and one `sm` line inside the panel, not on leader lines: the panels fill the canvas.
- Panels are neutral `box`; the selected object and the field the action changes take their concept colours.
- One action per figure, as one dashed arrow that does not cross any label.
- The caption says "Schematic layout, not a screenshot" / "版面為示意，不是實際截圖". If the reader must find a real button, a screenshot is clearer: ask the user for one from their own copy of the program.
