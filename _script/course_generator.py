#!/usr/bin/env python3

# Copyright (C) 2019-2020 MASCOR Institute. All rights reserved.

__author__ = "Meeßen, Marcus"
__copyright__ = "Copyright (C) 2019-2020 MASCOR Institute"
__version__ = "1.0"

import argparse
import os
from pprint import pprint
from typing import Any, List, Dict

import yaml
from sphinx.util.tags import Tags

TITLE: str = 'title'
DEFAULT_SCENARIOS: str = 'default_scenarios'
SCENARIOS: str = 'scenarios'
DEFAULT_LEVELS: str = 'default_levels'
LEVELS: str = 'levels'
DEFAULT_LECTURERS: str = 'default_lecturers'
LECTURERS: str = 'lecturers'
COMPONENTS: str = 'components'
ALL: str = 'all'
DEFAULT: str = 'default'


class ConfigurationError(Exception):
    pass


class Arguments(object):
    source: str
    format: str
    output: str
    root: str

    @staticmethod
    def parse_arguments() -> None:
        parser = argparse.ArgumentParser(
            description="Generates an entire ROS-I Academy course or program "
                        "from a YAML file.",
        )
        parser.add_argument('-s', '--source',
                            metavar='file',
                            required=True,
                            type=str,
                            help="Specify the YAML file that describes the "
                                 "course or program.",
                            )
        parser.add_argument('-f', '--format',
                            choices=['html', 'latexpdf'],
                            default='html',
                            type=str,
                            help="Use either HTML as the output format or "
                                 "generate a PDF instead.",
                            )
        parser.add_argument('-o', '--output',
                            metavar='directory',
                            type=str,
                            default='./build',
                            help="Specify where Sphinx will save the generated "
                                 "output.",
                            )
        parser.add_argument('-r', '--root',
                            metavar='directory',
                            type=str,
                            default=os.getcwd(),
                            help="Specify the root directory of the Sphinx "
                                 "documentation, i.e. where the `conf.py` is "
                                 "located. The generated `index.rst` will be "
                                 "placed there.",
                            )

        for argument, value in vars(parser.parse_args()).items():
            setattr(Arguments, argument, value)


