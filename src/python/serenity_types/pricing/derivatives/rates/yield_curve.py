from datetime import date, datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class CurveType(Enum):
    """
    Varieties of yield curves supported.
    """

    RAW = "RAW"
    """
    Raw inputs, e.g. rates or prices.
    """

    INTERPOLATED = "INTERPOLATED"
    """
    Interpolated curve, with intermediate points filled in.
    """


class RateSourceType(Enum):
    """
    Sources of rates & discount factors. In the most general case
    the yield curve can be built from multiple imports, so we
    tag each CurvePoint that is the input to the interpolated YC
    with the particular source, e.g. we might have an 8H rate
    at the short end from perpetual future funding rates and
    implied forwards backed out from calendar spreads.
    """

    FUTURE_PX = "FUTURE_PX"
    """
    Implied forward backed out from observed future prices.
    """

    OPTION_PX = "OPTION_PX"
    """
    Implied forward backed out from observed option prices & spreads.
    """

    FIXING = "FIXING"
    """
    Observed traditional rate fixings.
    """

    FUNDING_RATE = "FUNDING_RATE"
    """
    Observed exchange perpetual future funding rate.
    """

    LENDING_RATE = "LENDING_RATE"
    """
    Observed CeFi / OTC or DeFi lending rate.
    """

    STAKING_RATE = "STAKING_RATE"
    """
    Observed proof-of-stake protocol staking rate.
    """


class InterpolationMethod(Enum):
    """
    Specific interpolation method used. Currently only supports flat-forward.
    """
    FLAT_FWD = "FLAT_FWD"


class CurvePoint(BaseModel):
    """
    A discrete input point on the curve, with all the metadata describing
    what is being provided and its source to help reproduce the results.
    """

    tenor: Optional[str]
    """
    A relative date code, e.g. 1Y or 3M.
    """

    pillar_date: Optional[date]
    """
    The specific forward date for the given rate and DF, e.g. the 1W point for today would be the next
    business day a week ahead.
    """

    duration: Optional[float]
    """
    The duration for this point, expressed as a year fraction.
    """

    rate_source_type: RateSourceType
    """
    The type of input being provided for this CurvePoint, e.g. if it's from a 3M future,
    this would be FUTURE_PX, while if it's from traditional rates fixings, it would be FIXINGS.
    """

    rate_sources: Optional[List[str]]
    """
    The specific rate sources used, e.g. OIS, SOFR or LIBOR; for LENDING_RATE, DeFi or other sources
    used, e.g. CHAINLINK, IPOR or AAVE. For FUNDING_RATE this holds the UUID for the exchange Organization ID.
    """

    reference_assets: Optional[List[UUID]]
    """
    In the case where an implied forward is backed out from market observables, the assets observed.
    """

    mark_prices: Optional[List[float]]
    """
    In the case where a DF is backed out from the implied forward of a reference asset or basket thereof,
    the observed prices that should go into the bootstrapping method.
    """

    rate: float
    """
    The input rate value, if DF not provided.
    """

    discount_factor: float
    """
    The input DF value, if rate not provided.
    """


class YieldCurve(BaseModel):
    """
    Base type for both RAW and INTERPOLATED yield curve representations: a term structure.
    """

    display_name: str
    """
    Human-readable descrition of this curve, e.g. OIS (RAW) or OIS (Interpolated, FLAT_FWD)
    """

    as_of_time: datetime
    """
    The time window, generally UTC midnight, for which we have bootstrapped this yield curve; latest rates / input
    prices as of this time are used.
    """

    build_time: datetime
    """
    The actual time of the build; due to DQ or system issues this might be different from as_of_time.
    """


class RawYieldCurve(YieldCurve):
    """
    A term structure of yield curve inputs. The RAW representation is offered to clients so they
    can either do their own interpolation or for diagnostics.
    """
    points: List[CurvePoint]


class InterpolatedYieldCurve(YieldCurve):
    """
    A term structure of rates and discount factors built from a RAW representation. This is the version
    that you should pass in for option valuation purposes, and is suitable for extracting rates and discount
    factors as well as plotting purposes.
    """

    rate_source_types: List[RateSourceType]
    """
    For reference purposes, the list of rate sources that were used to bootstrap this curve.
    """

    interpolation_method: InterpolationMethod
    """
    The specific interpolator type used to bootstrap this curve.
    """

    durations: List[float]
    """
    Array of all durations along the curve, as year fractions.
    """

    rates: List[float]
    """
    Array of all interpolated rates along the curve.
    """

    discount_factors: List[float]
    """
    Array of all discount factors (DF's) along the curve.
    """
