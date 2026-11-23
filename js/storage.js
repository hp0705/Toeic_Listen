/**
 * Storage Layer for TOEIC Listening 300
 * Complies with PROGRESS_STORAGE_SPEC.md v1.2 & SPEC_WEB_APP.md v2.3
 */

const STORAGE_KEY = 'toeic_listening_300_v2';
const BACKUP_LAST_KEY = 'toeic_listening_300_backup_last';

export const storage = {
  createDefaultState(courseId = 'toeic-listening-300') {
    return {
      schemaVersion: 2,
      specVersion: '2.3',
      courseId: courseId,
      contentVersion: '1.0.0',
      updatedAt: new Date().toISOString(),
      runs: [],
      attempts: [],
      settings: {
        lastBackupAt: null,
        remindBackup: true
      }
    };
  },

  loadState() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) {
        const defaultState = this.createDefaultState();
        this.saveState(defaultState);
        return defaultState;
      }
      const parsed = JSON.parse(raw);
      if (!parsed || parsed.schemaVersion !== 2) {
        console.warn('Storage schema version mismatch, upgrading or initializing default.');
        const state = Object.assign(this.createDefaultState(), parsed, { schemaVersion: 2 });
        return state;
      }
      return parsed;
    } catch (err) {
      console.error('Error loading state from localStorage:', err);
      return this.createDefaultState();
    }
  },

  saveState(state) {
    if (!state) return false;
    try {
      // 1. Snapshot last valid state before overwriting
      const currentRaw = localStorage.getItem(STORAGE_KEY);
      if (currentRaw) {
        localStorage.setItem(BACKUP_LAST_KEY, currentRaw);
      }

      state.updatedAt = new Date().toISOString();
      const serialized = JSON.stringify(state);
      localStorage.setItem(STORAGE_KEY, serialized);
      return true;
    } catch (err) {
      console.error('Error saving state to localStorage:', err);
      if (err.name === 'QuotaExceededError') {
        alert('Cảnh báo: Bộ nhớ trình duyệt (LocalStorage) đã đầy. Vui lòng vào trang "Lịch sử & Sao lưu" để xuất bản sao lưu!');
      }
      return false;
    }
  },

  hasSnapshot() {
    return !!localStorage.getItem(BACKUP_LAST_KEY);
  },

  restoreSnapshot() {
    try {
      const snapshotRaw = localStorage.getItem(BACKUP_LAST_KEY);
      if (!snapshotRaw) return null;
      const parsed = JSON.parse(snapshotRaw);
      localStorage.setItem(STORAGE_KEY, snapshotRaw);
      return parsed;
    } catch (err) {
      console.error('Error restoring snapshot:', err);
      return null;
    }
  },

  resetProgress() {
    const defaultState = this.createDefaultState();
    this.saveState(defaultState);
    return defaultState;
  }
};
