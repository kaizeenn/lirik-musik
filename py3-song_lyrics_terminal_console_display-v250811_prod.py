#  Code that ALWAYS get executed; either main, or imported as module from other script.
# print(__name__)

#  LIBRARIES / PACKAGES IMPORTS.

import os                                   #  To work with directories.
from rich import print as rprint            #  Rich text and beautiful formatting.
import warnings                             #  For showing warnings to developer.
import glob                                 #  For listing files, using UNIX REGEX.
import re                                   #  For REGEX, listing files, format validation of inputs, etc.
import yaml                                 #  For managing input files in YAML format.
import json                                 #  To convert Python objects (generally lists and dictionaries with appropiate structure) to JSONs strings (a.k.a. 'dumps'), and viceversa (a.k.a. 'loads').
import datetime                             #  To manage dates, times, and time durations.
import zoneinfo                             #  For timezones.
import pandas as pd                         #  Dataframes, and csv's.
import numpy as np                          #  Dataframes NaNs to None, and viceversa.
import copy                                 #  For shallow and deep copies, specially oj objects such as dictionaries, dataframes, etc.
import sys                                  #  To adjust default system output flush.
from time import sleep                      #  To manage pauses on code execution, for lyrics / song lines display.

#  USER DEFINEND FUNCTIONS (UDFs).

#  Validate if a DIRECTORY path exists, and creates it (optionally, True by default) if it doesn't exist.
def UDFValidateDirectoryExists(IPath: str, ICreateDir: bool = True) -> None:
    if (not os.path.exists(IPath)):
        warnings.warn(f"[WARNING] Directory '{IPath}' should exist in order for current script to run properly.")
        if (ICreateDir):
            rprint(f"[LOG] Creating directory: '{IPath}'.")
            os.mkdir(IPath)
    else:
        rprint(f"[LOG] Directory found: '{IPath}'.")
    
    return None

#  Search for basename paths (i.e. files OR directories), starting from a given directory (CURRENT working directory, if not provided) in a RECURSIVELY manner.
def UDFSearchPaths(IBasename: str, IDirpath: str = '**') -> list:
    basename_regex = IBasename.encode('unicode-escape').decode('unicode-escape') + r'$'     #  Python raw strings and RegEx: 'https://www.digitalocean.com/community/tutorials/python-raw-string'.
    search_space_pattern = IDirpath if (IDirpath == '**') else (IDirpath + '/**')
    filepaths_list = [i for i in glob.iglob(search_space_pattern, recursive = True) if re.search(basename_regex, i, re.IGNORECASE)]     #  RegEx re.search() vs. re.match(): 'https://www.geeksforgeeks.org/python/python-re-search-vs-re-match/'.
    #  Throws an AssertionError, if no path found.
    assert len(filepaths_list) > 0, f"[ERROR] File or directory called '{basename_regex[:-1]}' (after unicode escaping) should exist in order for current script to run properly."
    
    return filepaths_list

#  [AUXILIARY] Prettify JSONs; i.e. converts Python object (generally lists and dictionaries with appropiate structure) to JSON string (a.k.a. 'dumps'). Ref. 'https://www.dataquest.io/blog/api-in-python/'.
def UDFJsonPrint(IObject) -> None:
    text = json.dumps(IObject, sort_keys = False, indent = 4)
    print(text)
    
    return None

