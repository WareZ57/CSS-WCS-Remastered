# Changelog

## 1.0.0 — 2026-10-28

First release: Warcraft Source 0.78.5g.4g.3 for [CSS EventScripts Remastered](https://github.com/WareZ57/CSS-EventScripts-Remastered)
on Counter-Strike: Source as of 2025. Details: [docs/TECHNICAL.md](docs/TECHNICAL.md).

### Added

- `addons/eventscripts/_autoload/wcs.cfg`: WCS loads at server start, no `autoexec.cfg` change needed.
- `est_compat.smx`: es_tools commands used by WCS (`est_setgravity`, `est_getwallbetween`…).
- [docs/RACES.md](docs/RACES.md): the 12 races and their skills.

### Fixed

- `wcs_restriction` did not start (event hooked before WCS declares it).
- Hundreds of `DataTable warning` lines per minute from effects above the engine limits (`wcs_effects` clamps them).
- WCS admins erased at every restart (keygroup file name case).
- Admin example in the old `STEAM_0:x:y` SteamID format, which never matches on the current game.
- SourceMod plugins updated (deprecated `FindSendPropOffs` and `FCVAR_PLUGIN`, compile without warnings).

The crash when loading WCS was an EventScripts bug, fixed in CSS EventScripts Remastered 1.0.0.

## 0.78.5g.4g.3 Beta

The original release by Tha Pwned and kRypT0n!Te, kept unchanged in [original/](original).
