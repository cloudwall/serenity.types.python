from serenity_types.refdata.currency import Currency
from serenity_types.refdata.exposure import Exposure
from serenity_types.refdata.futures import Future
from serenity_types.refdata.index import ReferenceIndex
from serenity_types.refdata.options import ListedOption
from serenity_types.refdata.sector import AssetSectorMappings, SectorTaxonomy
from serenity_types.refdata.symbology import SymbolAuthority, XRefSymbol
from serenity_types.refdata.token import TokenAsset, WrappedTokenAsset
from serenity_types_tests.testutils.serialization import roundtrip


def test_roundtrip_asset_objects():
    roundtrip(Currency)
    roundtrip(Future)
    roundtrip(ListedOption)
    roundtrip(ReferenceIndex)
    roundtrip(TokenAsset)
    roundtrip(WrappedTokenAsset)


def test_roundtrip_exposure_objects():
    roundtrip(Exposure)


def test_roundtrip_sector_objects():
    roundtrip(AssetSectorMappings)
    roundtrip(SectorTaxonomy)


def test_roundtrip_symbology_objects():
    roundtrip(SymbolAuthority)
    roundtrip(XRefSymbol)
