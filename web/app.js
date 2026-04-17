const { createApp, ref, computed, onMounted, watch } = Vue;

const API_BASE = '/api';

const app = createApp({
    setup() {
        const currentTab = ref('search');
        const searchQuery = ref('');
        const filterStatus = ref('active');
        const records = ref([]);
        const loading = ref(true);
        const selectedReviewId = ref(null);
        const selectedRecord = ref(null);

        // Fetch index on load
        const fetchIndex = async () => {
            loading.value = true;
            try {
                const res = await fetch(`${API_BASE}/index`);
                if (res.ok) {
                    records.value = await res.json();
                    renderCharts();
                } else {
                    console.error("Failed to load index");
                }
            } catch (e) {
                console.error(e);
            } finally {
                loading.value = false;
            }
        };

        // Filter logic
        const filteredRecords = computed(() => {
            let result = records.value;
            
            if (filterStatus.value !== 'all') {
                result = result.filter(r => r.status === filterStatus.value);
            }
            
            if (searchQuery.value.trim()) {
                const q = searchQuery.value.toLowerCase();
                result = result.filter(r => 
                    (r.task_type || '').toLowerCase().includes(q) ||
                    (r.conclusions || []).some(c => c.toLowerCase().includes(q)) ||
                    (r.action_items || []).some(a => a.toLowerCase().includes(q))
                );
            }
            
            return result;
        });

        // Load detail
        const selectRecord = async (id) => {
            selectedReviewId.value = id;
            try {
                const res = await fetch(`${API_BASE}/reviews/${id}`);
                if (res.ok) {
                    selectedRecord.value = await res.json();
                }
            } catch (e) {
                console.error(e);
            }
        };

        // Format Date
        const formatDate = (isoString) => {
            if (!isoString) return 'Unknown Date';
            const date = new Date(isoString);
            return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
        };

        // Archive
        const archiveRecord = async () => {
            if (!selectedRecord.value) return;
            if (!confirm("Are you sure you want to archive this record?")) return;
            
            try {
                const res = await fetch(`${API_BASE}/reviews/${selectedRecord.value.review_id}/archive`, {
                    method: 'POST'
                });
                if (res.ok) {
                    selectedRecord.value.status = 'archived';
                    // Update list
                    const item = records.value.find(r => r.review_id === selectedRecord.value.review_id);
                    if (item) item.status = 'archived';
                }
            } catch (e) {
                console.error("Failed to archive:", e);
            }
        };

        // Add item
        const addListItem = async (field, value) => {
            if (!selectedRecord.value) return;
            
            try {
                const res = await fetch(`${API_BASE}/reviews/${selectedRecord.value.review_id}/update`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ field, value, append: true })
                });
                if (res.ok) {
                    if (!selectedRecord.value[field]) {
                        selectedRecord.value[field] = [];
                    }
                    selectedRecord.value[field].push(value);
                } else {
                    alert("Failed to update record.");
                }
            } catch (e) {
                console.error("Failed to update:", e);
                alert("Network error.");
            }
        };

        // Charts
        const renderCharts = () => {
            if (!document.getElementById('chart-pie') || !document.getElementById('chart-line')) return;
            
            // Pie Chart (Task Types)
            const typeCounts = {};
            records.value.forEach(r => {
                const type = r.task_type || 'Unknown';
                typeCounts[type] = (typeCounts[type] || 0) + 1;
            });
            
            const pieData = Object.entries(typeCounts).map(([name, value]) => ({name, value}));
            const pieChart = echarts.init(document.getElementById('chart-pie'));
            pieChart.setOption({
                tooltip: { trigger: 'item' },
                series: [{
                    type: 'pie',
                    radius: ['40%', '70%'],
                    itemStyle: { borderRadius: 5, borderColor: '#fff', borderWidth: 2 },
                    data: pieData,
                    label: { show: false }
                }]
            });

            // Line Chart (Timeline - by month)
            const timeCounts = {};
            records.value.forEach(r => {
                if (r.timestamp) {
                    const month = r.timestamp.substring(0, 7); // YYYY-MM
                    timeCounts[month] = (timeCounts[month] || 0) + 1;
                }
            });
            const sortedMonths = Object.keys(timeCounts).sort();
            const lineData = sortedMonths.map(m => timeCounts[m]);
            
            const lineChart = echarts.init(document.getElementById('chart-line'));
            lineChart.setOption({
                tooltip: { trigger: 'axis' },
                xAxis: { type: 'category', data: sortedMonths },
                yAxis: { type: 'value', minInterval: 1 },
                series: [{
                    data: lineData,
                    type: 'bar',
                    smooth: true,
                    itemStyle: { color: '#6366f1' },
                    areaStyle: {
                        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                            { offset: 0, color: 'rgba(99, 102, 241, 0.5)' },
                            { offset: 1, color: 'rgba(99, 102, 241, 0.1)' }
                        ])
                    }
                }]
            });
            
            window.addEventListener('resize', () => {
                pieChart.resize();
                lineChart.resize();
            });
        };

        watch(currentTab, (newTab) => {
            if (newTab === 'analytics') {
                setTimeout(renderCharts, 100);
            }
        });

        onMounted(() => {
            fetchIndex();
        });

        return {
            currentTab, searchQuery, filterStatus, records, filteredRecords, loading,
            selectedReviewId, selectedRecord, selectRecord, formatDate, archiveRecord, addListItem
        };
    }
});

// Component for detail sections
app.component('DetailSection', {
    template: '#detail-section-template',
    props: ['title', 'icon', 'items', 'field', 'archived'],
    emits: ['add'],
    setup(props, { emit }) {
        const newValue = ref('');
        const isSubmitting = ref(false);

        const submit = async () => {
            if (!newValue.value.trim() || isSubmitting.value) return;
            isSubmitting.value = true;
            await emit('add', props.field, newValue.value.trim());
            newValue.value = '';
            isSubmitting.value = false;
        };

        return { newValue, isSubmitting, submit };
    }
});

app.mount('#app');