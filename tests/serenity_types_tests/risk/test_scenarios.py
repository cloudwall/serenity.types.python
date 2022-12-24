from datetime import date, datetime
from uuid import uuid4

from serenity_types.portfolio.core import AssetPosition, SimplePortfolio
from serenity_types.pricing.core import PricingContext, MarkTime
from serenity_types.risk.scenarios import (AssetPnL, FactorPnL, PnL, RunStatus, ScenarioCloneRequest,
                                           ScenarioDefinition, ScenarioRequest, ScenarioResult,
                                           ScenarioRun, ScenarioSource, Shock, ShockPnL, ShockTo)


def test_roundtrip_objects():
    # clone request
    request = ScenarioCloneRequest(scenario_id=uuid4(), scenario_name='Test')
    raw_json = request.json()
    request_out = ScenarioCloneRequest.parse_raw(raw_json)
    assert request.scenario_name == request_out.scenario_name

    # scenario definition
    asset_id = str(uuid4())
    shock = Shock(shock_id=uuid4(), target=asset_id, target_type=ShockTo.ASSET, magnitude=-10.0)
    definition = ScenarioDefinition(scenario_id=uuid4(), source=ScenarioSource.CUSTOM, name='Test',
                                    shocks=[shock])
    raw_json = definition.json()
    definition_out = ScenarioDefinition.parse_raw(raw_json)
    assert definition.shocks[0].shock_id == definition_out.shocks[0].shock_id

    # scenario request
    position = AssetPosition(asset_id=uuid4(), quantity=1)
    portfolio = SimplePortfolio(portfolio_id=uuid4(), base_currency_id=uuid4(),
                                portfolio_name='Test PF', portfolio_manager='Brooklyn Simone',
                                positions=[position])
    ctx = PricingContext(mark_time=MarkTime.LN_EOD)
    request = ScenarioRequest(scenario=definition, portfolio=portfolio, pricing_context=ctx,
                              model_config_id=uuid4(), start_date=date.today(), end_date=date.today())

    # scenario run
    run = ScenarioRun(run_id=uuid4(), status=RunStatus.COMPLETED, scenario_request=request, base_pnl=-100.0,
                      total_shock_pnl=-10000.0, start_datetime=datetime.now(), end_datetime=datetime.now())
    run_out = ScenarioRun.parse_raw(run.json())
    assert run_out.status == run.status

    # scenario result
    shock_pnl = ShockPnL(shock_id=uuid4(), shock_pnl=-5.0)
    pnl = PnL(base_pnl=-10.0, total_shock_pnl=-1000.0, pnl_by_shock=[shock_pnl])
    asset_pnl = AssetPnL(asset_id=uuid4(), sector_levels=['A', 'B', 'C'], asset_pnl=pnl)
    factor_pnl = FactorPnL(factor='beta', factor_exposure_base_ccy=250000, factor_pnl=pnl)
    result = ScenarioResult(portfolio_pnl=pnl, asset_pnl=[asset_pnl], factor_pnl=[factor_pnl])
    result_out = ScenarioResult.parse_raw(result.json())
    assert result_out.portfolio_pnl.base_pnl == result.portfolio_pnl.base_pnl
