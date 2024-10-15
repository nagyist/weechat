# -*- coding: utf-8 -*-
#
# Copyright (C) 2017-2024 Sébastien Helleu <flashcode@flashtux.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

"""
This script contains WeeChat scripting API tests
(it cannot be run directly and cannot be loaded in WeeChat).

It is parsed by testapigen.py, using Python AST (Abstract Syntax Trees),
to generate scripts in all supported languages (Python, Perl, Ruby, ...).
The resulting scripts can be loaded in WeeChat to test the scripting API.
"""

# pylint: disable=line-too-long,no-value-for-parameter,too-many-locals
# pylint: disable=too-many-statements

import weechat  # pylint: disable=import-error


def check(result, condition, lineno):
    """Display the result of a test."""
    if result:
        weechat.prnt('', '      TEST OK: ' + condition)
    else:
        weechat.prnt('',
                     '{SCRIPT_SOURCE}' + ':' + lineno + ':1: ' +
                     'ERROR: [' + '{SCRIPT_NAME}' + '] condition is false: ' +
                     condition)


def test_constants():
    """Test constants."""
    check(weechat.WEECHAT_RC_OK == 0)
    check(weechat.WEECHAT_RC_OK_EAT == 1)
    check(weechat.WEECHAT_RC_ERROR == -1)
    check(weechat.WEECHAT_CONFIG_READ_OK == 0)
    check(weechat.WEECHAT_CONFIG_READ_MEMORY_ERROR == -1)
    check(weechat.WEECHAT_CONFIG_READ_FILE_NOT_FOUND == -2)
    check(weechat.WEECHAT_CONFIG_WRITE_OK == 0)
    check(weechat.WEECHAT_CONFIG_WRITE_ERROR == -1)
    check(weechat.WEECHAT_CONFIG_WRITE_MEMORY_ERROR == -2)
    check(weechat.WEECHAT_CONFIG_OPTION_SET_OK_CHANGED == 2)
    check(weechat.WEECHAT_CONFIG_OPTION_SET_OK_SAME_VALUE == 1)
    check(weechat.WEECHAT_CONFIG_OPTION_SET_ERROR == 0)
    check(weechat.WEECHAT_CONFIG_OPTION_SET_OPTION_NOT_FOUND == -1)
    check(weechat.WEECHAT_CONFIG_OPTION_UNSET_OK_NO_RESET == 0)
    check(weechat.WEECHAT_CONFIG_OPTION_UNSET_OK_RESET == 1)
    check(weechat.WEECHAT_CONFIG_OPTION_UNSET_OK_REMOVED == 2)
    check(weechat.WEECHAT_CONFIG_OPTION_UNSET_ERROR == -1)
    check(weechat.WEECHAT_LIST_POS_SORT == 'sort')
    check(weechat.WEECHAT_LIST_POS_BEGINNING == 'beginning')
    check(weechat.WEECHAT_LIST_POS_END == 'end')
    check(weechat.WEECHAT_HOTLIST_LOW == '0')
    check(weechat.WEECHAT_HOTLIST_MESSAGE == '1')
    check(weechat.WEECHAT_HOTLIST_PRIVATE == '2')
    check(weechat.WEECHAT_HOTLIST_HIGHLIGHT == '3')
    check(weechat.WEECHAT_HOOK_PROCESS_RUNNING == -1)
    check(weechat.WEECHAT_HOOK_PROCESS_ERROR == -2)
    check(weechat.WEECHAT_HOOK_CONNECT_IPV6_DISABLE == 0)
    check(weechat.WEECHAT_HOOK_CONNECT_IPV6_AUTO == 1)
    check(weechat.WEECHAT_HOOK_CONNECT_IPV6_FORCE == 2)
    check(weechat.WEECHAT_HOOK_CONNECT_OK == 0)
    check(weechat.WEECHAT_HOOK_CONNECT_ADDRESS_NOT_FOUND == 1)
    check(weechat.WEECHAT_HOOK_CONNECT_IP_ADDRESS_NOT_FOUND == 2)
    check(weechat.WEECHAT_HOOK_CONNECT_CONNECTION_REFUSED == 3)
    check(weechat.WEECHAT_HOOK_CONNECT_PROXY_ERROR == 4)
    check(weechat.WEECHAT_HOOK_CONNECT_LOCAL_HOSTNAME_ERROR == 5)
    check(weechat.WEECHAT_HOOK_CONNECT_GNUTLS_INIT_ERROR == 6)
    check(weechat.WEECHAT_HOOK_CONNECT_GNUTLS_HANDSHAKE_ERROR == 7)
    check(weechat.WEECHAT_HOOK_CONNECT_MEMORY_ERROR == 8)
    check(weechat.WEECHAT_HOOK_CONNECT_TIMEOUT == 9)
    check(weechat.WEECHAT_HOOK_CONNECT_SOCKET_ERROR == 10)
    check(weechat.WEECHAT_HOOK_SIGNAL_STRING == 'string')
    check(weechat.WEECHAT_HOOK_SIGNAL_INT == 'int')
    check(weechat.WEECHAT_HOOK_SIGNAL_POINTER == 'pointer')


def test_plugins():
    """Test plugins functions."""
    check(weechat.plugin_get_name('') == 'core')
    check(weechat.plugin_get_name(
        weechat.buffer_get_pointer(
            weechat.buffer_search_main(), 'plugin')) == 'core')


