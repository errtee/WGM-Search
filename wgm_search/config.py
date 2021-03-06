#!/usr/bin/env python
# configuration
class Config(object):
    "Default Config environment, parent to all other Config environments"

    DATABASE = 'sqlite:///wgm.db'
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    "Development environment config"

    DEBUG = True

class TestingConfig(Config):
    "Testing environment config"

    TESTING = True
    DATABASE = 'sqlite:///wgm_test.db'

class ProductionConfig(Config):
    "Production environment config"
