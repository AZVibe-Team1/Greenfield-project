"""
GICS Helper Module

This module provides utilities for working with GICS (Global Industry Classification Standard)
codes used for classifying companies by industry sector.

GICS is a four-tiered, hierarchical industry classification system:
- Level 1: Sector (2 digits)
- Level 2: Industry Group (4 digits)
- Level 3: Industry (6 digits)
- Level 4: Sub-Industry (8 digits)
"""

from gics import GICS
from pydantic import BaseModel, Field, field_validator


class GICSInfo(BaseModel):
    """
    Pydantic model for GICS code information.

    Attributes:
        code: The GICS code (2, 4, 6, or 8 digits)
        sector_name: Name of the sector (level 1)
        sector_code: Code of the sector
        industry_group_name: Name of the industry group (level 2, if available)
        industry_name: Name of the industry (level 3, if available)
        sub_industry_name: Name of the sub-industry (level 4, if available)
        level: The level of detail (1-4)
    """
    code: str = Field(..., description="GICS code")
    sector_name: str = Field(..., description="Sector name")
    sector_code: str = Field(..., description="Sector code")
    industry_group_name: str | None = Field(None, description="Industry group name")
    industry_name: str | None = Field(None, description="Industry name")
    sub_industry_name: str | None = Field(None, description="Sub-industry name")
    level: int = Field(..., ge=1, le=4, description="GICS level (1-4)")

    @field_validator('code')
    @classmethod
    def validate_gics_code(cls, v: str) -> str:
        """Validate that the GICS code is valid."""
        if len(v) not in [2, 4, 6, 8]:
            raise ValueError("GICS code must be 2, 4, 6, or 8 digits")
        if not v.isdigit():
            raise ValueError("GICS code must contain only digits")
        try:
            GICS(v)
        except Exception as e:
            raise ValueError(f"Invalid GICS code: {e}") from e
        return v


def parse_gics_code(code: str) -> GICSInfo:
    """
    Parse a GICS code and return structured information.

    Args:
        code: GICS code (2, 4, 6, or 8 digits)

    Returns:
        GICSInfo object with parsed information

    Raises:
        ValueError: If the GICS code is invalid

    Example:
        >>> info = parse_gics_code('10101010')
        >>> print(info.sector_name)
        'Energy'
        >>> print(info.sub_industry_name)
        'Oil & Gas Drilling'
    """
    try:
        gics = GICS(code)
    except Exception as e:
        raise ValueError(f"Invalid GICS code '{code}': {e}") from e

    # Determine the level based on code length
    level = len(code) // 2

    # Extract information based on level
    info = {
        "code": code,
        "sector_name": gics.sector.name,
        "sector_code": gics.sector.code,
        "level": level,
    }

    # Add industry group info if available (level 2+)
    if level >= 2:
        info["industry_group_name"] = gics.industry_group.name

    # Add industry info if available (level 3+)
    if level >= 3:
        info["industry_name"] = gics.industry.name

    # Add sub-industry info if available (level 4)
    if level == 4:
        info["sub_industry_name"] = gics.sub_industry.name

    return GICSInfo(**info)


def get_sector_name(code: str) -> str:
    """
    Get the sector name from a GICS code.

    Args:
        code: GICS code (any level)

    Returns:
        Sector name

    Example:
        >>> get_sector_name('10101010')
        'Energy'
    """
    gics = GICS(code)
    return gics.sector.name


def get_sector_code(code: str) -> str:
    """
    Get the sector code from a GICS code.

    Args:
        code: GICS code (any level)

    Returns:
        Sector code (2 digits)

    Example:
        >>> get_sector_code('10101010')
        '10'
    """
    gics = GICS(code)
    return gics.sector.code


def get_level_name(code: str, level: int) -> str:
    """
    Get the name at a specific GICS level.

    Args:
        code: GICS code (must be at or above the requested level)
        level: Level to retrieve (1=sector, 2=industry group, 3=industry, 4=sub-industry)

    Returns:
        Name at the specified level

    Raises:
        ValueError: If the code is not detailed enough for the requested level

    Example:
        >>> get_level_name('10101010', 4)
        'Oil & Gas Drilling'
        >>> get_level_name('10101010', 3)
        'Energy Equipment & Services'
    """
    gics = GICS(code)
    code_level = len(code) // 2

    if level > code_level:
        raise ValueError(f"Code '{code}' is level {code_level}, cannot get level {level}")

    return gics.level(level).name