def test_strings():
    """Test string functions."""
    check(weechat.charset_set('iso-8859-15') == 1)
    check(weechat.charset_set('') == 1)
    check(weechat.iconv_to_internal('iso-8859-15', 'abc') == 'abc')
    check(weechat.iconv_from_internal('iso-8859-15', 'abcd') == 'abcd')
    check(weechat.gettext('abcdef') == 'abcdef')
    check(weechat.ngettext('file', 'files', 1) == 'file')
    check(weechat.ngettext('file', 'files', 2) == 'files')
    check(weechat.strlen_screen('abcd') == 4)
    check(weechat.string_match('abcdef', 'abc*', 0) == 1)
    check(weechat.string_match('abcdef', 'abc*', 1) == 1)
    check(weechat.string_match('ABCDEF', 'abc*', 1) == 0)
    check(weechat.string_match_list('abcdef', '*,!abc*', 0) == 0)
    check(weechat.string_match_list('ABCDEF', '*,!abc*', 1) == 1)
    check(weechat.string_match_list('def', '*,!abc*', 0) == 1)
    check(weechat.string_eval_path_home('test ${abc}', {}, {'abc': '123'}, {}) == 'test 123')
    check(weechat.string_mask_to_regex('test*mask') == 'test.*mask')
    check(weechat.string_has_highlight('my test string', 'test,word2') == 1)
    check(weechat.string_has_highlight_regex('my test string', 'test|word2') == 1)
    check(weechat.string_format_size(0) == '0 bytes')
    check(weechat.string_format_size(1) == '1 byte')
    check(weechat.string_format_size(2097152) == '2.10 MB')
    check(weechat.string_format_size(420000000) == '420.00 MB')
    check(weechat.string_parse_size('') == 0)
    check(weechat.string_parse_size('*') == 0)
    check(weechat.string_parse_size('z') == 0)
    check(weechat.string_parse_size('1ba') == 0)
    check(weechat.string_parse_size('1') == 1)
    check(weechat.string_parse_size('12b') == 12)
    check(weechat.string_parse_size('123 b') == 123)
    check(weechat.string_parse_size('120k') == 120000)
    check(weechat.string_parse_size('1500m') == 1500000000)
    check(weechat.string_parse_size('2g') == 2000000000)
    check(weechat.string_color_code_size('') == 0)
    check(weechat.string_color_code_size('test') == 0)
    str_color = weechat.color('yellow,red')
    check(weechat.string_color_code_size(str_color) == 7)
    check(weechat.string_remove_color('test', '?') == 'test')
    check(weechat.string_is_command_char('/test') == 1)
    check(weechat.string_is_command_char('test') == 0)
    check(weechat.string_input_for_buffer('test') == 'test')
    check(weechat.string_input_for_buffer('/test') == '')
    check(weechat.string_input_for_buffer('//test') == '/test')
    check(weechat.string_eval_expression("100 > 50", {}, {}, {"type": "condition"}) == '1')
    check(weechat.string_eval_expression("-50 < 100", {}, {}, {"type": "condition"}) == '1')
    check(weechat.string_eval_expression("18.2 > 5", {}, {}, {"type": "condition"}) == '1')
    check(weechat.string_eval_expression("0xA3 > 2", {}, {}, {"type": "condition"}) == '1')
    check(weechat.string_eval_expression("${buffer.full_name}", {}, {}, {}) == 'core.weechat')


def test_lists():
    """Test list functions."""
    ptr_list = weechat.list_new()
    check(ptr_list != '')
    check(weechat.list_size(ptr_list) == 0)
    item_def = weechat.list_add(ptr_list, 'def', weechat.WEECHAT_LIST_POS_SORT, '')
    check(weechat.list_size(ptr_list) == 1)
    item_abc = weechat.list_add(ptr_list, 'abc', weechat.WEECHAT_LIST_POS_SORT, '')
    check(weechat.list_size(ptr_list) == 2)
    check(weechat.list_search(ptr_list, 'abc') == item_abc)
    check(weechat.list_search(ptr_list, 'def') == item_def)
    check(weechat.list_search(ptr_list, 'ghi') == '')
    check(weechat.list_search_pos(ptr_list, 'abc') == 0)
    check(weechat.list_search_pos(ptr_list, 'def') == 1)
    check(weechat.list_search_pos(ptr_list, 'ghi') == -1)
    check(weechat.list_casesearch(ptr_list, 'abc') == item_abc)
    check(weechat.list_casesearch(ptr_list, 'def') == item_def)
    check(weechat.list_casesearch(ptr_list, 'ghi') == '')
    check(weechat.list_casesearch(ptr_list, 'ABC') == item_abc)
    check(weechat.list_casesearch(ptr_list, 'DEF') == item_def)
    check(weechat.list_casesearch(ptr_list, 'GHI') == '')
    check(weechat.list_casesearch_pos(ptr_list, 'abc') == 0)
    check(weechat.list_casesearch_pos(ptr_list, 'def') == 1)
    check(weechat.list_casesearch_pos(ptr_list, 'ghi') == -1)
    check(weechat.list_casesearch_pos(ptr_list, 'ABC') == 0)
    check(weechat.list_casesearch_pos(ptr_list, 'DEF') == 1)
    check(weechat.list_casesearch_pos(ptr_list, 'GHI') == -1)
    check(weechat.list_get(ptr_list, 0) == item_abc)
    check(weechat.list_get(ptr_list, 1) == item_def)
    check(weechat.list_get(ptr_list, 2) == '')
    weechat.list_set(item_def, 'def2')
    check(weechat.list_string(item_def) == 'def2')
    check(weechat.list_next(item_abc) == item_def)
    check(weechat.list_next(item_def) == '')
    check(weechat.list_prev(item_abc) == '')
    check(weechat.list_prev(item_def) == item_abc)
    weechat.list_remove(ptr_list, item_abc)
    check(weechat.list_size(ptr_list) == 1)
    check(weechat.list_get(ptr_list, 0) == item_def)
    check(weechat.list_get(ptr_list, 1) == '')
    weechat.list_remove_all(ptr_list)
    check(weechat.list_size(ptr_list) == 0)
    weechat.list_free(ptr_list)


def config_reload_cb(data, config_file):
    """Config reload callback."""
    return weechat.WEECHAT_RC_OK


def config_update_cb(data, config_file, version, data_read):
    """Config update callback."""
    return weechat.WEECHAT_RC_OK


def section_read_cb(data, config_file, section, option_name, value):
    """Section read callback."""
    return weechat.WEECHAT_RC_OK


def section_write_cb(data, config_file, section_name):
    """Section write callback."""
    return weechat.WEECHAT_RC_OK


def section_write_default_cb(data, config_file, section_name):
    """Section write default callback."""
    return weechat.WEECHAT_RC_OK


