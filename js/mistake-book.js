/**
 * Mistake Book View for TOEIC Listening 300
 * Displays errors, filters by skillGroup, and enables mistake recovery
 */

import { storage } from './storage.js';
import { rebuildDerived } from './progress.js';

export class MistakeBookView {
  constructor(options = {}) {
    this.container = options.container;
    this.dataLoader = options.dataLoader;
    this.onPracticeMistake = options.onPracticeMistake || (() => {});
    this.currentFilter = 'all'; // 'all', 'needs_review', 'resolved'
    this.currentGroupFilter = 'all';
  }

  async render() {
    if (!this.container) return;
    this.container.innerHTML = '<div class="loading">Đang tải sổ lỗi...</div>';

    await this.dataLoader.loadAllChapters();
    const state = storage.loadState();
    const derived = rebuildDerived(state, this.dataLoader);

    const mistakes = derived ? derived.mistakes : [];
    const skillGroups = [...new Set(mistakes.map(m => m.skillGroup).filter(Boolean))];

    // Filter
    let filtered = mistakes;
    if (this.currentFilter === 'needs_review') {
      filtered = filtered.filter(m => m.status === 'needs_review' || m.status === 'practicing');
    } else if (this.currentFilter === 'resolved') {
      filtered = filtered.filter(m => m.status === 'resolved');
    }

    if (this.currentGroupFilter !== 'all') {
      filtered = filtered.filter(m => m.skillGroup === this.currentGroupFilter);
    }

    const el = document.createElement('div');
    el.className = 'mistake-book-view';

    el.innerHTML = `
      <div class="mistake-header-card">
        <h1 class="page-title">📕 Sổ lỗi cá nhân (Mistake Book)</h1>
        <p class="page-subtitle">Ghi nhận các câu đã từng làm sai và kiểm tra việc khắc phục lỗi dứt điểm theo nhóm kỹ năng.</p>
        
        <div class="mistake-stats-bar">
          <div class="stat-pill">Tổng số lỗi ghi nhận: <strong>${mistakes.length}</strong></div>
          <div class="stat-pill pill-warning">Cần khắc phục: <strong>${derived.openMistakesCount}</strong></div>
          <div class="stat-pill pill-success">Đã khắc phục: <strong>${derived.resolvedMistakesCount}</strong></div>
        </div>
      </div>

      <!-- Filters -->
      <div class="mistake-filters-card">
        <div class="filter-row">
          <label>Trạng thái:</label>
          <div class="btn-group">
            <button class="filter-btn ${this.currentFilter === 'all' ? 'active' : ''}" data-status="all">Tất cả (${mistakes.length})</button>
            <button class="filter-btn ${this.currentFilter === 'needs_review' ? 'active' : ''}" data-status="needs_review">Chưa khắc phục (${derived.openMistakesCount})</button>
            <button class="filter-btn ${this.currentFilter === 'resolved' ? 'active' : ''}" data-status="resolved">Đã khắc phục (${derived.resolvedMistakesCount})</button>
          </div>
        </div>

        ${skillGroups.length > 0 ? `
          <div class="filter-row">
            <label>Nhóm kỹ năng (skillGroup):</label>
            <select class="group-select">
              <option value="all">Tất cả nhóm kỹ năng</option>
              ${skillGroups.map(g => `
                <option value="${g}" ${this.currentGroupFilter === g ? 'selected' : ''}>${g.replace(/_/g, ' ')}</option>
              `).join('')}
            </select>
          </div>
        ` : ''}
      </div>

      <!-- Mistake List -->
      <div class="mistake-list">
        ${filtered.length === 0 ? `
          <div class="empty-state">
            <div class="empty-icon">🎉</div>
            <h3>Không có câu sai nào trong mục này!</h3>
            <p>Tuyệt vời, bạn đang nắm rất chắc kiến thức.</p>
          </div>
        ` : filtered.map(m => {
          const q = m.question;
          const isResolved = m.status === 'resolved';
          return `
            <div class="mistake-card ${isResolved ? 'card-resolved' : 'card-pending'}">
              <div class="mistake-card-header">
                <span class="m-qid">${m.questionId}</span>
                <span class="m-badge ${isResolved ? 'badge-resolved' : 'badge-pending'}">
                  ${isResolved ? '✓ Đã khắc phục' : '⏳ Cần ôn tập'}
                </span>
                <span class="m-group-tag">${m.skillGroup.replace(/_/g, ' ')}</span>
              </div>

              <div class="mistake-body">
                ${q && q.prompt ? `<div class="m-prompt"><strong>Câu hỏi:</strong> ${q.prompt}</div>` : ''}
                ${q && q.transcript ? `<div class="m-transcript"><strong>Transcript:</strong> ${q.transcript}</div>` : ''}
                
                <div class="m-answers-row">
                  <div class="ans-badge ans-user">Đã chọn: (${m.lastAttempt.selected})</div>
                  <div class="ans-badge ans-correct">Đáp án đúng: (${q ? q.correctAnswer : '?'})</div>
                </div>

                ${q && q.explanation ? `
                  <div class="m-explanation">
                    <strong>Giải thích:</strong> ${q.explanation}
                  </div>
                ` : ''}
              </div>

              <div class="mistake-footer">
                <button class="btn-practice-skill" data-qid="${m.questionId}" data-group="${m.skillGroup}">
                  🎯 Luyện câu mới cùng nhóm "${m.skillGroup.replace(/_/g, ' ')}"
                </button>
              </div>
            </div>
          `;
        }).join('')}
      </div>
    `;

    // Filter event handlers
    el.querySelectorAll('.filter-btn').forEach(btn => {
      btn.onclick = () => {
        this.currentFilter = btn.dataset.status;
        this.render();
      };
    });

    const selectEl = el.querySelector('.group-select');
    if (selectEl) {
      selectEl.onchange = (e) => {
        this.currentGroupFilter = e.target.value;
        this.render();
      };
    }

    // Practice button handlers
    el.querySelectorAll('.btn-practice-skill').forEach(btn => {
      btn.onclick = () => {
        const qid = btn.dataset.qid;
        const group = btn.dataset.group;
        this.onPracticeMistake(qid, group);
      };
    });

    this.container.innerHTML = '';
    this.container.appendChild(el);
  }
}
