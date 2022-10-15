# Imports
import os
import logging




# Relative imports
from . import validate as v




# Non-standard-library imports
colorlog_imported = False
try:
  import colorlog
  colorlog_imported = True
except Exception as e:
  colorlog_imported = False




# Notes:
# - We generally create a logger for each module (i.e. each python file).
# - Each logger has its own name (which is its namespaced path, not just its name), and can have its own specific log level if this is useful.
# - This function is used to automatically configure a logger based on the supplied settings.




def configure_module_logger(
    logger,
    logger_name,
    log_level,
    debug,
    log_timestamp,
    log_file,
    ):
  # Avoid continually setting up a new logger on every new web request.
  if hasattr(logger, 'initialised') and logger.initialised:
    return
  # Validate input.
  v.validate_string(logger_name, 'logger_name', 'configure_module_logger')
  v.validate_string(log_level, 'log_level', 'configure_module_logger')
  v.validate_boolean(debug, 'debug', 'configure_module_logger')
  if log_timestamp is not None:
    v.validate_boolean(log_timestamp, 'log_timestamp', 'configure_module_logger')
  if log_file is not None:
    v.validate_string(log_file, 'log_file', 'configure_module_logger')
  # Configure logger.
  logger.propagate = False
  level_str = log_level
  level_str = 'debug' if debug else level_str
  levels = {
    'error': logging.ERROR,
    'warning': logging.WARNING,
    'info': logging.INFO,
    'debug': logging.DEBUG,
  }
  level = levels[level_str]
  logger.setLevel(level)
  logger.level_str = level_str
  # Add a convenience method.
  # Use camelCase to match logging module convention.

  def setLevelStr(level_str):
    level = levels[level_str]
    logger.setLevel(level)
    logger.level_str = level_str

  logger.setLevelStr = setLevelStr
  # Construct log_format.
  # Example log_format:
  # '%(asctime)s %(levelname)-8s [%(name)s: %(lineno)s (%(funcName)s)] %(message)s'
  # Example logLine:
  # 2020-11-19 13:14:10 DEBUG    [demo1.basic: 19 (hello)] Entered into basic.hello.
  log_format = '[' + logger_name + ': %(lineno)s (%(funcName)s)] %(message)s'
  # Note: In "%(levelname)-8s", the '8' pads the levelname length with spaces up to 8 characters, and the hyphen left-aligns the levelname.
  log_format = '%(levelname)-8s ' + log_format
  if log_timestamp:
    log_format = '%(asctime)s ' + log_format
  log_formatter = logging.Formatter(
    fmt = log_format,
    datefmt = '%Y-%m-%d %H:%M:%S'
  )
  log_formatter2 = None
  if colorlog_imported:
    # Build a new log format in which we apply colors to sections of the log line.
    # Notes:
    # - The default color is white.
    # - The default approach is to color only the log level text (e.g. INFO) so that everything else is easily readable if the background color of the terminal is changed (e.g. to 'red' to indicate a production server).
    # - A log color applies to the text that starts immediately afterwards, and continues until the end of the line or until a new log color is applied.
    log_format_color = log_format.replace('%(levelname)-8s ', '%(log_color)s%(levelname)-8s %(baseline_log_color)s')
    # Apply the message log color to the message text.
    log_format_color = log_format_color.replace('%(message)', '%(message_log_color)s%(message)')
    # Example log_format_color:
    # '%(asctime)s %(log_color)s%(levelname)-8s %(baseline_log_color)s[%(name)s: %(lineno)s (%(funcName)s)] %(message_log_color)s%(message)s'
    log_formatter2 = colorlog.ColoredFormatter(
      log_format_color,
      datefmt='%Y-%m-%d %H:%M:%S',
      reset=True,  # Clear all formatting (both foreground and background colors).
      # log_colors controls the base text color for particular log levels.
      # A second comma-separated value, if provided, controls the background color.
      log_colors={
        'DEBUG': 'blue',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
      },
      # secondary_log_colors controls the value of baseline & message log colors.
      # If a level is commented out, the relevant color from log_colors will be used instead.
      secondary_log_colors={
        'baseline': {
          'DEBUG': 'white',
          'INFO': 'white',
          'WARNING': 'white',
          'ERROR': 'white',
          'CRITICAL': 'white',
        },
        'message': {
          'DEBUG': 'white',
          'INFO': 'white',
          'WARNING': 'white',
          'ERROR': 'white',
          'CRITICAL': 'white',
        },
      },
    )
  # Set up console handler.
  if not colorlog_imported:
    # 1) Standard console handler:
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(log_formatter)
    logger.addHandler(console_handler)
  else:
    # 2) Colored console handler:
    console_handler2 = colorlog.StreamHandler()
    console_handler2.setLevel(level)
    console_handler2.setFormatter(log_formatter2)
    logger.addHandler(console_handler2)
  # Set up file handler.
  if log_file:
    # Create log_file directory if it doesn't exist.
    log_dir = os.path.dirname(log_file)
    if log_dir != '':
      if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    # Note: If log file already exists, new log lines will be appended to it.
    file_handler = logging.FileHandler(log_file, mode='a', delay=True)
    # If delay is true, then file opening is deferred until the first call to emit().
    file_handler.setLevel(level)
    # It turns out that the colorLog formatter's ANSI escape codes work in 'cat' & 'tail' (but not vim).
    # 'less' can, with the -R flag.
    # To display in vim, strip the escape chars: $ sed 's|\x1b\[[;0-9]*m||g' somefile | vim -
    if not colorlog_imported:
      file_handler.setFormatter(log_formatter)
    else:
      file_handler.setFormatter(log_formatter2)
    logger.addHandler(file_handler)
  logger.initialised = True