class Consistency(object):
    levels: Dict[str, str]
    scenarios: Dict[str, str]

    @staticmethod
    def is_valid_key_list(parent: str, artifact: List[str],
                          required: List[str] = None,
                          optional: List[str] = None) -> None:
        for key in (required or []):
            if key not in artifact:
                raise ConfigurationError("Key '%s' is required in '%s'."
                                         % (key, parent))

        for key in artifact:
            if key not in (required or []) + (optional or []):
                raise ConfigurationError("Key '%s' is not allowed in '%s'."
                                         % (key, parent))

    @staticmethod
    def is_list_of_strings(parent: str, artifact: Any) -> None:
        if type(artifact) is not list:
            raise ConfigurationError("Value of '%s' must be a list, but is "
                                     "'%s'." % (parent, type(artifact)))

        for index, item in enumerate(artifact):
            if type(item) is not str:
                raise ConfigurationError("Item %d of '%s' must be a string, "
                                         "but is '%s'."
                                         % (index, parent, type(item)))

    @staticmethod
    def is_dictionary(parent: str, artifact: Any) -> None:
        if type(artifact) is not dict:
            raise ConfigurationError("Value of '%s' must be a dictionary, "
                                     "but is %s." % (parent, type(artifact)))

    @staticmethod
    def is_scenario_list(parent: str, artifact: List[str]) -> None:
        scenarios = Consistency.scenarios
        for index, item in enumerate(artifact):
            if item not in scenarios:
                raise ConfigurationError("Item %d of '%s' must be one of %s, "
                                         "but is '%s'."
                                         % (index, parent, scenarios, item))

    @staticmethod
    def is_level_list(parent: str, artifact: List[str]) -> None:
        levels = Consistency.levels
        for index, item in enumerate(artifact):
            if item not in levels:
                raise ConfigurationError("Item %d of '%s' must be one of %s, "
                                         "but is '%s'."
                                         % (index, parent, levels, item))

    @staticmethod
    def component_exists(artifact: str) -> None:
        base_file_name: str = os.path.join(Arguments.root, artifact)
        if (artifact not in [ALL, DEFAULT]
                and not os.path.exists('%s.yaml' % base_file_name)
                and not os.path.exists('%s.rst' % base_file_name)):
            raise ConfigurationError("Component '%s' points to '%s' but "
                                     "there is no such .yaml or .rst file."
                                     % (artifact, base_file_name))

    @staticmethod
    def check_consistency(config: dict) -> None:
        # all required keys must be present
        Consistency.is_valid_key_list('root', list(config.keys()),
                                      required=[
                                          TITLE,
                                          COMPONENTS,
                                      ],
                                      optional=[
                                          DEFAULT_SCENARIOS,
                                          DEFAULT_LEVELS,
                                          DEFAULT_LECTURERS,
                                      ])

        # title must be a string
        if type(config[TITLE]) is not str:
            raise ConfigurationError("Value of '%s' must be a string, but is "
                                     "'%s'." % (TITLE, type(config[TITLE])))

        # each default option must be a list of strings
        if DEFAULT_SCENARIOS in config:
            Consistency.is_list_of_strings(DEFAULT_SCENARIOS,
                                           config[DEFAULT_SCENARIOS])
            Consistency.is_scenario_list(DEFAULT_SCENARIOS,
                                         config[DEFAULT_SCENARIOS])
        if DEFAULT_LEVELS in config:
            Consistency.is_list_of_strings(DEFAULT_LEVELS,
                                           config[DEFAULT_LEVELS])
            Consistency.is_level_list(DEFAULT_LEVELS,
                                      config[DEFAULT_LEVELS])
        if DEFAULT_LECTURERS in config:
            Consistency.is_list_of_strings(DEFAULT_LECTURERS,
                                           config[DEFAULT_LECTURERS])

        # components must be be contained in a dictionary
        Consistency.is_dictionary(COMPONENTS, config[COMPONENTS])

        for component, item in config[COMPONENTS].items():
            Consistency.is_dictionary(component, item)
            Consistency.component_exists(component)
            Consistency.is_valid_key_list(component, (item or {}),
                                          optional=[
                                              SCENARIOS,
                                              LEVELS,
                                              LECTURERS,
                                          ])

            for key in item.keys():
                Consistency.is_list_of_strings('%s/%s' % (component, key),
                                               item[key])

            Consistency.is_scenario_list(SCENARIOS, item.get(SCENARIOS, []))
            Consistency.is_level_list(LEVELS, item.get(LEVELS, []))


class Parse(object):
    @staticmethod
    def load_configuration(file_name: str) -> dict:
        with open(file_name, 'r') as file:
            config = yaml.load(file,
                               Loader=getattr(yaml, "FullLoader", yaml.Loader))
            Consistency.check_consistency(config)

            for component, item in config[COMPONENTS].items():
                yaml_file_name = '%s.yaml' % os.path.join(Arguments.root,
                                                          component)
                if os.path.exists(yaml_file_name):
                    item['child'] = Parse.load_configuration(yaml_file_name)

            return config


class Build(object):
    @staticmethod
    def generate_build(config: dict) -> str:
        flags = ''
        for course, item in config[COMPONENTS].items():
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
    Arguments.parse_arguments()

    tags: Tags = Tags()
    local = locals()
    exec(open('./conf.py').read(), local)
    Consistency.levels = (list(local['didactic_levels'].keys())
                          + [ALL, DEFAULT])
    Consistency.scenarios = (list(local['didactic_scenarios'].keys())
                             + [ALL, DEFAULT])

    configuration = Parse.load_configuration(Arguments.source)
    pprint(configuration)
    # os.system('make %s BUILD_DIR="%s" SPHINX_OPTS="%s"'
    #          % (arguments.format,
    #             arguments.output,
    #             generate_build(configuration)))


if __name__ == "__main__":
    main()