#  Converts to basic* data types; it requires at MINIMUM: value to convert, and specify it's data type.
#  - *No-iterables: null, boolean, string, integer, decimal, complex, and numeric range (last one, returns a list).
#  - *Iterables: list, tuple, and set. These requiere additionally specification of the data subtype (i.e. type of their elements).
#  It returns the converted value, or 'None' if any mistake on the inputs like:
#  - The data type is not of any of the basic* data types.
def UDFConvertToBasicDataTypes(IValue, IDataType: str, IDataSubType = None):
    
    value_string                = str(IValue).strip()           #  It tries ALWAYS to convert value to string, as a starting point.
    data_type                   = str(IDataType).strip()        #  It tries ALWAYS to convert the input of data type to string, and clean it.
    data_subtype                = str(IDataSubType).strip() if (IDataSubType is not None) else (None)   #  By default is 'None'; otherwise, try to clean it.
    value_converted             = None
    DATA_TYPES                  = (
        'null', 'boolean', 'string', 'integer', 'decimal', 'complex', 'range'
        , 'date and/or time (with or without timezone)'
        , 'time duration'
        , 'list', 'tuple', 'set'
    )
    DATA_TYPES_FOR_ITERABLES    = (
        'null', 'boolean', 'string', 'integer', 'decimal', 'complex', 'range'
        , 'date and/or time (with or without timezone)'
        , 'time duration'
    )

    if data_type not in DATA_TYPES:
        value_converted = None
    else:
        if data_type == 'null':
            value_converted = None
        if data_type == 'boolean':
            value_converted = True if (value_string.lower().capitalize() == 'True') else (False)
        if data_type == 'string':
            value_converted = value_string
        if data_type == 'integer':
            value_converted = int(value_string)
        if data_type == 'decimal':
            value_converted = float(value_string)
        if data_type == 'complex':
            value_converted = complex(value_string)
        if data_type == 'range':
            value_converted = list(range(int(value_string)))
        if data_type == 'date and/or time (with or without timezone)':
            date_time_timezone_format = ''
            date_time = None
            date_time_timezone = None
            #  RegEx expression for searching matches:
            #+ YYYY/MM/DD HH:MM:SS.X[+/-]timezone(in HHMM),
            #+ where YYYY: [1900, 2099], MM: [01, 12], DD: [01, 31], HH: [00, 23], MM: [00, 59], SS: [00, 59], X: [0, 999999].
            #+ e.g. '2011/08/15 12:45:01.095673-0500'.
            #  Test at 'https://regex101.com'.
            date_time_timezone_regex = r'^(?P<date>(?P<year>(19|20)\d{2})/(?P<month>0[1-9]|1[0-2])/(?P<day>0[1-9]|[12][0-9]|3[0-1])\b)? ?(?P<time>\b(?P<hour>[01][0-9]|2[0-3]):(?P<min>[0-5][0-9]):(?P<sec>[0-5][0-9])(\.(?P<microsec>\d{1,6}))?(?P<timezone>(?P<timezone_sign>[+-])(?P<timezone_hour>[01][0-9]|2[0-3])(?P<timezone_min>[0-5][0-9]))?)?$'
            regex_match = re.search(date_time_timezone_regex, value_string)    #  If using re.match(), date_time_timezone_regex = r'...' DOESN'T require '^'; i.e. RegEx re.search() vs. re.match(): 'https://www.geeksforgeeks.org/python/python-re-search-vs-re-match/'.
            if regex_match is not None:
                #  e.g. '2011/08/15 12:45:01.095673-0500'.
                #  date_time_timezone_format = '%Y/%m/%d %H:%M:%S.%f%z'    :date+time+tz    : datetime.datetime.strptime(value_string, date_time_timezone_format) > datetime.datetime.
                #  date_time_timezone_format = '%Y/%m/%d %H:%M:%S.%f'      :date+time       : datetime.datetime.strptime(value_string, date_time_timezone_format) > datetime.datetime.
                #  date_time_timezone_format = '%Y/%m/%d %H:%M:%S'         :date+time       : datetime.datetime.strptime(value_string, date_time_timezone_format) > datetime.datetime.
                #  date_time_timezone_format = '%Y/%m/%d'                  :date            : datetime.datetime.strptime(value_string, date_time_timezone_format) > datetime.date.
                #  date_time_timezone_format = '%H:%M:%S'                  :time            : datetime.datetime.strptime(value_string, date_time_timezone_format) > datetime.time.
                #  date_time_timezone_format = '%H:%M:%S.%f'               :time            : datetime.datetime.strptime(value_string, date_time_timezone_format) > datetime.time.
                #  date_time_timezone_format = '%H:%M:%S.%f%z'             :time+tz         : datetime.datetime.strptime(value_string, date_time_timezone_format) > datetime.time.
                term = (regex_match.group('date') is not None, regex_match.group('time') is not None, regex_match.group('microsec') is not None, regex_match.group('timezone') is not None)
                match term:
                    case (True, True, True, True):          #  e.g. '2011/08/15 12:45:01.095673-0500'.
                        date_time_timezone_format           = '%Y/%m/%d %H:%M:%S.%f%z'
                        date_time                           = datetime.datetime.strptime(value_string, date_time_timezone_format)
                        date_time_timezone                  = date_time
                    case (True, True, True, False):         #  e.g. '2011/08/15 12:45:01.095673'.
                        date_time_timezone_format           = '%Y/%m/%d %H:%M:%S.%f'
                        date_time                           = datetime.datetime.strptime(value_string, date_time_timezone_format)
                        date_time_timezone                  = date_time
                    case (True, True, False, False):        #  e.g. '2011/08/15 12:45:01'.
                        date_time_timezone_format           = '%Y/%m/%d %H:%M:%S'
                        date_time                           = datetime.datetime.strptime(value_string, date_time_timezone_format)
                        date_time_timezone                  = date_time
                    case (True, False, False, False):       #  e.g. '2011/08/15'.
                        date_time_timezone_format           = '%Y/%m/%d'
                        date_time                           = datetime.datetime.strptime(value_string, date_time_timezone_format)
                        date_time_timezone                  = date_time.date()
                    case (False, True, False, False):       #  e.g. '12:45:01'.
                        date_time_timezone_format           = '%H:%M:%S'
                        date_time                           = datetime.datetime.strptime(value_string, date_time_timezone_format)
                        date_time_timezone                  = date_time.time()
                    case (False, True, True, False):        #  e.g. '12:45:01.095673'.
                        date_time_timezone_format           = '%H:%M:%S.%f'
                        date_time                           = datetime.datetime.strptime(value_string, date_time_timezone_format)
                        date_time_timezone                  = date_time.time()
                    case (False, True, True, True):         #  e.g. '12:45:01.095673-0500'. NOTE: timezone data will be lost, since only a 'datetime.datetime' object can store timezone data; not 'datetime.date' nor 'datetime.time' alone.
                        date_time_timezone_format           = '%H:%M:%S.%f%z'
                        date_time                           = datetime.datetime.strptime(value_string, date_time_timezone_format)
                        date_time_timezone                  = date_time.time()
                    case _:                                 #  'Default'.
                        warnings.warn(f"Entry: '{value_string}' doesn't match the format; entry won't be processed. Please review it follows the format: 'YYYY/MM/DD HH:MM:SS.X[+/-]timezone(in HHMM)', where YYYY: [1900, 2099], MM: [01, 12], DD: [01, 31], HH: [00, 23], MM: [00, 59], SS: [00, 59], X: [0, 999999]; e.g. '2011/08/15 12:45:01.095673-0500'.")
            else:
                warnings.warn(f"Entry: '{value_string}' doesn't match the format; entry won't be processed. Please review it follows the format: 'YYYY/MM/DD HH:MM:SS.X[+/-]timezone(in HHMM)', where YYYY: [1900, 2099], MM: [01, 12], DD: [01, 31], HH: [00, 23], MM: [00, 59], SS: [00, 59], X: [0, 999999]; e.g. '2011/08/15 12:45:01.095673-0500'.")
            value_converted = date_time_timezone
        if data_type == 'time duration':
            time_delta = None
            #  Format for time splitting:
            #+ HH:MM:SS,
            #+ where HH: number (integer or decimal), MM: number (integer or decimal), SS: number (integer or decimal).
            #+ e.g. 2 days > 24h*2 > '48:00:00'; 36 min and 2.56 sec > '36:2.56'.
            term = tuple(map(float, value_string.split(':')))
            match term:
                case (split_hours, split_minutes, split_seconds):
                    time_delta = datetime.timedelta(hours = split_hours, minutes = split_minutes, seconds = split_seconds)
                case (split_minutes, split_seconds):
                    time_delta = datetime.timedelta(minutes = split_minutes, seconds = split_seconds)
                case (split_seconds, ):
                    time_delta = datetime.timedelta(seconds = split_seconds)
                case _:                                     #  'Default'.
                    warnings.warn(f"Entry: '{value_string}' doesn't match the format; entry won't be processed. Please review it follows the format: 'HH:MM:SS', where HH: number (integer or decimal), MM: number (integer or decimal), SS: number (integer or decimal); e.g. 2 days > 24h*2 > '48:00:00'; 36 min and 2.56 sec > '36:2.56'")
                    # time_delta = datetime.timedelta()     # '0:00:00'. If ever required in a future, but right now, default return for no matches is 'None'.
            value_converted = time_delta
        if data_subtype in DATA_TYPES_FOR_ITERABLES:            #  To avoid INFINITE RECURSIVENESS; e.g. data_type: 'list', and data_subtype: 'tuple'.
            #  Use of 'map()' to apply a function to iterable(s): 'https://www.geeksforgeeks.org/python/python-map-function/', 'https://www.w3schools.com/python/ref_func_map.asp'.
            #  Repeat an element, several times in a list: 'https://stackoverflow.com/questions/3459098/create-list-of-single-item-repeated-n-times/3459131#3459131'.
            if data_type == 'list':
                value_converted = list(map(UDFConvertToBasicDataTypes, value_string.split('|'), [data_subtype] * len(value_string.split('|'))))
            if data_type == 'tuple':
                value_converted = tuple(map(UDFConvertToBasicDataTypes, value_string.split('|'), [data_subtype] * len(value_string.split('|'))))
            if data_type == 'set':
                value_converted = set(map(UDFConvertToBasicDataTypes, value_string.split('|'), [data_subtype] * len(value_string.split('|'))))

    return value_converted

