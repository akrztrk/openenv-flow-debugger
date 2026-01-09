import re
from flow_debugger_env.env import FlowDebugEnv

def rule_based_agent(obs):
    condition_step = next(s for s in obs["steps"] if s["name"] == "Condition_Check")
    expr = condition_step["inputs"]["expression"]

    fixed = expr
    fixed = fixed.replace("@equal(", "@equals(")
    fixed = re.sub(r",\s*xlsx\s*\)", r",'xlsx')", fixed)
    fixed = re.sub(r"\)\s*'xlsx'\s*\)", r"),'xlsx')", fixed)

    if fixed.count("(") > fixed.count(")"):
        fixed = fixed + (")" * (fixed.count("(") - fixed.count(")")))

    while fixed.endswith("))") and fixed.count(")") > fixed.count("("):
        fixed = fixed[:-1]

    return {
        "action": "patch_step",
        "step": "Condition_Check",
        "field": "inputs.expression",
        "value": fixed
    }

def main():
    env = FlowDebugEnv.from_json("flow_debugger_env/data/cases.json", max_attempts=3, seed=42)
    obs = env.reset()
    done = False
    total = 0.0

    while not done:
        action = rule_based_agent(obs)
        result = env.step(action)
        obs, reward, done, info = result.obs, result.reward, result.done, result.info
        total += reward

    print("Finished:", info, "total_reward:", total)

if __name__ == "__main__":
    main()
