from enum import Enum


class InconsistenceType(Enum):
    DateOutOfPeriod = 'date_out_of_valid_range'
    EmptyValue = 'empty'
    WhiteSpaceValue = 'white_space'
    ZeroValue = 'zero_value'
    HyphenValue = 'hyphen_value'

    @classmethod
    def get_dict_values(cls):
        response=[]
        for inconsistence_enum in InconsistenceType:
            response.append(
                {
                    'id':name,
                    'inconsistence_label':value
                }
            )
        return sorted(response, key=lambda d: d['id'])