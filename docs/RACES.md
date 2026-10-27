# Races

The 12 races shipped with WCS 0.78.5g.4g.3, as defined in `cstrike/addons/eventscripts/wcs/ini/races.ini`.
**Required level** is the total level a player needs (sum of all their races) to choose the race. Each skill can be
raised up to the number of levels shown; the last skill of a race is usually its **ultimate** (`bind <key> ultimate`),
and some races have an **ability** (`bind <key> ability`).

| Race | Required level | Levels per skill | Skills | Author |
|---|---|---|---|---|
| [Undead Scourge](#undead-scourge) | 0 | 8 | Vampiric Aura, Unholy Aura, Levitation, Suicide Bomber | Kryptonite [WCS team] |
| [Human Alliance](#human-alliance) | 0 | 8 | Invisibility, Devotion Aura, Bash, Teleport | Kryptonite [WCS team] |
| [Orcish Horde](#orcish-horde) | 0 | 8 | Critical Strike, Critical Grenade, Reincarnation, Chain Lightning | Kryptonite [WCS team] |
| [Night Elves](#night-elves) | 0 | 8 | Evasion, Thorns Aura, Trueshot Aura, Entangling Roots | Kryptonite [WCS team] |
| [Blood Mage](#blood-mage) | 40 | 6 | Phoenix, Banish, Siphon Mana, Flame Strike, Curing Ritual | Kryptonite [WCS team] |
| [Archmage Proudmoore](#archmage-proudmoore) | 50 | 6 | Earthquake, Broom of Velocity, Weapon of the Sorcerer, Lift off | Fast.Food |
| [Shadow Hunter](#shadow-hunter) | 60 | 5 | Healing Wave, Hex, Serpent Ward, Bid Bad Voodoo | Kryptonite [WCS team] |
| [Warden](#warden) | 70 | 5 | Fan of Knives, Blink, Shadow Strike, Vengeance | Kryptonite [WCS team] |
| [Crypt Lord](#crypt-lord) | 80 | 5 | Impale, Spiked Carapace, Carrion Beetles, Locust Swarm | Kryptonite [WCS team] |
| [Flame Predator](#flame-predator) | 80 | 4 | Berserk (You will need it), Cloak of Invisibility, Levitation, Claw Attack, Burning Blade, Burning Inferno | Kryptonite/Fast.Food |
| [Succubus Hunter](#succubus-hunter) | 90 | 3 | Daemonic Knife, Head Hunter, Totem Incantation, Assault Tackle, Deamonic Transformation | Kryptonite [WCS team] |
| [Chameleon](#chameleon) | 100 | 5 | Spawn Powers, Attacking Powers, Victim Powers, Death Powers, Ultimate Powers | Kryptonite/soundn3ko |

## Undead Scourge

HP,speed,gravity,explode

| Skill | Effect |
|---|---|
| Vampiric Aura | Gives you a 60% chance to gain 12-30% of the damage you do in attack, back as health |
| Unholy Aura | Gives you a speed boost, 8-36% faster |
| Levitation | Allows you to jump higher by reducing your gravity for 8-64% |
| Suicide Bomber | On death, you have a 20-70% chance to explode and make 70-160 damage on each player in 12-18 feet range |

## Human Alliance

invis,HP,stun,teleport

| Skill | Effect |
|---|---|
| Invisibility | Makes you partially invisible, 62-37% |
| Devotion Aura | Gives you additional 15-50 health each round |
| Bash | Have a 15-32% chance to render an enemy immobile for 1 second |
| Teleport | Allows you to teleport to where you aim, range is 60-108 feet |

## Orcish Horde

crit strike,crit HE,reinc,chain light

| Skill | Effect |
|---|---|
| Critical Strike | Gives you a 15% chance of doing 40-240% more damage |
| Critical Grenade | Grenades will always do a 40-240% more damage |
| Reincarnation | Gives you a 15-80% chance of respawning once, with old equipment and where you died |
| Chain Lightning | Discharges a bolt of lightning that jumps on up to 4 nearby enemies 40-75 feet range, dealing each 32 damage |

## Night Elves

evade,reflect,dmg,freeze

| Skill | Effect |
|---|---|
| Evasion | Gives you 5-30% chance of evading a shot |
| Thorns Aura | Does 30% mirror damage to the person who shot you, chance to activate 15-50% |
| Trueshot Aura | Does 10-60% extra damage to the enemy, chance is 30% |
| Entangling Roots | Every enemy in 25-60 feet range will not be able to move for 10 seconds |

## Blood Mage

respawn,confuse,money,burn,health

| Skill | Effect |
|---|---|
| Phoenix | You have 15-90% chance of reviving the fist teammate who dies |
| Banish | Get 30% chance to confuse the enemy for 1-3 seconds |
| Siphon Mana | Get 30% chance to steal $20-170 from the enemy |
| Flame Strike | On hit, you have a 10-40% chance to burn an enemy player for 1-3.5 seconds |
| Curing Ritual | Sacrifice 100 mana (money) to gain 15-25 HP health |

## Archmage Proudmoore

shake,speed,summon weapon,fly

| Skill | Effect |
|---|---|
| Earthquake | Shake your enemy on attack, 25% to activate for 3-6 seconds |
| Broom of Velocity | You can run and fly (with lift-off) faster, 5-30% more speed |
| Weapon of the Sorcerer | On spawn, you may get for 30-50% a Desert Eagle/M4A1 or in DOD:S Colt/Bazooka |
| Lift off | You can fly and gain 5-10 additional health while flying |

## Shadow Hunter

heal,slowdown,warden,immortal

| Skill | Effect |
|---|---|
| Healing Wave | Heals teammates in 15-25ft range, 2-6HP every 6-8sec for 10-12 waves (maxHP 150) |
| Hex | Destroy boots of speed and slowdown enemy for 2-6sec by 25-45%, 30% chance |
| Serpent Ward | 1-2 serpent wards, damage enemy in 20-28ft range for 10-14sec and 12-20 damage/sec. Bind or say 'ability' |
| Bid Bad Voodoo | Invincibility for 2-3 seconds |

## Warden

mole,ulti immunity,dmg,respawn

| Skill | Effect |
|---|---|
| Fan of Knives | You have a 30-40% chance of becoming a mole |
| Blink | Chance of 50-70% to disable all enemy ultimates in 30ft range |
| Shadow Strike | You have a 13-33% chance doing 10 additional damage |
| Vengeance | Respawn once with 20-100HP and your old weapon |

## Crypt Lord

shake,mirror dmg+armor,dmg,random hit

| Skill | Effect |
|---|---|
| Impale | Shake and push the enemy, 10-33% chance |
| Spiked Carapace | Get 110-200 armor on spawn, 20-40% chance to deal 10-20% mirror damage |
| Carrion Beetles | You have a 20-33% chance of your beetles attacking the enemy for 5-15 extra damage |
| Locust Swarm | A Swarm of Locusts steals 25HP and 10-30 armor from one random enemy (max 150HP/200armor) |

## Flame Predator

(knife only)speed+HP,invis,gravity,force drop,dmg,explode

| Skill | Effect |
|---|---|
| Berserk (You will need it) | Pump yourself with adrenaline to gain 45-60% more speed and 25-40 HP |
| Cloak of Invisibility | Put on your cloak to be 69-81% invisible. |
| Levitation | Reduce your gravity by 30-60% |
| Claw Attack | Hit an enemy, 30-40% chance to force a weapon drop. |
| Burning Blade | Hit an enemy, 20-35% chance that he catch on fire |
| Burning Inferno | 20-40% chance that you deal 100-180 damage in 17-20ft range on death |

## Succubus Hunter

extra dmg/knife,dmg+XP+skull,HP,jump,invis+levi+HP

| Skill | Effect |
|---|---|
| Daemonic Knife | Do 50-90% extra damange with knife |
| Head Hunter | 30% chance to do 20-40% more damage, gain extra 5-20 XP and collect a SKULL |
| Totem Incantation | You gain 2-4HP for each skull and $5-20 |
| Assault Tackle | Makes you jump longer |
| Deamonic Transformation | Get 22-70% invis, 20-50% lower gravity and 20-50 HP. Costs 1/2/3 SKULLs. (max 200HP) |

## Chameleon

Random skills every round!

| Skill | Effect |
|---|---|
| Spawn Powers | 50-90% chance of spawning with either HP, speed, longjump, lowgravity, mole or regeneration |
| Attacking Powers | 33% chance of extra damage, burning, freezing, blinding or leeching health |
| Victim Powers | 33% chance to evade, mirror damage, slowdown attacker or get invisibility |
| Death Powers | 30-70% chance on death to explode, respawn, give team some health or gain mana |
| Ultimate Powers | 80% chance to mimic roots, teleport, chain lightning, health boost or fly |

Races are edited in `races.ini` (format at the top of the file); `wcs_reload_races` reloads it without a restart.
