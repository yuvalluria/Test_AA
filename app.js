// Intelligence Evaluations App
let evaluationsData = null;
let filteredModels = null;

// Load data on page load
document.addEventListener('DOMContentLoaded', () => {
    loadData();
    setupEventListeners();
});

function setupEventListeners() {
    document.getElementById('refreshBtn').addEventListener('click', loadData);
    document.getElementById('searchInput').addEventListener('input', handleSearch);
}

async function loadData() {
    try {
        // Try to fetch from API first, then fallback to local JSON
        const response = await fetch('evaluations_data.json');
        if (!response.ok) {
            throw new Error('Failed to load data');
        }
        evaluationsData = await response.json();
        filteredModels = evaluationsData.models;
        renderTable();
        updateStats();
        renderBenchmarks();
    } catch (error) {
        console.error('Error loading data:', error);
        document.getElementById('tableBody').innerHTML = 
            '<tr><td colspan="100%" class="loading">Error loading data. Please run data_fetcher.py first.</td></tr>';
    }
}

function renderBenchmarks() {
    const benchmarkList = document.getElementById('benchmarkList');
    if (!evaluationsData || !evaluationsData.benchmarks) return;

    benchmarkList.innerHTML = evaluationsData.benchmarks
        .map(benchmark => 
            `<span class="benchmark-tag" title="${benchmark.full_name || benchmark.description || ''}">
                ${benchmark.name}
            </span>`
        ).join('');
}

function renderTable() {
    if (!evaluationsData || !filteredModels) return;

    const tableBody = document.getElementById('tableBody');
    const benchmarkHeaders = document.getElementById('benchmarkHeaders');
    const benchmarks = evaluationsData.benchmarks || [];

    // Render benchmark headers
    benchmarkHeaders.innerHTML = benchmarks
        .map(benchmark => `<th>${benchmark.name}</th>`)
        .join('');

    // Render model rows
    if (filteredModels.length === 0) {
        tableBody.innerHTML = '<tr><td colspan="100%" class="loading">No models found matching your search.</td></tr>';
        return;
    }

    tableBody.innerHTML = filteredModels.map(model => {
        const scores = model.scores || {};
        const scoreCells = benchmarks.map(benchmark => {
            const score = scores[benchmark.id];
            return renderScoreCell(score);
        }).join('');

        return `
            <tr>
                <td class="sticky-col">
                    <div class="model-name">${model.name}</div>
                    ${model.provider ? `<div class="model-provider">${model.provider}</div>` : ''}
                    ${model.dataset ? `<div class="model-dataset">${model.dataset}</div>` : ''}
                </td>
                ${scoreCells}
            </tr>
        `;
    }).join('');
}

function renderScoreCell(score) {
    if (score === null || score === undefined) {
        return '<td class="score-cell"><span class="score-value score-na">N/A</span></td>';
    }

    const scoreClass = score >= 0.8 ? 'score-high' : score >= 0.6 ? 'score-medium' : 'score-low';
    const formattedScore = (score * 100).toFixed(1) + '%';
    
    return `<td class="score-cell"><span class="score-value ${scoreClass}">${formattedScore}</span></td>`;
}

function handleSearch(event) {
    const searchTerm = event.target.value.toLowerCase().trim();
    
    if (!evaluationsData || !evaluationsData.models) return;

    if (searchTerm === '') {
        filteredModels = evaluationsData.models;
    } else {
        filteredModels = evaluationsData.models.filter(model => {
            const nameMatch = model.name.toLowerCase().includes(searchTerm);
            const providerMatch = model.provider && model.provider.toLowerCase().includes(searchTerm);
            const datasetMatch = model.dataset && model.dataset.toLowerCase().includes(searchTerm);
            const idMatch = model.id.toLowerCase().includes(searchTerm);
            return nameMatch || providerMatch || datasetMatch || idMatch;
        });
    }

    renderTable();
    updateStats();
}

function updateStats() {
    const totalModels = filteredModels ? filteredModels.length : 0;
    const totalBenchmarks = evaluationsData && evaluationsData.benchmarks ? evaluationsData.benchmarks.length : 0;

    document.getElementById('totalModels').textContent = totalModels;
    document.getElementById('totalBenchmarks').textContent = totalBenchmarks;
}