def section_create_option_cb(data, config_file, section, option_name, value):
    """Section create option callback."""
    return weechat.WEECHAT_RC_OK


def section_delete_option_cb(data, config_file, section, option):
    """Section delete option callback."""
    return weechat.WEECHAT_RC_OK


def option_check_value_cb(data, option, value):
    """Option check value callback."""
    return 1


def option_change_cb(data, option):
    """Option change callback."""
    pass  # pylint: disable=unnecessary-pass


def option_delete_cb(data, option):
    """Option delete callback."""
    pass  # pylint: disable=unnecessary-pass


def test_config():
    """Test config functions."""
    # config
    ptr_config = weechat.config_new('test_config_' + '{SCRIPT_LANGUAGE}',
                                    'config_reload_cb', 'config_reload_data')
    check(ptr_config != '')
    # set version
    weechat.config_set_version(ptr_config, 2,
                               'config_update_cb', 'config_update_data')
    # section
    ptr_section = weechat.config_new_section(
        ptr_config, 'section1', 0, 0,
        'section_read_cb', '',
        'section_write_cb', '',
        'section_write_default_cb', '',
        'section_create_option_cb', '',
        'section_delete_option_cb', '',
    )
    check(ptr_section != '')
    # search section
    ptr_section2 = weechat.config_search_section(ptr_config, 'section1')
    check(ptr_section2 == ptr_section)
    # boolean option
    ptr_opt_bool = weechat.config_new_option(
        ptr_config, ptr_section, 'option_bool', 'boolean', 'bool option',
        '', 0, 0, 'on', 'on', 0,
        'option_check_value_cb', '',
        'option_change_cb', '',
        'option_delete_cb', '',
    )
    check(ptr_opt_bool != '')
    check(weechat.config_boolean(ptr_opt_bool) == 1)
    check(weechat.config_option_set(ptr_opt_bool, 'off', 1) == 2)  # SET_OK_CHANGED
    check(weechat.config_option_set(ptr_opt_bool, 'off', 1) == 1)  # SET_OK_SAME_VALUE
    check(weechat.config_boolean(ptr_opt_bool) == 0)
    check(weechat.config_boolean_default(ptr_opt_bool) == 1)
    check(weechat.config_option_reset(ptr_opt_bool, 1) == 2)  # SET_OK_CHANGED
    check(weechat.config_option_reset(ptr_opt_bool, 1) == 1)  # SET_OK_SAME_VALUE
    check(weechat.config_boolean(ptr_opt_bool) == 1)
    # boolean option with parent option
    ptr_opt_bool_child = weechat.config_new_option(
        ptr_config, ptr_section,
        'option_bool_child << test_config_' + '{SCRIPT_LANGUAGE}' + '.section1.option_bool',
        'boolean', 'bool option', '', 0, 0, None, None, 1,
        'option_check_value_cb', '',
        'option_change_cb', '',
        'option_delete_cb', '',
    )
    check(ptr_opt_bool_child != '')
    check(weechat.config_boolean(ptr_opt_bool_child) == 0)
    check(weechat.config_boolean_inherited(ptr_opt_bool_child) == 1)
    # integer option
    ptr_opt_int = weechat.config_new_option(
        ptr_config, ptr_section, 'option_int', 'integer', 'int option',
        '', 0, 256, '2', '2', 0,
        'option_check_value_cb', '',
        'option_change_cb', '',
        'option_delete_cb', '',
    )
    check(ptr_opt_int != '')
    check(weechat.config_integer(ptr_opt_int) == 2)
    check(weechat.config_option_set(ptr_opt_int, '15', 1) == 2)  # SET_OK_CHANGED
    check(weechat.config_option_set(ptr_opt_int, '15', 1) == 1)  # SET_OK_SAME_VALUE
    check(weechat.config_integer(ptr_opt_int) == 15)
    check(weechat.config_integer_default(ptr_opt_int) == 2)
    check(weechat.config_option_reset(ptr_opt_int, 1) == 2)  # SET_OK_CHANGED
    check(weechat.config_option_reset(ptr_opt_int, 1) == 1)  # SET_OK_SAME_VALUE
    check(weechat.config_integer(ptr_opt_int) == 2)
    # integer option with parent option
    ptr_opt_int_child = weechat.config_new_option(
        ptr_config, ptr_section,
        'option_int_child << test_config_' + '{SCRIPT_LANGUAGE}' + '.section1.option_int',
        'integer', 'int option', '', 0, 256, None, None, 1,
        'option_check_value_cb', '',
        'option_change_cb', '',
        'option_delete_cb', '',
    )
    check(ptr_opt_int_child != '')
    check(weechat.config_integer(ptr_opt_int_child) == 0)
    check(weechat.config_integer_inherited(ptr_opt_int_child) == 2)
    # integer option (with string values: enum with WeeChat >= 4.1.0)
    ptr_opt_int_str = weechat.config_new_option(
        ptr_config, ptr_section, 'option_int_str', 'integer', 'int option str',
        'val1|val2|val3', 0, 0, 'val2', 'val2', 0,
        'option_check_value_cb', '',
        'option_change_cb', '',
        'option_delete_cb', '',
    )
    check(ptr_opt_int_str != '')
    check(weechat.config_integer(ptr_opt_int_str) == 1)
    check(weechat.config_string(ptr_opt_int_str) == 'val2')
    check(weechat.config_option_set(ptr_opt_int_str, 'val1', 1) == 2)  # SET_OK_CHANGED
    check(weechat.config_option_set(ptr_opt_int_str, 'val1', 1) == 1)  # SET_OK_SAME_VALUE
    check(weechat.config_integer(ptr_opt_int_str) == 0)
    check(weechat.config_string(ptr_opt_int_str) == 'val1')
    check(weechat.config_integer_default(ptr_opt_int_str) == 1)
    check(weechat.config_string_default(ptr_opt_int_str) == 'val2')
    check(weechat.config_option_reset(ptr_opt_int_str, 1) == 2)  # SET_OK_CHANGED
    check(weechat.config_option_reset(ptr_opt_int_str, 1) == 1)  # SET_OK_SAME_VALUE
    check(weechat.config_integer(ptr_opt_int_str) == 1)
    check(weechat.config_string(ptr_opt_int_str) == 'val2')
    # integer option with parent option (with string values: enum with WeeChat >= 4.1.0)
    ptr_opt_int_str_child = weechat.config_new_option(
        ptr_config, ptr_section,
        'option_int_str_child << test_config_' + '{SCRIPT_LANGUAGE}' + '.section1.option_int_str',
        'integer', 'int option str',
        'val1|val2|val3', 0, 0, None, None, 1,
        'option_check_value_cb', '',
        'option_change_cb', '',
        'option_delete_cb', '',
    )
    check(ptr_opt_int_str_child != '')
    check(weechat.config_integer(ptr_opt_int_str_child) == 0)
    check(weechat.config_integer_inherited(ptr_opt_int_str_child) == 1)
    # string option
    ptr_opt_str = weechat.config_new_option(
        ptr_config, ptr_section, 'option_str', 'string', 'str option',
        '', 0, 0, 'value', 'value', 1,
        'option_check_value_cb', '',
        'option_change_cb', '',
        'option_delete_cb', '',
    )
    check(ptr_opt_str != '')
    check(weechat.config_string(ptr_opt_str) == 'value')
    check(weechat.config_option_set(ptr_opt_str, 'value2', 1) == 2)  # SET_OK_CHANGED
    check(weechat.config_option_set(ptr_opt_str, 'value2', 1) == 1)  # SET_OK_SAME_VALUE
    check(weechat.config_string(ptr_opt_str) == 'value2')
    check(weechat.config_string_default(ptr_opt_str) == 'value')
    check(weechat.config_option_reset(ptr_opt_str, 1) == 2)  # SET_OK_CHANGED
    check(weechat.config_option_reset(ptr_opt_str, 1) == 1)  # SET_OK_SAME_VALUE
    check(weechat.config_string(ptr_opt_str) == 'value')
    check(weechat.config_option_is_null(ptr_opt_str) == 0)
    check(weechat.config_option_set_null(ptr_opt_str, 1) == 2)  # SET_OK_CHANGED
    check(weechat.config_option_set_null(ptr_opt_str, 1) == 1)  # SET_OK_SAME_VALUE
    check(weechat.config_option_is_null(ptr_opt_str) == 1)
    check(weechat.config_string(ptr_opt_str) == '')
    check(weechat.config_option_unset(ptr_opt_str) == 1)  # UNSET_OK_RESET
    check(weechat.config_option_unset(ptr_opt_str) == 0)  # UNSET_OK_NO_RESET
    check(weechat.config_string(ptr_opt_str) == 'value')
    check(weechat.config_option_default_is_null(ptr_opt_str) == 0)
    # string option with parent option
    ptr_opt_str_child = weechat.config_new_option(
        ptr_config, ptr_section,
        'option_str_child << test_config_' + '{SCRIPT_LANGUAGE}' + '.section1.option_str',
        'string', 'str option', '', 0, 0, None, None, 1,
        'option_check_value_cb', '',
        'option_change_cb', '',
        'option_delete_cb', '',
    )
    check(ptr_opt_str_child != '')
    check(weechat.config_string(ptr_opt_str_child) == '')
    check(weechat.config_string_inherited(ptr_opt_str_child) == 'value')
    # color option
    ptr_opt_col = weechat.config_new_option(
        ptr_config, ptr_section, 'option_col', 'color', 'col option',
        '', 0, 0, 'lightgreen', 'lightgreen', 0,
        'option_check_value_cb', '',
        'option_change_cb', '',
        'option_delete_cb', '',
    )
    check(ptr_opt_col != '')
    check(weechat.config_color(ptr_opt_col) == 'lightgreen')
    check(weechat.config_option_set(ptr_opt_col, 'red', 1) == 2)  # SET_OK_CHANGED
    check(weechat.config_option_set(ptr_opt_col, 'red', 1) == 1)  # SET_OK_SAME_VALUE
    check(weechat.config_color(ptr_opt_col) == 'red')
    check(weechat.config_color_default(ptr_opt_col) == 'lightgreen')
    check(weechat.config_option_reset(ptr_opt_col, 1) == 2)  # SET_OK_CHANGED
    check(weechat.config_option_reset(ptr_opt_col, 1) == 1)  # SET_OK_SAME_VALUE
    check(weechat.config_color(ptr_opt_col) == 'lightgreen')
    # color option with parent option
    ptr_opt_col_child = weechat.config_new_option(
        ptr_config, ptr_section,
        'option_col_child << test_config_' + '{SCRIPT_LANGUAGE}' + '.section1.option_col',
        'color', 'col option', '', 0, 0, None, None, 1,
        'option_check_value_cb', '',
        'option_change_cb', '',
        'option_delete_cb', '',
    )
    check(ptr_opt_col_child != '')
    check(weechat.config_color(ptr_opt_col_child) == '')
    check(weechat.config_color_inherited(ptr_opt_col_child) == 'lightgreen')
    # enum option
    ptr_opt_enum = weechat.config_new_option(
        ptr_config, ptr_section, 'option_enum', 'enum', 'enum option',
        'val1|val2|val3', 0, 0, 'val2', 'val2', 0,
        'option_check_value_cb', '',
        'option_change_cb', '',
        'option_delete_cb', '',
    )
    check(ptr_opt_enum != '')
    check(weechat.config_enum(ptr_opt_enum) == 1)
    check(weechat.config_integer(ptr_opt_enum) == 1)
    check(weechat.config_string(ptr_opt_enum) == 'val2')
    check(weechat.config_option_set(ptr_opt_enum, 'val1', 1) == 2)  # SET_OK_CHANGED
    check(weechat.config_option_set(ptr_opt_enum, 'val1', 1) == 1)  # SET_OK_SAME_VALUE
    check(weechat.config_enum(ptr_opt_enum) == 0)
    check(weechat.config_integer(ptr_opt_enum) == 0)
    check(weechat.config_string(ptr_opt_enum) == 'val1')
    check(weechat.config_enum_default(ptr_opt_enum) == 1)
    check(weechat.config_integer_default(ptr_opt_enum) == 1)
    check(weechat.config_string_default(ptr_opt_enum) == 'val2')
    check(weechat.config_option_reset(ptr_opt_enum, 1) == 2)  # SET_OK_CHANGED
    check(weechat.config_option_reset(ptr_opt_enum, 1) == 1)  # SET_OK_SAME_VALUE
    check(weechat.config_enum(ptr_opt_enum) == 1)
    check(weechat.config_integer(ptr_opt_enum) == 1)
    check(weechat.config_string(ptr_opt_enum) == 'val2')
    # enum option with parent option
    ptr_opt_enum_child = weechat.config_new_option(
        ptr_config, ptr_section,
        'option_enum_child << test_config_' + '{SCRIPT_LANGUAGE}' + '.section1.option_enum',
        'enum', 'enum option', 'val1|val2|val3', 0, 0, None, None, 1,
        'option_check_value_cb', '',
        'option_change_cb', '',
        'option_delete_cb', '',
    )
    check(ptr_opt_enum_child != '')
    check(weechat.config_enum(ptr_opt_enum_child) == 0)
    check(weechat.config_enum_inherited(ptr_opt_enum_child) == 1)
    # search option
    ptr_opt_bool2 = weechat.config_search_option(ptr_config, ptr_section,
                                                 'option_bool')
    check(ptr_opt_bool2 == ptr_opt_bool)
    # string to boolean
    check(weechat.config_string_to_boolean('') == 0)
    check(weechat.config_string_to_boolean('off') == 0)
    check(weechat.config_string_to_boolean('0') == 0)
    check(weechat.config_string_to_boolean('on') == 1)
    check(weechat.config_string_to_boolean('1') == 1)
    # rename option
    weechat.config_option_rename(ptr_opt_bool, 'option_bool_renamed')
    # get string property of option
    check(weechat.config_option_get_string(ptr_opt_bool, 'type') == 'boolean')
    check(weechat.config_option_get_string(ptr_opt_bool, 'name') == 'option_bool_renamed')
    # get pointer property of option
    check(weechat.config_option_get_pointer(ptr_opt_bool, 'config_file') == ptr_config)
    check(weechat.config_option_get_pointer(ptr_opt_bool, 'section') == ptr_section)
    # read config (create it because it does not exist yet)
    check(weechat.config_read(ptr_config) == 0)  # CONFIG_READ_OK
    # write config
    check(weechat.config_write(ptr_config) == 0)  # CONFIG_WRITE_OK
    # reload config
    check(weechat.config_reload(ptr_config) == 0)  # CONFIG_READ_OK
    # free option
    weechat.config_option_free(ptr_opt_bool)
    # free options in section
    weechat.config_section_free_options(ptr_section)
    # free section
    weechat.config_section_free(ptr_section)
    # free config
    weechat.config_free(ptr_config)
    # config_get
    ptr_option = weechat.config_get('weechat.look.item_time_format')
    check(ptr_option != '')
    check(weechat.config_string(ptr_option) == '%H:%M')
    # config plugin
    check(weechat.config_get_plugin('option') == '')
    check(weechat.config_is_set_plugin('option') == 0)
    check(weechat.config_set_plugin('option', 'value') == 1)  # SET_OK_SAME_VALUE
    weechat.config_set_desc_plugin('option', 'description of option')
    check(weechat.config_get_plugin('option') == 'value')
    check(weechat.config_is_set_plugin('option') == 1)
    check(weechat.config_unset_plugin('option') == 2)  # UNSET_OK_REMOVED
    check(weechat.config_unset_plugin('option') == -1)  # UNSET_ERROR


