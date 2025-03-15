# Development

This repository manages the Python development environment as a [Nix flake](https://nixos.wiki/wiki/Flakes) and requires [Nix to be installed](https://github.com/DeterminateSystems/nix-installer).

When you enter the directory by default it will build & load the Nix development
shell via `direnv`.

Pypi dependencies are installed using the `dev setup` command.

```console
> dev
USAGE: dev <COMMAND>

COMMANDS:
  setup      Ensures configuration has been initialized
  check      Ensures code is formatted and that tests pass
  dream2nix  Manage nix flake dev shell & python deps
  pypi       Python package management
```

## Commands

- [setup](#setup)
- [check](#check)
- [dream2nix](#dream2nix)
  - [lock](#dream2nix-lock)
  - [build](#dream2nix-build)
  - [clean](#dream2nix-clean)
- [pypi](#pypi)
  - [build](#pypi-build)
  - [publish](#pypi-publish)
  - [clean](#pypi-clean)

### setup

```console
> dev setup -h
Ensures all necessary configuration has been initialized

USAGE: dev setup [OPTIONS]

OPTIONS:
  -h, --help     Print help
```

### check

```console
> dev check -h
Ensures code is formatted and that tests pass

USAGE: dev check [OPTIONS]

OPTIONS:
      --format        Run formatters
      --lint          Run ruff linter
      --typecheck     Run typechecks
      --test          Run tests
  -h, --help          Print help
```

### dream2nix

```console
> dev dream2nix
Manage nix flake dev shell & python deps

USAGE: dev dream2nix <COMMAND>

COMMANDS:
  lock   Create lock files
  build  Build packages from lock files
  clean  Delete dream2nix artifacts
```

#### dream2nix lock

```console
> dev dream2nix lock -h
Create lock files

USAGE: dev dream2nix lock
      --prod     Create production lock file
      --dev      Create development lock file
  -h, --help     Print help
```

#### dream2nix build

```console
> dev dream2nix build -h
Build packages from lock files

USAGE: dev dream2nix build [OPTIONS]

OPTIONS:
      --prod     Create production lock file
      --dev      Create development lock file
  -h, --help     Print help
```

#### dream2nix clean

```console
> dev dream2nix clean -h
Delete dream2nix artifacts

USAGE: dev dream2nix clean
```


### pypi

```console
> dev pypi
Python package management

USAGE: dev pypi <COMMAND>

COMMANDS:
  build    Build distribution package
  publish  Publish distribution package
  clean    Delete distribution package
```

#### pypi build

```console
> dev pypi build -h
Build distribution package

USAGE: dev pypi build
```

#### pypi publish

```console
> dev pypi publish -h
Publish distribution package

USAGE: dev pypi publish
```

#### pypi clean

```console
> dev pypi clean -h
Delete distribution package

USAGE: dev pypi clean
```
