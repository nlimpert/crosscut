#!/usr/bin/env python3

# Copyright (C) 2019-2020 MASCOR Institute. All rights reserved.

__author__ = "Meeßen, Marcus"
__copyright__ = "Copyright (C) 2019-2020 MASCOR Institute"
__version__ = "1.1"

import argparse
import os
from typing import Any, Callable, Dict, Iterable, List, Union

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
SELF: str = 'self'
ALL: str = 'all'
DEFAULT: str = 'default'
AUTHOR: str = 'author'
TEACHER: str = 'teacher'
TUTOR: str = 'tutor'
LEARNER: str = 'learner'
EDITION_CHOICES: List[str] = [
    AUTHOR,
    TEACHER,
    TUTOR,
    LEARNER,
    '+'.join([AUTHOR, TEACHER]),
    '+'.join([AUTHOR, TUTOR]),
    '+'.join([TEACHER, TUTOR]),
    '+'.join([AUTHOR, TEACHER, TUTOR]),
]
FORBIDDEN_COMPONENT_NAMES: List[str] = [
    # ALL is explicitly allowed!
    TITLE,
    DEFAULT_SCENARIOS,
    SCENARIOS,
    DEFAULT_LEVELS,
    LEVELS,
    DEFAULT_LECTURERS,
    LECTURERS,
    COMPONENTS,
    SELF,
    DEFAULT,
    *EDITION_CHOICES,
]

hex_hash: Union[Callable[[str], str], None] = None


class ArgumentError(Exception):
    pass


class ConfigurationError(Exception):
    pass


class Arguments(object):
    source: str
    format: str
    output: str
    indices: str
    root: str
    editions: List[str]
    generate: bool

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
                            choices=['html', 'latex''pdf'],
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
                            default='.',
                            help="Specify the root directory of the Sphinx "
                                 "documentation, i.e. where the 'conf.py' is "
                                 "located. The generated 'index.rst' will be "
                                 "placed there.",
                            )
        parser.add_argument('-e', '--editions',
                            choices=EDITION_CHOICES,
                            metavar='edition',
                            nargs='+',
                            default=[LEARNER],
                            help="Specify the editions to be generated. Choose "
                                 "from '%s', '%s', '%s', and '%s'. The first "
                                 "three of these can be combined with a '+' to "
                                 "'%s', '%s', '%s', and '%s'. The %s's edition "
                                 "is always included in any combination."
                                 % (*EDITION_CHOICES, LEARNER),
                            )
        generation = parser.add_argument_group("Generation",
                                               "Automatically run the Sphinx "
                                               "documentation generator after "
                                               "compiling the 'index.rst'.")
        mutual_generation = generation.add_mutually_exclusive_group()
        mutual_generation.add_argument('--generate',
                                       dest='generate',
                                       action='store_true',
                                       )
        mutual_generation.add_argument('--no-generate',
                                       dest='generate',
                                       action='store_true',
                                       help="(default)",
                                       )
        parser.set_defaults(
            generate=False,
        )

        for argument, value in vars(parser.parse_args()).items():
            setattr(Arguments, argument, value)

        if not os.path.abspath(Arguments.output).startswith(
                os.path.abspath(Arguments.root)):
            ArgumentError("Sphinx currently does not support processing .rst "
                          "files outside the root directory. Choose an output "
                          "directory that is placed inside the root.")

        # create directory where Sphinx builds output
        os.makedirs(Arguments.output, exist_ok=True)

        # set and create directory for indices generated from .yaml files
        Arguments.indices = os.path.relpath(
            os.path.join(Arguments.output, 'indices'),
            start=Arguments.root,
        )
        os.makedirs(Arguments.indices, exist_ok=True)


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
    def is_string(parent: str, artifact: Any) -> None:
        if type(artifact) is not str:
            raise ConfigurationError("Value of '%s' must be a string, but is "
                                     "'%s'." % (parent, type(artifact)))

    @staticmethod
    def is_dictionary(parent: str, artifact: Any) -> None:
        if type(artifact) is not dict:
            raise ConfigurationError("Value of '%s' must be a dictionary, "
                                     "but is %s." % (parent, type(artifact)))

    @staticmethod
    def is_list(parent: str, artifact: Any) -> None:
        if type(artifact) is not list:
            raise ConfigurationError("Value of '%s' must be a list, but is "
                                     "'%s'." % (parent, type(artifact)))

    @staticmethod
    def is_list_of_strings(parent: str, artifact: Any) -> None:
        Consistency.is_list(parent, artifact)
        for index, item in enumerate(artifact):
            if type(item) is not str:
                raise ConfigurationError("Item %d of '%s' must be a string, "
                                         "but is '%s'."
                                         % (index, parent, type(item)))

    @staticmethod
    def is_restricted_list(parent: str, artifact: Any,
                           allowed: Iterable = None,
                           forbidden: Iterable = None) -> None:
        Consistency.is_list(parent, artifact)
        for index, item in enumerate(artifact):
            if item not in (allowed or []) or item in (forbidden or []):
                raise ConfigurationError("Item %d of '%s' must be one of %s, "
                                         "but is '%s'."
                                         % (index, parent, allowed, item))

    @staticmethod
    def component_name_valid(artifact: Any) -> None:
        Consistency.is_string(COMPONENTS, artifact)
        if artifact in FORBIDDEN_COMPONENT_NAMES:
            raise ConfigurationError("Item '%s' is one of the forbidden "
                                     "component names %s."
                                     % (artifact, FORBIDDEN_COMPONENT_NAMES))

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
                                      ],
                                      )

        # title must be a string
        Consistency.is_string(TITLE, config[TITLE])

        # each default option must be a list of strings
        Consistency.is_restricted_list(DEFAULT_SCENARIOS,
                                       config.get(DEFAULT_SCENARIOS, []),
                                       allowed=Consistency.scenarios,
                                       )
        Consistency.is_restricted_list(DEFAULT_LEVELS,
                                       config.get(DEFAULT_LEVELS, []),
                                       allowed=Consistency.levels,
                                       )
        Consistency.is_list_of_strings(DEFAULT_LECTURERS,
                                       config.get(DEFAULT_LECTURERS, []))

        # components must be be contained in a dictionary
        Consistency.is_dictionary(COMPONENTS, config[COMPONENTS])

        for component, item in config[COMPONENTS].items():
            Consistency.is_dictionary(component, item)
            Consistency.component_name_valid(component)
            Consistency.component_exists(component)
            Consistency.is_valid_key_list(component, (item or {}),
                                          optional=[
                                              SCENARIOS,
                                              LEVELS,
                                              LECTURERS,
                                          ],
                                          )

            Consistency.is_restricted_list('%s/%s' % (component, SCENARIOS),
                                           item.get(SCENARIOS, []),
                                           allowed=Consistency.scenarios,
                                           )
            Consistency.is_restricted_list('%s/%s' % (component, LEVELS),
                                           item.get(LEVELS, []),
                                           allowed=Consistency.levels,
                                           )
            Consistency.is_list_of_strings('%s/%s' % (component, LECTURERS),
                                           item.get(LEVELS, []))


