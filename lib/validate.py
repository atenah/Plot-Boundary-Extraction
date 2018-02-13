def validate(configpath, dtdpath, xsdpath):
    try:
        from lxml import objectify, etree               # may raise ImportError

        with open(configpath, 'rU') as configfile:
            config = objectify.parse(configfile)

            with open(dtdpath, 'rU') as dtdfile:
                dtd = etree.DTD(dtdfile)
                if not dtd.validate(config):
                    raise Exception(dtd.error_log.filter_from_errors()[0])

            with open(xsdpath, 'rU') as xsdfile:
                xsd = objectify.parse(xsdfile)
                xmlschema = etree.XMLSchema(xsd)
                xmlschema.assertValid(config)

    except ImportError:
        return
