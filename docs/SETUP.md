# Setup: Unity 6 + Claude Code

Do this on **your own computer** (the Unity Editor and Claude Code's Unity plugin run locally).

## 1. Install the tools
1. **Unity Hub** → install the latest **Unity 6 LTS** editor. Add build support for your OS (Windows / Mac / Linux).
2. **Git** and **Git LFS** (Large File Storage, for art and audio). After installing LFS, run once:
   ```bash
   git lfs install
   ```
3. **Claude Code** on your computer.

## 2. Get the repo
```bash
git clone https://github.com/latifed/gam.git
```
```bash
cd gam
```
```bash
git checkout claude/peaceful-ritchie-ucadgx
```

## 3. Create the Unity project
1. Unity Hub → **New project** → template **Universal 2D** (2D with URP).
2. Project name: **Hollowmere**. Location: the `gam` folder you just cloned.
   → the project ends up in `gam/Hollowmere/`, next to `docs/`.
3. In the editor, check *Edit → Project Settings → Editor*: **Asset Serialization = Force Text** and **Visible Meta Files** (both are the default in Unity 6).

## 4. Pixel-art settings (Stardew / Graveyard Keeper look)
- Import sprites with **Filter Mode = Point (no filter)**, **Compression = None**, **Pixels Per Unit = 16**.
- Add a **Pixel Perfect Camera** to the main camera (Reference Resolution e.g. 480×270, scales cleanly to 1080p and 4K).
- Use a **Tilemap** (Grid + Tilemap) for the town ground, paths and walls.

## 5. Connect Claude Code to Unity
- Install Unity's **official Claude Code plugin** (released Sept 2026) from Claude Code's plugin directory (the `/plugin` command), and follow Unity's guide: <https://unity.com/blog/unity-plugin-for-claude-code>.
- Its live editor control needs **Unity 6+**, a **Unity Cloud** connection, and Unity's **AI tools** (trial or subscription). Check the price first.
- Start Claude Code **inside the `gam` folder**, so it sees both the design docs and the Unity project.

## 6. First commit
```bash
git add .
```
```bash
git commit -m "Create Unity project"
```
```bash
git push
```
`.gitignore` already skips Unity's generated folders (`Library/`, `Temp/`, `Logs/`...), and `.gitattributes` sends art and audio in `Hollowmere/` through Git LFS.