class Parse(object):
    @staticmethod
    def load_configuration(file_name: str) -> dict:
        with open(file_name, 'r') as file:
            config = yaml.load(file,
                               Loader=getattr(yaml, "FullLoader",
                                              yaml.Loader),
                               )
            Consistency.check_consistency(config)

            # load all subordinate .yaml files recursively
            for component, item in config[COMPONENTS].items():
                yaml_file_name = os.path.join(Arguments.root,
                                              '%s.yaml' % component)
                if os.path.exists(yaml_file_name):
                    item[SELF] = Parse.load_configuration(yaml_file_name)

            return config


class Build(object):
    @staticmethod
    def flatten(file_name: str) -> str:
        import re
        return re.sub(r'\W+', '_', file_name)

    @staticmethod
    def generate_main_index(file_name: str) -> None:
        rst_file_name: str = os.path.join(Arguments.root, 'index.rst')

        with open(rst_file_name, 'w+') as file:
            file.writelines([line + '\n' for line in [
                '.. meta::',  # prevents warnings
                '   :description lang=en: Table of Contents',
                '',
                '#' * 80,
                'ROS-I Academy',
                '#' * 80,
                '',
                '.. toc''tree::',
                '   :max''depth: 1',
                '   :numbered:',
                '',
                '   guideline',
                '   %s' % file_name,  # the .rst created from the root .yaml
                '',
                '.. toc''tree::',
                '   :max''depth: 1',
                '',
                '   contributors',
                '',
                '.. toc''tree::',
                '   :hidden:',
                '',
                '   general_glossary',
                '',
                '*' * 80,
                'Essential Material',
                '*' * 80,
                '',
                '.. toc''tree_required::',
                '',
                '*' * 80,
                'Additional Material',
                '*' * 80,
                '',
                '.. toc''tree_mentioned::',
            ]])

    @staticmethod
    def generate_indices(component_config: dict, file_name: str) -> None:
        root_relative: str = os.path.relpath(Arguments.root,
                                             start=Arguments.indices,
                                             )

        rst_file_name: str = os.path.join(Arguments.indices, '%s.rst'
                                          % file_name)

        with open(rst_file_name, 'w+') as file:
            components: List[str] = []
            # collect paths and file names to all components
            for component, item in component_config[COMPONENTS].items():
                # ALL is a phony target
                if component == ALL:
                    continue
                # paths to .rst files must be relative
                elif os.path.exists(os.path.join(Arguments.root,
                                                 '%s.rst' % component)):
                    components.append(os.path.join(root_relative, component))
                # generated indices from .yaml files share the same directory
                elif os.path.exists(os.path.join(Arguments.root,
                                                 '%s.yaml' % component)):
                    flat_component: str = Build.flatten(component)
                    components.append(flat_component)
                    # build .rst files for subordinate .yaml files recursively
                    Build.generate_indices(item[SELF], flat_component)

            file.writelines([line + '\n' for line in [
                '.. meta::',  # prevents warnings
                '   :description lang=en: Table of Contents',
                '',
                '#' * 80,
                component_config[TITLE],
                '#' * 80,
                '',
                '.. toc''tree::',
                '   :max''depth: 2',
                '',
                *['   %s' % component for component in components]
            ]])

    @staticmethod
    def generate_flags(component_config: dict, file_name: str,
                       inherited_default_scenarios: List[str] = None,
                       inherited_default_levels: List[str] = None,
                       inherited_default_lecturers: List[str] = None) -> str:
        flags: str = ' -t %s' % hex_hash(os.path.join(Arguments.indices,
                                                      file_name))

        # inherit defaults if there are no own defaults set
        for default_key, inherited_default in [
            (DEFAULT_SCENARIOS, inherited_default_scenarios),
            (DEFAULT_LEVELS, inherited_default_levels),
            (DEFAULT_LECTURERS, inherited_default_lecturers),
        ]:
            component_config.setdefault(default_key, inherited_default or [])

        # assign default values to components that have no own values
        for component, item in component_config[COMPONENTS].items():
            for key, default_key in [
                (SCENARIOS, DEFAULT_SCENARIOS),
                (LEVELS, DEFAULT_LEVELS),
                (LECTURERS, DEFAULT_LECTURERS),
            ]:
                item.setdefault(key, component_config[default_key])
                if DEFAULT in item[key]:
                    item[key].remove(DEFAULT)
                    item[key].extend(component_config[default_key])
                if ALL in item[key]:
                    item[key] = [ALL]

            # generate flags for subordinate .yaml files recursively
            if os.path.exists(os.path.join(Arguments.root,
                                           '%s.yaml' % component)):
                flags += Build.generate_flags(
                    item[SELF], Build.flatten(component),
                    inherited_default_scenarios=item[SCENARIOS],
                    inherited_default_levels=item[LEVELS],
                    inherited_default_lecturers=item[LECTURERS],
                )
            # add flags for .rst files, ALL is a phony target
            elif (component == ALL or
                  os.path.exists(os.path.join(Arguments.root,
                                              '%s.rst' % component))):
                flags += ' -t %s' % hex_hash(component)

                for key in [
                    SCENARIOS,
                    LEVELS,
                ]:
                    for entry in item[key]:
                        flags += ' -t %s_%s_%s' % (hex_hash(component), key,
                                                   entry)

        return flags

    @staticmethod
    def generate_build(config: dict) -> None:
        indices_directory: str = os.path.relpath(
            os.path.join(Arguments.output, 'indices'),
            start=Arguments.root,
        )
        source_name: str = os.path.splitext(Arguments.source)[0]
        flat_source_name: str = Build.flatten(source_name)
        Build.generate_main_index(os.path.join(indices_directory,
                                               flat_source_name))
        Build.generate_indices(config, flat_source_name)
        flags: str = Build.generate_flags(config, flat_source_name)
        flags += ' -t %s' % hex_hash('index')  # main doc must be available

        for edition in Arguments.editions:
            for part in edition.split('+'):
                flags += ' -t %s' % part

            command: str = ('sphinx-build -M %s "%s" "%s/%s" %s'
                            % (Arguments.format, Arguments.root,
                               Arguments.output, edition, flags))

            if Arguments.generate:
                os.system(command)
            else:
                print("To generate the '%s' edition output with Sphinx, run: "
                      "\n%s\n%s\n%s" % (edition, '#' * 20, command, '#' * 20))


def main():
    Arguments.parse_arguments()

    tags: Tags = Tags()
    local = locals()
    exec(open(os.path.join(Arguments.root, 'conf.py')).read(), local)
    Consistency.levels = (list(local['didactic_levels'].keys())
                          + [ALL, DEFAULT])
    Consistency.scenarios = (list(local['didactic_scenarios'].keys())
                             + [ALL, DEFAULT])
    global hex_hash
    hex_hash = local['hex_hash']

    Build.generate_build(Parse.load_configuration(Arguments.source))


if __name__ == "__main__":
    main()