def test_key():
    """Test key functions."""
    check(
        weechat.key_bind(
            'mouse',
            {
                '@chat(plugin.test):button1': 'hsignal:test_mouse',
                '@chat(plugin.test):wheelup': '/mycommand up',
                '@chat(plugin.test):wheeldown': '/mycommand down',
                '__quiet': '',
            }
        ) == 3)
    check(weechat.key_unbind('mouse', 'quiet:area:chat(plugin.test)') == 3)


def buffer_input_cb(data, buffer, input_data):
    """Buffer input callback."""
    return weechat.WEECHAT_RC_OK


def buffer_close_cb(data, buffer):
    """Buffer close callback."""
    return weechat.WEECHAT_RC_OK


def test_display():
    """Test display functions."""
    check(weechat.prefix('action') != '')
    check(weechat.prefix('error') != '')
    check(weechat.prefix('join') != '')
    check(weechat.prefix('network') != '')
    check(weechat.prefix('quit') != '')
    check(weechat.prefix('unknown') == '')
    check(weechat.color('green') != '')
    check(weechat.color('unknown') == '')
    weechat.prnt('', '## test print core buffer')
    weechat.prnt_date_tags('', 946681200, 'tag1,tag2',
                           '## test print_date_tags core buffer')
    weechat.prnt_datetime_tags('', 2146383600, 123456, 'tag1,tag2',
                               '## test print_date_tags core buffer, January, 6th 2038')
    hdata_buffer = weechat.hdata_get('buffer')
    hdata_lines = weechat.hdata_get('lines')
    hdata_line = weechat.hdata_get('line')
    hdata_line_data = weechat.hdata_get('line_data')
    buffer = weechat.buffer_search_main()
    own_lines = weechat.hdata_pointer(hdata_buffer, buffer, 'own_lines')
    line = weechat.hdata_pointer(hdata_lines, own_lines, 'last_line')
    data = weechat.hdata_pointer(hdata_line, line, 'data')
    check(weechat.hdata_time(hdata_line_data, data, 'date') == 2146383600)
    check(weechat.hdata_integer(hdata_line_data, data, 'date_usec') == 123456)
    buffer = weechat.buffer_new('test_formatted',
                                'buffer_input_cb', '', 'buffer_close_cb', '')
    check(buffer != '')
    check(weechat.buffer_get_integer(buffer, 'type') == 0)
    weechat.prnt(buffer, '## test print formatted buffer')
    weechat.prnt_date_tags(buffer, 946681200, 'tag1,tag2',
                           '## test print_date_tags formatted buffer')
    weechat.buffer_close(buffer)
    buffer = weechat.buffer_new_props('test_free', {'type': 'free'},
                                      'buffer_input_cb', '', 'buffer_close_cb', '')
    check(weechat.buffer_get_integer(buffer, 'type') == 1)
    check(buffer != '')
    weechat.prnt_y(buffer, 0, '## test print_y free buffer')
    weechat.prnt_y_date_tags(buffer, 0, 946681200, 'tag1,tag2',
                             '## test print_y_date_tags free buffer')
    weechat.prnt_y_datetime_tags(buffer, 1, 2146383600, 123456, 'tag1,tag2',
                                 '## test print_y_date_tags free buffer, January, 6th 2038')
    weechat.buffer_close(buffer)


