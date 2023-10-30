## Project too big to scan
Add something like the following to `settings.json`:

```
    "files.watcherExclude": {
        "**/.git/objects/**": true,
        "**/.git/subtree-cache/**": true,
        "**/node_modules/*/**": true,
        "**/.hg/store/**": true,
        "**/.nox/**": true,
        "**/.mypy_cache/**": true,
        "**/.github/**": true,
        "**/.pytest_cache/**": true
    }
```
## Column Width Markers
Edit either the folder, workspace, or user `settings.json` file (quick access via
File > Preferences > Settings and then searching for `editor.rulers`) and add the following:

```
    "editor.rulers": [80, 100],
    "workbench.colorCustomizations": {
        "editorRuler.foreground": "#ff0000"
    },
```

## Setting Up PyTest
Add to `settings.json`:

```
    "python.testing.pytestArgs": [
        "-vvs", "tests"
    ],
    "python.testing.unittestEnabled": false,
    "python.testing.pytestEnabled": true,
    "terminal.integrated.env.linux": {"PYTHONPATH": "${workspaceFolder}"}
```

## Default Build Using Makefile
In `tasks.json` in your folder/workspace `.vscode` config:

```
{
    "version": "2.0.0",
    "tasks": [
        {
            "type": "shell",
            "label": "Build Project",
            "command": "make <command line args here>,
            "options": {
                "cwd": "${workspaceFolder}/someOptionalLocation"
            },
            "group": {
                "kind": "build",
                "isDefault": true   <---- NOTE this makes CTRL+SHIFT+b run this task
            },
            "problemMatcher": {
                "base": "$gcc", 
                "fileLocation": ["relative", "${workspaceFolder}/someOptionalLocation"]
            }
        },
        ...
    }
}
```

If you require some user input to pass to the build, for example some kind of label etc,

```
{
    "version": "2.0.0",
    "tasks": [
        {
            "type": "shell",
            "label": "Build Project",
            "command": "make SOMEVAR=${input:variableNameHere},  <---+
            ... snip ...                                             |
        },                                                           |
        ...                                                          |
    },                                                               |
    "inputs": [                                                      |
        {                                                            |
            "type": "promptString",                                  |
            "id": "variableNameHere", <------------------------------+
            "description": "Put a description here",
            "default": "Some string"
        }
    ]
}
```


## Ceedling
### Integrate into test tab
Add to `settings.json`:

```
    "ceedlingExplorer.projectPath": "./path/from/prjRoot/to/ceedlingCmd",
    "ceedlingExplorer.debugConfiguration": "ceedling_gdb",
    "ceedlingExplorer.problemMatching": {
    }
```

### Using GDB debugger
In `launch.json` in your folder/workspace `.vscode` config:

```
        {
            "name": "ceedling_gdb",
            "type": "cppdbg",
            "request": "launch",
            "program": "${workspaceFolder}/.../ceedling/build/test/out/${command:ceedlingExplorer.debugTestExecutable}",
            "args": [],
            "stopAtEntry": false,
            "cwd": "${workspaceFolder}",
            "environment": [],
            "externalConsole": false,
            "MIMode": "gdb",
            "miDebuggerPath": "/usr/bin/gdb",
            "setupCommands": [
                {
                    "description": "Enable pretty-printing for gdb",
                    "text": "-enable-pretty-printing",
                    "ignoreFailures": true
                }
            ],
        }
```

## Segger Debugging
Add to `launch.json`

```
    "configurations": [
        {
            "cwd": "${workspaceRoot}/any/path/u/like",
            "executable": "./path/to/ELF",
            "name": "Debug My App",
            "request": "launch",
            "type": "cortex-debug",
            "showDevDebugOutput": "parsed",
            "servertype": "jlink",
            "serverpath": "/path/to/segger/jlink/X.Y/JLinkGDBServerCLExe",
            "serverArgs": ["-strict", "-timeout", "0", "-endian", "little", "-speed", "1000"],
            "overrideLaunchCommands": [],
            "postLaunchCommands": [
                <list of strings>
            ],
            "runToEntryPoint": "main",
            "postRestartCommands": [
                <list of strings>
            ],
            "armToolchainPath": "/path/to/gnu/arm/compiler/bin/",
            "device": "ATSAML21J18B",
            "interface": "swd",
            "serialNumber": "", // add J-Link serial number if having multiple attached the same time.
            "runToMain": false,
            "svdFile": "${workspaceRoot}/path/to/svd/file.svd",
        },
        ...
    ]
```
