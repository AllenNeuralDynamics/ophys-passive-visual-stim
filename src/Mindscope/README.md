# Mindscope Oddball Workflow

This folder contains the Bonsai workflow and Python stimulus generator adapted from the
[OpenScope Community Predictive Processing project](https://github.com/AllenNeuralDynamics/openscope-community-predictive-processing)
for use with the SLAP2 rig.

## Files

| File | Description |
|---|---|
| `generic_oddball_slap2.bonsai` | Main Bonsai workflow. Reads a CSV stimulus table row by row and renders drifting gratings and/or movie clips in sync with SLAP2 imaging. |
| `generate_experiment_csv.py` | Python script that generates the CSV stimulus table before each session. Called automatically by the launcher. |
| `Extensions/ColorBalance.bonsai` | Sub-workflow for color balance correction, included by the main workflow. |

### Dependencies (resolved relative to this folder)

| Path | What it is |
|---|---|
| `..\Extensions\SLAP-Start.bonsai` | Sends TTL start pulse to SLAP2 |
| `..\Extensions\SLAP-Stop.bonsai` | Sends TTL stop pulse to SLAP2 |
| `..\Extensions\SLAP-Tag.bonsai` | Sends TTL tag pulse per trial |
| `..\Extensions\behavior_camera.bonsai` | Behavior camera sub-workflow |
| `..\..\bonsai\Shaders\ColorBalance.frag` | GLSL fragment shader for color balance |
| `..\Movies\zebra_allen_screen_tscale_30_scale_10.mp4` | Zebra noise movie (300s) |
| `..\Movies\Compressed_MATLAB_trippy_150s_1920x1200_30fps_120x95.mp4` | Trippy noise movie (150s) — loaded at startup, not used in all session types |

## How it works

1. The launcher runs `generate_experiment_csv.py` to produce a CSV stimulus table for the session.
2. Bonsai starts and loads the CSV. Each row is one trial; the workflow renders the stimulus and sends sync pulses to SLAP2.
3. After the session, the post-acquisition pipeline annotates and archives the data.

## Stimulus design — Indicator Testing

**Session type:** `gratings_and_zebra`

The session has three blocks in order:

| Block | Type | Duration | Details |
|---|---|---|---|
| 1 | Drifting gratings | 5 min | 14 orientations (0–292.5° in 22.5° steps), shuffled randomly with omission and halt trials. Each trial: 343 ms stimulus + 343 ms delay, 0.04 cpd, 2 Hz, full field. |
| 2 | Zebra noise movie | 15 min | 3 × 300s repeats of the zebra noise movie. 120° × 95° display. |
| 3 | Drifting gratings | 5 min | Same as Block 1, independent shuffle. |

**Total session duration:** ~25 minutes

**Param file:** `openscope-params/packs/projects/indicator_testing/behavior/gratings_and_zebra.json`

To change the stimulus design, edit the `gratings_and_zebra` entry in `session_configs` inside `generate_experiment_csv.py`.
