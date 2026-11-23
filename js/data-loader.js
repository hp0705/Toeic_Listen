/**
 * Data Loader for TOEIC Listening 300
 * Loads course.json and chapter JSON files
 */

export class DataLoader {
  constructor() {
    this.course = null;
    this.chapters = new Map();
    this.questionsMap = new Map();
    this.groupsMap = new Map();
  }

  async loadCourse() {
    if (this.course) return this.course;
    try {
      const res = await fetch(`data/course.json?v=${Date.now()}`);
      if (!res.ok) throw new Error(`HTTP ${res.status} loading course.json`);
      this.course = await res.json();
      return this.course;
    } catch (err) {
      console.error('Failed to load course.json:', err);
      throw err;
    }
  }

  async loadChapter(chapterId) {
    if (this.chapters.has(chapterId)) {
      return this.chapters.get(chapterId);
    }
    const course = await this.loadCourse();
    const chapterMeta = course.chapters.find(c => c.id === chapterId);
    if (!chapterMeta) throw new Error(`Chapter ${chapterId} not found in course.json`);

    try {
      const res = await fetch(`data/${chapterMeta.file}?v=${course.contentVersion}`);
      if (!res.ok) throw new Error(`HTTP ${res.status} loading chapter ${chapterId}`);
      const data = await res.json();
      this.chapters.set(chapterId, data);

      // Index questions
      if (Array.isArray(data.questions)) {
        for (const q of data.questions) {
          this.questionsMap.set(q.id, q);
        }
      }

      // Index groups (Part 3/4)
      if (Array.isArray(data.groups)) {
        for (const g of data.groups) {
          this.groupsMap.set(g.id, g);
        }
      }

      return data;
    } catch (err) {
      console.error(`Failed to load chapter ${chapterId}:`, err);
      throw err;
    }
  }

  async loadAllChapters() {
    const course = await this.loadCourse();
    for (const ch of course.chapters) {
      await this.loadChapter(ch.id);
    }
    return this.chapters;
  }

  getQuestion(questionId) {
    return this.questionsMap.get(questionId) || null;
  }

  getGroup(groupId) {
    return this.groupsMap.get(groupId) || null;
  }
}

export const dataLoader = new DataLoader();