#  Creates a dictionary of variables, with proper data conversion.
#  - IT REQUIRES CUSTOM FUNCTION UDFConvertToBasicDataTypes().
#  - Input is a LIST in proper format for each variable:
#+ [ { 'name': <variable_name>, 'type': <variable_type_from_UDFConvertToBasicDataTypes()>, 'subtype': <variable_subtype_from_UDFConvertToBasicDataTypes()>,
#+ 'comment': <variable_comment>, 'value': <variable_value> }, { ... } ].
#  - Output format: { <variable1_name> : <variable1_value>, <variable2_name> : <variable2_value>, ...}.
def UDFCreateVariablesDictionaryFromFormattedList(IList: list) -> dict:
    variables_dictionary  = {}
    
    for index, variable in enumerate(IList):                                                        #  Get index of a list iterator: 'https://www.stellargrove.com/how-to-blog/find-the-index-of-the-iterator-of-a-list'.
        (variable_name, variable_type, variable_subtype, variable_comment, variable_value)          = \
        (variable['name'], variable['type'], variable['subtype'], variable['comment'], variable['value'])
        #  Validates MINIMUM fields for a variable to be valid; e.g. 'name', and 'type'. Ref. 'https://ellibrodepython.com/assert-python'.
        assert all([
            variable_name is not None, variable_type is not None
            ]), f"[Variable number '{index + 1}'] In order for a variable to be processed, it requires at MINIMUM: a 'name', and 'type' defined; at least 1 is missing."
        
        variable_name_clean                         = str(variable_name).strip()
        variable_type_clean                         = str(variable_type).strip()
        variable_subtype_clean                      = str(variable_subtype).strip() if (variable_subtype is not None) else (None)

        #  Data transformation.
        variables_dictionary[variable_name_clean]   = UDFConvertToBasicDataTypes(variable_value, variable_type_clean, variable_subtype_clean)

    return variables_dictionary

#  Load variables from formatted dictionary into globals().
def UDFLoadVariablesToGlobals(IDictionary: dict) -> None:
    for variable_name, variable_value in IDictionary.items():
        globals()[variable_name] = variable_value
    rprint(f"[LOG] Variables loaded to 'globals()' (x{len(IDictionary)}): '{"' | '".join([*IDictionary.keys()])}'.")

    return None

