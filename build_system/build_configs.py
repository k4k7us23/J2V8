"""
This file contains the collection of build-configurations that are available
for selection when running the build.py script with the --interactive, -i parameter.

Parameters for the build can be specified by their variable-name ("dest" defined in the cli.py arguments).
An array of build-steps can also be specified here, if none are specified then "all" steps will be run.
"""
import constants as c

configs = [
      # ANDROID builds
      {
            "name": "android-x86 @ Docker",
            "params": {
                  "target": c.target_android,
                  "arch": c.arch_x86,
                  "docker": True,
                  "node_enabled": True,
            },
      },
      {
            "name": "android-x86_64 @ Docker",
            "params": {
                  "target": c.target_android,
                  "arch": c.arch_x86_64,
                  "docker": True,
                  "node_enabled": True,
            },
      },
      {
            "name": "android-arm @ Docker",
            "params": {
                  "target": c.target_android,
                  "arch": c.arch_arm,
                  "docker": True,
                  "node_enabled": True,
            },
      },
      {
            "name": "android-arm64 @ Docker",
            "params": {
                  "target": c.target_android,
                  "arch": c.arch_arm64,
                  "docker": True,
                  "node_enabled": False,
            },
      },
  ]
