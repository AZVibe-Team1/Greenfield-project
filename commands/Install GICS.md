Implement this library that provides a way to parse, manipulate and analyze GICS codes. 
GICS (Global Industry Classification Standard) is a classification system by MSCI.
Put the code in the backend/utils folder calling it gics_helper.py
Example:
from gics import GICS

valid_sector_level_GICS = GICS('10')
print(valid_sector_level_GICS.sector.name)  # 'Energy'

valid_full_GICS = GICS('10101010')
print(valid_full_GICS.sector.name)  # 'Energy'
print(valid_full_GICS.sub_industry.name)  # 'Oil & Gas Drilling'
print(valid_full_GICS.level(4).name)  # 'Oil & Gas Drilling'
print(valid_full_GICS.level(3).name)  # 'Energy Equipment & Services'
print(valid_full_GICS.sector.code)  # '10'