#!/usr/bin/env python3

import argparse
import os
import re
from typing import Any, List

import yaml

TITLE = 'title'
DEFAULT_SCENARIOS = 'default_scenarios'
SCENARIOS = 'scenarios'
DEFAULT_LEVELS = 'default_levels'
LEVELS = 'levels'
DEFAULT_LECTURERS = 'default_lecturers'
LECTURERS = 'lecturers'
COURSES = 'courses'
ALL = 'all'
DEFAULT = 'default'


class ConfigurationError(Exception):
    pass


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generates a ROS-I Academy course from a YAML file."
    )
    parser.add_argument(
        '-c', '--course',
        metavar='file',
        required=True,
        type=str,
        help="Specify the YAML file that describes the course."
    )
    parser.add_argument(
        '-f', '--format',
        choices=['html', 'latexpdf'],
        default='html',
        type=str,
        help="Use either .html as the output format or generate a .pdf instead."
    )
    parser.add_argument(
        '-o', '--output',
        metavar='directory',
        type=str,
        default='./build',
        help="Specify where Sphinx will save the generated output."
    )

    return parser.parse_args()


def check_config_key_list(parent: str, artifact: List[str],
                          required: List[str] = None,
                          optional: List[str] = None):
    for key in (required or []):
        if key not in artifact:
            raise ConfigurationError("Key '%s' is required in '%s'."
                                     % (key, parent))
    for key in artifact:
        if key not in (required or []) + (optional or []):
            raise ConfigurationError("Key '%s' is not allowed in '%s'."
                                     % (key, parent))


def check_config_list_of_strings(parent: str, artifact: Any) -> None:
    if type(artifact) is not list:
        raise ConfigurationError("Value of '%s' must be a list, but is '%s'."
                                 % (parent, type(artifact)))

    for index, item in enumerate(artifact):
        if type(item) is not str:
            raise ConfigurationError("Item %i of '%s' must be a string, but is "
                                     "'%s'." % (index, parent, type(item)))


def check_config_scenario_list(parent: str, artifact: List[str]) -> None:
    # scenario descriptions must be lower snake case with some limitation
    scenario_description = re.compile('^[a-z](_?[a-z0-9]+)*$')
    for index, item in enumerate(artifact):
        if scenario_description.match(item) is None:
            raise ConfigurationError("Item %i of '%s' must contain only latin "
                                     "lower case, numbers (except the first "
                                     "letter), and single underscores (except "
                                     "the first and last letter), but is '%s'."
                                     % (index, parent, item))


def check_config_level_list(parent: str, artifact: List[str]) -> None:
    # levels have standardised names based on CEFR
    levels = ['beginner',
              'elementary',
              'intermediate',
              'advanced',
              'proficient',
              ALL,
              DEFAULT, ]
    for index, item in enumerate(artifact):
        if item not in levels:
            raise ConfigurationError("Item %i of '%s' must be one of %s, but "
                                     "is '%s'." % (index, parent, levels, item))


def parse_configuration(file_name: str) -> dict:
    with open(file_name, 'r') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

        # all required keys must be present
        check_config_key_list('root', config.keys(),
                              required=[TITLE,
                                        DEFAULT_SCENARIOS,
                                        DEFAULT_LEVELS,
                                        DEFAULT_LECTURERS,
                                        COURSES, ])

        # title must be a string
        if type(config[TITLE]) is not str:
            raise ConfigurationError("Value of '%s' must be a string, but is "
                                     "'%s'." % (TITLE, type(config[TITLE])))

        # each default option must be a list of strings
        for key in [DEFAULT_SCENARIOS,
                    DEFAULT_LEVELS,
                    DEFAULT_LECTURERS, ]:
            check_config_list_of_strings(key, config[key])

        check_config_scenario_list(DEFAULT_SCENARIOS, config[DEFAULT_SCENARIOS])
        check_config_level_list(DEFAULT_LEVELS, config[DEFAULT_LEVELS])

        # courses must be be contained in a dictionary
        if type(config[COURSES]) is not dict:
            raise ConfigurationError("Value of '%s' must be a dictionary, but "
                                     "is %s."
                                     % (COURSES, type(config[COURSES])))

        for course, item in config[COURSES].items():
            if type(item) is not dict:
                raise ConfigurationError("Value of '%s' must be a dictionary, "
                                         "but is %s." % (course, type(item)))

            check_config_key_list(course, (item or {}),
                                  optional=[SCENARIOS,
                                            LEVELS,
                                            LECTURERS, ])

            for key in item.keys():
                check_config_list_of_strings(course + '/' + key, item[key])

            check_config_scenario_list(SCENARIOS, item.get(SCENARIOS, []))
            check_config_level_list(LEVELS, item.get(LEVELS, []))

        return config


def generate_build(config: dict) -> str:
    flags = ''
    for course, item in config[COURSES].items():
        for key, default_key in [(SCENARIOS, DEFAULT_SCENARIOS),
                                 (LEVELS, DEFAULT_LEVELS),
                                 (LECTURERS, DEFAULT_LECTURERS), ]:
            item.setdefault(key, config[default_key])
            if DEFAULT in item[key]:
                item[key].remove(DEFAULT)
                item[key].extend(config[default_key])
            if ALL in item[key]:
                item[key] = [ALL]

            if key in [SCENARIOS,
                       LEVELS, ]:
                for entry in item[key]:
                    flags += ' -t %s_%s_%s' % (course, key, entry)
    return flags


def main():
    arguments = parse_arguments()
    configuration = parse_configuration(arguments.course)
    os.system('make %s BUILD_DIR="%s" SPHINX_OPTS="%s"'
              % (arguments.format,
                 arguments.output,
                 generate_build(configuration)))


if __name__ == "__main__":
    main()
