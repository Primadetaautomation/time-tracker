/**
 * Utility functies voor de Tijdregistratie applicatie
 */

const Utils = {
    /**
     * Genereer een unieke ID
     */
    generateId() {
        return Date.now().toString(36) + Math.random().toString(36).substring(2);
    },

    /**
     * Formatteer tijd in HH:MM:SS formaat
     */
    formatTime(seconds) {
        const hrs = Math.floor(seconds / 3600);
        const mins = Math.floor((seconds % 3600) / 60);
        const secs = seconds % 60;
        return [hrs, mins, secs]
            .map(v => v.toString().padStart(2, '0'))
            .join(':');
    },

    /**
     * Formatteer seconden naar uren (decimaal)
     */
    secondsToHours(seconds) {
        return (seconds / 3600).toFixed(2);
    },

    /**
     * Formatteer uren naar leesbare string
     */
    formatHours(hours) {
        const hrs = Math.floor(hours);
        const mins = Math.round((hours - hrs) * 60);
        if (hrs === 0) {
            return `${mins}m`;
        }
        if (mins === 0) {
            return `${hrs}u`;
        }
        return `${hrs}u ${mins}m`;
    },

    /**
     * Formatteer datum naar Nederlandse notatie
     */
    formatDate(date) {
        const d = new Date(date);
        return d.toLocaleDateString('nl-NL', {
            weekday: 'short',
            day: 'numeric',
            month: 'short',
            year: 'numeric'
        });
    },

    /**
     * Formatteer datum voor input veld (YYYY-MM-DD)
     */
    formatDateForInput(date) {
        const d = new Date(date);
        return d.toISOString().split('T')[0];
    },

    /**
     * Haal vandaag op als YYYY-MM-DD
     */
    getToday() {
        return this.formatDateForInput(new Date());
    },

    /**
     * Haal start van de week op (maandag)
     */
    getStartOfWeek(date = new Date()) {
        const d = new Date(date);
        const day = d.getDay();
        const diff = d.getDate() - day + (day === 0 ? -6 : 1);
        d.setDate(diff);
        d.setHours(0, 0, 0, 0);
        return d;
    },

    /**
     * Haal start van de maand op
     */
    getStartOfMonth(date = new Date()) {
        const d = new Date(date);
        d.setDate(1);
        d.setHours(0, 0, 0, 0);
        return d;
    },

    /**
     * Check of datum binnen periode valt
     */
    isWithinPeriod(date, period) {
        const d = new Date(date);
        const now = new Date();

        switch (period) {
            case 'week':
                return d >= this.getStartOfWeek();
            case 'month':
                return d >= this.getStartOfMonth();
            case 'all':
            default:
                return true;
        }
    },

    /**
     * Converteer CSV data naar downloadbare blob
     */
    convertToCSV(data, headers) {
        const headerRow = headers.join(';');
        const rows = data.map(row =>
            headers.map(header => {
                let value = row[header] || '';
                // Escape quotes en wrap in quotes als er speciale karakters zijn
                if (typeof value === 'string' && (value.includes(';') || value.includes('"') || value.includes('\n'))) {
                    value = '"' + value.replace(/"/g, '""') + '"';
                }
                return value;
            }).join(';')
        );
        return [headerRow, ...rows].join('\n');
    },

    /**
     * Download bestand
     */
    downloadFile(content, filename, mimeType = 'text/csv;charset=utf-8;') {
        const blob = new Blob(['\ufeff' + content], { type: mimeType });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(link.href);
    },

    /**
     * Debounce functie
     */
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },

    /**
     * Parse klant/project uit window titel
     */
    parseClientFromTitle(title, rules) {
        for (const rule of rules) {
            if (title.toLowerCase().includes(rule.pattern.toLowerCase())) {
                return rule.projectId;
            }
        }
        return null;
    },

    /**
     * Groepeer entries per dag
     */
    groupEntriesByDate(entries) {
        return entries.reduce((groups, entry) => {
            const date = entry.date;
            if (!groups[date]) {
                groups[date] = [];
            }
            groups[date].push(entry);
            return groups;
        }, {});
    },

    /**
     * Bereken totaal uren
     */
    calculateTotalHours(entries) {
        return entries.reduce((total, entry) => total + parseFloat(entry.hours || 0), 0);
    }
};
