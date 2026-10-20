This folder stores Bonsai code used by AIND Ophys to run passive visual stimulation tasks on the Visual Cortex Observatory (VCO) rig.

## Organization

All Bonsai workflows should go into `./src`, along with the `Extensions` folder.

## Deployment

To deploy the Bonsai code, run `./bonsai/setup.cmd`. This small script will download and regenerate the current Bonsai environment ([see tutorial for further details.](https://bonsai-rx.org/docs/articles/environments.html)).
Each time you change a project dependency via the `Package Manager`, the `Bonsai.Config` file will be updated. Read [Bonsai.config: fresh installs vs existing installs](#bonsaiconfig-fresh-installs-vs-existing-installs) before committing it.

### How the install works

1. `setup.cmd` runs `setup.ps1` with the execution policy bypassed.
2. `setup.ps1` only downloads Bonsai if `bonsai/Bonsai.exe` is missing. It then runs `Bonsai.exe --no-editor`.
3. That first launch installs every package listed in `bonsai/Bonsai.config` into `bonsai/Packages/`.

The `Bonsai` and `Bonsai.Core` entries in `Bonsai.config` set the Bonsai version that runs (the zip that `setup.ps1` downloads is the starter that installs it). The other package versions also come from `Bonsai.config`. If `Bonsai.exe` already exists, nothing is re-downloaded and `setup.cmd` is not run, so editing `Bonsai.config` has no effect until the packages are reinstalled (see below).

---

## Prerequisites

These should only need to be installed once on a fresh new system, and are not required if simply refreshing the install or deploying to a new folder.

- Windows 10 or 11
- [Visual Studio Code](https://code.visualstudio.com/) (highly recommended for editing code scripts and git commits)
- [Git for Windows](https://gitforwindows.org/) (highly recommended for cloning and manipulating this repository)
- [.NET Framework 4.7.2 Developer Pack](https://dotnet.microsoft.com/download/dotnet-framework/thank-you/net472-developer-pack-offline-installer) (required for intellisense when editing code scripts)
- [Visual C++ Redistributable for Visual Studio 2012](https://www.microsoft.com/en-us/download/details.aspx?id=30679) (native dependency for OpenCV)

### Hardware specific:
Those are needed to run Bonsai workflows onto the allen institute rigs with HARP devices. 
- [FTDI CDM Driver 2.12.28](https://www.ftdichip.com/Drivers/CDM/CDM21228_Setup.zip) (serial port drivers for HARP devices)
- [Spinnaker SDK 1.29.0.5](https://www.flir.co.uk/support/products/spinnaker-sdk/#Downloads) (device drivers for FLIR cameras)
  - On FLIR website: `Download > archive > 1.29.0.5 > SpinnakerSDK_FULL_1.29.0.5_x64.exe`
- [NI-DAQmx 19.0](https://www.ni.com/en-gb/support/downloads/drivers/download.ni-daq-mx.html#301173) (drivers for NI-DAQ devices)

---

## Bonsai.config: fresh installs vs existing installs

`bonsai/Bonsai.config` always has `<Packages>` and `<AssemblyReferences>`. When the install step runs (`setup.cmd` → `Bonsai.exe --no-editor`), Bonsai adds two more sections to it:

- `<AssemblyLocations>` (paths such as `Packages/<id>.<version>/lib/...`)
- `<LibraryFolders>`

These two sections matter in opposite ways:

| Situation | Config it needs |
|---|---|
| **Fresh install** (`Bonsai.exe` and `Packages/` do not exist yet) | **A config WITHOUT `<AssemblyLocations>` and `<LibraryFolders>`.** They point at `Packages/` folders that do not exist yet, and a fresh install from a config that has them fails. |
| **Existing install** (`Packages/` already installed) | **A config WITH those two sections.** Bonsai cannot find its assemblies without them, and only the install step writes them. |

Check which form a checkout has:

```
findstr /i "AssemblyLocation LibraryFolder" bonsai\Bonsai.config
```

No output means the fresh-install form. Output means the form for an existing install.

**What this means in practice**
- **Fresh install:** before the first run, make sure `bonsai\Bonsai.config` is the form without the two sections. If it has them, delete the whole `<AssemblyLocations>...</AssemblyLocations>` and `<LibraryFolders>...</LibraryFolders>` blocks first. The install then writes the sections itself.
- **The launcher resets the repo when it switches commits.** It runs `git reset --hard`, which restores the committed `Bonsai.config` and discards what the install wrote. `Packages/` and `Bonsai.exe` are git-ignored, so they stay. If the committed config has no location sections, the existing install stops working (Bonsai cannot find its assemblies) until the install step is run again. The launcher only runs `setup.cmd` when `Bonsai.exe` is missing, so it will not do this by itself.
- A pinned commit therefore has to match how it will be used: a commit whose config has the sections for installs that already exist, and the fresh-install form for new rigs.
- Do not commit `bonsai/Bonsai.config.backup` (it was removed from the repo).

## Troubleshooting

### Force a clean reinstall of Bonsai and its packages

In the `bonsai` folder of the clone, rename the install and run the launcher or `setup.cmd` again:

```
ren Packages Packages_backup
ren Bonsai.exe Bonsai.exe.bak
```

### Bonsai still loads the wrong package versions

NuGet keeps caches outside the repo, so a new clone can still pick up old packages. Clear them:

```
dotnet nuget locals all --list
dotnet nuget locals all --clear
```

The folders are `%UserProfile%\.nuget\packages`, `%LocalAppData%\NuGet\v3-cache` and `%LocalAppData%\Temp\NuGetScratch`. These are per user, so run the commands as the account that runs Bonsai. `NUGET_PACKAGES` or a `NuGet.Config` under `%ProgramData%\NuGet\Config` can move them.

### Files are missing from the clone (for example `src/Extensions` is empty)

Run `git status`. If tracked files show as deleted, restore them with `git restore .`, or reset the clone to the pinned commit with `git reset --hard <commit>`. This discards local changes, so check `git status` first. Do not share one clone between workflows that run at the same time. Give each workflow its own clone and `local_repository_path`.

### Bonsai cannot find assemblies after the launcher switched commits

A launch that worked before now fails to find assemblies, and `bonsai\Bonsai.config` has no `AssemblyLocation` lines. The launcher's `git reset --hard` restored a config without them while `Packages/` was still installed. Run `bonsai\setup.cmd` once to regenerate them (it does not re-download Bonsai when `Bonsai.exe` exists). See [Bonsai.config: fresh installs vs existing installs](#bonsaiconfig-fresh-installs-vs-existing-installs).

### Bonsai exits with code 3762504530 (0xE0434352)

The stack trace ends in `System.IO.Ports.SerialStream.Finalize()`. This is a .NET Framework double-dispose of the serial port at exit. The data has been saved. `Bonsai.Harp 3.6.1` triggers it, and `3.5.2` does not. The launcher can treat the code as success with `bonsai_acceptable_exit_codes: [3762504530]`.

### "failed to load image texture" or a movie fails to load

Paths in a workflow are relative to the `.bonsai` file. For a workflow in `src/Mindscope/`, the gamma LUT is `..\Gamma\2025-05-22-SLAP2-gammalut.bmp` and movies are in `..\Movies\`.

### Include workflow not found (`CameraOnlineQC` / `CameraOnlineQA`)

`src/Extensions/CameraOnlineQC.bonsai` was renamed to `CameraOnlineQA.bonsai` on 2026-01-29. A workflow and its `Extensions` folder must come from the same commit.
