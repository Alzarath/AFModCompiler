# AFModCompiler
The Acolyte Fight Mod Compiler. Used to compile Acolyte Fight mod projects into a single playable json file.

## Usage
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

## Expectations

A mod project is expected to follow a specific directory and file sturcture, although no singular file or directory is required.

The project directory name does not matter, but the files `mod.json` and all constants must have their appropriate names to be included. Objects in the other folders do not need to follow any particular naming scheme, but object names should be addressed consistently when it comes to parenting and templating.

```
project_directory/
├─ constants/
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

Mod information is located in the `mod.json` file in the root directory. The file is expected to contain a single key-less dictionary value.

### Constants

Constants are located in the `constants` directory. There are 8 constant files:

* `ai.js` contains javascript code for the NPC's AI. Formatted as a standard Javascript file.
* `audio.json` contains global settings for the game's audio. Formatted as a key-less dictionary value.
* `choices.json` contains global settings for players' spell selection. Formatted as a key-less dictionary value.
* `hero.json` contains global settings for player characters. Formatted as a key-less dictionary value.
* `matchmaking.json` contains global settings for the game's matchmaking. Formatted as a key-less dictionary value.
* `obstacle.json` contains global settings for the game's obstacles. Formatted as a key-less dictionary value.
* `tips.json` contains randomized tips for the game. Formatted as a list.
* `visuals.json` contains global settings for the game's visuals. Formatted as a key-less dictionary value.
* `world.json` contains global settings for the game maps. Formatted as a key-less dictionary value.

Tips are the one file that expects a list `[]` rather than a dictionary `{}`. As it's how the game implements tips, tips in the `tips.json` file will replace all of the existing game's tips.

### Icons

Icons are located in the `icons` directory. Sub-directories are acceptable, but not important.

An icon is generated from a json file where the icon entry uses the file name without the file extension. Each icon file is expected to contain a single key-less dictionary value.

### Maps

Maps are located in the `maps` directory. Sub-directories are acceptable, but not important.

A map is generated from a json file where the map entry uses the file name without the file extension. Each map file is expected to contain a single key-less dictionary value.

### Obstacles

Obstacles are located in the `obstacles` directory. Sub-directories are acceptable, but not important.

An obstacle is generated from a json file where the obstacle entry uses the file name without the file extension. Each obstacle file is expected to contain a single key-less dictionary value.

### Projectiles

AFModCompiler introduces the concept of Projectile Templating.

A projectile template string can be used in place of a `projectile`'s value. For clarity, I use `"ProjectileTemplate:fireball"` where projectileTemplate is the name of a projectile template file (without the file extension), but you may exclude `ProjectileTemplate:` and it should also function (untested).

```json
"projectile": "ProjectileTemplate:fireball"
```

These can be placed in place of a Spell's `projectile` field, or in place of a `spawn` behaviour's `projectile` field.

Projectile Templates are located in the `projectiles` directory. Sub-directories are acceptable, but not important.

A projectile is generated from a json file where the projectile template name uses the file name without the file extension. Each projectile file is expected to contain a single key-less dictionary value.

### Sounds

Sounds are located in the `sounds` directory. Sub-directories are acceptable, but not important.

A sound is generated from a json file where the sound entry uses the file name without the file extension. Each sound file is expected to contain a single key-less dictionary value.

### Spells

Spells are located in the `spells` directory. Sub-directories are acceptable, but not important.

A spell is generated from a json file where the spell entry uses the file name without the file extension. Each spell file is expected to contain a single key-less dictionary value.

## Parenting

AFModCompiler checks for the key `"basedOn"` and uses its value (formatted as a file name without the extension) to generate a base object that the settings then overwrite.

One thing to keep in mind is that you can only replace values in the root, so attempting to add something to a nested dictionary or list will not work.
