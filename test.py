from oslo_config import cfg
from oslo_log import log as logging

LOG = logging.getLogger(__name__)

def init_config_and_logging(opts):
    conf = cfg.CONF
    conf.register_cli_opts(opts)
    conf.register_opts(opts)
    logging.register_options(conf)
    logging.set_defaults()


    logging.setup(conf, 'performa')
    LOG.info('Logging enabled')

    conf.log_opt_values(LOG, logging.DEBUG)
    logging.debug('Logging enabled')

