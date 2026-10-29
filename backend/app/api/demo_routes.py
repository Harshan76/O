from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
from app.db.scenarios import DEMO_SCENARIOS, load_scenario

router = APIRouter(tags=["Demonstration Scenarios"])

@router.get("/demo/scenarios")
def list_demo_scenarios():
    """Lists all 10 reproducible demonstration scenarios for evaluators & judges."""
    scenarios_list = []
    for s_id, s in DEMO_SCENARIOS.items():
        scenarios_list.append({
            "id": s["id"],
            "title": s["title"],
            "learner_name": s["learner_name"],
            "email": s["email"],
            "goal_title": s["goal_title"],
            "domain": s["domain"],
            "experience_level": s["experience_level"],
            "overall_mastery": s["overall_mastery"],
            "description": s["description"],
            "is_simulated": True
        })
    return sorted(scenarios_list, key=lambda x: int(x["id"]))

@router.get("/demo/scenarios/{scenario_id}")
def get_scenario_detail(scenario_id: str):
    if scenario_id not in DEMO_SCENARIOS:
        raise HTTPException(status_code=404, detail="Scenario not found")
    return DEMO_SCENARIOS[scenario_id]

@router.post("/demo/scenarios/{scenario_id}/switch")
def switch_active_scenario(scenario_id: str):
    """Loads and sets the specified scenario as active in the database."""
    if scenario_id not in DEMO_SCENARIOS:
        raise HTTPException(status_code=404, detail="Scenario not found")
    active_scenario = load_scenario(scenario_id)
    return {
        "status": "success",
        "message": f"Switched to Scenario {scenario_id}: {active_scenario['title']}",
        "scenario": active_scenario,
        "learner_id": f"demo-learner-{scenario_id}"
    }
