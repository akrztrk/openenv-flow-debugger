import copy
import json
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional, List


@dataclass
class StepResult:
    obs: Dict[str, Any]
    reward: float
    done: bool
    info: Dict[str, Any]


class FlowDebugEnv:
    """
    This is a simple environment made for OpenEnv.
    Here's what it does:
    - It gives you information in text or JSON.
    - You can only do one thing: fix the 'inputs.expression' in a 'Condition_Check' step.
    - If your fix is exactly right, you win!
    """
    def __init__(self, cases: List[Dict[str, Any]], max_attempts: int = 3, seed: Optional[int] = None):
        self.cases = cases
        self.max_attempts = max_attempts
        self.rng = random.Random(seed)
        self.current_case: Optional[Dict[str, Any]] = None
        self.attempts_left = max_attempts

    @classmethod
    def from_json(cls, cases_json_path: str, max_attempts: int = 3, seed: Optional[int] = None):
        path = Path(cases_json_path)
        with open(path, "r", encoding="utf-8") as f:
            cases = json.load(f)
        return cls(cases=cases, max_attempts=max_attempts, seed=seed)

    def reset(self) -> Dict[str, Any]:
        self.current_case = copy.deepcopy(self.rng.choice(self.cases))
        self.attempts_left = self.max_attempts
        return self._make_observation()

    def step(self, action: Dict[str, Any]) -> StepResult:
        if self.current_case is None:
            raise RuntimeError("Call reset() before step().")

        self.attempts_left -= 1

        if action.get("action") != "patch_step":
            return self._invalid_action("Unsupported action type")

        step_name = action.get("step")
        field = action.get("field")
        value = action.get("value")

        patched_ok = self._apply_patch(step_name, field, value)
        if not patched_ok:
            return self._invalid_action("Patch failed (step/field not found)")

        gold = self.current_case["gold_fix"]
        solved = (step_name == gold["step"] and field == gold["field"] and value == gold["value"])

        if solved:
            self._mark_success()
            obs = self._make_observation(run_status="Succeeded", error=None, failed_step=None)
            return StepResult(obs=obs, reward=1.0, done=True,
                              info={"result": "success", "case_id": self.current_case["case_id"]})

        if self.attempts_left <= 0:
            obs = self._make_observation()
            return StepResult(obs=obs, reward=-0.2, done=True,
                              info={"result": "out_of_attempts", "case_id": self.current_case["case_id"]})

        obs = self._make_observation()
        return StepResult(obs=obs, reward=-0.1, done=False,
                          info={"result": "still_failed", "case_id": self.current_case["case_id"]})

    # --------- helpers ----------
    def _apply_patch(self, step_name: str, field: str, value: str) -> bool:
        for step in self.current_case["steps"]:
            if step["name"] == step_name:
                if field == "inputs.expression":
                    step.setdefault("inputs", {})
                    step["inputs"]["expression"] = value
                    return True
        return False

    def _mark_success(self):
        for step in self.current_case["steps"]:
            step["status"] = "Succeeded"

    def _make_observation(self, run_status="Failed", error="keep", failed_step="keep"):
        if error == "keep":
            err_obj = self.current_case["error"]
        else:
            err_obj = error

        if failed_step == "keep":
            failed = self.current_case["failed_step"]
        else:
            failed = failed_step

        return {
            "case_id": self.current_case["case_id"],
            "run_status": run_status,
            "failed_step": failed,
            "error": err_obj,
            "steps": self.current_case["steps"],
            "attempts_left": self.attempts_left
        }

    def _invalid_action(self, msg: str) -> StepResult:
        obs = self._make_observation()
        done = (self.attempts_left <= 0)
        return StepResult(obs=obs, reward=-0.1, done=done,
                          info={"result": "invalid_action", "message": msg, "case_id": self.current_case["case_id"]})
