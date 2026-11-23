/**
 * Backup, Export, Import and Merge Manager for TOEIC Listening 300
 * Complies with PROGRESS_STORAGE_SPEC.md v1.2
 */

import { storage } from './storage.js';
import { rebuildDerived } from './progress.js';

export class BackupManager {
  static createCoachSummary(state, derived) {
    if (!derived) return null;
    const completedChapters = Object.entries(derived.chapterStatus)
      .filter(([_, s]) => s.completed)
      .map(([id]) => id);

    let currentUnlocked = 'CH01';
    if (derived.chapterStatus.CH03 && derived.chapterStatus.CH03.unlocked) currentUnlocked = 'CH03';
    else if (derived.chapterStatus.CH02 && derived.chapterStatus.CH02.unlocked) currentUnlocked = 'CH02';

    const weakSkillGroups = [];
    const strongSkillGroups = [];

    for (const [group, stat] of Object.entries(derived.skillGroupStats || {})) {
      const pct = stat.total > 0 ? (stat.correct / stat.total) * 100 : 0;
      if (pct < 70) weakSkillGroups.push(group);
      else if (pct >= 85) strongSkillGroups.push(group);
    }

    return {
      totalAttempts: derived.totalAttemptsCount,
      accuracy: Math.round(derived.overallAccuracy * 100) / 100,
      chaptersCompleted: completedChapters,
      currentUnlockedChapter: currentUnlocked,
      openMistakesCount: derived.openMistakesCount,
      weakSkillGroups,
      strongSkillGroups
    };
  }

  static exportBackup(dataLoader) {
    const state = storage.loadState();
    const derived = rebuildDerived(state, dataLoader);
    const coachSummary = this.createCoachSummary(state, derived);

    state.settings = state.settings || {};
    state.settings.lastBackupAt = new Date().toISOString();
    storage.saveState(state);

    const exportData = {
      schemaVersion: 2,
      specVersion: '2.3',
      contentVersion: '1.0.0',
      courseId: state.courseId || 'toeic-listening-300',
      exportedAt: new Date().toISOString(),
      runs: state.runs || [],
      attempts: state.attempts || [],
      settings: state.settings,
      coachSummary
    };

    const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    const dateStr = new Date().toISOString().slice(0, 10);
    a.download = `toeic-listening-300-backup-${dateStr}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);

    return exportData;
  }

  static importBackup(jsonString, mode = 'merge') {
    let imported;
    try {
      imported = JSON.parse(jsonString);
    } catch (e) {
      throw new Error('Tập tin không phải là JSON hợp lệ!');
    }

    if (!imported || imported.schemaVersion !== 2 || !Array.isArray(imported.runs) || !Array.isArray(imported.attempts)) {
      throw new Error('Dữ liệu sao lưu không đúng định dạng chuẩn (schemaVersion phải là 2)!');
    }

    const currentState = storage.loadState();

    if (mode === 'replace') {
      // Save snapshot before replace
      storage.saveState(currentState);
      const newState = {
        schemaVersion: 2,
        specVersion: imported.specVersion || '2.3',
        courseId: imported.courseId || currentState.courseId,
        contentVersion: imported.contentVersion || '1.0.0',
        updatedAt: new Date().toISOString(),
        runs: imported.runs,
        attempts: imported.attempts,
        settings: imported.settings || currentState.settings
      };
      storage.saveState(newState);
      return {
        success: true,
        mode: 'replace',
        totalRuns: newState.runs.length,
        totalAttempts: newState.attempts.length
      };
    } else {
      // Merge mode
      const existingRunIds = new Set(currentState.runs.map(r => r.id));
      const existingAttemptIds = new Set(currentState.attempts.map(a => a.id));

      let newRunsCount = 0;
      let newAttemptsCount = 0;

      for (const r of imported.runs) {
        if (!existingRunIds.has(r.id)) {
          currentState.runs.push(r);
          existingRunIds.add(r.id);
          newRunsCount++;
        }
      }

      for (const a of imported.attempts) {
        if (!existingAttemptIds.has(a.id)) {
          currentState.attempts.push(a);
          existingAttemptIds.add(a.id);
          newAttemptsCount++;
        }
      }

      currentState.updatedAt = new Date().toISOString();
      storage.saveState(currentState);

      return {
        success: true,
        mode: 'merge',
        newRunsCount,
        newAttemptsCount,
        totalRuns: currentState.runs.length,
        totalAttempts: currentState.attempts.length
      };
    }
  }
}
