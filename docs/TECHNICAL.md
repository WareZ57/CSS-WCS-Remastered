# Technical details

What it took to run WCS 0.78.5g.4g.3 on the current Counter-Strike: Source (2025 engine branch, `ServerVersion 11003710`),
on top of [CSS EventScripts Remastered](https://github.com/WareZ57/CSS-EventScripts-Remastered). The full list of
changes against the original archive is [`original/changes-vs-0.78.5g.4g.3.patch`](../original/changes-vs-0.78.5g.4g.3.patch).

## Fixed in EventScripts

WCS is the addon that revealed the worst EventScripts bug: loading it crashed the server in `PyObject_Malloc`, every time,
while Python compiled an unrelated file. The cause was in the EventScripts core: every `es.*` function returns the shared
`g_pPyReturn` without resetting it, so when `wcs/tools/abilitys/warden` loaded `wcs/addons/cmdskillspy` with `es.load`,
and `cmdskillspy` read the spawn points with `es.entitygetvalue`, `es.load` returned the spawn point string a second
time, and Python freed it one time too many. The fix lives in EventScripts Remastered's loader (see its
[TECHNICAL.md](https://github.com/WareZ57/CSS-EventScripts-Remastered/blob/main/docs/TECHNICAL.md), bug 3). The other
EventScripts fixes WCS relies on: stack alignment for Python calls into the engine, lower-case folder links, UTF-8
commands, and the corelib `while` loop.

## wcs_restriction did not start

`wcs_restriction.smx` handles weapon restrictions (`wcs_restrict` / `wcs_unrestrict`). In `OnPluginStart` it called
`HookEvent("wcs_changerace")`, but that event is declared by WCS (`wcs/events/events.res`) when EventScripts loads it,
which happens after SourceMod plugins start. `HookEvent` on an unknown event is a fatal error: the plugin never loaded.
It now uses `HookEventEx`, retried by the plugin's existing 0.6-second timer until the event exists.

## Effect values above the engine limits

WCS effects (rings, beams) use values such as an end radius of 5000, a width of 900 or an amplitude of 255. The temp
entity network properties are limited to 4096, 128 and 64; the engine clamps the values and prints
`DataTable warning: Out-of-range value ... clamping` for each one, hundreds of lines per minute during games.
`wcs_effects.smx` (which provides `est_effect`) now clamps radii, widths and amplitudes before sending them: same visual
result, quiet console.

## Admins erased at every restart

`core/admin` loaded the admins with:

```python
if not os.path.isfile(os.path.join(wcs.wcs.ini.path, 'data', 'es_WCSadmins_db.txt')):
    es.keygroupcreate('WCSadmins')
    self.save()
es.keygroupload('WCSadmins', '|wcs/data')
```

The current engine filesystem writes a new keygroup file with a lower-case name (`es_wcsadmins_db.txt`) and finds files
case-insensitively, but Python's `isfile` is case-sensitive. When the file did not exist yet, WCS saved an empty list as
`es_wcsadmins_db.txt`; at the next start `isfile` did not see it, so WCS created an empty keygroup again and saved it over
the file: every admin added in game was lost. `core/admin` and `core/group` now look the file up case-insensitively
(verified: an admin entry survives a restart and is read by WCS).

## SteamID format

The current game reports SteamIDs as `[U:1:123456789]` (`es.getplayersteamid`), while WCS-era files use
`STEAM_0:Y:Z`. WCS compares the strings as they are, so admin entries must use the new format. The admin example file is
converted (`STEAM_0:Y:Z` is `[U:1:2Z+Y]`).

## Automatic loading

EventScripts runs every `.cfg` of `addons/eventscripts/_autoload/` at startup (`installlib._executeAutoLoad`, called by
`corelib/es_install`, which EventScripts Remastered keeps loaded for this reason). `_autoload/wcs.cfg` contains
`es_load wcs`, so the repository works by copying it, without editing `autoexec.cfg`. The SourceMod plugins load at the
first map, after WCS: that is why `wcs_restriction` must hook its event late (see above).

## es_tools commands

WCS calls `est_setgravity` directly in `tools/setfx/es_setfx_2.txt`, and checks for `est_getwallbetween` before using it.
`est_compat.smx` (from EventScripts Remastered) provides them; `est_effect` comes from `wcs_effects.smx`.

## Verified behaviour

With 8 bots on a classic install, both batches of races at level 40 with ultimates and abilities triggered every 15
seconds: 26 kills in 5 minutes including skill kills, no Python exception, no SourceMod error, no crash. EventScripts'
`verify_data` ran alongside: the engine, the network props and the events always agreed, and frags, deaths and team
scores followed the game rules. Its two "vanilla" checks differ by design with WCS: some races spawn with more than
100 health, and some skills lower health directly, without a damage event.
