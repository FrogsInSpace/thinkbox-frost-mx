# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
from typing import Any
from conans import ConanFile

import os
import pathlib
import shutil

VALID_MAX_CONFIGS: dict[tuple[str, str], set[str]] = {
    ('Visual Studio', '15'): { '2017', '2018', '2019', '2020', '2021', '2022' },
    ('Visual Studio', '16'): { '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024' },
    ('Visual Studio', '17'): { '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026', '2027' },
}

VALID_VRAY_CONFIGS: dict[str, set[str]] = {
    '5': { '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024' },
    '6': { '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025' },
    '7': { '2020', '2021', '2022', '2023', '2024', '2025', '2026' },
}

SETTINGS: dict[str, Any] = {
    'os': ['Windows'],
    'compiler': {
        'Visual Studio': {'version': ['15', '16', '17']},
    },
    'build_type': None,
    'arch': 'x86_64'
}

# DEFAULT_VRAY_PATH: str = 'C:/Program Files/Chaos Group/V-Ray/3ds Max {}'
# DEFAULT_VRAY_PATH: str = os.getenv('VRAY_FOR_3DSMAX2024_SDK', 'C:/Program Files/Chaos Group/V-Ray/3ds Max {}')
CHAOSGROUP_SDK_ROOT: str = os.getenv('CHAOSGROUP_SDK_ROOT', 'F:/_SDKs/3dsMax/ChaosGroup/' )
VRAY_SDK_PATH: str = CHAOSGROUP_SDK_ROOT +  '/Vray{}/3dsMax{}'
 
class VRayMaxSDKConan(ConanFile):
    name: str = 'vraysdk'
    version: str = '1.0.0'
    description: str = 'A Conan package containing the Chaos Group V-Ray SDK.'
    settings: dict[str, Any] = SETTINGS
    options: dict[str, Any] = {
        'max_version': ['2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026', '2027'],
        'vray_version': ['5','6','7'],
        'vray_path': 'ANY'
    }

    def configure(self) -> None:
        if self.options.max_version == None:
            self.options.max_version = '2024'
        if self.options.vray_version == None:
            self.options.vray_version = '5'
        if self.options.vray_path == None:
            self.options.vray_path = VRAY_SDK_PATH.format(self.options.vray_version, self.options.max_version)
            # self.options.vray_path = DEFAULT_VRAY_PATH.format(self.options.max_version)
        print ('VraySDK path: ', self.options.vray_path)
        if self.options.vray_path == None:
            print ('VraySDK path not found, terminating...', self.options.vray_path)
            exit()
        
    def validate(self) -> None:
        compiler = str(self.settings.compiler)
        compiler_version = str(self.settings.compiler.version)
        compiler_tuple = (compiler, compiler_version)
        max_version = str(self.options.max_version)
        vray_version = str(self.options.vray_version)
        if max_version not in VALID_MAX_CONFIGS[compiler_tuple]:
            raise Exception(f'{str(compiler_tuple)} is not a valid configuration for 3ds Max {max_version}')
        if max_version not in VALID_VRAY_CONFIGS[vray_version]:
            raise Exception(f'{vray_version} is not a valid major Vray version for 3ds Max {max_version}')

    def build(self) -> None:
        # Copy Headers
        build_include_dir = os.path.join(self.build_folder, 'include')
        if os.path.exists(build_include_dir):
            shutil.rmtree(build_include_dir)
        shutil.copytree(
            os.path.join(str(self.options.vray_path), 'include'),
            build_include_dir
        )

        # Copy Libraries
        build_library_dir = os.path.join(
            self.build_folder,
            'lib'
        )
        if os.path.exists(build_library_dir):
            shutil.rmtree(build_library_dir)
        os.makedirs(build_library_dir)

        lib_source_path = pathlib.Path(str(self.options.vray_path)) / 'lib'
        for lib in lib_source_path.glob('*.lib'):
            shutil.copy(
                str(lib),
                build_library_dir
            )

    def package(self) -> None:
        self.copy('*', dst='lib', src='lib')
        self.copy('*', dst='include', src='include')

    def package_info(self) -> None:
        self.cpp_info.libs = self.collect_libs()

    def deploy(self) -> None:
        self.copy('*', dst='lib', src='lib')
        self.copy('*', dst='include', src='include')
