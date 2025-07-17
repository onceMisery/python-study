// 伪代码/原型：实际项目建议用React+ReactFlow构建
window.onload = function() {
    // 这里应由React渲染FlowEditor组件
    document.getElementById('root').innerHTML = '<div style="padding:24px;color:#888;">[ReactFlow 审批流设计器将在此渲染]</div>';
};

function exportDSL() {
    // 获取当前DSL（伪代码）
    const dsl = window.currentDSL || { nodes: [], edges: [] };
    const blob = new Blob([JSON.stringify(dsl, null, 2)], {type: 'application/json'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'flow.json';
    a.click();
    URL.revokeObjectURL(url);
}

function importDSL(event) {
    const file = event.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = function(e) {
        try {
            const dsl = JSON.parse(e.target.result);
            window.currentDSL = dsl;
            alert('DSL导入成功！（实际应刷新ReactFlow视图）');
        } catch (err) {
            alert('DSL格式错误');
        }
    };
    reader.readAsText(file);
}

function showMermaid() {
    // 伪代码：实际应将DSL转为Mermaid字符串
    const mermaidStr = `graph TD\nstart-->risk_eval_1\nrisk_eval_1-->branch_1\nbranch_1--高-->approve_manager\nbranch_1--中-->approve_finance\nbranch_1--低-->approve_auto\napprove_manager-->end\napprove_finance-->end\napprove_auto-->end`;
    const preview = document.getElementById('mermaid-preview');
    preview.style.display = 'block';
    preview.innerHTML = `<div class='mermaid'>${mermaidStr}</div>`;
    if(window.mermaid) window.mermaid.init(undefined, preview);
} 