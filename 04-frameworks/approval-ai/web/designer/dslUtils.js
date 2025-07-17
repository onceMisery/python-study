/**
 * dslUtils.js - 审批流DSL与ReactFlow数据互转
 *
 * dslToFlow(dsl): flow.json -> { nodes, edges }
 * flowToDsl({nodes, edges}): { nodes, edges } -> flow.json
 */

// DSL -> ReactFlow数据结构
export function dslToFlow(dsl) {
  // 这里只做简单映射，实际需根据DSL结构完善
  if (!dsl || !dsl.nodes) return { nodes: [], edges: [] };
  const nodes = dsl.nodes.map((n, idx) => ({
    id: n.id,
    type: n.type,
    position: { x: 100 + idx * 120, y: 100 },
    data: { ...n }
  }));
  // edges: 通过next/branches生成
  let edges = [];
  dsl.nodes.forEach(n => {
    if (n.next) {
      edges.push({ id: `${n.id}->${n.next}`, source: n.id, target: n.next });
    }
    if (n.branches) {
      n.branches.forEach(b => {
        edges.push({ id: `${n.id}->${b.next}`, source: n.id, target: b.next, label: b.condition });
      });
    }
  });
  return { nodes, edges };
}

// ReactFlow数据结构 -> DSL
export function flowToDsl({ nodes, edges }) {
  // 这里只做简单映射，实际需根据业务完善
  const nodeMap = Object.fromEntries(nodes.map(n => [n.id, n]));
  // 生成DSL节点
  const dslNodes = nodes.map(n => {
    const d = { id: n.id, type: n.type, ...n.data };
    // 处理next/branches
    const outgoing = edges.filter(e => e.source === n.id);
    if (outgoing.length === 1) {
      d.next = outgoing[0].target;
    } else if (outgoing.length > 1) {
      d.branches = outgoing.map(e => ({ condition: e.label || '', next: e.target }));
    }
    return d;
  });
  return { nodes: dslNodes };
}

// API调用示例
export async function fetchCurrentDsl() {
  const res = await fetch('/api/flow_dsl');
  return await res.json();
}

export async function saveCurrentDsl(dsl) {
  const res = await fetch('/api/flow_dsl', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(dsl)
  });
  return await res.json();
} 