#  Load CSV, SPECIFIC to user parameters; e.g. 'py3-song_lyrics_terminal_console_display-v250811-input_user_params.csv'.
#  - Input is a csv file in proper format:
#+ a. csv file MUST NOT have a header.
#+ b. EACH csv record MUST BE in format: '<variable_name>, <variable_value>'.
#  - Output: a dictionary containing objects.
#+ Format is { '<object1_name>': <object1>, '<object2_name>': <object2>, ... }
def UDFLoadCSVUserParameters(ICsvFilepath: str) -> list:
    objects_dictionary = {}

    #  Pandas dataframe custom parameters. 'dtypes' list available at: 'https://pandas.pydata.org/docs/user_guide/basics.html#dtypes'.
    DATAFRAME_COLUMN_TYPES = {'name': 'string', 'value': object}
    DATAFRAME_COLUMN_NAMES = list(DATAFRAME_COLUMN_TYPES.keys())

    #  Create Pandas dataframe, from '.csv' file: 'https://www.datacamp.com/tutorial/pandas-read-csv', 'https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html'.
    #  - Forces NOT to create header from file.
    #  - Header with column names will be provided with list 'DATAFRAME_COLUMN_NAMES'; e.g. 'name', and 'value'.
    #  - Columns data types will be provided with list 'DATAFRAME_COLUMN_TYPES'; e.g. dtype 'string' for 'name', and dtype 'object' for 'value' (to keep intended original value).
    user_variables_dataframe = pd.read_csv(ICsvFilepath, header = None, names = DATAFRAME_COLUMN_NAMES, dtype = DATAFRAME_COLUMN_TYPES)

    #  Remapping of new values, matching to indexes.
    name_dictionary         = {
        0: 'user_song_lines_file'
    }
    type_dictionary         = {
        0: 'string'
    }
    subtype_dictionary      = {
        0: None
    }
    comment_dictionary      = {
        0: "POSITION 0 (row 1): 'user_song_lines_file'. Variable for choosing which song lines file to play, using the file's name; e.g. 'song_lines-lemon_demon-fine.csv'."
    }
    # value_dictionary        = {0: ...}  #  Not used since it's provided by user.

    #  Remap columns data with additional details of variables.
    #+ NOTE: entries already in the dataframe with no match in previously defined dictionaries, will be LOST; i.e. get a value of 'NaN'.
    user_variables_dataframe['name']        = user_variables_dataframe.index.map(name_dictionary)
    #  New columns, with python dictionary: 'https://builtin.com/data-science/pandas-add-column'.
    user_variables_dataframe['type']        = user_variables_dataframe.index.map(type_dictionary)
    user_variables_dataframe['subtype']     = user_variables_dataframe.index.map(subtype_dictionary)
    user_variables_dataframe['comment']     = user_variables_dataframe.index.map(comment_dictionary)

    #  Clean dataframe.
    column_order_list                       = ['name', 'type', 'subtype', 'comment', 'value']           #  Rearrange columns order: define order with list.
    user_variables_dataframe                = user_variables_dataframe[column_order_list]               #  Rearrange columns order.
    user_variables_dataframe                = user_variables_dataframe.replace(np.nan, None)            #  Clean nulls ('NaN's to 'None'): 'https://www.statology.org/pandas-replace-nan-with-none/'.
    user_variables_dataframe                = user_variables_dataframe[
        user_variables_dataframe['name'].apply(lambda x : x is not None)]                               #  Filter rows with 'name' entries valid; i.e. not 'None'.
    # rprint(user_variables_dataframe.isnull())                                                           #  Quick check of null values.

    # #  NOTES ON ACCESSING CELLS, ROWS AND COLUMNS WITHIN A DATAFRAME.
    # #
    # #  DATAFRAME QUICK VIEW:
    # rprint(
    #     user_variables_dataframe.info(), '---',
    #     user_variables_dataframe.head(), '---',
    #     user_variables_dataframe.describe(), '---',
    #     sep = '\n\n'
    # )
    # #
    # #  HOW TO ACCESS A CELL OF A DATAFRAME:                                                                                 : 'https://stackoverflow.com/questions/28757389/pandas-loc-vs-iloc-vs-at-vs-iat/30022658#30022658'.
    # #  - '.at'      : access SINGLE CELL using labels (i.e. indexes for rows, names for columns) and filters.               : 'https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.at.html#pandas.DataFrame.at'.
    # #  - '.iat'     : access SINGLE CELL using positions (i.e. position [x,y], starting at [0, 0]). NO FILTERS.             : 'https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.iat.html'.
    # #  - '.loc'     : access SEVERAL cells (groups) using labels.                                                           : 'https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.loc.html#pandas.DataFrame.loc'.
    # #  - '.iloc'    : access SEVERAL cells (groups) using positions (positions end at [shape[0] - 1, shape[1] - 1]).        : 'https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.iloc.html#pandas.DataFrame.iloc'.
    # #  - '.loc' vs '.iloc' examples.                                                                                        : 'https://www.datacamp.com/tutorial/loc-vs-iloc'.
    # rprint(user_variables_dataframe.iat[0,4])                                                                               #  GET cell value (e.g. as a string) in dataframe POSITION [0, 4]; i.e. row = 0, column = 4.
    # user_variables_dataframe.at[0, 'name'] = 'user_song_lines_file'                                                         #  SET cell value in dataframe referenced by LABELS: row INDEX (not POSITION) = 0, column CALLED = 'name'.
    # #  - Filtering dataframe and getting cell values (a.k.a. 'scalar')                                                      : 'https://stackoverflow.com/questions/65829774/how-to-get-the-value-of-a-cell-based-on-filtering-efficently/65829854#65829854'.
    # #  - Use '.values' to get cell values (a.k.a. 'scalar')                                                                 : 'https://stackoverflow.com/questions/70422875/difference-between-values-and-iloc-on-a-pandas-series/70422985#70422985'.
    # rprint(user_variables_dataframe.loc[user_variables_dataframe['name'] == 'user_song_lines_file'])                        #  GET rows (and columns; as a dataframe, 'filtered'), where cell (row) value is 'user_song_lines_file' in column 'name'.
    # rprint(user_variables_dataframe.loc[user_variables_dataframe['name'] == 'user_song_lines_file'].values)                 #  GET rows (and columns; as numpy array (similar to a list)), where cell (row) value is 'user_song_lines_file' in column 'name'.
    # rprint(user_variables_dataframe.loc[user_variables_dataframe['name'] == 'user_song_lines_file'].values[0])              #  GET 1st row (and columns; as numpy array (similar to a list)), from previous numpy array example.
    # rprint(user_variables_dataframe.loc[user_variables_dataframe['name'] == 'user_song_lines_file'].values[0][4])           #  GET value (e.g. as a string) of 'column' 4 (more like item in POSITON 4), from previous numpy array example.
    # rprint(user_variables_dataframe.loc[user_variables_dataframe['name'] == 'user_song_lines_file'].iat[0, 4])              #  GET cell value (e.g. as a string) from 'filtered' dataframe in last previous dataframe results example.
    # #
    # rprint(user_variables_dataframe.loc[user_variables_dataframe['name'] == 'user_song_lines_file', 'value'])               #  GET column (and rows; as pandas series, 'filtered') called 'value', where cell (row) value is 'user_song_lines_file' in column 'name'.
    # rprint(user_variables_dataframe.loc[user_variables_dataframe['name'] == 'user_song_lines_file', 'value'].values)        #  GET column (and rows; as numpy array (similar to a list)), where cell (row) value is 'user_song_lines_file' in column 'name'.
    # rprint(user_variables_dataframe.loc[user_variables_dataframe['name'] == 'user_song_lines_file', 'value'].values[0])     #  GET 1st value (e.g. as a string), from previous numpy array example. Unlike previous example section, the filtering of 'column 4' was not necessary, since it was done in the 1st filtering (as a pandas series).
    # rprint(user_variables_dataframe.loc[user_variables_dataframe['name'] == 'user_song_lines_file', 'value'].iat[0])        #  GET cell value (e.g. as a string) from 'filtered' pandas series in last previous pandas series results example.

    #  Transforms dataframe into dictionary with proper format: 'https://stackoverflow.com/questions/26716616/convert-a-pandas-dataframe-to-a-dictionary/26716774#26716774'.
    user_variables_list = user_variables_dataframe.to_dict(orient = 'records')

    rprint(f"[LOG] Variables imported in total (x{len(user_variables_list)}), from: '{ICsvFilepath}'.")

    #  Return objects in a dictionary.
    #+ 'copy.deepcopy()' function should be used outside of this function, whenever is called. Putting it here, would be inefficient in terms of memory.
    #+ Ref. 'https://www.geeksforgeeks.org/python/copy-python-deep-copy-shallow-copy/'.
    objects_dictionary = {
        'user_variables_dataframe': user_variables_dataframe,
        'user_variables_list': user_variables_list
    }

    return objects_dictionary

