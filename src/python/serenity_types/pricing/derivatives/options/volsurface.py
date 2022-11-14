from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class VolModel(Enum):
    """
    Currently supported volatility models.
    """

    SVI = "SVI"
    """
    Stochastic volatility (SVI) calibrated volatility model.
    """

    BLACK_SCHOLES = "BLACK_SCHOLES"
    """
    Classic Black-Scholes volatility model.
    """


class VolSurfaceType(Enum):
    """
    Representation of the volatility surface, e.g. raw inputs vs. fitted surface.
    """

    RAW = "RAW"
    """
    A volatility surface containing the raw inputs: the option prices, IV's, etc..
    """

    FITTED = "FITTED"
    """
    A calibrated and fitted volatility surface with a dense grid of IV's.
    """


class StrikeType(Enum):
    """
    Currently supported strike representations.
    """

    ABSOLUTE = "ABSOLUTE"
    """
    Absolute value of strike, e.g. the 20000 option.
    """

    LOG_MONEYNESS = "LOG_MONEYNESS"
    """
    Relative value of strike vs. current spot, with log transformation, e.g. 1.05
    """


class VolatilitySurface(BaseModel):
    """
    Base type for both RAW and INTERPOLATED yield curve representations: a term structure.
    """

    display_name: str
    """
    Human-readable descrition of this curve, e.g. OIS (RAW) or OIS (Interpolated, FLAT_FWD)
    """

    vol_model: VolModel
    """
    Volatility model used for this surface.
    """

    strike_type: StrikeType
    """
    Strike representation used for this surface, e.g. ABSOLUTE or LOG_MONEYNESS.
    """

    as_of_time: datetime
    """
    The time window, generally top of the hour, for which we have bootstrapped this yield curve; latest prices
    as of this time are used as input to the surface calibration.
    """

    build_time: datetime
    """
    The actual time of the build; due to DQ or system issues this might be different from as_of_time.
    """


class VolPoint:
    """
    An individual IV input point.
    """

    maturity: Optional[str]
    """
    A relative date code, e.g. 1Y or 3M.
    """

    expiry: Optional[datetime]
    """
    The specific expiry for the option that was the input for this vol point.
    """

    time_to_expiry: Optional[float]
    """
    The time to expiry for this point, expressed as a year fraction.
    """

    mark_price: float
    """
    The observed option premium used as input to the IV calculation.
    """

    iv: float
    """
    The computed implied volatility (IV) that corresponds to the given mark_price and other inputs.
    """


class RawVolatilitySurface(VolatilitySurface):
    vol_points: List[VolPoint]


class FittedVolatilitySurface(VolatilitySurface):
    """
    A calibrated volatility surface with a dense grid of implied vols. Each array
    is of equal length and corresponds to (x, y, z) for the mesh.
    """
    strikes: List[float]

    time_to_maturities: List[float]

    vols: List[float]
