/**
 * Hoofdapplicatie voor Tijdregistratie
 */

class TimeTrackerApp {
    constructor() {
        this.timerInterval = null;
        this.timerSeconds = 0;
        this.timerRunning = false;
        this.timerStartTime = null;
        this.currentProjectId = null;
        this.editingProjectId = null;

        this.init();
    }

    init() {
        this.bindElements();
        this.bindEvents();
        this.loadProjects();
        this.loadEntries();
        this.restoreTimer();
        this.setDefaultDate();
    }

    bindElements() {
        // Timer elements
        this.timerDisplay = document.getElementById('timerDisplay');
        this.startTimerBtn = document.getElementById('startTimerBtn');
        this.stopTimerBtn = document.getElementById('stopTimerBtn');
        this.projectSelect = document.getElementById('projectSelect');
        this.taskDescription = document.getElementById('taskDescription');

        // Project elements
        this.projectList = document.getElementById('projectList');
        this.addProjectBtn = document.getElementById('addProjectBtn');
        this.projectModal = document.getElementById('projectModal');
        this.projectForm = document.getElementById('projectForm');
        this.projectModalTitle = document.getElementById('projectModalTitle');
        this.projectName = document.getElementById('projectName');
        this.projectColor = document.getElementById('projectColor');
        this.projectRate = document.getElementById('projectRate');

        // Manual entry elements
        this.manualEntryForm = document.getElementById('manualEntryForm');
        this.manualProject = document.getElementById('manualProject');
        this.manualDate = document.getElementById('manualDate');
        this.manualHours = document.getElementById('manualHours');
        this.manualDescription = document.getElementById('manualDescription');

        // Entries elements
        this.entriesTableBody = document.getElementById('entriesTableBody');
        this.filterProject = document.getElementById('filterProject');
        this.filterPeriod = document.getElementById('filterPeriod');
        this.totalHours = document.getElementById('totalHours');

        // Export
        this.exportBtn = document.getElementById('exportBtn');
    }