def completion_cb(data, completion_item, buf, completion):
    """Completion callback."""
    check(data == 'completion_data')
    check(completion_item == '{SCRIPT_NAME}')
    check(weechat.completion_get_string(completion, 'args') == 'w')
    weechat.completion_list_add(completion, 'word_completed',
                                0, weechat.WEECHAT_LIST_POS_END)
    return weechat.WEECHAT_RC_OK


def command_cb(data, buf, args):
    """Command callback."""
    check(data == 'command_data')
    check(args == 'word_completed')
    return weechat.WEECHAT_RC_OK


def command_run_cb(data, buf, command):
    """Command_run callback."""
    check(data == 'command_run_data')
    check(command == '/cmd' + '{SCRIPT_NAME}' + ' word_completed')
    return weechat.WEECHAT_RC_OK


def timer_cb(data, remaining_calls):
    """Timer callback."""
    return weechat.WEECHAT_RC_OK


def test_hooks():
    """Test hook functions."""
    # hook_completion / hook_completion_args / and hook_command
    hook_cmplt = weechat.hook_completion('{SCRIPT_NAME}', 'description',
                                         'completion_cb', 'completion_data')
    hook_cmd = weechat.hook_command('cmd' + '{SCRIPT_NAME}', 'description',
                                    'arguments', 'description arguments',
                                    '%(' + '{SCRIPT_NAME}' + ')',
                                    'command_cb', 'command_data')
    weechat.command('', '/input insert /cmd' + '{SCRIPT_NAME}' + ' w')
    weechat.command('', '/input complete_next')
    # hook_command_run
    hook_cmd_run = weechat.hook_command_run('/cmd' + '{SCRIPT_NAME}' + '*',
                                            'command_run_cb', 'command_run_data')
    weechat.command('', '/input return')
    weechat.unhook(hook_cmd_run)
    weechat.unhook(hook_cmd)
    weechat.unhook(hook_cmplt)
    # hook_timer
    hook_timer = weechat.hook_timer(2000111000, 0, 1,
                                    'timer_cb', 'timer_cb_data')
    ptr_infolist = weechat.infolist_get('hook', hook_timer, '')
    check(ptr_infolist != '')
    check(weechat.infolist_next(ptr_infolist) == 1)
    check(weechat.infolist_string(ptr_infolist, 'interval') == '2000111000')
    weechat.infolist_free(ptr_infolist)
    weechat.unhook(hook_timer)