#  Load CSV, SPECIFIC to song lines; e.g. 'song_lines-lemon_demon-fine.csv'.
#  - Input is a csv file in proper format:
#+ a. csv file MUST have a header with 'column' names: 'line', 'line_character_delay', 'line_repetition', and 'line_end_delay'.
#+ b. EACH csv record MUST BE of type: 'string, float, integer, float'.
#  - Output: a dictionary containing objects.
#+ Format is { '<object1_name>': <object1>, '<object2_name>': <object2>, ... }
def UDFLoadCSVSongLines(ICsvFilepath: str) -> list:
    objects_dictionary = {}

    #  Pandas dataframe custom parameters. 'dtypes' list available at: 'https://pandas.pydata.org/docs/user_guide/basics.html#dtypes'.
    DATAFRAME_COLUMN_TYPES = {'line': 'string', 'line_character_delay': 'Float64', 'line_repetition': 'Int64', 'line_end_delay': 'Float64'}
    DATAFRAME_COLUMN_NAMES = list(DATAFRAME_COLUMN_TYPES.keys())

    #  Create Pandas dataframe, from '.csv' file: 'https://www.datacamp.com/tutorial/pandas-read-csv', 'https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html'.
    #  - Forces to avoid creating header from file, ommiting line 0 (first data point).
    #  - Header with column names will be provided with list 'DATAFRAME_COLUMN_NAMES'; e.g. 'name', and 'value'.
    #  - Columns data types will be provided with list 'DATAFRAME_COLUMN_TYPES'; e.g. dtype 'string' for 'name', and dtype 'object' for 'value' (to keep intended original value).
    song_lines_dataframe = pd.read_csv(ICsvFilepath, header = 0, names = DATAFRAME_COLUMN_NAMES, dtype = DATAFRAME_COLUMN_TYPES)

    #  Transforms dataframe into list of tuples: 'https://blog.finxter.com/python-create-list-of-tuples-from-dataframe/'.
    song_lines_list = [tuple(row) for index, row in song_lines_dataframe.iterrows()]

    rprint(f"[LOG] Song lyrics (lines) imported (x{len(song_lines_list)}), from: '{ICsvFilepath}'.")

    #  Return objects in a dictionary.
    #+ 'copy.deepcopy()' function should be used outside of this function, whenever is called. Putting it here, would be inefficient in terms of memory.
    #+ Ref. 'https://www.geeksforgeeks.org/python/copy-python-deep-copy-shallow-copy/'.
    objects_dictionary = {
        'song_lines_dataframe': song_lines_dataframe,
        'song_lines_list': song_lines_list
    }

    return objects_dictionary

