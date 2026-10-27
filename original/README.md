# Original WCS 0.78.5g.4g.3

`wcs_v0.78.5g.4g.3.zip` is the original Warcraft Source 0.78.5g.4g.3 Beta package (EventScripts addon, two EventScripts
libraries and three SourceMod plugins with their sources and precompiled `.smx`), unchanged. SHA-256:
[SHA256SUMS](SHA256SUMS).

The `cstrike/` folder of this repository is its content without the precompiled `.pyc` and `.smx` files (the plugins
are rebuilt from source), plus `addons/eventscripts/_autoload/wcs.cfg` and `est_compat`, with the changes listed in
[`changes-vs-0.78.5g.4g.3.patch`](changes-vs-0.78.5g.4g.3.patch). The patch applies to the extracted archive:

```sh
mkdir wcs && cd wcs
unzip ../wcs_v0.78.5g.4g.3.zip
patch -p1 < ../changes-vs-0.78.5g.4g.3.patch
```