def test_buffers():
    """Test buffer functions."""
    buffer1 = weechat.buffer_new('test1', 'buffer_input_cb', '', 'buffer_close_cb', '')
    check(buffer1 != '')
    check(weechat.buffer_get_integer(buffer1, 'number') == 2)
    check(weechat.buffer_get_string(buffer1, 'short_name') == 'test1')
    props = {
        'short_name': 't2',
    }
    buffer2 = weechat.buffer_new_props('test2', props, 'buffer_input_cb', '', 'buffer_close_cb', '')
    check(buffer2 != '')
    check(weechat.buffer_get_integer(buffer2, 'number') == 3)
    check(weechat.buffer_get_string(buffer2, 'short_name') == 't2')
    check(weechat.buffer_get_integer(buffer2, 'next_line_id') == 0)
    weechat.prnt(buffer2, '## test line 1')
    check(weechat.buffer_get_integer(buffer2, 'next_line_id') == 1)
    weechat.buffer_clear(buffer2)
    weechat.buffer_merge(buffer2, buffer1)
    check(weechat.buffer_get_integer(buffer1, 'number') == 2)
    check(weechat.buffer_get_integer(buffer2, 'number') == 2)
    weechat.buffer_unmerge(buffer2, 3)
    check(weechat.buffer_get_integer(buffer1, 'number') == 2)
    check(weechat.buffer_get_integer(buffer2, 'number') == 3)
    check(weechat.current_buffer() != '')
    check(weechat.buffer_get_integer(buffer1, 'hidden') == 0)
    weechat.buffer_set(buffer1, 'hidden', '1')
    check(weechat.buffer_get_integer(buffer1, 'hidden') == 1)
    weechat.buffer_set(buffer1, 'hidden', '0')
    check(weechat.buffer_get_integer(buffer1, 'hidden') == 0)
    weechat.buffer_set(buffer1, 'localvar_set_var1', 'value1')
    check(weechat.buffer_string_replace_local_var(buffer1, 'test $var1') == 'test value1')
    buffer = weechat.buffer_search_main()
    buffer_id = weechat.buffer_get_string(buffer, 'id')
    check(weechat.buffer_search('xxx', 'yyy') == '')
    check(weechat.buffer_search('==', 'xxx') == '')
    check(weechat.buffer_search('==id', '0') == '')
    check(weechat.buffer_search('core', 'weechat') == buffer)
    check(weechat.buffer_search('==', 'core.weechat') == buffer)
    check(weechat.buffer_search('==id', buffer_id) == buffer)
    check(weechat.buffer_match_list(buffer, '') == 0)
    check(weechat.buffer_match_list(buffer, '*') == 1)
    check(weechat.buffer_match_list(buffer, 'core.weechat') == 1)
    check(weechat.buffer_match_list(buffer, '*,!core.weechat') == 0)
    weechat.buffer_close(buffer1)
    weechat.buffer_close(buffer2)


