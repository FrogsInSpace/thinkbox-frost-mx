# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
from typing import Any
from cpt.packager import ConanMultiPackager

import argparse
import platform
import pprint


VALID_MAX_CONFIGS: dict[tuple[str, str], set[str]] = {
    ('Visual Studio', '15'): { '2017', '2018', '2019', '2020', '2021', '2022' },
    ('Visual Studio', '16'): { '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024' },
    ('Visual Studio', '17'): { '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026' }
}

VALID_VRAY_CONFIGS: dict[str, set[str]] = {
    '5': { '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024' },
    '6': { '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025' },
    '7': { '2020', '2021', '2022', '2023', '2024', '2025', '2026' }
}

COMMON_PACKAGER_ARGS: dict[str, Any] = {
    'build_types': ['Release'],
    'archs': ['x86_64'],
    'build_policy': 'missing'
}

WINDOWS_PACKAGER_ARGS: dict[str, Any] = {
    'visual_versions': ['17'],
    'visual_runtimes': ['MD']
}

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', default=None, help='The Conan username to use for the built package.')
    parser.add_argument('-c', '--channel', default=None, help='The Conan channel to use for the built package.')
    parser.add_argument('-o', '--option', action='append', dest='options', help='Specify package options to be used by the build.')
    parser.add_argument('--dry-run', action='store_true', help='Print the configurations that would be built without actually building them.')
    return parser.parse_args()

def main() -> None:
    args = parse_arguments()

    packager_args = {
        'username': args.username,
        'channel': args.channel,
        'options': args.options
    }
    packager_args.update(COMMON_PACKAGER_ARGS)

    if platform.system() == 'Windows':
        packager_args.update(WINDOWS_PACKAGER_ARGS)
    else:
        raise Exception('Platform not supported.')

    builder = ConanMultiPackager(**packager_args)
    builder.add_common_builds(build_all_options_values=[
        'max_version',
        'vray_version'
    ], pure_c=False)
    builder.remove_build_if(
        lambda build: build.options['frostvry:max_version'] not in VALID_VRAY_CONFIGS[build.options['frostvry:vray_version']])

    if args.dry_run:
        pprint.pprint(builder.builds, indent=4)
    else:
        builder.run()


if __name__ == '__main__':
    main()
