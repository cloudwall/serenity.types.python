from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel

from serenity_types.refdata.options import OptionType


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


class VolatilitySurfaceDefinition(BaseModel):
    """
    A uniquely-identified set of VS parameters for fitting a VolatilitySurface.
    """

    vol_surface_id: UUID
    """
    Unique ID for this volatility surface's collection of attributes; note that surfaces
    are re-fitted hourly, and so there are going to be many versions over time.
    """

    vol_model: VolModel
    """
    Volatility model used for this surface.
    """

    strike_type: StrikeType
    """
    Strike representation used for this surface, e.g. ABSOLUTE or LOG_MONEYNESS.
    """

    underlier_asset_id: UUID
    """
    The linked asset for this surface, e.g. for a Bitcoin volatility surface, this is BTC.
    """

    display_name: str
    """
    Human-readable descrition of this curve, e.g. OIS (RAW) or OIS (Interpolated, FLAT_FWD)
    """


class VolatilitySurfaceAvailability(BaseModel):
    """
    Information about version availability for a given volsurface definition.
    """

    definition: VolatilitySurfaceDefinition
    """
    Description of the particular volsurface parameters that are available to load.
    """

    build_times: List[datetime]
    """
    The list of all available build times in the requested window.
    """


class VolPoint(BaseModel):
    """
    An individual IV input point.
    """

    option_asset_id: UUID
    """
    The specific option that was used for vol fitting purposes.
    """

    time_to_expiry: float
    """
    The time to expiry for this point, expressed as a year fraction.
    """

    mark_price: float
    """
    The observed option premium used as input to the IV calculation.
    """

    rates: Optional[Dict[UUID, float]]
    """
    The observed discounting rates that went into the IV calculations, if any.
    """

    forward_price: float
    """
    The observed or calculated forward price that went into the IV calculation.
    """

    iv: float
    """
    The computed implied volatility (IV) that corresponds to the given mark_price and other inputs.
    """


class RawVolatilitySurface(BaseModel):
    definition: VolatilitySurfaceDefinition
    """
    The unique set of parameters used to calibrate / fit this surface.
    """
    
    spot_price: float
    """
    The observed spot price that went into the IV calculations.
    """

    vol_points: List[VolPoint]
    """
    The discrete IV points available for fitting as a volatility surface.
    """


class InterpolatedVolatilitySurface(BaseModel):
    """
    A calibrated volatility surface with a dense grid of fitted vols. Each array
    is of equal length and corresponds to (x, y, z) for the mesh.
    """

    definition: VolatilitySurfaceDefinition
    """
    The unique set of parameters used to calibrate / fit this surface.
    """

    strikes: List[float]
    """
    All strikes expressed as log-money values, the x-axis in the mesh.
    """

    time_to_expiries: List[float]
    """
    All times to expiry expressed as year fractions, the y-axis in the mesh.
    """

    vols: List[float]
    """
    All fitted vols, the z-axis in the mesh.
    """

    option_types: List[OptionType]
    """
    Due to dirty data on Deribit, our calibration fits separately for PUT and CALL options.
    To allow pricing of either option type, the fitted surface returns both. This array
    tells you the type for the corresponding fitted volatility in the vols array.
    """


class VolatilitySurfaceVersion(BaseModel):
    """
    A single version of a fitted volatility surface, with both the raw and interpolated content.
    """

    raw: RawVolatilitySurface
    """
    The raw volatility surface inputs.
    """

    interpolated: InterpolatedVolatilitySurface
    """
    The interpolated volatility surface.
    """

    as_of_time: datetime
    """
    The time window, generally top of the hour, for which we have fitted the volatility surface; latest prices
    as of this time are used as input to the surface calibration.
    """

    build_time: datetime
    """
    The actual time of the build; due to DQ or system issues this might be different from as_of_time.
    """
