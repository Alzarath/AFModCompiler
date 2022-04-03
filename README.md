# AFModCompiler
The Acolyte Fight Mod Compiler. Used to compile Acolyte Fight mod projects into a single playable json file.

## Table of Contents

* [Usage](#usage)
* [Project Structure](#project-structure)
  * [Mod Info](#mod-info)
    * [Example](#mod-info-example)
  * [Constants](#constants)
  * [Icons](#icons)
    * [Example](#icon-example)
  * [Maps](#maps)
    * [Example](#map-example)
  * [Obstacles](#obstacles)
    * [Example](#obstacle-example)
  * [Projectiles](#projectiles)
    * [Example](#projectile-example)
  * [Sounds](#sounds)
    * [Example](#sound-example)
  * [Spells](#spells)
    * [Example](#spell-example)
* [Parenting](#parenting)

## Usage

### Requirements

* [Python version 3.4 or higher](https://www.python.org/downloads/)

### Instructions

TL;DR: Copy AFModCompiler.py to the mod project directory. Open a terminal/command prompt. `cd` into the mod project directory. Run `python AFModCompiler.py`. It will generate a mod json file called mod_output.json by default. Load it in Acolyte Fight and play.

```
usage: AFModCompiler.py [-h] [--output, -o [OUTPUT_FILE]]
                        [--max-projectile-depth [MAX_PROJECTILE_DEPTH]]
                        [--max-parent-depth [MAX_PARENT_DEPTH]]
                        [Directory]

Process a mod project

positional arguments:
  Directory             Directory that will be processed

options:
  -h, --help            show this help message and exit
  --output, -o [OUTPUT_FILE]
                        Set the destination file that the mod will be compiled
                        to
  --max-projectile-depth [MAX_PROJECTILE_DEPTH]
                        Sets the maximum depth projectiles will generate in
                        the case of recursion or sufficiently long
                        projectile chains
  --max-parent-depth [MAX_PARENT_DEPTH]
                        Sets the maximum depth parents will be searched to
                        generate in the case of nested parent chains and
                        infinite loops
```

## Project Structure

A mod project is expected to follow a specific directory and file sturcture, although no singular file or directory is required.

The project directory name does not matter, but the files **mod.json** and all constants must have their appropriate names to be included. Objects in the other folders do not need to follow any particular naming scheme, but object names should be addressed consistently when it comes to parenting and templating. An example of a project directory and file structure is as follows:

```
project_directory/
├─ constants/
│  ├─ ai.js
│  ├─ audio.json
│  ├─ choices.json
│  ├─ hero.json
│  ├─ matchmaking.json
│  ├─ obstacle.json
│  ├─ tips.json
│  ├─ visuals.json
│  └─ world.json
├─ icons/
│  └─ thunderball.json
├─ maps/
│  └─ circle.json
├─ obstacles/
│  └─ mirror.json
├─ projectiles/
│  └─ fireball.json
├─ sounds/
│  ├─ fireball.json
│  └─ standard-hit.json
├─ spells/
│  └─ fireball.json
└─ mod.json
```

### Mod Info

Mod information is located in the **mod.json** file in the root directory. The file is expected to contain a single key-less dictionary value.

#### Mod Info example

The following example is the contents of a default mod that should be located in the file **project_directory/mod.json**

<details>
 <summary><b>Click to Reveal: <code>mod.json</code></b></summary>

```json
{
  "Mod": {
    "name": "Acolyte's mod",
    "author": "Acolyte",
    "description": "Mon, 21 Mar 2022 12:00:00 GMT",
    "titleLeft": "Acolyte's",
    "titleRight": "Mod!",
    "subtitleLeft": "",
    "subtitleRight": ""
  }
}
```
</details>

### Constants

Constants are located in the **constants** directory. There are 8 constant files:

* **ai.js** contains javascript code for the NPC's AI. Formatted as a standard Javascript file.
* **audio.json** contains global settings for the game's audio. Formatted as a key-less dictionary value.
* **choices.json** contains global settings for players' spell selection. Formatted as a key-less dictionary value.
* **hero.json** contains global settings for player characters. Formatted as a key-less dictionary value.
* **matchmaking.json** contains global settings for the game's matchmaking. Formatted as a key-less dictionary value.
* **obstacle.json** contains global settings for the game's obstacles. Formatted as a key-less dictionary value.
* **tips.json** contains randomized tips for the game. Formatted as a list.
* **visuals.json** contains global settings for the game's visuals. Formatted as a key-less dictionary value.
* **world.json** contains global settings for the game maps. Formatted as a key-less dictionary value.

Tips are the one file that expects a list `[]` rather than a dictionary `{}`. As it's how the game implements tips, tips in the **tips.json** file will replace all of the existing game's tips.

### Icons

Icons are located in the **icons** directory. Sub-directories are acceptable, but not important.

An icon is generated from a json file where the icon entry uses the file name without the file extension. Each icon file is expected to contain a single key-less dictionary value.

#### Icon Example

There is no icon example due to copyright concerns. Look at other examples e.g. [Map Example](#map-example) to get an idea of how to format it.

An icon **.json** file would be located in the **project_directory/icons/** directory.

### Maps

Maps are located in the **maps** directory. Sub-directories are acceptable, but not important.

A map is generated from a json file where the map entry uses the file name without the file extension. Each map file is expected to contain a single key-less dictionary value.

#### Map Example

The following examples is the contents of the Mirrors map (as of this writing) that might be located in the file **project_directory/maps/mirrors.json**

<details>
 <summary><b>Click to Reveal: <code>mirrors.json</code></b></summary>

```json
{
  "id": "mirrors",
  "color": "#41334d",
  "background": "#25192e",
  "obstacles": [
    {
      "type": "mirror",
      "numObstacles": 7,
      "layoutRadius": 0.22,
      "layoutAngleOffsetInRevs": 0,
      "numPoints": 4,
      "extent": 0.005,
      "orientationAngleOffsetInRevs": 0,
      "angularWidthInRevs": 0.05
    }
  ],
  "numPoints": 7
}
```
</details>

### Obstacles

Obstacles are located in the **obstacles** directory. Sub-directories are acceptable, but not important.

An obstacle is generated from a json file where the obstacle entry uses the file name without the file extension. Each obstacle file is expected to contain a single key-less dictionary value.

#### Obstacle Example

The following example is the contents of the vanilla healing pool (as of this writing) that might be located in the file **project_directory/obstacles/healing.json**

<details>
  <summary><b>Click to Reveal: <code>healing.json</code></b></summary>

```json
{
  "id": "healing",
  "health": 50,
  "collideWith": 9,
  "sensor": true,
  "static": true,
  "undamageable": true,
  "strike": {
    "ticks": 15,
    "flash": true
  },
  "hitInterval": 15,
  "selfDamage": 1,
  "decayPerSecond": 2,
  "render": [
    {
      "type": "solid",
      "color": "#0f9e",
      "deadColor": "#0f94",
      "glow": 0.2
    },
    {
      "type": "smoke",
      "color": "#0f9",
      "particleRadius": 0.005,
      "fade": "#0000",
      "bloom": 0.01,
      "glow": 0.05,
      "ticks": 30,
      "interval": 8,
      "speed": 0.1
    }
  ],
  "buffs": [
    {
      "type": "burn",
      "maxTicks": 15,
      "collideWith": 65535,
      "packet": {
        "damage": -1,
        "lifeSteal": 0,
        "noKnockback": true,
        "noHit": true,
        "isLava": true
      },
      "hitInterval": 5,
      "stack": "healing",
      "maxStacks": 1
    }
  ]
}
```
</details>

### Projectiles

AFModCompiler introduces the concept of Projectile Templating.

A projectile template string can be used in place of a `projectile`'s value. For clarity, I use `"ProjectileTemplate:fireball"` where fireball is the name of a projectile template file (**projectiles/fireball.json**) without the file extension, but you may exclude `ProjectileTemplate:` and it should also function (untested).

```json
"projectile": "ProjectileTemplate:fireball"
```

These can be placed in place of a Spell's `projectile` field, or in place of a `spawn` behaviour's `projectile` field.

Projectile Templates are located in the **projectiles** directory. Sub-directories are acceptable, but not important.

A projectile is generated from a json file where the projectile template name uses the file name without the file extension. Each projectile file is expected to contain a single key-less dictionary value.

To avoid infinite loops, there is a limit to how many projectiles deep a projectile can spawn from a `spawn` behaviour. By default this is 20, but can be overwritten with the `--max-projectile-depth` argument. Be warned that sufficiently deep recursive projectiles *can* contribute to a very large compiled file size.

#### Projectile Example

The following example is the contents of the Fireball's projectile dictionary (as of this writing) that might be located in the file **project_directory/projectiles/fireball.json**

<details>
  <summary><b>Click to Reveal: <code>fireball.json</code></b></summary>

```json
{
  "density": 25,
  "radius": 0.003,
  "speed": 0.6,
  "maxTicks": 90,
  "damage": 16,
  "lifeSteal": 0.3,
  "categories": 2,
  "sound": "fireball",
  "soundHit": "standard",
  "color": "#f80",
  "renderers": [
    {
      "type": "bloom",
      "radius": 0.045
    },
    {
      "type": "projectile",
      "ticks": 30,
      "smoke": 0.05
    },
    {
      "type": "ray",
      "ticks": 30
    },
    {
      "type": "strike",
      "ticks": 30,
      "flash": true,
      "numParticles": 5
    }
  ]
}
```
</details>

### Sounds

Sounds are located in the **sounds** directory. Sub-directories are acceptable, but not important.

A sound is generated from a json file where the sound entry uses the file name without the file extension. Each sound file is expected to contain a single key-less dictionary value.

#### Sound Example

The following example is the contents of the vanilla Fireball's sound effect (as of this writing) that might be located in the file **project_directory/sounds/fireball.json**

<details>
  <summary><b>Click to Reveal: <code>fireball.json</code></b></summary>

```json
{
  "id": "fireball",
  "sustain": [
    {
      "stopTime": 1.5,
      "attack": 0.25,
      "decay": 0.25,
      "highPass": 432,
      "lowPass": 438,
      "wave": "brown-noise"
    }
  ]
}
```
</details>

### Spells

Spells are located in the **spells** directory. Sub-directories are acceptable, but not important.

A spell is generated from a json file where the spell entry uses the file name without the file extension. Each spell file is expected to contain a single key-less dictionary value.

#### Spell Example

The following example is the contents of the vanilla Fireball (as of this writing) that might be located in the file **project_directory/spells/fireball.json**

<details>
 <summary><b>Click to Reveal: <code>fireball.json</code></b></summary>

```json
{
  "id": "fireball",
  "description": "Quick cooldown and packs a punch. Good old trusty fireball.",
  "action": "projectile",
  "color": "#f80",
  "icon": "thunderball",
  "maxAngleDiffInRevs": 0.01,
  "cooldown": 90,
  "throttle": true,
  "projectile": {
    "density": 25,
    "radius": 0.003,
    "speed": 0.6,
    "maxTicks": 90,
    "damage": 16,
    "lifeSteal": 0.3,
    "categories": 2,
    "sound": "fireball",
    "soundHit": "standard",
    "color": "#f80",
    "renderers": [
      {
        "type": "bloom",
        "radius": 0.045
      },
      {
        "type": "projectile",
        "ticks": 30,
        "smoke": 0.05
      },
      {
        "type": "ray",
        "ticks": 30
      },
      {
        "type": "strike",
        "ticks": 30,
        "flash": true,
        "numParticles": 5
      }
    ]
  }
}
```
</details>

Note that the `projectile`'s' dictionary value could be replaced with a [Projectile Template](#projectiles) string (e.g. `"projectile": "ProjectileTemplate:fireball.json"`) to condense things here.

## Parenting

AFModCompiler checks for the key `basedOn` and uses its value (formatted as a file name without the extension) to generate a base object that the settings then overwrite.

One thing to keep in mind is that you can only replace values in the root, so attempting to add something to a nested dictionary or list (e.g. a `renderers` list in a projectile) will instead overwrite it. Additionally, the compiler only searches a root object and will not search nested objects.

It is possible to parent an object from an object that itself has a parent. There is a limit of 50 (that can be overwritten with the `--max-parent-depth` argument) to avoid infinite loops.
