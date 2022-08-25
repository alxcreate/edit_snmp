from pysnmp.hlapi import *


def snmp_get(target, oids, credentials, port=161, timeout=1, retries=0, engine=SnmpEngine(), context=ContextData()):
    handler = getCmd(
        engine,
        credentials,
        UdpTransportTarget((target, port, timeout, retries)),
        context,
        *construct_object_types(oids)
    )
    return fetch(handler, 1)[0]


def construct_object_types(list_of_oids):
    object_types = []
    for oid in list_of_oids:
        object_types.append(ObjectType(ObjectIdentity(oid)))
    return object_types


def fetch(handler, count):
    result = []
    for i in range(count):
        try:
            error_indication, error_status, error_index, var_binds = next(handler)
            if not error_indication and not error_status:
                items = {}
                for var_bind in var_binds:
                    items[str(var_bind[0])] = cast(var_bind[1])
                result.append(items)
            else:
                raise RuntimeError('Got SNMP error: {0}'.format(error_indication))
        except StopIteration:
            break
    return result


def cast(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        try:
            return float(value)
        except (ValueError, TypeError):
            try:
                return str(value)
            except (ValueError, TypeError):
                pass
    return value


# CommunityData('public')
# UsmUserData('testuser', authKey='authenticationkey', privKey='encryptionkey', authProtocol=usmHMACSHAAuthProtocol, privProtocol=usmAesCfb128Protocol)


def snmp_set(target, value_pairs, credentials, port=161, timeout=1, retries=0, engine=SnmpEngine(), context=ContextData()):
    handler = setCmd(
        engine,
        credentials,
        UdpTransportTarget((target, port, timeout, retries)),
        context,
        *construct_value_pairs(value_pairs)
    )
    return fetch(handler, 1)[0]


def construct_value_pairs(list_of_pairs):
    pairs = []
    for key, value in list_of_pairs.items():
        pairs.append(ObjectType(ObjectIdentity(key), value))
    return pairs
