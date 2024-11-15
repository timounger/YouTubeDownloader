"""!
********************************************************************************
@file   configParser.py
@brief  Load and store settings from doxyfile
        origin code see: https://github.com/TraceSoftwareInternational/doxygen-python-interface
********************************************************************************
"""

import logging
import os
import re


class ParseException(Exception):
    """!
    @brief Exception throw when error during parsing doxygen config.
           Will probably means that there is an error in the doxygen config file
    """


class ConfigParser:
    """!
    @brief This class should be used to parse and store a doxygen configuration file
    """

    def __init__(self) -> None:
        self.__single_line_option_regex = re.compile("^\\s*(\\w+)\\s*=\\s*([^\\\\]*)\\s*$")
        self.__first_line_of_multine_option_regex = re.compile("^\\s*(\\w+)\\s*=\\s*(.*)\\\\$")

    def load_configuration(self, doxyfile: str) -> dict[str, str | list[str]]:
        """!
        @brief Parse a Doxygen configuration file
        @param doxyfile : doxyfile: Path to the Doxygen configuration file
        @return A dict with all doxygen configuration
        """

        if not os.path.exists(doxyfile):
            logging.error("Impossible to access to %s", doxyfile)
            raise FileNotFoundError(doxyfile)

        configuration: dict[str, str | list[str]] = {}

        with open(doxyfile, 'r', encoding='utf-8') as file:

            in_multiline_option = False
            current_multiline_option_name = None

            for line in file.readlines():
                line = line.strip()
                if len(line) == 0:
                    continue

                if self.__is_comment_line(line):
                    continue

                if in_multiline_option:
                    if not line.endswith('\\'):
                        in_multiline_option = False
                    option_value = line.rstrip('\\').strip()
                    if current_multiline_option_name is not None:
                        configuration[current_multiline_option_name].append(option_value)

                elif self.__is_first_line_of_multiline_option(line):
                    current_multiline_option_name, option_value = self.__extract_multiline_option_name_and_first_value(line)
                    configuration[current_multiline_option_name] = [option_value]
                    in_multiline_option = True

                elif self.__is_single_line_option(line):
                    option_name, option_value = self.__extract_single_line_option_name_and_value(line)
                    configuration[option_name] = option_value

        return configuration

    def store_configuration(self, config: dict[str, str | list[str]], doxyfile: str) -> None:
        """!
        @brief Store the doxygen configuration to the disk
        @param config : The doxygen configuration you want to write on disk
        @param doxyfile : The output path where configuration will be written. If the file exist, it will be truncated
        """

        logging.debug("Store configuration in %s", doxyfile)

        lines = []
        for option_name, option_value in config.items():
            if isinstance(option_value, list):
                # Changes by Timo Unger (add with force_double_quote) */
                lines.append(f"{option_name} = {self.__add_double_quote_if_required(option_value[0], force_double_quote=True)} \\")
                lines.extend([f"\t{self.__add_double_quote_if_required(value, force_double_quote=True)} \\" for value in option_value[1:-1]])
                lines.append(f"\t{self.__add_double_quote_if_required(option_value[-1], force_double_quote=True)}")
            elif isinstance(option_value, str):
                lines.append(f"{option_name} = {self.__add_double_quote_if_required(option_value)}")

        with open(doxyfile, 'w', encoding='utf-8') as file:
            file.write("\n".join(lines))

    def __extract_multiline_option_name_and_first_value(self, line: str) -> tuple[str, str]:
        """!
        @brief Extract the option name and the first value of multi line option
        @param line : The line you want to parse
        @return the option name and the option first value
        """

        matches = self.__first_line_of_multine_option_regex.search(line)
        if matches is None or len(matches.groups()) != 2:
            logging.error("Impossible to extract first value off multi line option from: %s", line)
            raise ParseException(f"Impossible to extract first value off multi line option from: {line}")

        return matches.group(1), self.__remove_double_quote_if_required(matches.group(2))

    def __extract_single_line_option_name_and_value(self, line: str) -> tuple[str, str]:
        """!
        @brief Extract the option name and the value of single line option
        @param line : The line you want to parse
        @return the option name and the option value
        """

        matches = self.__single_line_option_regex.search(line)

        if matches is None or len(matches.groups()) != 2:
            logging.error("Impossible to extract option name and value from: %s", line)
            raise ParseException(f"Impossible to extract option name and value from: {line}")

        return matches.group(1), self.__remove_double_quote_if_required(matches.group(2))

    def __is_single_line_option(self, line: str) -> bool:
        """!
        @brief Match single line option
        @param line : The line you want to parse
        @return single line option status
        """
        return self.__single_line_option_regex.match(line) is not None

    def __is_comment_line(self, line: str) -> bool:
        """!
        @brief Match comment line
        @param line : The line you want to parse
        @return comment line option status
        """
        return line.startswith("#")

    def __is_first_line_of_multiline_option(self, line: str) -> bool:
        """!
        @brief Match first line option
        @param line : The line you want to parse
        @return first line option status
        """
        return self.__first_line_of_multine_option_regex.match(line) is not None

    @staticmethod
    def __remove_double_quote_if_required(option_value: str) -> str:
        """!
        @brief Remove the double quote around string in option value.
               Will be replaced when rewrite the configuration
        @param option_value : The value you want to work on
        @return The option value proper
        """
        if option_value.startswith('"') and option_value.endswith('"'):
            option_value_formatted = option_value[1:-1]
            logging.debug("Remove quote from %s to %s", option_value, option_value_formatted)
            return option_value_formatted

        return option_value

    @staticmethod
    def __add_double_quote_if_required(option_value: str, force_double_quote: bool = False) -> str:
        """!
        @brief Add the double quote around string in option value if its required
        @param option_value : The value you want to work on
        @param force_double_quote : force double quote
        @return The option value proper
        """
        if (" " in option_value) or force_double_quote:  # Changes by Timo Unger (additional force_double_quote option) */
            option_value_formatted = f'"{option_value}"'
            logging.debug("Add quote from %s to %s", option_value, option_value_formatted)
            return option_value_formatted

        return option_value
