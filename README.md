# 🌾 IntercroppingGZ

Procedural Gazebo (gz sim) environment for simulating intercropping agricultural fields.

Generates alternating crop rows, places plant models, configures lighting, and exports a ready-to-run SDF world for robotics and agricultural experiments.

![Intercropping field](resources/intercropping_field.png)

---

## Quick Overview

- **Generator:** `scripts/generate_world.py`
- **Models:** `models/` (crop_row_a, crop_row_b, ground, weed)
- **Output world:** `worlds/intercrop_world.sdf`
- **Config:** `config.yaml` (tweak layout and spacing)

---

## Features

- Procedural crop-row layout with alternating intercrop patterns
- Configurable rows, spacing, plant spacing, and field origin
- Uses OBJ + texture plant models and a ground model
- Adds lighting and sun so the generated world is simulation-ready
- Targeted for Gazebo / gz sim (HarmonIC-compatible)

---

## Requirements

- `gz` (gz-sim / Gazebo Harmonic) installed and on `PATH`
- `python3` (3.8+ recommended)
- Optional: a Python virtualenv for dependencies

---

## Quick Start

Clone the repo and jump in:

```bash
git clone https://github.com/patrikpordi/IntercroppingGZ.git
cd IntercroppingGZ
```

Point Gazebo to the local models directory and generate the world:

```bash
export GZ_SIM_RESOURCE_PATH="$PWD/models"
python3 scripts/generate_world.py
gz sim --verbose 3 ./worlds/intercrop_world.sdf
```

If you prefer, run the generator with a custom config file:

```bash
python3 scripts/generate_world.py --config config.yaml
```

---

## Configuration

Edit `config.yaml` to change basic parameters such as:

- `rows`: number of crop rows
- `row_spacing`: distance between rows (meters)
- `plant_spacing`: distance between individual plants along a row
- `origin`: world origin for the field placement

The generator loads the config, places models from `models/`, and writes the SDF to `worlds/intercrop_world.sdf`.

See the generator header for the full list of options: [scripts/generate_world.py](scripts/generate_world.py)

---

## Project layout

- `models/` — Gazebo model folders (crop_row_a, crop_row_b, ground, weed)
- `scripts/generate_world.py` — world generator
- `worlds/` — generated SDF files (output)
- `config.yaml` — generator configuration (optional)

---

## Tips & Notes

- Verify that `GZ_SIM_RESOURCE_PATH` points to the `models/` directory so gz can find the models.
- You can preview the generated SDF in a text editor or open it directly with `gz sim`.
- Replace or add model folders under `models/` to experiment with different plants or assets.

---

## Contributing

Contributions welcome — open issues or PRs for bug fixes, new plant models, or generator improvements.

---

## License

This project does not include a license file. Add `LICENSE` if you want to clarify reuse terms.
