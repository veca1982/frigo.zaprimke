# config.py


class Config(object):
    """
    Common configurations
    """
    SECRET_KEY = 'p9Bv<3Eid9%$i01'
    SQLALCHEMY_DATABASE_URI = 'mysql://dt_admin:dt2016@localhost/dreamteam_db'

    # Put any configurations here that are common across all environments


class DevelopmentConfig(Config):
    """
    Development configurations
    """
    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    """
    Production configurations
    """
    SECRET_KEY = '7228e25f3eaeb82bc02be55ba3c3f1fb6f96a1a9383c0722be65da0965c58afd'
    SQLALCHEMY_DATABASE_URI = 'postgres://vetskieamburwa:7228e25f3eaeb82bc02be55ba3c3f1fb6f96a1a9383c0722be65da0965c58afd@ec2-184-73-189-221.compute-1.amazonaws.com:5432/d589d4h3qqiui'

    DEBUG = False


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