def is_valid_gics_code(code: str) -> bool:
    """
    Check if a string is a valid GICS code.

    Args:
        code: String to validate

    Returns:
        True if valid, False otherwise

    Example:
        >>> is_valid_gics_code('10101010')
        True
        >>> is_valid_gics_code('99999999')
        False
    """
    try:
        GICS(code)
        return True
    except Exception:
        return False


def get_all_sectors() -> list[dict[str, str]]:
    """
    Get all available GICS sectors.

    Returns:
        List of dictionaries with sector codes and names

    Example:
        >>> sectors = get_all_sectors()
        >>> print(sectors[0])
        {'code': '10', 'name': 'Energy'}
    """
    # GICS sectors (as of the latest standard)
    sector_codes = ['10', '15', '20', '25', '30', '35', '40', '45', '50', '55', '60']
    sectors = []

    for code in sector_codes:
        try:
            gics = GICS(code)
            sectors.append({
                'code': code,
                'name': gics.sector.name
            })
        except Exception:
            continue

    return sectors


def compare_gics_codes(code1: str, code2: str) -> dict[str, bool]:
    """
    Compare two GICS codes to see their relationships.

    Args:
        code1: First GICS code
        code2: Second GICS code

    Returns:
        Dictionary with comparison results

    Example:
        >>> compare_gics_codes('10', '10101010')
        {'same_sector': True, 'same_industry_group': False, ...}
    """
    gics1 = GICS(code1)
    gics2 = GICS(code2)

    level1 = len(code1) // 2
    level2 = len(code2) // 2
    max_comparable_level = min(level1, level2)

    comparison = {
        'same_sector': False,
        'same_industry_group': False,
        'same_industry': False,
        'same_sub_industry': False,
    }

    # Compare at each level up to the maximum comparable level
    if max_comparable_level >= 1:
        comparison['same_sector'] = gics1.sector.code == gics2.sector.code

    if max_comparable_level >= 2:
        comparison['same_industry_group'] = gics1.industry_group.code == gics2.industry_group.code

    if max_comparable_level >= 3:
        comparison['same_industry'] = gics1.industry.code == gics2.industry.code

    if max_comparable_level >= 4:
        comparison['same_sub_industry'] = gics1.sub_industry.code == gics2.sub_industry.code

    return comparison


# Example usage and tests
if __name__ == "__main__":
    print("=== GICS Helper Module Examples ===\n")

    # Example 1: Parse a sector-level GICS code
    print("Example 1: Sector-level GICS code")
    sector_gics = GICS('10')
    print(f"  Code: 10")
    print(f"  Sector: {sector_gics.sector.name}")
    print()

    # Example 2: Parse a full GICS code
    print("Example 2: Full GICS code")
    full_gics = GICS('10101010')
    print(f"  Code: 10101010")
    print(f"  Sector: {full_gics.sector.name}")
    print(f"  Sub-Industry: {full_gics.sub_industry.name}")
    print(f"  Level 4: {full_gics.level(4).name}")
    print(f"  Level 3: {full_gics.level(3).name}")
    print(f"  Sector Code: {full_gics.sector.code}")
    print()

    # Example 3: Using helper functions
    print("Example 3: Using helper functions")
    info = parse_gics_code('10101010')
    print(f"  Parsed info: {info.sector_name} - {info.sub_industry_name}")
    print(f"  Level: {info.level}")
    print()

    # Example 4: Validation
    print("Example 4: Validation")
    print(f"  Is '10101010' valid? {is_valid_gics_code('10101010')}")
    print(f"  Is '99999999' valid? {is_valid_gics_code('99999999')}")
    print()

    # Example 5: Get all sectors
    print("Example 5: All sectors")
    sectors = get_all_sectors()
    for sector in sectors[:3]:  # Show first 3
        print(f"  {sector['code']}: {sector['name']}")
    print(f"  ... ({len(sectors)} total sectors)")
    print()

    # Example 6: Compare codes
    print("Example 6: Compare GICS codes")
    comparison = compare_gics_codes('10', '10101010')
    print(f"  Comparing '10' and '10101010':")
    print(f"  Same sector: {comparison['same_sector']}")

