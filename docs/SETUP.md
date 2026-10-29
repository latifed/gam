# Setup: Unity 6 + Claude Code

Do this on **your own computer** (the Unity Editor and Claude Code's Unity plugin run locally).

## 1. Install the tools

**Must have**
1. **Unity Hub**: <https://unity.com/download>
2. **Unity 6 LTS editor**, installed *from inside Unity Hub* (Installs → Install Editor → the newest **Unity 6 … LTS**). Tick these modules:
   - **Windows Build Support** (on Windows: Mono is enough; add IL2CPP later for release builds) / **Mac Build Support** (on a Mac)
   - **Linux Build Support** (optional: a native Steam Deck/Linux build; the Deck can also run Windows builds)
   - **Microsoft Visual Studio Community** (Windows, offered by the Hub) *or* skip it and use **JetBrains Rider** (free for non-commercial use) or **VS Code** with the Unity extension
   - Skip Android, iOS and WebGL.
3. **Git** with **Git LFS**: Windows: <https://git-scm.com> (includes LFS). Mac: `brew install git git-lfs`. Then once: `git lfs install`.
4. **Claude Code** on your computer: <https://code.claude.com/docs/en/setup>
5. **Unity's Claude Code plugin**: inside Claude Code run `/plugin`, find Unity's official plugin and install it (guide: <https://unity.com/blog/unity-plugin-for-claude-code>). Its live editor control needs a **Unity Cloud** account and Unity's **AI tools** trial or subscription. Check the price before you rely on it.

**Nice to have**
- **GitHub Desktop** (<https://desktop.github.com>) if you'd rather click than type git commands.
- **Aseprite** (about $20, the standard pixel-art tool; free if you compile it yourself) or **LibreSprite** (free) for editing sprites.

**Disk space:** plan for roughly 15–20 GB (editor, modules, project cache).

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

## 3b. Packages to add inside the project
*Window → Package Manager → Unity Registry.* The **Universal 2D** template already includes URP 2D, Sprite, Tilemap, 2D Animation and **2D Pixel Perfect**. Add:
- **Input System** (usually on by default in Unity 6): keyboard, mouse and controller (Steam Deck).
- **Cinemachine**: camera that follows the player, with its Pixel Perfect extension.
- **2D Tilemap Extras**: rule tiles for paths, fences, walls.
- Later, not now: **Steamworks.NET** (Steam achievements, cloud saves), when we make the demo build.

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
