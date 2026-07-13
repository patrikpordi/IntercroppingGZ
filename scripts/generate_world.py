#!/usr/bin/env python3

import os
import yaml
from pathlib import Path
from ament_index_python.packages import get_package_share_directory

# --------------------------------------------------
# PATHS
# --------------------------------------------------

PACKAGE_DIR = Path(get_package_share_directory("intercropping_gz"))
CONFIG_FILE = PACKAGE_DIR / 'config' / "config.yaml"

# --------------------------------------------------
# LOAD CONFIG
# --------------------------------------------------

with open(CONFIG_FILE, "r") as f:
    cfg = yaml.safe_load(f)

# --------------------------------------------------
# PARAMETERS FROM YAML
# --------------------------------------------------

WORLD_NAME = cfg["world"]["name"]
SOURCE_ROOT = CONFIG_FILE.resolve().parents[2] if CONFIG_FILE.is_symlink() else PACKAGE_DIR # Resolve symlinks back to the source directory if installed as symlinks, otherwise just use package directory
OUTPUT_FILE = SOURCE_ROOT / cfg["world"]["output_file"]

NUM_ROWS = cfg["field"]["num_rows"]
ROW_LENGTH = cfg["field"]["row_length"]
ROW_SPACING = cfg["field"]["row_spacing"]
PLANT_SPACING = cfg["field"]["plant_spacing"]

START_X = cfg["origin"]["start_x"]
START_Y = cfg["origin"]["start_y"]
PLANT_Z = cfg["origin"]["plant_z"]

def resolve_model(model, collision):
    return model if collision else f"{model}_no_collision"


EVEN_ROW_MODEL = resolve_model(
    cfg["crops"]["even_rows"],
    cfg["crops"].get("even_rows_collision", True)
)
ODD_ROW_MODEL = resolve_model(
    cfg["crops"]["odd_rows"],
    cfg["crops"].get("odd_rows_collision", True)
)

GROUND_MODEL = cfg["ground"]["model"]
GROUND_POSE = cfg["ground"]["pose"]

AMBIENT = cfg["lighting"]["ambient"]
BACKGROUND = cfg["lighting"]["background"]

SUN_POSE = cfg["sun"]["pose"]
SUN_DIFFUSE = cfg["sun"]["diffuse"]
SUN_SPECULAR = cfg["sun"]["specular"]
SUN_DIRECTION = cfg["sun"]["direction"]

# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def vec_to_str(v):
    return " ".join(str(x) for x in v)


def make_include(model, name, x, y, z=0.0):
    return f"""
    <include>
      <name>{name}</name>
      <uri>model://{model}</uri>
      <pose>{x} {y} {z} 0 0 0</pose>
    </include>
    """


# --------------------------------------------------
# WORLD GENERATION
# --------------------------------------------------

def generate_world():

    includes = []

    # Center rows around START_Y
    y_offset = -(NUM_ROWS - 1) * ROW_SPACING / 2.0

    idx = 0

    for row in range(NUM_ROWS):

        y = START_Y + y_offset + row * ROW_SPACING

        model = (
            EVEN_ROW_MODEL
            if row % 2 == 0
            else ODD_ROW_MODEL
        )

        x = START_X

        while x < START_X + ROW_LENGTH:

            name = f"{model}_{idx}"

            includes.append(
                make_include(
                    model=model,
                    name=name,
                    x=x,
                    y=y,
                    z=PLANT_Z
                )
            )

            x += PLANT_SPACING
            idx += 1

    world = f"""<?xml version="1.0" ?>
<sdf version="1.9">

  <world name="{WORLD_NAME}">

    <!-- Physics -->
    <physics type="ignored">
      <max_step_size>0.001</max_step_size>
    </physics>

    <!-- Scene -->
    <scene>
      <ambient>{vec_to_str(AMBIENT)}</ambient>
      <background>{vec_to_str(BACKGROUND)}</background>
    </scene>

    <!-- Sun -->
    <light type="directional" name="sun">

      <cast_shadows>true</cast_shadows>

      <pose>{vec_to_str(SUN_POSE)}</pose>

      <diffuse>{vec_to_str(SUN_DIFFUSE)}</diffuse>

      <specular>{vec_to_str(SUN_SPECULAR)}</specular>

      <direction>{vec_to_str(SUN_DIRECTION)}</direction>

    </light>

    <!-- Ground -->
    <include>
      <uri>model://{GROUND_MODEL}</uri>
      <pose>{vec_to_str(GROUND_POSE)}</pose>
    </include>

    <!-- Crops -->
    {''.join(includes)}

  </world>

</sdf>
"""

    os.makedirs(
        os.path.dirname(OUTPUT_FILE),
        exist_ok=True
    )

    with open(OUTPUT_FILE, "w") as f:
        f.write(world)

    print(f"[OK] Generated: {OUTPUT_FILE}")
    print(f"[INFO] World name: {WORLD_NAME}")
    print(f"[INFO] Start position: ({START_X}, {START_Y})")
    print(f"[INFO] Total plants: {idx}")


# --------------------------------------------------
# MAIN
# --------------------------------------------------

if __name__ == "__main__":
    generate_world()