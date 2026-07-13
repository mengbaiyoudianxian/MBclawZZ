from self_select_router.capability_profile import AgentProfile


class AgentRegistry:

    def __init__(self):

        self.agents = {}

        self._init_default()

    def _init_default(self):

        self.agents["claude"] = AgentProfile(
            name="claude",
            strengths=["reasoning", "coding", "architecture"],
            cost_level=0.8,
            speed=0.6,
            reliability=0.95,
            tool_stack=["claude_code", "tool_exec"]
        )

        self.agents["deepseek"] = AgentProfile(
            name="deepseek",
            strengths=["general", "coding", "search_reasoning"],
            cost_level=0.3,
            speed=0.9,
            reliability=0.8,
            tool_stack=["code_exec"]
        )

        self.agents["xiaomi_mimo"] = AgentProfile(
            name="mimo",
            strengths=["fast_ops", "automation", "light_tasks"],
            cost_level=0.1,
            speed=0.95,
            reliability=0.6,
            tool_stack=["mobile_control"]
        )

        self.agents["doubao"] = AgentProfile(
            name="doubao",
            strengths=["ui", "image", "vision"],
            cost_level=0.4,
            speed=0.8,
            reliability=0.75,
            tool_stack=["image_gen", "vision_api"]
        )