def test_lines():
    """Test line functions."""
    buffer = weechat.buffer_search_main()
    check(weechat.line_search_by_id(buffer, -1) == '')
    check(weechat.line_search_by_id(buffer, 1234567) == '')
    check(weechat.line_search_by_id(buffer, 0) != '')


def test_windows():
    """Test window functions."""
    window = weechat.current_window()
    check(window != '')
    buffer = weechat.buffer_search_main()
    check(weechat.window_search_with_buffer(buffer) != '')
    buffer1 = weechat.buffer_new('test1', 'buffer_input_cb', '', 'buffer_close_cb', '')
    check(buffer1 != '')
    check(weechat.window_search_with_buffer(buffer1) == '')
    weechat.buffer_close(buffer1)
    check(weechat.window_get_integer(window, 'number') == 1)
    check(weechat.window_get_string(window, 'xxx') == '')


def test_command():
    """Test command functions."""
    check(weechat.command('', '/mute') == 0)
    check(weechat.command_options('', '/mute', {'commands': '*,!print'}) == 0)
    check(weechat.command_options('', '/mute', {'commands': '*,!mute'}) == -1)


def infolist_cb(data, infolist_name, pointer, arguments):
    """Infolist callback."""
    infolist = weechat.infolist_new()
    check(infolist != '')
    item = weechat.infolist_new_item(infolist)
    check(item != '')
    check(weechat.infolist_new_var_integer(item, 'integer', 123) != '')
    check(weechat.infolist_new_var_string(item, 'string', 'test string') != '')
    check(weechat.infolist_new_var_pointer(item, 'pointer', '0xabcdef') != '')
    # Tue Jan 06 2009 08:40:30 GMT+0000
    check(weechat.infolist_new_var_time(item, 'time1', 1231231230) != '')
    # Wed Jan 06 2038 09:40:00 GMT+0000
    check(weechat.infolist_new_var_time(item, 'time2', 2146383600) != '')
    return infolist


def test_infolist():
    """Test infolist functions."""
    hook_infolist = weechat.hook_infolist('infolist_test_script',
                                          'description', '', '',
                                          'infolist_cb', '')
    check(weechat.infolist_get('infolist_does_not_exist', '', '') == '')
    ptr_infolist = weechat.infolist_get('infolist_test_script', '', '')
    check(ptr_infolist != '')
    check(weechat.infolist_next(ptr_infolist) == 1)
    check(weechat.infolist_integer(ptr_infolist, 'integer') == 123)
    check(weechat.infolist_string(ptr_infolist, 'string') == 'test string')
    check(weechat.infolist_pointer(ptr_infolist, 'pointer') == '0xabcdef')
    check(weechat.infolist_time(ptr_infolist, 'time1') == 1231231230)
    check(weechat.infolist_time(ptr_infolist, 'time2') == 2146383600)
    check(weechat.infolist_fields(ptr_infolist) == 'i:integer,s:string,p:pointer,t:time1,t:time2')
    check(weechat.infolist_next(ptr_infolist) == 0)
    weechat.infolist_free(ptr_infolist)
    weechat.unhook(hook_infolist)


