def get_different_roules(dict_data, key):
    """
    获取不同规则
    :param dict_data:
    :param key:
    :return:
    """
    roule = {
        "shareholderChange": {
            "licenseNum": "",
            "assigneeLicenseNum": "",
            "assigneeCid": "",
            "executionDate": "",
            "assigneeLicenseType": "",
            "executedPerson": "",
            "assignee": "",
            "executeOrderNum": "",
            "equityAmountOther": "",
            "implementationMatters": "",
            "executiveCourt": "",
            "assigneeType": "",
            "executeNoticeNum": "",
            "executedPersonCid": "",
            "executedPersonType": "",
            "licenseType": ""
        },
        "frozen": {
            "id": "",
            "equityAmount": "",
            "typeState": "",
            "executiveCourt": "",
            "executedPerson": "",
            "executeNoticeNum": "",
            "executedPersonCid": "",
            "assId": "",
            "executedPersonType": ""
        },
        "removeFrozen": {
            "licenseNum": "",
            "executedPersonHid": "",
            "executiveCourt": "",
            "executedPerson": "",
            "executeNoticeNum": "",
            "executedPersonCid": "",
            "frozenRemoveDate": "",
            "equityAmountOther": "",
            "executeOrderNum": "",
            "executedPersonType": "",
            "licenseType": "",
            "implementationMatters": ""
        },
        "keepFrozen": {
            "licenseNum": "",
            "executedPersonHid": "",
            "executedPerson": "",
            "toDate": "",
            "executeOrderNum": "",
            "equityAmountOther": "",
            "period": "",
            "implementationMatters": "",
            "executiveCourt": "",
            "fromDate": "",
            "executeNoticeNum": "",
            "executedPersonCid": "",
            "executedPersonType": "",
            "licenseType": "",
            "publicityAate": ""
        },
        "invalidationFrozen": {
            "invalidationDate": "",
            "invalidationReason": ""
        },
        "assDetail": {
            "equityAmount": "",
            "executeNoticeNum": "",
            "executedPerson": "",
            "executedPersonCid": "",
            "executedPersonHid": "",
            "executedPersonType": "",
            "executiveCourt": "",
            "id": "",
            "typeState": ""
        }

    }

    data_info = {}
    for k in roule.get(key).keys():
        data_info[k] = dict_data.get(k)

    return data_info


if __name__ == '__main__':
    pass