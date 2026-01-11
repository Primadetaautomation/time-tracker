const { contextBridge, ipcRenderer } = require('electron');

// Expose veilige API aan de renderer
contextBridge.exposeInMainWorld('electronAPI', {
    // App informatie
    getVersion: () => ipcRenderer.invoke('get-app-version'),

    // Notificaties
    showNotification: (title, body) => ipcRenderer.invoke('show-notification', title, body),

    // Platform info
    platform: process.platform,
    isElectron: true
});
