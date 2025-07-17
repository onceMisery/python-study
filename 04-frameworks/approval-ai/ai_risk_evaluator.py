import os
from typing import Dict, Any

# 假设有DeepSeek LLM的API调用工具包（可根据实际SDK替换）
# from deepseek_sdk import DeepSeekLLM

class AIRiskEvaluator:
    """
    AI风险评估器，默认调用DeepSeek大模型。
    输入业务上下文，输出风险等级、推荐路径和建议。
    """
    def __init__(self, llm_provider: str = "deepseek", api_key_env: str = "DEEPSEEK_API_KEY"):
        self.llm_provider = llm_provider
        self.api_key = os.getenv(api_key_env, "test-api-key")
        # self.llm = DeepSeekLLM(api_key=self.api_key)  # 伪代码

    def build_prompt(self, context: Dict[str, Any]) -> str:
        """
        构建风险评估Prompt，适配费用报销等场景。
        """
        prompt = f"""
你是一名企业智能审批助手，请根据如下信息进行风险评估：
- 报销金额：{context.get('amount')}
- 紧急程度：{context.get('urgency')}
- 申请人历史：{context.get('applicant_history')}
请判断风险等级（高/中/低），推荐审批路径，并给出简要建议。
输出格式：
风险等级: <高/中/低>\n推荐路径: <审批节点>\n建议: <简要说明>
"""
        return prompt

    def call_llm(self, prompt: str) -> str:
        """
        调用DeepSeek大模型API，返回原始文本结果。
        这里用伪代码模拟，实际可用requests或SDK实现。
        """
        # result = self.llm.chat(prompt)
        # return result['content']
        # --- 模拟返回 ---
        if "金额" in prompt and "12000" in prompt:
            return "风险等级: 高\n推荐路径: 经理审批\n建议: 建议经理重点关注，金额较大且申请人有违规历史。"
        else:
            return "风险等级: 低\n推荐路径: 自动通过\n建议: 金额较小，历史正常，可自动通过。"

    def parse_result(self, llm_output: str) -> Dict[str, str]:
        """
        解析大模型输出，提取风险等级、推荐路径和建议。
        """
        result = {"risk": "", "recommend_path": "", "suggestion": ""}
        for line in llm_output.split("\n"):
            if line.startswith("风险等级"):
                result["risk"] = line.split(":")[-1].strip()
            elif line.startswith("推荐路径"):
                result["recommend_path"] = line.split(":")[-1].strip()
            elif line.startswith("建议"):
                result["suggestion"] = line.split(":")[-1].strip()
        return result

    def evaluate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        综合评估入口，返回完整评估结果。
        """
        prompt = self.build_prompt(context)
        llm_output = self.call_llm(prompt)
        parsed = self.parse_result(llm_output)
        return {
            "llm_provider": self.llm_provider,
            **context,
            **parsed
        }

# 示例用法
if __name__ == "__main__":
    evaluator = AIRiskEvaluator()
    context = {
        "amount": 12000,
        "urgency": "高",
        "applicant_history": "有一次违规记录"
    }
    result = evaluator.evaluate(context)
    print("AI风险评估结果：", result) 