    bindEvents() {
        // Timer events
        this.startTimerBtn.addEventListener('click', () => this.startTimer());
        this.stopTimerBtn.addEventListener('click', () => this.stopTimer());

        // Project events
        this.addProjectBtn.addEventListener('click', () => this.openProjectModal());
        this.projectForm.addEventListener('submit', (e) => this.handleProjectSubmit(e));

        // Modal events
        this.projectModal.querySelectorAll('.modal-close, .modal-cancel').forEach(btn => {
            btn.addEventListener('click', () => this.closeProjectModal());
        });
        this.projectModal.addEventListener('click', (e) => {
            if (e.target === this.projectModal) this.closeProjectModal();
        });

        // Manual entry events
        this.manualEntryForm.addEventListener('submit', (e) => this.handleManualEntry(e));

        // Filter events
        this.filterProject.addEventListener('change', () => this.loadEntries());
        this.filterPeriod.addEventListener('change', () => this.loadEntries());

        // Export event
        this.exportBtn.addEventListener('click', () => this.exportToCSV());

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.closeProjectModal();
            }
        });
    }

    // ==================== TIMER ====================

    startTimer() {
        if (!this.projectSelect.value) {
            alert('Selecteer eerst een project');
            return;
        }

        this.timerRunning = true;
        this.timerStartTime = Date.now();
        this.currentProjectId = this.projectSelect.value;

        this.startTimerBtn.disabled = true;
        this.stopTimerBtn.disabled = false;
        this.projectSelect.disabled = true;

        this.timerInterval = setInterval(() => {
            this.timerSeconds = Math.floor((Date.now() - this.timerStartTime) / 1000);
            this.updateTimerDisplay();
        }, 1000);

        // Sla timer state op voor het geval de pagina wordt herladen
        Storage.saveActiveTimer({
            startTime: this.timerStartTime,
            projectId: this.currentProjectId,
            description: this.taskDescription.value
        });
    }

    stopTimer() {
        if (!this.timerRunning) return;

        clearInterval(this.timerInterval);
        this.timerRunning = false;

        const hours = this.timerSeconds / 3600;

        if (hours >= 0.01) { // Minimaal ~30 seconden
            Storage.addEntry({
                projectId: this.currentProjectId,
                date: Utils.getToday(),
                hours: hours.toFixed(2),
                description: this.taskDescription.value,
                source: 'timer'
            });

            this.loadEntries();
            this.loadProjects(); // Update uren in sidebar
        }

        this.resetTimer();
        Storage.clearActiveTimer();
    }

    resetTimer() {
        this.timerSeconds = 0;
        this.timerStartTime = null;
        this.currentProjectId = null;
        this.updateTimerDisplay();

        this.startTimerBtn.disabled = false;
        this.stopTimerBtn.disabled = true;
        this.projectSelect.disabled = false;
        this.taskDescription.value = '';
    }

    updateTimerDisplay() {
        this.timerDisplay.textContent = Utils.formatTime(this.timerSeconds);
    }

    restoreTimer() {
        const savedTimer = Storage.getActiveTimer();
        if (savedTimer && savedTimer.startTime) {
            this.timerStartTime = savedTimer.startTime;
            this.currentProjectId = savedTimer.projectId;
            this.projectSelect.value = savedTimer.projectId;
            this.taskDescription.value = savedTimer.description || '';

            this.timerRunning = true;
            this.startTimerBtn.disabled = true;
            this.stopTimerBtn.disabled = false;
            this.projectSelect.disabled = true;

            this.timerInterval = setInterval(() => {
                this.timerSeconds = Math.floor((Date.now() - this.timerStartTime) / 1000);
                this.updateTimerDisplay();
            }, 1000);
        }
    }

    // ==================== PROJECTEN ====================

    loadProjects() {
        const projects = Storage.getProjects();
        const hoursPerProject = Storage.getHoursPerProject();

        // Update sidebar
        this.projectList.innerHTML = '';
        projects.forEach(project => {
            const hours = hoursPerProject[project.id] || 0;
            const li = document.createElement('li');
            li.className = 'project-item';
            li.dataset.id = project.id;
            li.innerHTML = `
                <span class="project-color" style="background-color: ${project.color}"></span>
                <span class="project-name">${this.escapeHtml(project.name)}</span>
                <span class="project-hours">${hours.toFixed(1)}u</span>
                <div class="project-actions">
                    <button class="project-action-btn edit-project" title="Bewerk">✏️</button>
                    <button class="project-action-btn delete-project" title="Verwijder">🗑️</button>
                </div>
            `;

            li.querySelector('.edit-project').addEventListener('click', (e) => {
                e.stopPropagation();
                this.editProject(project.id);
            });

            li.querySelector('.delete-project').addEventListener('click', (e) => {
                e.stopPropagation();
                this.deleteProject(project.id);
            });

            this.projectList.appendChild(li);
        });

        // Update dropdowns
        const projectOptions = projects.map(p =>
            `<option value="${p.id}">${this.escapeHtml(p.name)}</option>`
        ).join('');

        this.projectSelect.innerHTML = '<option value="">Selecteer project...</option>' + projectOptions;
        this.manualProject.innerHTML = '<option value="">Selecteer project...</option>' + projectOptions;
        this.filterProject.innerHTML = '<option value="">Alle projecten</option>' + projectOptions;

        // Restore selection if timer was running
        if (this.currentProjectId) {
            this.projectSelect.value = this.currentProjectId;
        }
    }

    openProjectModal(projectId = null) {
        this.editingProjectId = projectId;

        if (projectId) {
            const project = Storage.getProject(projectId);
            if (project) {
                this.projectModalTitle.textContent = 'Project bewerken';
                this.projectName.value = project.name;
                this.projectColor.value = project.color;
                this.projectRate.value = project.rate || '';
            }
        } else {
            this.projectModalTitle.textContent = 'Nieuw Project';
            this.projectForm.reset();
            this.projectColor.value = '#3498db';
        }

        this.projectModal.classList.add('active');
        this.projectName.focus();
    }

    closeProjectModal() {
        this.projectModal.classList.remove('active');
        this.editingProjectId = null;
        this.projectForm.reset();
    }

    handleProjectSubmit(e) {
        e.preventDefault();

        const projectData = {
            name: this.projectName.value.trim(),
            color: this.projectColor.value,
            rate: parseFloat(this.projectRate.value) || 0
        };

        if (this.editingProjectId) {
            Storage.updateProject(this.editingProjectId, projectData);
        } else {
            Storage.addProject(projectData);
        }

        this.closeProjectModal();
        this.loadProjects();
        this.loadEntries();
    }

    editProject(projectId) {
        this.openProjectModal(projectId);
    }

    deleteProject(projectId) {
        const project = Storage.getProject(projectId);
        if (project && confirm(`Weet je zeker dat je "${project.name}" wilt verwijderen?\n\nAlle uren voor dit project worden ook verwijderd.`)) {
            Storage.deleteProject(projectId);
            this.loadProjects();
            this.loadEntries();
        }
    }

    // ==================== ENTRIES ====================

    setDefaultDate() {
        this.manualDate.value = Utils.getToday();
    }

    loadEntries() {
        let entries = Storage.getEntries();
        const projects = Storage.getProjects();
        const projectMap = {};
        projects.forEach(p => projectMap[p.id] = p);

        // Filter op project
        const filterProjectId = this.filterProject.value;
        if (filterProjectId) {
            entries = entries.filter(e => e.projectId === filterProjectId);
        }

        // Filter op periode
        const period = this.filterPeriod.value;
        entries = entries.filter(e => Utils.isWithinPeriod(e.date, period));

        // Sorteer op datum (nieuwste eerst)
        entries.sort((a, b) => new Date(b.date) - new Date(a.date));

        // Bereken totaal
        const totalHrs = entries.reduce((sum, e) => sum + parseFloat(e.hours || 0), 0);
        this.totalHours.textContent = totalHrs.toFixed(2);

        // Render tabel
        if (entries.length === 0) {
            this.entriesTableBody.innerHTML = `
                <tr>
                    <td colspan="5" class="empty-state">
                        <div class="empty-state-icon">📝</div>
                        <p>Nog geen uren geregistreerd</p>
                    </td>
                </tr>
            `;
            return;
        }

        this.entriesTableBody.innerHTML = entries.map(entry => {
            const project = projectMap[entry.projectId];
            const projectName = project ? project.name : 'Onbekend project';
            const projectColor = project ? project.color : '#ccc';

            return `
                <tr data-id="${entry.id}">
                    <td>${Utils.formatDate(entry.date)}</td>
                    <td>
                        <div class="entry-project">
                            <span class="project-color" style="background-color: ${projectColor}"></span>
                            ${this.escapeHtml(projectName)}
                        </div>
                    </td>
                    <td>${this.escapeHtml(entry.description) || '-'}</td>
                    <td>${parseFloat(entry.hours).toFixed(2)}</td>
                    <td class="entry-actions">
                        <button class="btn btn-icon delete-entry" title="Verwijder">🗑️</button>
                    </td>
                </tr>
            `;
        }).join('');

        // Bind delete events
        this.entriesTableBody.querySelectorAll('.delete-entry').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const row = e.target.closest('tr');
                const entryId = row.dataset.id;
                this.deleteEntry(entryId);
            });
        });
    }

    handleManualEntry(e) {
        e.preventDefault();

        const entry = {
            projectId: this.manualProject.value,
            date: this.manualDate.value,
            hours: parseFloat(this.manualHours.value),
            description: this.manualDescription.value.trim(),
            source: 'manual'
        };

        if (!entry.projectId) {
            alert('Selecteer een project');
            return;
        }

        Storage.addEntry(entry);

        // Reset form maar behoud datum
        this.manualHours.value = '';
        this.manualDescription.value = '';

        this.loadEntries();
        this.loadProjects(); // Update uren in sidebar
    }

    deleteEntry(entryId) {
        if (confirm('Weet je zeker dat je deze registratie wilt verwijderen?')) {
            Storage.deleteEntry(entryId);
            this.loadEntries();
            this.loadProjects();
        }
    }

    // ==================== EXPORT ====================

    exportToCSV() {
        const entries = Storage.getEntries();
        const projects = Storage.getProjects();
        const projectMap = {};
        projects.forEach(p => projectMap[p.id] = p);

        if (entries.length === 0) {
            alert('Geen uren om te exporteren');
            return;
        }

        // Sorteer op datum
        entries.sort((a, b) => new Date(a.date) - new Date(b.date));

        const data = entries.map(entry => {
            const project = projectMap[entry.projectId];
            return {
                Datum: entry.date,
                Project: project ? project.name : 'Onbekend',
                Beschrijving: entry.description || '',
                Uren: parseFloat(entry.hours).toFixed(2),
                Tarief: project ? project.rate.toFixed(2) : '0.00',
                Bedrag: project ? (parseFloat(entry.hours) * project.rate).toFixed(2) : '0.00'
            };
        });

        const headers = ['Datum', 'Project', 'Beschrijving', 'Uren', 'Tarief', 'Bedrag'];
        const csv = Utils.convertToCSV(data, headers);

        const filename = `tijdregistratie_${Utils.getToday()}.csv`;
        Utils.downloadFile(csv, filename);
    }

    // ==================== HELPERS ====================

    escapeHtml(text) {
        if (!text) return '';
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Start de applicatie
document.addEventListener('DOMContentLoaded', () => {
    window.app = new TimeTrackerApp();
});