#  [Fast user defined function (UDF) definition] Clear terminal / console output.
#  [OP01] Traditional way.
# def UDFClearOutput() -> None:
#     os.system('clear')      #  Executes os function called 'clear'. Either in Linux or Windows, clear() clears terminal / console / CLI output.
#     return None
#
#  [OP02] Using lambda, anonymous / nameless functions. Ref. 'https://www.freecodecamp.org/news/lambda-expressions-in-python/', 'https://www.geeksforgeeks.org/python/python-lambda-anonymous-functions-filter-map-reduce/'.
UDFClearOutput = lambda: os.system('clear')

#  Core function of displaying song lyrics / lines.
#  - IT REQUIRES CUSTOM FUNCTION UDFClearOutput().
#  - Input is 1. a list of tuples; a list for a single song, with each tuple representing a song line,
#+ and 2. an integer defining the regular lines interval for clearing the console / terminal / CLI.
#+ Format follows requirements of function UDFLoadCSVSongLines() for each csv record.
#  NOTE: output is not properly rendered in Jupyter Notebooks.
def UDFSongLinesTypewriter(ISongLinesList: list, ILinesIntervalOutputClearing: int) -> None:
    line_counter = 0        #  Counter to determine when to clear console / terminal / CLI output.
    UDFClearOutput()

    #  Iterates over each song line.
    for i, (line, line_character_delay, line_repetition, line_end_delay) in enumerate(ISongLinesList):
        if (line_repetition == 1): line_counter += 1                #  Only count lines for regular song lines; i.e. ones that 'play' ONCE, unlike lines such as '[delay]' or '. . .', that will repeat more than ONCE (i.e. line_repetition > 1).
        line_repetition_backward_counter = line_repetition - 1      #  For non-regular song lines, such as delay flags (e.g. '[delay]', '. . .'), it will display the counter in the console / terminal / CLI.

        for j in range(line_repetition):                            #  For regular song lines, it will iterate only ONCE.
            line_repetition_text = '' if (line_repetition == 1) else (' x' + str(line_repetition_backward_counter))
            line_adjusted = line + line_repetition_text             #  Adds backwards counter to text if line repeats more than ONCE; empty otherwise.
            
            for line_character in line_adjusted:                    #  Iterates over the line, showing one character at a time.
                rprint(f'[gold1]{line_character}[/gold1]', end = '')
                sys.stdout.flush()                                  #  Forces terminal to print a character: 'https://stackoverflow.com/questions/10019456/usage-of-sys-stdout-flush-method/10019605#10019605', 'https://medium.com/@hhtg250/stdin-stdout-flush-and-buffering-in-python-e747b85cb6ae'.
                sleep(line_character_delay)
            
            rprint()
            if line_repetition != 1: UDFClearOutput()               #  Clears output, if it's a non-regular song line.
            line_repetition_backward_counter -= 1

        sleep(line_end_delay)

        if (line_counter == ILinesIntervalOutputClearing):          #  Clears output and resets line counter, if reaches user-defined regular song lines to show.
            UDFClearOutput()
            line_counter = 0
    
    UDFClearOutput()                                                #  Clears output when finalizing song.
    return None

