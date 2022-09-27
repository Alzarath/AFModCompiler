from pathlib import Path
import json
import argparse
from random import randint

parser = argparse.ArgumentParser(description='Process a mod project')
parser.add_argument('--output, -o', type=str, nargs='?',
					default='mod_output.json', dest='output_file',
                    help='Set the destination file that the mod will be compiled to')
parser.add_argument('project_directory', metavar='Directory', type=str, nargs='?',
                    default='.', help='Directory that will be processed')
parser.add_argument('--max-projectile-depth', type=int, nargs='?',
                    default=20, dest='max_projectile_depth',
                    help='Sets the maximum depth projectiles will generate ' +
                    'in the case of recursion or sufficiently long projectile chains')
parser.add_argument('--max-parent-depth', type=int, nargs='?',
                    default=50, dest='max_parent_depth',
                    help='Sets the maximum depth parents will be searched to ' +
                    'generate in the case of nested parent chains and infinite loops')
args = parser.parse_args()

def get_jsons(directory):
	if not directory.is_dir():
		return None

	files = []

	for file in directory.iterdir():
		if file.is_dir():
			files += get_jsons(file)
		elif file.suffix == ".json":
			files.append(file)

	return files

def get_data(directory):
	returned_data = {}

	data_files = get_jsons(directory)

	if len(data_files) == 0:
		return None

	for file in data_files:
		file_json = parse_json_from_file(file)
		data_name = file.stem
		returned_data[data_name] = file_json.copy()

	return returned_data

def get_constants(directory):
	constant_info = {}

	# AI Javascript
	ai_file = directory.joinpath("ai.js")
	if ai_file.exists() and not ai_file.is_dir():
		constant_info["Code"] = ai_file.read_text()

	# Audio constants
	audio_file = directory.joinpath("audio.json")
	audio_data = parse_json_from_file(audio_file)
	if audio_data:
		constant_info["Audio"] = audio_data

	# Choices constants
	choices_file = directory.joinpath("choices.json")
	choices_data = parse_json_from_file(choices_file)
	if choices_data:
		constant_info["Choices"] = parse_json_from_file(choices_file)

	# Hero constants
	hero_file = directory.joinpath("hero.json")
	hero_data = parse_json_from_file(hero_file)
	if hero_data:
		constant_info["Hero"] = parse_json_from_file(hero_file)

	# Matchmaking constants
	matchmaking_file = directory.joinpath("matchmaking.json")
	matchmaking_data = parse_json_from_file(matchmaking_file)
	if matchmaking_data:
		constant_info["Matchmaking"] = parse_json_from_file(matchmaking_file)

	# Obstacle constants
	obstacle_file = directory.joinpath("obstacle.json")
	obstacle_data = parse_json_from_file(obstacle_file)
	if obstacle_data:
		constant_info["Obstacle"] = parse_json_from_file(obstacle_file)

	# Tips list
	tips_file = directory.joinpath("tips.json")
	tips_data = parse_json_from_file(tips_file)
	if tips_data:
		constant_info["Tips"] = parse_json_from_file(tips_file)

	# Visuals constants
	visuals_file = directory.joinpath("visuals.json")
	visuals_data = parse_json_from_file(visuals_file)
	if visuals_data:
		constant_info["Visuals"] = parse_json_from_file(visuals_file)

	# World constants
	world_file = directory.joinpath("world.json")
	world_data = parse_json_from_file(world_file)
	if world_data:
		constant_info["World"] = parse_json_from_file(world_file)

	return constant_info

def parse_json_from_file(path):
	returned_value = None
	if path.exists() and not path.is_dir():
		try:
			returned_value = json.loads(path.read_text())
		except json.decoder.JSONDecodeError as e:
			print(f"JSON Error in {path.resolve()}\n{e}")
			sys.exit(1)
	return returned_value

def template_projectile(projectile, projectiles):
	projectile_template = projectile.replace("ProjectileTemplate:", "")
	
	return list(projectiles.values())[randint(0, len(projectiles)-1)].copy()

