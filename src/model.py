from dataclasses import dataclass, asdict
from enum import Enum
from collections import OrderedDict


class Ratings(Enum):
    NONE = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    def __str__(self):
        return str(self.value)
    
    def as_api(self):
        return f'IN:{self.value}:5'
    

class QuaRatings(Enum):
    NONE = 0
    NEGATIVE = 1
    NEUTRAL = 2
    BRONZE = 3
    SILVER = 4
    GOLD = 5
    def __str__(self):
        return str(self.value)
    
    def as_api(self):
        return f'IN:{self.value}:5'


class Levels(Enum):
    NONE = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    def __str__(self):
        if self == Levels.NONE:
            return "NONE"
        return str(self.value)
    
    def as_api(self):
        return f'IN:{self.value}:5'

class Charge(Enum):
    NONE = 0
    LT_05 = 1
    BTW_05_1 = 2
    BTW_1_15 = 3
    BTW_15_2 = 4
    GT_2 = 5
    def __str__(self):
        if self == Charge.NONE:
             return "NONE"
        if self == Charge.LT_05:
             return ":LT:0.5"
        if self == Charge.BTW_05_1:
             return ":BTW:0.5:1"
        if self == Charge.BTW_1_15:
             return ":BTW:1:1.5"
        if self == Charge.BTW_15_2:
             return ":BTW:1.5:2"
        if self == Charge.GT_2:
             return ":GT:2"
        return str(self.value)

class ManagementStyle(Enum):
    NONE = 0
    ACTIVE = 1
    PASIVE = 2
    def __str__(self):
        if self == Charge.NONE:
             return "NONE"
        if self == ManagementStyle.ACTIVE:
             return "false"
        return "true"

class FundSize(Enum):
    NONE = 0
    LT_100m = 1
    BTW_100m_500m = 2
    BTW_500m_1b = 3
    BTW_1b_10b = 4
    GT_10b = 5
    def __str__(self):
        if self == Charge.NONE:
             return "NONE"
        if self == FundSize.LT_100m:
             return ":LT:100000000"
        if self == FundSize.BTW_100m_500m:
             return ":BTW:100000000:500000000"
        if self == FundSize.BTW_500m_1b:
             return ":BTW:500000000:1000000000"
        if self == FundSize.BTW_1b_10b:
             return ":BTW:1000000000:10000000000"
        if self == FundSize.GT_10b:
             return ":GT:10000000000"
        return str(self.value)


class YieldPercent(Enum):
    NONE = 0
    BTW_0_2 = 1
    BTW_2_4 = 2
    BTW_4_6 = 3
    BTW_6_8 = 4
    GT_8 = 5
    def __str__(self):
        if self == YieldPercent.NONE:
             return "NONE"
        if self == YieldPercent.BTW_0_2:
             return ":BTW:0:2"
        if self == YieldPercent.BTW_2_4:
             return ":BTW:2:4"
        if self == YieldPercent.BTW_4_6:
             return ":BTW:4:6"
        if self == YieldPercent.BTW_6_8:
             return ":BTW:6:8"
        if self == YieldPercent.GT_8:
             return ":GT:8"
        return str(self.value)
    
def quarating_from_class(rating_class):
    number = int(rating_class[-1])
    if number == 1:
        return "Negative"
    if number == 2:
        return "Neutral"
    if number == 3:
        return "Bronze"
    if number == 4:
        return "Silver"
    if number == 5:
        return "Gold"
    if number == 6:
        return "Under Review"
    if number == 7:
        return "Not Ratable"    
    return None


class MSUniverses(Enum):
    FUND = 0
    ETF = 1

@dataclass
class MSFundFilter:
    """Class model the filterSelectedValue 
    """    
    analystRatingScale: QuaRatings = QuaRatings.NONE
    brandingCompanyId: str = None
    categoryId: str = None  
    managementStyle: ManagementStyle = ManagementStyle.NONE  
    ongoingCharge: Charge  = Charge.NONE#check values
    quantitativeRating: QuaRatings = QuaRatings.NONE
    starRating: Levels = Levels.NONE
    sustainabilityRating: Levels = Levels.NONE    
    fundSize: FundSize = FundSize.NONE       
    yieldPercent: YieldPercent = YieldPercent.NONE 
    universe: MSUniverses = MSUniverses.FUND   
    #TODO: There are more filters that can be applyied but those are the more common.


    def to_id_string(self, name, value):
        """Helper method that just format the name and value into the 
        ms filter json structure filtering out the ones with NONE

        Args:
            name (str): name of the filter field to use
            value (): value to be expressed as str

        Returns:
            str: the field formated in ms json form 'name:{id:value}'
        """
        if isinstance(value, Enum) and value.name == 'NONE':
            return ""        
        return f'"{name}":{{"id":"{str(value)}"}}'

    def to_filter_json(self):
        """Returns the filter representation as MS json string
        Note: This is not a normal field:value list json representation
        """                    
        m_dict = asdict(self)        
        rep = [self.to_id_string(key, val) for key, val in m_dict.items() if val!= None]
        rep2 = [v for v in rep if v != ""]
        return "{" + ','.join(rep2) + "}"
    
    def to_api_filter(self):
        """Returns the filter as a string to be used on the ms api to filter
        TODO: Not all options are yet used

        Returns:
            str: Filter string to be used in the api calls
        """
        rep = []
        if self.starRating != Levels.NONE:
            rep.append('StarRatingM255:' + self.starRating.as_api())
            
        if self.sustainabilityRating != Levels.NONE:
            rep.append('SustainabilityRank:' + self.sustainabilityRating.as_api())
        
        if self.quantitativeRating != QuaRatings.NONE:
            rep.append('AnalystRatingScale:' + self.quantitativeRating.as_api())

        return '|'.join(rep)


@dataclass
class MSFund:
    """Class to keep information of funds.
    The use of a class allows to better abstraction and allows to 
    define several output formats
    """    
    MSID: str = None #the id for morning star
    ISIN: str = None #the fund isin
    name: str = None
    rating: int = 1 # change to range from 1-5
    quarating: str = None 
    sustainability: int = 1 #change to range from 1-5  
    vl: float = 0.0
    date_vl: str = None
    daily_change: str = None
    category: str  = None 
    heritage: str = None
    date_heritage: str = None
    heritage_class: str = None 
    date_heritage_class: str = None 
    comission_max: str = None
    common_expenses: str = None
    date_common_expenses: str = None    
    volatility:  float = 0.0
    rentabilidad:  float = 0.0
    sharpe: float = 0.0
    
    

    def get_properties_names(self):
        """Returns the dataclass properties names as list 

        Returns:
            list[str]: List of the names of the properties
        """
        #use of an ordereddict to ensure that all instances provides same output        
        rep = [key for key, val in  asdict(self,  dict_factory=OrderedDict).items()]
        return rep    

    def get_properties(self):
        """Returns the dataclass properties values as list 

        Returns:
            list: list of the values of the properties
        """
        #use of an ordereddict to ensure that all instances provides same output        
        rep = [val for key, val in  asdict(self,  dict_factory=OrderedDict).items()]
        return rep    
    
