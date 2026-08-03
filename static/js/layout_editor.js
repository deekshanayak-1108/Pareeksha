document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('preview-grid')) {
        generateLayoutPreview();
    }
});

function generateLayoutPreview() {
    const rows = parseInt(document.getElementById('rows').value) || 6;
    const cols = parseInt(document.getElementById('cols').value) || 6;
    const walkwayCol = parseInt(document.getElementById('walkway-col').value) || 0;
    const doorPos = document.getElementById('door-pos').value;
    const blackboardPos = document.getElementById('blackboard-pos').value;
    
    const grid = document.getElementById('preview-grid');
    grid.style.gridTemplateColumns = `repeat(${cols}, minmax(40px, 1fr))`;
    grid.innerHTML = '';
    
    // Position Blackboard
    const blackboard = document.getElementById('preview-blackboard');
    if (blackboardPos === 'bottom') {
        blackboard.parentNode.appendChild(blackboard); // Move to bottom
    } else {
        blackboard.parentNode.insertBefore(blackboard, grid); // Move to top
    }
    
    // Position Door relative to bottom/top
    const door = document.getElementById('preview-door');
    door.style.bottom = '';
    door.style.top = '';
    door.style.left = '';
    door.style.right = '';
    
    if (doorPos === 'bottom-right') {
        door.style.bottom = '10px';
        door.style.right = '10px';
    } else if (doorPos === 'bottom-left') {
        door.style.bottom = '10px';
        door.style.left = '10px';
    } else if (doorPos === 'top-right') {
        door.style.top = '10px';
        door.style.right = '10px';
    } else if (doorPos === 'top-left') {
        door.style.top = '10px';
        door.style.left = '10px';
    }
    
    // Generate Cells
    for (let r = 1; r <= rows; r++) {
        for (let c = 1; c <= cols; c++) {
            const cell = document.createElement('div');
            cell.className = 'border rounded text-center py-2 text-white';
            cell.style.fontSize = '12px';
            
            if (walkwayCol > 0 && c === walkwayCol) {
                cell.className += ' walkway-cell';
                cell.innerText = 'W';
                cell.style.background = '#1e293b';
            } else {
                cell.className += ' bg-primary border-primary';
                cell.innerText = `R${r}-C${c}`;
            }
            grid.appendChild(cell);
        }
    }
}

function saveLayout() {
    alert('Layout configuration saved successfully!');
}

function resetLayout() {
    document.getElementById('rows').value = 6;
    document.getElementById('cols').value = 6;
    document.getElementById('walkway-col').value = 3;
    document.getElementById('door-pos').value = 'bottom-right';
    document.getElementById('blackboard-pos').value = 'top';
    generateLayoutPreview();
}