def test_hdata():
    """Test hdata functions."""
    buffer = weechat.buffer_search_main()
    # get hdata
    hdata_buffer = weechat.hdata_get('buffer')
    check(hdata_buffer != '')
    hdata_lines = weechat.hdata_get('lines')
    check(hdata_lines != '')
    hdata_line = weechat.hdata_get('line')
    check(hdata_line != '')
    hdata_line_data = weechat.hdata_get('line_data')
    check(hdata_line_data != '')
    hdata_key = weechat.hdata_get('key')
    check(hdata_key != '')
    hdata_hotlist = weechat.hdata_get('hotlist')
    check(hdata_hotlist != '')
    hdata_irc_server = weechat.hdata_get('irc_server')
    check(hdata_irc_server != '')
    # create a test buffer with 3 messages
    buffer2 = weechat.buffer_new('test', 'buffer_input_cb', '', 'buffer_close_cb', '')
    weechat.prnt_date_tags(buffer2, 2146383600, 'tag1,tag2', 'prefix1\t## msg1')
    weechat.prnt_date_tags(buffer2, 2146383601, 'tag3,tag4', 'prefix2\t## msg2')
    weechat.prnt_date_tags(buffer2, 2146383602, 'tag5,tag6', 'prefix3\t## msg3')
    own_lines = weechat.hdata_pointer(hdata_buffer, buffer2, 'own_lines')
    line1 = weechat.hdata_pointer(hdata_lines, own_lines, 'first_line')
    line1_data = weechat.hdata_pointer(hdata_line, line1, 'data')
    line2 = weechat.hdata_pointer(hdata_line, line1, 'next_line')
    line3 = weechat.hdata_pointer(hdata_line, line2, 'next_line')
    # hdata_get_var_offset
    check(weechat.hdata_get_var_offset(hdata_buffer, 'id') == 0)
    check(weechat.hdata_get_var_offset(hdata_buffer, 'plugin') > 0)
    # hdata_get_var_type_string
    check(weechat.hdata_get_var_type_string(hdata_buffer, 'plugin') == 'pointer')
    check(weechat.hdata_get_var_type_string(hdata_buffer, 'number') == 'integer')
    check(weechat.hdata_get_var_type_string(hdata_buffer, 'name') == 'string')
    check(weechat.hdata_get_var_type_string(hdata_buffer, 'local_variables') == 'hashtable')
    check(weechat.hdata_get_var_type_string(hdata_line_data, 'displayed') == 'char')
    check(weechat.hdata_get_var_type_string(hdata_line_data, 'prefix') == 'shared_string')
    check(weechat.hdata_get_var_type_string(hdata_line_data, 'date') == 'time')
    check(weechat.hdata_get_var_type_string(hdata_hotlist, 'time') == 'time')
    check(weechat.hdata_get_var_type_string(hdata_hotlist, 'time_usec') == 'long')
    check(weechat.hdata_get_var_type_string(hdata_irc_server, 'sasl_scram_salted_pwd') == 'other')
    # hdata_get_var_array_size
    check(weechat.hdata_get_var_array_size(hdata_buffer, buffer2, 'name') == -1)
    check(weechat.hdata_get_var_array_size(hdata_buffer, buffer2, 'highlight_tags_array') >= 0)
    # hdata_get_var_array_size_string
    check(weechat.hdata_get_var_array_size_string(hdata_buffer, buffer2, 'name') == '')
    check(weechat.hdata_get_var_array_size_string(
        hdata_buffer, buffer2, 'highlight_tags_array') == 'highlight_tags_count')
    # hdata_get_var_hdata
    check(weechat.hdata_get_var_hdata(hdata_buffer, 'plugin') == 'plugin')
    check(weechat.hdata_get_var_hdata(hdata_buffer, 'own_lines') == 'lines')
    check(weechat.hdata_get_var_hdata(hdata_buffer, 'name') == '')
    # hdata_get_list
    check(weechat.hdata_get_list(hdata_buffer, 'gui_buffers') == buffer)
    # hdata_check_pointer
    check(weechat.hdata_check_pointer(hdata_buffer, buffer, buffer) == 1)
    check(weechat.hdata_check_pointer(hdata_buffer, buffer, buffer2) == 1)
    check(weechat.hdata_check_pointer(hdata_buffer, buffer, own_lines) == 0)
    # hdata_move
    check(weechat.hdata_move(hdata_line, line1, 1) == line2)
    check(weechat.hdata_move(hdata_line, line1, 2) == line3)
    check(weechat.hdata_move(hdata_line, line3, -1) == line2)
    check(weechat.hdata_move(hdata_line, line3, -2) == line1)
    check(weechat.hdata_move(hdata_line, line1, -1) == '')
    # hdata_search
    check(weechat.hdata_search(hdata_buffer, buffer, '${name} == test', {}, {}, {}, 1) == buffer2)
    check(weechat.hdata_search(hdata_buffer, buffer, '${name} == xxx', {}, {}, {}, 1) == '')
    # hdata_char
    check(weechat.hdata_char(hdata_line_data, line1_data, 'displayed') == 1)
    # hdata_integer
    check(weechat.hdata_integer(hdata_buffer, buffer2, 'number') == 2)
    # hdata_long
    weechat.buffer_set(buffer, 'hotlist', weechat.WEECHAT_HOTLIST_MESSAGE)
    gui_hotlist = weechat.hdata_get_list(hdata_hotlist, 'gui_hotlist')
    check(weechat.hdata_long(hdata_hotlist, gui_hotlist, 'creation_time.tv_usec') >= 0)
    # hdata_longlong
    check(weechat.hdata_longlong(hdata_buffer, buffer2, 'id') > 1708874542000000)
    # hdata_string
    check(weechat.hdata_string(hdata_buffer, buffer2, 'name') == 'test')
    # hdata_pointer
    check(weechat.hdata_pointer(hdata_buffer, buffer2, 'own_lines') == own_lines)
    # hdata_time
    check(weechat.hdata_time(hdata_line_data, line1_data, 'date') > 1659430030)
    # hdata_hashtable
    local_vars = weechat.hdata_hashtable(hdata_buffer, buffer2, 'local_variables')
    value = local_vars['name']
    check(value == 'test')
    # hdata_compare
    check(weechat.hdata_compare(hdata_buffer, buffer, buffer2, 'name', 0) > 0)
    check(weechat.hdata_compare(hdata_buffer, buffer2, buffer, 'name', 0) < 0)
    check(weechat.hdata_compare(hdata_buffer, buffer, buffer, 'name', 0) == 0)
    # hdata_update
    check(weechat.hdata_time(hdata_line_data, line1_data, 'date') == 2146383600)
    check(weechat.hdata_string(hdata_line_data, line1_data, 'prefix') == 'prefix1')
    check(weechat.hdata_string(hdata_line_data, line1_data, 'message') == '## msg1')
    update = {
        'date': '2146383605',
        'prefix': 'new_prefix1',
        'message': 'new_message1'
    }
    check(weechat.hdata_update(hdata_line_data, line1_data, update) == 3)
    check(weechat.hdata_time(hdata_line_data, line1_data, 'date') == 2146383605)
    check(weechat.hdata_string(hdata_line_data, line1_data, 'prefix') == 'new_prefix1')
    check(weechat.hdata_string(hdata_line_data, line1_data, 'message') == 'new_message1')
    # hdata_get_string
    check(weechat.hdata_get_string(hdata_line, 'var_prev') == 'prev_line')
    check(weechat.hdata_get_string(hdata_line, 'var_next') == 'next_line')
    # destroy test buffer
    weechat.buffer_close(buffer2)


def cmd_test_cb(data, buf, args):
    """Run all the tests."""
    weechat.prnt('', '>>>')
    weechat.prnt('', '>>> ------------------------------')
    weechat.prnt('', '>>> Testing ' + '{SCRIPT_LANGUAGE}' + ' API')
    weechat.prnt('', '  > TESTS: ' + '{SCRIPT_TESTS}')
    test_constants()
    test_plugins()
    test_strings()
    test_lists()
    test_config()
    test_key()
    test_display()
    test_hooks()
    test_buffers()
    test_lines()
    test_windows()
    test_command()
    test_infolist()
    test_hdata()
    weechat.prnt('', '  > TESTS END')
    return weechat.WEECHAT_RC_OK


def weechat_init():
    """Main function."""
    weechat.register('{SCRIPT_NAME}', '{SCRIPT_AUTHOR}', '{SCRIPT_VERSION}',
                     '{SCRIPT_LICENSE}', '{SCRIPT_DESCRIPTION}', '', '')
    weechat.hook_command('{SCRIPT_NAME}', '', '', '', '', 'cmd_test_cb', '')
