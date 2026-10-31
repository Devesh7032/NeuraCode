import json
from typing import Dict, Any
from app.services.ai_tutor.base import BaseAIProvider

class FallbackProvider(BaseAIProvider):
    async def generate_response(self, system_instruction: str, user_prompt: str, context: Dict[str, Any]) -> str:
        """
        Generates a context-driven intelligent tutor response using challenge metadata,
        user code analysis, execution diagnostic output, and visualization trace data.
        """
        action = context.get("action_type", "CHAT")
        challenge = context.get("challenge", {})
        title = challenge.get("title", "this challenge")
        slug = challenge.get("slug", "")
        code = context.get("user_code", "")
        sub = context.get("latest_submission")
        vis = context.get("visualization")
        missing_prereqs = context.get("missing_prerequisites", [])

        # Check missing prerequisites warning
        prereq_note = ""
        if missing_prereqs:
            prereq_note = f"\n\n> 💡 **Prerequisite Tip**: You have not yet completed `{missing_prereqs[0]}`. Reviewing it first will help solidify the core concepts needed here."

        if action == "EXPLAIN_CONCEPT":
            concept = challenge.get("concept", "")
            desc = challenge.get("description", "")
            return (
                f"### 📖 Conceptual Overview: {title}\n\n"
                f"{desc}\n\n"
                f"**Mathematical Intuition**:\n{concept if concept else 'This challenge evaluates fundamental tensor/array transformations.'}\n\n"
                f"**Key Steps**:\n"
                f"1. Identify input argument shapes and numerical types.\n"
                f"2. Apply vectorized array operations (e.g. NumPy or core math operations).\n"
                f"3. Return outputs strictly matching expected output data structures.{prereq_note}"
            )

        elif action == "EXPLAIN_CODE":
            code_lines = [line for line in code.split("\n") if line.strip() and not line.strip().startswith("#")]
            num_lines = len(code_lines)
            return (
                f"### 🔍 Code Walkthrough ({title})\n\n"
                f"Here is an analysis of your current solution implementation:\n\n"
                f"```python\n{code}\n```\n\n"
                f"**Structure Analysis**:\n"
                f"- Your implementation consists of **{num_lines} lines** of Python code.\n"
                f"- Function signature target: `{challenge.get('subcategory', 'Function')}` implementation.\n\n"
                f"**Key Implementation Detail**:\n"
                f"Make sure all mathematical operations maintain float precision and return standard Python numeric/list types rather than un-converted temporary wrappers."
            )

        elif action == "GIVE_HINT":
            level = context.get("hint_level", 1)
            if level == 1:
                return (
                    f"### 💡 Hint Level 1 (Conceptual Direction)\n\n"
                    f"Focus on the underlying mathematical formula for **{title}**:\n\n"
                    f"Check input dimensions and ensure you apply the formula step-by-step."
                )
            elif level == 2:
                return (
                    f"### 💡 Hint Level 2 (Specific Guidance)\n\n"
                    f"For **{title}**, check your variable order and mathematical operators:\n\n"
                    f"- Are you applying operations in the correct sequence?\n"
                    f"- Verify float division vs integer truncation."
                )
            elif level == 3:
                return (
                    f"### 💡 Hint Level 3 (Algorithmic Pseudocode)\n\n"
                    f"1. Convert input parameters to arrays if using NumPy.\n"
                    f"2. Compute intermediate dot products or mathematical transformations.\n"
                    f"3. Return the result formatted as expected by test assertions."
                )
            else:
                return (
                    f"### 💡 Hint Level 4 (Near-Solution Guidance)\n\n"
                    f"Review the starter signature:\n```python\n{challenge.get('starter_code', '')}\n```\n"
                    f"Ensure you compute the operation without mutating external parameters."
                )

        elif action == "EXPLAIN_ERROR":
            if sub and sub.get("status") in ["RUNTIME_ERROR", "COMPILATION_ERROR", "WRONG_ANSWER"]:
                stderr = sub.get("stderr", "")
                results = sub.get("results", [])
                failed_res = [r for r in results if r.get("status") != "passed"]
                
                err_detail = ""
                if stderr:
                    err_detail = f"**Execution Diagnostic**:\n```text\n{stderr}\n```\n"
                elif failed_res:
                    first_fail = failed_res[0]
                    err_detail = (
                        f"**Failed Test Outcome**:\n"
                        f"- Received: `{first_fail.get('actual_output')}`\n"
                        f"- Error info: `{first_fail.get('error_message')}`\n"
                    )

                return (
                    f"### ⚠️ Execution Error Analysis ({title})\n\n"
                    f"Your code did not pass validation tests.\n\n"
                    f"{err_detail}\n"
                    f"**Suggested Fix**:\n"
                    f"1. Verify input argument types and bounds.\n"
                    f"2. Check for sign errors, matrix dimension mismatches, or missing return statements."
                )
            else:
                return (
                    f"### ⚠️ Diagnostic Check\n\n"
                    f"No active runtime crash recorded. Run your solution using the **Run** button to generate empirical test reports."
                )

        elif action == "EXPLAIN_GRAPH":
            if vis:
                vis_type = vis.get("type", "UNKNOWN")
                if vis_type == "GRADIENT_DESCENT":
                    steps = vis.get("steps", [])
                    step0 = steps[0] if steps else {}
                    w_val = step0.get("weight", 0.0)
                    dw_val = step0.get("derivative", 0.0)
                    lr = vis.get("learning_rate", 0.1)
                    w_new = step0.get("w_new", w_val - lr * dw_val)
                    return (
                        f"### 📊 Gradient Descent Visualization Explanation\n\n"
                        f"This visualization represents the parameter trajectory update:\n\n"
                        f"- **Current Parameter ($w$)**: `{w_val:.4f}`\n"
                        f"- **Gradient ($dw$)**: `{dw_val:.4f}`\n"
                        f"- **Learning Rate ($\eta$)**: `{lr:.4f}`\n"
                        f"- **Updated Parameter ($w_{{new}}$)**: `{w_new:.4f}`\n\n"
                        f"**Update Formula**:\n"
                        f"$$w_{{new}} = w - \eta \\cdot dw$$\n\n"
                        f"Because the derivative $dw$ reflects loss steepness, subtracting $\eta \\cdot dw$ steps parameter $w$ toward the minimum loss."
                    )
                elif vis_type == "FUNCTION":
                    return (
                        f"### 📊 Activation Curve Explanation\n\n"
                        f"The curve shows output $y = f(x)$ across coordinate inputs. The highlighted point shows your function's response for input $x = {vis.get('custom_x')}$, producing output $y = {vis.get('custom_y')}$."
                    )
                elif vis_type == "MATRIX_MULTIPLICATION":
                    return (
                        f"### 📊 Matrix Multiplication Explanation\n\n"
                        f"Matrix $C = A \\times B$. Each cell $C[i, j]$ is calculated as the dot product between Row $i$ of Matrix $A$ and Column $j$ of Matrix $B$."
                    )
                elif vis_type == "VECTOR":
                    return (
                        f"### 📊 Vector L2 Normalization Explanation\n\n"
                        f"Original vector magnitude is `{vis.get('magnitude', 0.0):.4f}`. The normalized vector scales magnitude to exactly $1.0$ while preserving directional unit angle."
                    )
                else:
                    return (
                        f"### 📊 Visual Trace Trace Explanation\n\n"
                        f"Visualization Type: `{vis_type}`. Trace contains real sandbox execution data derived from running your implementation."
                    )
            else:
                return (
                    f"### 📊 Visualization Trace\n\n"
                    f"Click **Run** to execute your code and generate a real-time trace representation in the **Visual Experiment** tab."
                )

        elif action == "NEXT_RECOMMENDATION":
            next_ch = context.get("next_challenge")
            if next_ch:
                return (
                    f"### 🎯 Next Recommended Challenge\n\n"
                    f"Great job mastering **{title}**!\n\n"
                    f"Based on your Learning Path progression, your next recommended challenge is:\n\n"
                    f"👉 **[{next_ch.get('title')}](/problems/{next_ch.get('slug')})**"
                )
            else:
                return (
                    f"### 🎯 Milestone Complete!\n\n"
                    f"You have completed all challenges in this Learning Path module! Explore the **Challenges** menu for advanced AI topics."
                )

        else:
            # Natural Chat response
            prompt_lower = (user_prompt or "").lower()
            if "hint" in prompt_lower:
                return (
                    f"### 💡 Hint\n\n"
                    f"Review the mathematical formula in the **Concept** tab for **{title}** and check your return data type."
                )
            elif "wrong" in prompt_lower or "fail" in prompt_lower or "error" in prompt_lower:
                return (
                    f"### ⚠️ Debugging Advice\n\n"
                    f"Check for sign errors or list shape mismatches in `{title}`. Click **[ ⚠️ Explain Error ]** for a detailed test failure diagnosis."
                )
            elif "graph" in prompt_lower or "visualization" in prompt_lower:
                return (
                    f"### 📊 Graph Insights\n\n"
                    f"Run your code to generate execution traces, then inspect parameter shifts under the **Visual Experiment** tab."
                )
            else:
                return (
                    f"### 🤖 AI Tutor: {title}\n\n"
                    f"I am ready to help you master **{title}**!\n\n"
                    f"- Use **[ 📖 Explain Concept ]** to review the intuition.\n"
                    f"- Use **[ 💡 Give Hint ]** for progressive problem solving.\n"
                    f"- Use **[ 🔍 Explain Code ]** to analyze your implementation."
                )
