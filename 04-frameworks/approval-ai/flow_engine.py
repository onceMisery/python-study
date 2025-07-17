import json
import os
from typing import Dict, Any, List
from ai_risk_evaluator import AIRiskEvaluator

class FlowEngine:
    """
    审批流引擎：解析flow.json，自动执行risk_eval节点，支持AI智能分流。
    """
    def __init__(self, flow_path: str = None, risk_result_path: str = None):
        self.flow_path = flow_path or os.path.join(os.path.dirname(__file__), 'data', 'flow.json')
        self.risk_result_path = risk_result_path or os.path.join(os.path.dirname(__file__), 'data', 'risk_result.json')
        self.flow = self.load_flow()
        self.risk_evaluator = AIRiskEvaluator()
        self.risk_results = self.load_risk_results()

    def load_flow(self) -> Dict[str, Any]:
        with open(self.flow_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def load_risk_results(self) -> List[Dict[str, Any]]:
        if os.path.exists(self.risk_result_path):
            with open(self.risk_result_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def save_risk_result(self, result: Dict[str, Any]):
        self.risk_results.append(result)
        with open(self.risk_result_path, 'w', encoding='utf-8') as f:
            json.dump(self.risk_results, f, ensure_ascii=False, indent=2)

    def run(self, instance_id: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行审批流主流程。
        :param instance_id: 流程实例ID
        :param context: 业务上下文（如amount, urgency等）
        :return: 最终审批结果与AI分流建议
        """
        node_map = {node['id']: node for node in self.flow['nodes']}
        current_node = node_map.get('start')
        result_trace = []
        ai_risk_result = None
        while current_node:
            node_type = current_node['type']
            node_id = current_node['id']
            result_trace.append({"node_id": node_id, "type": node_type})
            if node_type == 'risk_eval':
                # 调用AI风险评估
                ai_risk_result = self.risk_evaluator.evaluate(context)
                ai_risk_result.update({
                    "instance_id": instance_id,
                    "flow_id": self.flow['flow_id'],
                    "node_id": node_id
                })
                self.save_risk_result(ai_risk_result)
                # 将AI结果写入context，供后续分支判断
                context['risk'] = ai_risk_result['risk']
                context['recommend_path'] = ai_risk_result['recommend_path']
                context['suggestion'] = ai_risk_result['suggestion']
                next_node_id = current_node.get('next')
            elif node_type == 'branch':
                # 根据AI风险等级分流
                next_node_id = None
                for branch in current_node['branches']:
                    # 仅支持简单表达式 risk == '高' 等
                    cond = branch['condition']
                    if eval(cond, {}, context):
                        next_node_id = branch['next']
                        break
                if not next_node_id:
                    raise Exception(f"No branch matched for node {node_id} with context {context}")
            elif node_type in ('approve', 'start'):
                next_node_id = current_node.get('next')
            elif node_type == 'end':
                break
            else:
                raise Exception(f"Unknown node type: {node_type}")
            current_node = node_map.get(next_node_id) if next_node_id else None
        return {
            "instance_id": instance_id,
            "trace": result_trace,
            "ai_risk_result": ai_risk_result,
            "final_node": current_node['id'] if current_node else None,
            "final_approver": context.get('recommend_path'),
            "ai_suggestion": context.get('suggestion')
        }

# 示例用法
if __name__ == "__main__":
    engine = FlowEngine()
    context = {
        "amount": 12000,
        "urgency": "高",
        "applicant_history": "有一次违规记录"
    }
    result = engine.run(instance_id="exp20240601-003", context=context)
    print("审批流执行结果：", json.dumps(result, ensure_ascii=False, indent=2)) 