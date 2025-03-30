# fre-conan-index

This repository contains a curated collection of Conan package recipes maintained by [Free Range Engineering](https://freerangeengineering.se/). It is intended to be used as a **Local Recipes Index Repository**, for inclusion as a Git submodule or direct clone in projects that use Conan for C/C++ dependency management.

## Purpose

The `fre-conan-index` repository provides:

- A consistent, version-controlled index of Conan recipes.
- Support for both open and closed source projects that prefer to manage their dependencies locally.
- A structure compatible with `conan export` and `conan create` for local package development and distribution.

This setup is especially useful for organizations or projects that:

- Want full control over their dependency recipes.
- Need patched or custom versions of upstream packages.
- Prefer to avoid depending on external remotes for reproducibility or reliability.

## Out of Scope

⚠️ Not for Upstreaming to Conan Center Index

While this repository is intended to be shared and reused, the packages it contains are not intended for submission to conan-center-index. This is out of scope for the following reasons:

- Recipes may contain project-specific patches or configurations.
- Some packages may be simplified or tailored for local use only.
- Strict adherence to Conan Center guidelines is not a goal of this repository.
- 
## Usage

### As a Git Submodule

Add this repository to your project as a submodule:

```
git submodule add https://github.com/FreeRangeEngineering/fre-conan-index.git extern/conan-index
```

Then configure Conan to use it as a local remote:

```
conan remote add fre-local /extern/conan-index 
```

This will make all recipes in the index available to your project.

### As a Standalone Local Index

You can also clone the repository directly and use it as a standalone local index:

```
git clone https://github.com/FreeRangeEngineering/fre-conan-index.git
conan remote add fre-local fre-conan-index 
```

## tasks.py `create` Command

The `create` command in `tasks.py` is primarily intended as a utility to verify that the packages in this repository can be successfully built. It ensures that the recipes are valid and compatible with the current system architecture and operating system.

### Usage

To use the `create` command, run the following:

```
invoke create
```

This will attempt to build all packages defined in the repository for the current system environment.

### Recommendation

While the `create` command is useful for validation purposes, users are encouraged to use the following alternatives for consuming the packages:

1. **`conan cci:export-all-versions` Command**  
   This command is available in the [Conan Extensions](https://github.com/conan-io/conan-extensions) and allows you to export all versions of a package to your local cache efficiently.

2. **Local Repository Functionality**  
   Use the local repository functionality in Conan to consume the packages directly from this repository. This approach is more suitable for integrating the packages into your workflows.

## Contributing

Contributions are welcome if they align with the goals of this project:

- Simplicity over completeness.
- Practicality over standardization.
- Usability in local and submodule-based workflows.

If you submit changes, please ensure they are compatible with Conan v2.

## License

This repository is licensed under the MIT License. Individual recipes may include or be derived from third-party code and are subject to the terms of their respective upstream licenses.