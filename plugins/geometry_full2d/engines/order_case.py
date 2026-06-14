from plugins.geometry_full2d.engine_contracts import EngineInputFull2D, EngineOutputFull2D, ResourceBudget, RunContext, diagnostic_output

ENGINE_ROLE = "order_case"


def run(engine_input: EngineInputFull2D, budget: ResourceBudget, context: RunContext) -> EngineOutputFull2D:
    return diagnostic_output(ENGINE_ROLE, engine_input, budget, context)