#  MAIN FUNCTION.
def main():
    # print('Hello World')

    #  INPUTS.

    #  Main directory.

    _PROJECT_BASE_FILENAME       = 'py3-song_lyrics_terminal_console_display'
    _VERSION_NAME                = 'v250811_prod'

    home_dirpath = None
    #  How to get a python filepath: 'https://note.nkmk.me/en/python-script-file-path/'.
    #  How to get a python filepath, considering Jupyter Notebooks: 'https://medium.com/@jennycoreholt/how-to-professionally-import-external-files-in-jupyter-notebooks-4000f1ce16f7'.
    if '__file__' in globals():
        file_filepath   = None
        #  If it's a regular python file / module: 'https://stackoverflow.com/questions/38412495/difference-between-os-path-dirnameos-path-abspath-file-and-os-path-dirnam/38412504#38412504', 'https://community.esri.com/t5/python-blog/finding-python-script-home-folder/bc-p/884009/highlight/true'.
        #  Alternative: 'https://saturncloud.io/blog/how-to-obtain-jupyter-notebooks-path/'.
        file_filepath   = os.path.abspath(__file__)
        home_dirpath    = os.path.dirname(file_filepath)
    else:
        #  If it's a Jupyter Notebook: 'https://stackoverflow.com/questions/39125532/file-does-not-exist-in-jupyter-notebook/53958599#53958599', 'https://forums.fast.ai/t/file-dunder-attribute-works-in-py-not-in-notebook/102400/7'.
        home_dirpath    = str(globals()['_dh'][0])

    #  Input: data.
    input_dirpath_relative_to_home                      = 'io_dir-input'        #  Dirpath relative to home directory.
    input_configuration_dirpath_relative_to_home        = os.path.join(input_dirpath_relative_to_home, 'config')        #  Directory for configuration files.
    input_user_parameters_dirpath_relative_to_home      = os.path.join(input_dirpath_relative_to_home, 'user_params')   #  Directory for input user instructions, if required.
    input_user_files_dirpath_relative_to_home           = os.path.join(input_dirpath_relative_to_home, 'user_files')    #  Directory for user files, if input required.

    input_configuration_filenames_regex     = _PROJECT_BASE_FILENAME + '-' + _VERSION_NAME + r'-input_.*\.yaml'           #  String literal for RegEx expresion of configuration filenames patterns; e.g. '...-input-<...>.yaml': 'https://www.w3schools.com/python/python_regex.asp', 'https://regex101.com'. Files listing base variables and their structure; e.g. user timezone, column names for dataframes, etc. NOTE: all matching files will be processed the SAME WAY.
    input_user_parameters_filename          = _PROJECT_BASE_FILENAME + '-' + _VERSION_NAME + r'-input_user_params.csv'    #  File listing variables that require input from user; e.g. copy or cut?, file to read, etc. Usually variables used here, SHOULD BE PRE-DECLARED in a YAML configration file; e.g. in 'py3-song_lyrics_terminal_console_display-v250811-input_config.yaml'.
    input_user_files_filename_regex         = r'song_lines-.*\.csv'                                                     #  String literal for RegEx expresion of user filenames patterns; e.g. 'song_lines-<...>.csv': 'https://www.w3schools.com/python/python_regex.asp', 'https://regex101.com'. NOTE: all matching files will be processed the SAME WAY.

    #  Output.
    output_dirpath_relative_to_home         = 'io_dir-output'                   #  Dirpath relative to home directory.

    #  INITIALIZATION.

    #  Print current working directory.
    working_directory = os.getcwd()
    rprint(f"[LOG] Current working directory: '{working_directory}'.")

    #  Set working directory to 'home'.
    rprint(f"[LOG] Changing current working directory to: '{home_dirpath}'.")
    os.chdir(home_dirpath)
    working_directory = os.getcwd()
    rprint(f"[LOG] Current working directory: '{working_directory}'.")

    #  [INITIALIZATION] PROJECT BASE STRUCTURE VALIDATION.

    #  Inputs validations: wheter or not exists input directory.
    UDFValidateDirectoryExists(input_dirpath_relative_to_home)

    #  Inputs validations: wheter or not exists configuration sub-directory (of input directory).
    #  NOTE: it REQUIRES parent directory (input directory) to exist.
    UDFValidateDirectoryExists(input_configuration_dirpath_relative_to_home)

    #  Inputs validations: wheter or not exists user parameters sub-directory (of input directory).
    #  NOTE: it REQUIRES parent directory (input directory) to exist.
    UDFValidateDirectoryExists(input_user_parameters_dirpath_relative_to_home)

    #  Inputs validations: wheter or not exists user files sub-directory (of input directory).
    #  NOTE: it REQUIRES parent directory (input directory) to exist.
    UDFValidateDirectoryExists(input_user_files_dirpath_relative_to_home)

    #  Outputs validations: wheter or not exists output directory.
    UDFValidateDirectoryExists(output_dirpath_relative_to_home)

    #  Inputs validations: searches for configuration of base variables.
    input_configuration_filepaths_relative_to_home          = UDFSearchPaths(input_configuration_filenames_regex, input_configuration_dirpath_relative_to_home)
    #  Inputs validations: searches for user parameters file.
    input_user_parameters_filepaths_relative_to_home        = UDFSearchPaths(input_user_parameters_filename, input_user_parameters_dirpath_relative_to_home)
    #  Inputs validations: searches for user files required as input, besides parameters, using REGEX.
    input_user_files_filepaths_relative_to_home             = UDFSearchPaths(input_user_files_filename_regex, input_user_files_dirpath_relative_to_home)

    rprint(f"[LOG] Configuration files found (x{len(input_configuration_filepaths_relative_to_home)}): '{"' | '".join(input_configuration_filepaths_relative_to_home)}'.")
    rprint(f"[LOG] User parameters files found (x{len(input_user_parameters_filepaths_relative_to_home)}): '{"' | '".join(input_user_parameters_filepaths_relative_to_home)}'.")
    rprint(f"[LOG] User files found (x{len(input_user_files_filepaths_relative_to_home)}): '{"' | '".join(input_user_files_filepaths_relative_to_home)}'.")

    #  [INITIALIZATION] INPUT: CONFIGURATION FILE(S) LOAD.

    #  Load configuration YAML file.
    #  - Load '.yaml' file: 'https://www.geeksforgeeks.org/python/parse-a-yaml-file-in-python/'.
    yaml_variables_data = None
    yaml_variables_list = []

    for yaml_filepath in input_configuration_filepaths_relative_to_home:
        with open(yaml_filepath, 'r') as file:
            yaml_variables_data = yaml.load(file, Loader = yaml.SafeLoader)
        if yaml_variables_data is not None:                              #  1st check YAML file is not empty.
            if yaml_variables_data['parameters'] is not None:            #  2nd check if there is a 'parameters' section.
                yaml_variables_list += yaml_variables_data['parameters']      #  Or also could use '<list>.extend(<other_list>)': 'https://sparkbyexamples.com/python/python-append-list-to-a-list/'.
                # rprint(f"[LOG] Variables imported (x{len(yaml_variables_data['parameters'])}), from '{yaml_filepath}'.")

    rprint(f"[LOG] Variables imported in total (x{len(yaml_variables_list)}), from: '{"' | '".join(input_configuration_filepaths_relative_to_home)}'.")

    #  Get a dictionary of variables from YAML file, with proper data conversion.
    yaml_variables_dictionary = UDFCreateVariablesDictionaryFromFormattedList(yaml_variables_list)

    #  Load variables YAML file into globals().
    UDFLoadVariablesToGlobals(yaml_variables_dictionary)

    #  Set execution timezone.
    _TIME_ZONE = zoneinfo.ZoneInfo(_USER_GEOGRAPHIC_TIMEZONE)

    #  [INITIALIZATION] INPUT: USER PARAMETERS FILE(S) LOAD.

    #  Load user parameters CSV file and gets a dictionary with 1. the dataframe, and 2. list equivalent (records-like).
    user_variables_objects_dictionary   = UDFLoadCSVUserParameters(input_user_parameters_filepaths_relative_to_home[0])

    #  Create deepcopy of output from loading user parameters CSV.
    # user_variables_dataframe            = copy.deepcopy(user_variables_objects_dictionary['user_variables_dataframe'])
    user_variables_list                 = copy.deepcopy(user_variables_objects_dictionary['user_variables_list'])

    #  Get a dictionary of variables from user configuration file, with proper data conversion.
    user_variables_dictionary = UDFCreateVariablesDictionaryFromFormattedList(user_variables_list)

    #  Load variables YAML file into globals().
    UDFLoadVariablesToGlobals(user_variables_dictionary)

    #  [MAIN] Load user selected song_lines file; e.g. 'song_lines-lemon_demon-fine.csv'

    #  Get filenames of user files, using the filepaths relative to home, previously obtained.
    #
    #  [OP01] Using list comprehension: 'https://stackoverflow.com/questions/25082410/apply-function-to-each-element-of-a-list/25082458#25082458', 'https://ellibrodepython.com/list-comprehension-python', 'https://www.geeksforgeeks.org/python/apply-function-to-each-element-of-a-list-python/'.
    input_user_files_filenames = [os.path.basename(input_user_files_filepath) for input_user_files_filepath in input_user_files_filepaths_relative_to_home]
    #  Throws an AssertionError, if no path found.
    assert user_song_lines_file in input_user_files_filenames, f"[ERROR] Input file called '{user_song_lines_file}', provided by user in '{input_user_parameters_filepaths_relative_to_home[0]}', should exist in order for current script to run properly."
    #
    # #  [OP02] Using filtering with lambda functions in lists: 'https://labex.io/tutorials/python-how-to-filter-list-with-conditions-419442'.
    # input_user_files_filename_list = list(filter(
    #         lambda x : x == user_song_lines_file,
    #         map(
    #             lambda y : os.path.basename(y),     #  Or simply 'os.path.basename', without using lambda.
    #             input_user_files_filepaths_relative_to_home
    #         )
    #     )
    # )
    # #  Throws an AssertionError, if no match.
    # assert len(input_user_files_filename_list) > 0, f"[ERROR] Input file called '{user_song_lines_file}', provided by user in '{input_user_parameters_filepaths_relative_to_home[0]}', should exist in order for current script to run properly."

    #  Gets filepaths of song lines file, defined by user in variable 'user_song_lines_file'.
    song_lines_csv_filepaths = list(filter(
            lambda x : os.path.basename(x) == user_song_lines_file,
            input_user_files_filepaths_relative_to_home
        )
    )

    #  Load song lines CSV file and gets a dictionary with 1. the dataframe, and 2. list of tuples.
    song_lines_objects_dictionary   = UDFLoadCSVSongLines(song_lines_csv_filepaths[0])

    #  Create deepcopy of output from loading song lines CSV.
    # song_lines_dataframe            = copy.deepcopy(song_lines_objects_dictionary['song_lines_dataframe'])
    song_lines_list                 = copy.deepcopy(song_lines_objects_dictionary['song_lines_list'])

    #  [MAIN] Play song lines typewriter.
    
    #  Delay message popup before starting song lines typewriter.
    #  - Backwards iteration: 'https://www.geeksforgeeks.org/python/backward-iteration-in-python/', 'https://docs.python.org/3/library/functions.html#func-range'.
    for i in range(_TIME_DELAY_FOR_START_OF_SONG_LINES_TYPEWRITER, 0, -1):
        if ((i == (_TIME_DELAY_FOR_START_OF_SONG_LINES_TYPEWRITER)) or (i == 5) or (i == 3) or (i == 2) or (i == 1)): {
            print(f"Song lyrics will start to roll in {i} seconds...")
        }
        sleep(1)
    
    UDFSongLinesTypewriter(song_lines_list, _INTERVAL_FOR_CLEARING_OUTPUT_AFTER_REGULAR_LINES)

#  CODE EXECUTION.

#  Code executed ONLY when script is called directly; NOT IMPORTED from other script.
if __name__ == '__main__':
    main()