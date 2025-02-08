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

## Enable (Free)RTOS Aware Debugging
```
openocd ... -c "[target current] configure -rtos FreeRTOS"
```

## Misc Save For CppDbg Attempt With ARM
Looks like the Microsoft cppdbg can also be used to debug an ARM target. The OpenOCD
server needs to be started before the debug launch, but it seems to work okay.

```
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Debug",
            "type":"cppdbg",
            "request": "launch",
            "program": "${command:cmake.launchTargetPath}",
            "cwd": "${workspaceFolder}",
            "miDebuggerPath": "/opt/gcc-arm-none-eabi/bin/arm-none-eabi-gdb",
            "miDebuggerServerAddress": "localhost:3333",
            "stopAtEntry": false,
            "preLaunchTask": "Wait For OpenOCD",
            "logging": {
                "engineLogging" : false, // Log the MICommands sent to the debugger and the responses returned. 
                "trace"         : false, 
                "traceResponse" : true
            },
            "customLaunchSetupCommands": [
                { "text": "set verbose on",                                            "ignoreFailures": false },
                { "text": "set debug remote 1",                                        "ignoreFailures": false },
                { "text": "set remotelogfile ${workspaceFolder}/gdb-server-debug.txt", "ignoreFailures": false },
                { "text": "set logging file ${workspaceFolder}/gdb-client-debug.log",  "ignoreFailures": false },
                { "text": "set logging debugredirect on",                              "ignoreFailures": false },
                { "text": "set logging overwrite on",                                  "ignoreFailures": false },
                { "text": "set logging enabled on",                                    "ignoreFailures": false },
                { "text": "set architecture armv7e-m",                                 "ignoreFailures": false },
                { "text": "file ${command:cmake.launchTargetPath}",                    "ignoreFailures": false },
                { "text": "target extended-remote :3333",                              "ignoreFailures": false },
                { "text": "monitor reset init ",                                       "ignoreFailures": false },
                { "text": "load ${command:cmake.launchTargetPath}",                    "ignoreFailures": false },
                { "text": "monitor reset halt ",                                       "ignoreFailures": false },
            ],
            "launchCompleteCommand": "exec-run",
        }
    ]
}
```


## Extensions
Install Yeoman globally:
```
npm install --global yo generator-code
```

Install the Visual Studio Code Extensions CLI:
```
npm install --global @vscode/vsce
```

Create an extension:
```
yo code
```

`src/extension.ts` the main file
`F5` from this file to debug

Extension was not being compiled! Run `tsc --watch` from the root directory.
Or always run `npm run compile` from the root dir (tsc eaiser!)

Run `vsce package` to package and create the `.vsix` file.
Install using `code --install-extension my-extension-0.0.1.vsix` [[Ref]](https://code.visualstudio.com/api/working-with-extensions/publishing-extension#packaging-extensions)

Test using `npm run test`

`npm install --save-dev mocha chai`
