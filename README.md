This folder stores Bonsai code used by AIND Ophys to run passive visual stimulation tasks on the Visual Cortex Observatory (VCO) rig.

## Organization

All Bonsai workflows should go into `./src`, along with the `Extensions` folder.

## Deployment

To deploy the Bonsai code, run `./bonsai/setup.cmd`. This small script will download and regenerate the current Bonsai environment ([see tutorial for further details.](https://bonsai-rx.org/docs/articles/environments.html)).
Each time you change a project dependency via the `Package Manager`, the `Bonsai.Config` file will be updated. Only commit those changes after removing the machine-generated sections (see [Bonsai.config rules](#bonsaiconfig-rules)).

### How the install works

1. `setup.cmd` runs `setup.ps1` with the execution policy bypassed.
2. `setup.ps1` only downloads Bonsai if `bonsai/Bonsai.exe` is missing. It then runs `Bonsai.exe --no-editor`.
3. That first launch installs every package listed in `bonsai/Bonsai.config` into `bonsai/Packages/`.

The Bonsai version comes from the download URL in `setup.ps1`. The package versions come from `Bonsai.config`. If `Bonsai.exe` already exists, nothing is re-downloaded, so editing `Bonsai.config` has no effect until the packages are reinstalled (see below).

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

## Bonsai.config rules

`bonsai/Bonsai.config` must contain only `<Packages>` and `<AssemblyReferences>`. Bonsai adds two more sections every time it runs:

- `<AssemblyLocations>` (paths such as `Packages/<id>.<version>/lib/...`)
- `<LibraryFolders>`

**Never commit these two sections.** They point at `Packages/` folders that do not exist on a fresh install, which breaks it. Before committing `Bonsai.config`, check that this returns nothing:

```
findstr /i "AssemblyLocation LibraryFolder" bonsai\Bonsai.config
```

If it does return lines, delete the whole `<AssemblyLocations>...</AssemblyLocations>` and `<LibraryFolders>...</LibraryFolders>` blocks before committing. Do not commit `bonsai/Bonsai.config.backup` either.

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

### Bonsai exits with code 3762504530 (0xE0434352)

The stack trace ends in `System.IO.Ports.SerialStream.Finalize()`. This is a .NET Framework double-dispose of the serial port at exit. The data has been saved. `Bonsai.Harp 3.6.1` triggers it, and `3.5.2` does not. The launcher can treat the code as success with `bonsai_acceptable_exit_codes: [3762504530]`.

### "failed to load image texture" or a movie fails to load

Paths in a workflow are relative to the `.bonsai` file. For a workflow in `src/Mindscope/`, the gamma LUT is `..\Gamma\2025-05-22-SLAP2-gammalut.bmp` and movies are in `..\Movies\`.

### Include workflow not found (`CameraOnlineQC` / `CameraOnlineQA`)

`src/Extensions/CameraOnlineQC.bonsai` was renamed to `CameraOnlineQA.bonsai` on 2026-01-29. A workflow and its `Extensions` folder must come from the same commit.
