# CSS WCS Remastered

**Warcraft Source (WCS) 0.78, the EventScripts mod, running again on today's Counter-Strike: Source.**

Warcraft Source brings Warcraft III to Counter-Strike: Source: pick a race (Undead Scourge, Human Alliance, Orcish Horde,
Night Elves, Blood Mage, Crypt Lord…), earn XP with kills, level up, spend points in skills, trigger your ultimate,
buy items in the shop. It was one of the most played EventScripts mods: written by Kryptonite in 2007, ported to Python
in 2010, last released as 0.78.5g.4g.3.

This repository is a drop-in add-on for [**CSS EventScripts Remastered**](https://github.com/WareZ57/CSS-EventScripts-Remastered),
the EventScripts 2.1.1 build fixed for the current engine. Once EventScripts Remastered is installed, copy the `cstrike/`
folder of this repository onto your server and WCS starts by itself.

## Status

Tested on a clean dedicated server installed the classic way (Ubuntu 22.04, `./srcds_run`): CSS EventScripts Remastered,
Metamod:Source 1.12 and SourceMod 1.12 installed by hand, then this `cstrike/` folder copied over, no other change.

| Test | Result |
|---|---|
| WCS starts by itself at server start | 56 modules loaded, no error |
| All 12 races at level 40 (every skill maxed), ultimates and abilities triggered | no error, no crash |
| Skill damage, effects, XP, levels, skill points, SQLite database | working (players, races, levels and XP saved) |
| SourceMod plugins (`wcs_effects`, `wcs_restriction`, `wcs_gamename`, `est_compat`) | loaded, no SourceMod error log |
| Admin file kept across restarts | fixed and verified |
| EventScripts data checks running alongside WCS ([`verify_data`](https://github.com/WareZ57/CSS-EventScripts-Remastered/tree/main/test-addons/verify_data)) | engine, props and events always agree; frags, deaths and scores follow the game rules |

These tests were run with bots. The menus (`changerace`, `wcsmenu`, `shopmenu`…) are sent with EventScripts' popup
library, which does not send menus to bots: their display was not checked by a human player during these tests.

## Requirements

1. A Linux Counter-Strike: Source server with [**CSS EventScripts Remastered**](https://github.com/WareZ57/CSS-EventScripts-Remastered)
   installed (see its README: Linux, 32-bit `srcds_linux`).
2. [Metamod:Source 1.12](https://www.sourcemm.net/downloads.php?branch=stable) and
   [SourceMod 1.12](https://www.sourcemod.net/downloads.php?branch=stable): WCS uses SourceMod plugins for its visual
   effects and weapon restrictions. Tested with Metamod:Source 1.12.0-git1228 and SourceMod 1.12.0.7255.

## Installation

1. Install CSS EventScripts Remastered, Metamod:Source and SourceMod.
2. Copy the `cstrike/` folder of this repository over the `cstrike/` folder of your server (merge the folders).
3. Restart the server.

Nothing else to edit: `addons/eventscripts/_autoload/wcs.cfg` makes EventScripts load WCS at every start. Check in the
server console:

- the startup log shows `[EventScripts] Loaded wcs/...` lines;
- `sm plugins list` lists `[Port] wcs_effects`, `WCS - Restrictions`, `Warcraft Source - GameInfo` and `est_compat`.

`est_compat.smx` is the same plugin as in EventScripts Remastered's `optional/` folder; overwriting it is fine.
To disable WCS, delete `addons/eventscripts/_autoload/wcs.cfg` (or run `es_unload wcs`).

## Playing

Every command works in the chat (`changerace`) and in the console. The 12 races, their skills and effects:
[docs/RACES.md](docs/RACES.md).

| Command | Effect |
|---|---|
| `wcsmenu` (or `wcs`) | main menu |
| `changerace` | choose your race (some races need a minimum total level) |
| `spendskills` | spend your skill points |
| `resetskills` | reset your skill points |
| `shopmenu` / `shopinfo` | item shop / item descriptions |
| `showxp`, `showskills`, `playerinfo`, `raceinfo` | your XP, your skills, info on a player, info on a race |
| `wcsrank`, `wcstop` | your rank, the top players |
| `wcshelp` | help |
| `ultimate` | triggers your ultimate: bind it to a key, `bind x ultimate` |
| `ability` | triggers your ability (races that have one): `bind c ability` |

## Configuration

- `addons/eventscripts/wcs/config/config.cfg` is created at the first start: XP per kill, headshot, knife and round,
  XP for bots, maximum level, shop, texts, effects, database… Restart after editing it.
- Races, items and shop categories: `addons/eventscripts/wcs/ini/` (`races.ini`, `items.ini`, `racecats.ini`);
  `wcs_reload_races` reloads `races.ini` without a restart. Ultimates: `addons/eventscripts/wcs/tools/ultimates/`.
- Optional modules (deathmatch, gold, levelbank, VIP, random race…) are switched on in
  `addons/eventscripts/wcs/config/addons.cfg`; tools in `config/tools.cfg`.
- Player data is stored in SQLite (`addons/eventscripts/wcs/data/players.sqlite`); a MySQL connection module exists
  (`addons/mysql_connection`, not tested).
- **Admins**: copy `addons/eventscripts/wcs/data/es_WCSadmins_db.example.txt` to `es_WCSadmins_db.txt` in the same folder
  and replace the SteamID with yours. Use the SteamID format the current game uses, `[U:1:123456789]`, as shown by the
  `status` console command; the old `STEAM_0:x:y` format of WCS-era documentation is never matched. The same applies to
  the `gold` module's admin file and to the `allowonly` field of `races.ini`.

## What was fixed

WCS needed fixes in EventScripts itself, made in CSS EventScripts Remastered, and a few in WCS and its SourceMod plugins.
Details: [docs/TECHNICAL.md](docs/TECHNICAL.md). The changes against the original archive are in
[`original/changes-vs-0.78.5g.4g.3.patch`](original/changes-vs-0.78.5g.4g.3.patch).

| Problem | Fix |
|---|---|
| Loading WCS crashed the server (Python heap corruption) | EventScripts bug from 2013 (nested `es.*` return values), fixed in EventScripts Remastered 1.0.0 |
| `wcs_restriction` did not start: it hooked the `wcs_changerace` event before WCS declares it | the hook is retried until the event exists |
| Hundreds of `DataTable warning: Out-of-range value` per minute: WCS effects use radii, widths and amplitudes above the engine limits | `wcs_effects` clamps them to the limits (4096, 128, 64); same look, no warnings |
| WCS admins erased at every restart: the engine saves keygroup files in lower case, WCS looked for `es_WCSadmins_db.txt` and recreated an empty list | admin and group files are looked up case-insensitively |
| The admin example used the old `STEAM_0:x:y` format, which never matches today | example converted to `[U:1:…]` |
| WCS had to be added to `autoexec.cfg` by hand | `_autoload/wcs.cfg` loads it |
| `est_setgravity` and other es_tools commands missing (es_tools binary dead) | `est_compat` plugin included |
| SourceMod plugins: deprecated calls (`FindSendPropOffs`, `FCVAR_PLUGIN`), warnings | updated, compile with warnings treated as errors |

## Limitations

- Linux only, 32-bit server only: the limits of [CSS EventScripts Remastered](https://github.com/WareZ57/CSS-EventScripts-Remastered#limitations).
- Menus not checked by a human player during the tests (see [Status](#status)).
- SPE (Source Python Extensions) does not exist anymore: WCS uses its fallbacks, as it was designed to.
- The MySQL module was not tested.
- `getplayerlocation, invalid userid` can appear in the console when an effect script reads the attacker of damage that
  has none (fall damage): harmless, as in the original.

## Repository content

```
cstrike/addons/eventscripts/wcs/        WCS 0.78.5g.4g.3 (with the fixes above)
cstrike/addons/eventscripts/_libs/      playerviewlib and saytextlib, libraries used by WCS
cstrike/addons/eventscripts/_autoload/  wcs.cfg, loads WCS at server start
cstrike/addons/sourcemod/plugins/       wcs_effects, wcs_restriction, wcs_gamename, est_compat (compiled)
cstrike/addons/sourcemod/scripting/     their sources
docs/                                   races, technical details
original/                               the original WCS archive and the patch against it
licenses/                               GPL v3 (SourceMod plugins)
```

The SourceMod plugins are compiled with SourceMod 1.12 (`spcomp64 <plugin>.sp`); the
[GitHub Actions workflow](.github/workflows/build.yml) builds them and checks the Python syntax of WCS on every push.

## Credits

- **Kryptonite** — original author of Warcraft Source (v0.77, December 2007) and of most races.
- **Tha Pwned and kRypT0n!Te** — Python port (2010) and the 0.78 releases.
- **The WCS team and contributors**, credited in WCS' documentation and changelog: Freddukes (parts of SourceRPG),
  Craziest (top 10), Fast.Food and soundn3ko (races), Jareth and Holliday (effects), Don Revan / Revan
  (`wcs_restriction`, `wcs_gamename`, effects of wcs-lagerhaus.de), joshtrav (`wcs_effects`), Kami, Muerte, MiB, Lukas,
  DoCky (playerview), GodJonez, Maxolahird (Portuguese), Jhonam (Russian), dAn!EL and Pookzabazz.
- **Mattie Casper** — EventScripts.
- **AlliedModders** — Metamod:Source and SourceMod.

## License

Warcraft Source was published freely by its authors without an explicit license; it is redistributed here as published,
with its credits, and every change is listed in [`original/`](original). The SourceMod plugins are released under the
GNU GPL v3, as SourceMod plugins are ([licenses/GPL-3.0.txt](licenses/GPL-3.0.txt)).

Warcraft is a trademark of Blizzard Entertainment. This fan project is not affiliated with Blizzard, Valve or the former
WCS team.
