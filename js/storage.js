/**
 * Storage module voor lokale data opslag
 * Gebruikt LocalStorage voor persistentie
 */

const Storage = {
    KEYS: {
        PROJECTS: 'timetracker_projects',
        ENTRIES: 'timetracker_entries',
        SETTINGS: 'timetracker_settings',
        RULES: 'timetracker_rules',
        ACTIVE_TIMER: 'timetracker_active_timer'
    },

    /**
     * Haal data op uit LocalStorage
     */
    get(key) {
        try {
            const data = localStorage.getItem(key);
            return data ? JSON.parse(data) : null;
        } catch (error) {
            console.error('Error reading from localStorage:', error);
            return null;
        }
    },

    /**
     * Sla data op in LocalStorage
     */
    set(key, data) {
        try {
            localStorage.setItem(key, JSON.stringify(data));
            return true;
        } catch (error) {
            console.error('Error writing to localStorage:', error);
            return false;
        }
    },

    /**
     * Verwijder data uit LocalStorage
     */
    remove(key) {
        try {
            localStorage.removeItem(key);
            return true;
        } catch (error) {
            console.error('Error removing from localStorage:', error);
            return false;
        }
    },

    // ==================== PROJECTEN ====================

    /**
     * Haal alle projecten op
     */
    getProjects() {
        return this.get(this.KEYS.PROJECTS) || [];
    },

    /**
     * Voeg een project toe
     */
    addProject(project) {
        const projects = this.getProjects();
        const newProject = {
            id: Utils.generateId(),
            name: project.name,
            color: project.color || '#3498db',
            rate: project.rate || 0,
            createdAt: new Date().toISOString(),
            archived: false
        };
        projects.push(newProject);
        this.set(this.KEYS.PROJECTS, projects);
        return newProject;
    },

    /**
     * Update een project
     */
    updateProject(id, updates) {
        const projects = this.getProjects();
        const index = projects.findIndex(p => p.id === id);
        if (index !== -1) {
            projects[index] = { ...projects[index], ...updates };
            this.set(this.KEYS.PROJECTS, projects);
            return projects[index];
        }
        return null;
    },

    /**
     * Verwijder een project
     */
    deleteProject(id) {
        const projects = this.getProjects();
        const filtered = projects.filter(p => p.id !== id);
        this.set(this.KEYS.PROJECTS, filtered);
        // Verwijder ook alle entries van dit project
        const entries = this.getEntries();
        const filteredEntries = entries.filter(e => e.projectId !== id);
        this.set(this.KEYS.ENTRIES, filteredEntries);
        return true;
    },

    /**
     * Haal project op basis van ID
     */
    getProject(id) {
        const projects = this.getProjects();
        return projects.find(p => p.id === id) || null;
    },

    // ==================== TIJD ENTRIES ====================

    /**
     * Haal alle entries op
     */
    getEntries() {
        return this.get(this.KEYS.ENTRIES) || [];
    },

    /**
     * Voeg een entry toe
     */
    addEntry(entry) {
        const entries = this.getEntries();
        const newEntry = {
            id: Utils.generateId(),
            projectId: entry.projectId,
            date: entry.date || Utils.getToday(),
            hours: parseFloat(entry.hours) || 0,
            description: entry.description || '',
            createdAt: new Date().toISOString(),
            source: entry.source || 'manual' // 'manual', 'timer', 'auto'
        };
        entries.push(newEntry);
        this.set(this.KEYS.ENTRIES, entries);
        return newEntry;
    },

    /**
     * Update een entry
     */
    updateEntry(id, updates) {
        const entries = this.getEntries();
        const index = entries.findIndex(e => e.id === id);
        if (index !== -1) {
            entries[index] = { ...entries[index], ...updates };
            this.set(this.KEYS.ENTRIES, entries);
            return entries[index];
        }
        return null;
    },

    /**
     * Verwijder een entry
     */
    deleteEntry(id) {
        const entries = this.getEntries();
        const filtered = entries.filter(e => e.id !== id);
        this.set(this.KEYS.ENTRIES, filtered);
        return true;
    },

    /**
     * Haal entries op voor een specifiek project
     */
    getEntriesByProject(projectId) {
        const entries = this.getEntries();
        return entries.filter(e => e.projectId === projectId);
    },

    /**
     * Haal entries op voor een specifieke periode
     */
    getEntriesByPeriod(period) {
        const entries = this.getEntries();
        return entries.filter(e => Utils.isWithinPeriod(e.date, period));
    },

    /**
     * Bereken totaal uren per project
     */
    getHoursPerProject() {
        const entries = this.getEntries();
        const projects = this.getProjects();

        const hoursMap = {};
        projects.forEach(p => {
            hoursMap[p.id] = 0;
        });

        entries.forEach(e => {
            if (hoursMap.hasOwnProperty(e.projectId)) {
                hoursMap[e.projectId] += parseFloat(e.hours) || 0;
            }
        });

        return hoursMap;
    },

    // ==================== TIMER ====================

    /**
     * Sla actieve timer state op
     */
    saveActiveTimer(timerState) {
        this.set(this.KEYS.ACTIVE_TIMER, timerState);
    },

    /**
     * Haal actieve timer state op
     */
    getActiveTimer() {
        return this.get(this.KEYS.ACTIVE_TIMER);
    },

    /**
     * Verwijder actieve timer state
     */
    clearActiveTimer() {
        this.remove(this.KEYS.ACTIVE_TIMER);
    },

    // ==================== REGELS ====================

    /**
     * Haal automatische toewijzingsregels op
     */
    getRules() {
        return this.get(this.KEYS.RULES) || [];
    },

    /**
     * Voeg een regel toe
     */
    addRule(rule) {
        const rules = this.getRules();
        const newRule = {
            id: Utils.generateId(),
            pattern: rule.pattern,
            projectId: rule.projectId,
            priority: rule.priority || 0
        };
        rules.push(newRule);
        this.set(this.KEYS.RULES, rules);
        return newRule;
    },

    /**
     * Verwijder een regel
     */
    deleteRule(id) {
        const rules = this.getRules();
        const filtered = rules.filter(r => r.id !== id);
        this.set(this.KEYS.RULES, filtered);
        return true;
    },

    // ==================== INSTELLINGEN ====================

    /**
     * Haal instellingen op
     */
    getSettings() {
        return this.get(this.KEYS.SETTINGS) || {
            hourlyRate: 0,
            currency: 'EUR',
            weekStartsOn: 1, // Maandag
            autoTrackingEnabled: false
        };
    },

    /**
     * Sla instellingen op
     */
    saveSettings(settings) {
        this.set(this.KEYS.SETTINGS, settings);
    },

    // ==================== EXPORT/IMPORT ====================

    /**
     * Exporteer alle data
     */
    exportAllData() {
        return {
            projects: this.getProjects(),
            entries: this.getEntries(),
            rules: this.getRules(),
            settings: this.getSettings(),
            exportedAt: new Date().toISOString()
        };
    },

    /**
     * Importeer data
     */
    importData(data) {
        if (data.projects) this.set(this.KEYS.PROJECTS, data.projects);
        if (data.entries) this.set(this.KEYS.ENTRIES, data.entries);
        if (data.rules) this.set(this.KEYS.RULES, data.rules);
        if (data.settings) this.set(this.KEYS.SETTINGS, data.settings);
        return true;
    },

    /**
     * Wis alle data
     */
    clearAllData() {
        Object.values(this.KEYS).forEach(key => this.remove(key));
        return true;
    }
};