def template_projectile_spawners(projectile, projectiles, spawner_depth = 0):
	returned_projectile = projectile.copy()
	if not returned_projectile.get("behaviours"):
		return returned_projectile
	popped_items = []
	for behaviour_index, behaviour_data in reversed(list(enumerate(returned_projectile["behaviours"].copy()))):
		if behaviour_data["type"] == "spawn" and type(behaviour_data["projectile"]) is str:
			if spawner_depth >= args.max_projectile_depth:
				popped_items.append(behaviour_index)
				continue
			else:
				returned_projectile["behaviours"][behaviour_index]["projectile"] = template_projectile_spawners(list(projectiles.values())[randint(0, len(projectiles)-1)], projectiles, spawner_depth + 1).copy()

	returned_projectile["behaviours"] = [behaviour.copy() for index, behaviour in enumerate(returned_projectile["behaviours"]) if index not in popped_items]
	return returned_projectile

def process_projectiles(projectiles):
	returned_projectiles = process_parents(projectiles)

	for projectile_index, projectile_data in returned_projectiles.items():
		returned_projectiles[projectile_index] = template_projectile_spawners(projectile_data, returned_projectiles)

	return returned_projectiles

def process_spells(spells, projectiles):
	returned_spells = process_parents(spells)

	for spell_index, spell_data in returned_spells.items():
		if spell_data.get("projectile") and type(spell_data["projectile"]) is str:
			spell_data["projectile"] = template_projectile(spell_data["projectile"], projectiles)

		if spell_data.get("releaseBehaviours"):
			for behaviour in spell_data["releaseBehaviours"]:
				if behaviour["type"] == "spawn" and type(behaviour["projectile"]) is str:
					behaviour["projectile"] = template_projectile(behaviour["projectile"], projectiles)

	return returned_spells

def process_parents(data):
	returned_data = data.copy()

	# Start parenting projectiles
	data_remains = True
	nested_parent_attempts = 0
	while nested_parent_attempts < args.max_parent_depth and data_remains:
		data_remains = False
		for data_index, data in returned_data.items():
			parent_data = data.get("basedOn")
			if parent_data:
				if not returned_data.get(parent_data):
					raise(f"{data['basedOn']} does not exist")
				if returned_data[parent_data].get("basedOn"):
					data_remains = True
					nested_parent_attempts += 1
					continue
				else:
					returned_data[data_index] = dict(returned_data[parent_data].copy(), **data)
					returned_data[data_index].pop("basedOn")
			else:
				returned_data[data_index] = data.copy()

	if nested_parent_attempts == args.max_parent_depth:
		raise("Timed out on parenting data. Infinite loop?")

	return returned_data

def main():
	project_directory = Path(args.project_directory)

	# Process all the mod data
	mod_path = project_directory.joinpath("mod.json")
	constant_path = project_directory.joinpath("constants")
	projectile_path = project_directory.joinpath("projectiles")
	spell_path = project_directory.joinpath("spells")
	obstacle_path = project_directory.joinpath("obstacles")
	map_path = project_directory.joinpath("maps")
	sound_path = project_directory.joinpath("sounds")
	icon_path = project_directory.joinpath("icons")

	mod_info = parse_json_from_file(mod_path)
	constant_info = get_constants(constant_path) if constant_path.exists() and constant_path.is_dir() else None

	processed_projectiles = process_projectiles(get_data(projectile_path)) if projectile_path.exists() and projectile_path.is_dir() else None
	processed_spells = process_spells(get_data(spell_path), processed_projectiles) if spell_path.exists() and spell_path.is_dir() else None
	processed_obstacles = process_parents(get_data(obstacle_path)) if obstacle_path.exists() and obstacle_path.is_dir() else None
	processed_maps = process_parents(get_data(map_path)) if map_path.exists() and map_path.is_dir() else None
	processed_sounds = process_parents(get_data(sound_path)) if sound_path.exists() and sound_path.is_dir() else None
	processed_icons = process_parents(get_data(icon_path)) if icon_path.exists() and icon_path.is_dir() else None

	# Format the mod data into a json
	mod_data = {}
	if mod_info:
		mod_data["Mod"] = mod_info
	for constant_index, constant_values in constant_info.items():
		mod_data[constant_index] = constant_values
	if processed_spells:
		mod_data["Spells"] = processed_spells
	if processed_maps:
		mod_data["Layouts"] = processed_maps
	if processed_obstacles:
		mod_data["ObstacleTemplates"] = processed_obstacles
	if processed_sounds:
		mod_data["Sounds"] = processed_sounds
	if processed_icons:
		mod_data["Icons"] = processed_icons

	# Export the mod data to the specified file
	mod_file = Path(args.output_file)
	mod_json = json.dumps(mod_data, indent=4)
	mod_file.write_text(str(mod_json))

main()