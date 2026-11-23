/**
 * Lesson View for TOEIC Listening 300
 * Renders lesson objectives, teaching blocks, vocabulary table, audio examples
 */

import { audioPlayer } from './audio-player.js';

export class LessonView {
  constructor(options = {}) {
    this.container = options.container;
    this.dataLoader = options.dataLoader;
    this.onStartQuiz = options.onStartQuiz || (() => {});
  }

  async render(chapterId, lessonId) {
    if (!this.container) return;
    this.container.innerHTML = '<div class="loading">Đang tải bài học...</div>';

    const chapter = await this.dataLoader.loadChapter(chapterId);
    const isFinal = lessonId.endsWith('-FINAL');

    if (isFinal) {
      this.renderFinalTest(chapter);
      return;
    }

    const lesson = chapter.lessons.find(l => l.lessonId === lessonId);
    if (!lesson) {
      this.container.innerHTML = '<div class="error-msg">Không tìm thấy bài học!</div>';
      return;
    }

    const el = document.createElement('div');
    el.className = 'lesson-detail-view';

    el.innerHTML = `
      <div class="lesson-header-card">
        <div class="badge-row">
          <span class="chapter-tag">${chapter.chapterId}</span>
          <span class="lesson-tag">${lesson.lessonId}</span>
        </div>
        <h1 class="lesson-title">${lesson.title}</h1>
        <div class="pass-rule-badge">
          Điều kiện đạt: Đúng từ ${lesson.passRule.minCorrect}/${lesson.passRule.total} câu (${lesson.passRule.percentage}%)
        </div>
      </div>

      <!-- Objectives -->
      ${lesson.objectives && lesson.objectives.length > 0 ? `
        <div class="card-section">
          <h2 class="section-title">🎯 Mục tiêu bài học</h2>
          <ul class="objectives-list">
            ${lesson.objectives.map(o => `<li>${o}</li>`).join('')}
          </ul>
        </div>
      ` : ''}

      <!-- Teaching Blocks -->
      ${lesson.teachingBlocks && lesson.teachingBlocks.length > 0 ? `
        <div class="card-section teaching-section">
          <h2 class="section-title">📖 Kiến thức cốt lõi</h2>
          ${lesson.teachingBlocks.map(tb => `
            <div class="teaching-block">
              <h3 class="teaching-title">${tb.title}</h3>
              <div class="teaching-content">${tb.content.replace(/\n\n/g, '<br><br>')}</div>
            </div>
          `).join('')}
        </div>
      ` : ''}

      <!-- Vocabulary -->
      ${lesson.vocabulary && lesson.vocabulary.length > 0 ? `
        <div class="card-section vocab-section">
          <h2 class="section-title">📝 Từ vựng quan trọng</h2>
          <div class="table-responsive">
            <table class="vocab-table">
              <thead>
                <tr>
                  <th>Từ / Cụm từ</th>
                  <th>Ý nghĩa</th>
                  <th>Ví dụ / Cụm thường gặp</th>
                </tr>
              </thead>
              <tbody>
                ${lesson.vocabulary.map(v => `
                  <tr>
                    <td><strong>${v.word}</strong></td>
                    <td>${v.meaning}</td>
                    <td><em>${v.example || ''}</em></td>
                  </tr>
                `).join('')}
              </tbody>
            </table>
          </div>
        </div>
      ` : ''}

      <!-- Audio Examples -->
      ${lesson.examples && lesson.examples.length > 0 ? `
        <div class="card-section examples-section">
          <h2 class="section-title">🎧 Ví dụ mẫu phát âm</h2>
          <div class="examples-list">
            ${lesson.examples.map(ex => `
              <div class="example-item">
                <button class="btn-play-sm" data-file="${ex.audioFile}" data-text="${ex.text}">▶</button>
                <div class="example-content">
                  <div class="example-en">${ex.text}</div>
                  <div class="example-vi">${ex.translation}</div>
                </div>
              </div>
            `).join('')}
          </div>
        </div>
      ` : ''}

      <!-- Action Buttons -->
      <div class="lesson-actions-card">
        <h3>Sẵn sàng luyện tập?</h3>
        <p>Chọn chế độ để bắt đầu làm ${lesson.questionIds.length} câu hỏi của bài học:</p>
        <div class="action-btn-row">
          <button class="btn-primary btn-large btn-start-learn">
            <span class="btn-icon">💡</span>
            <div class="btn-label-wrap">
              <strong>Luyện tập (Learn Mode)</strong>
              <small>Có thể chỉnh tốc độ 0.85x và xem giải thích</small>
            </div>
          </button>
          <button class="btn-secondary btn-large btn-start-test">
            <span class="btn-icon">⏱️</span>
            <div class="btn-label-wrap">
              <strong>Kiểm tra (Test Mode)</strong>
              <small>Tốc độ chuẩn 1.0x, chấm điểm sau khi nộp</small>
            </div>
          </button>
        </div>
      </div>
    `;

    // Example audio play handlers
    el.querySelectorAll('.btn-play-sm').forEach(btn => {
      btn.onclick = () => {
        const file = btn.dataset.file;
        const text = btn.dataset.text;
        audioPlayer.playSegments([{ text, file, pauseAfterMs: 0 }]);
      };
    });

    // Start Quiz handlers
    el.querySelector('.btn-start-learn').onclick = () => {
      this.onStartQuiz(chapterId, lessonId, 'learn');
    };
    el.querySelector('.btn-start-test').onclick = () => {
      this.onStartQuiz(chapterId, lessonId, 'test');
    };

    this.container.innerHTML = '';
    this.container.appendChild(el);
  }

  renderFinalTest(chapter) {
    const finalTest = chapter.finalTest;
    const el = document.createElement('div');
    el.className = 'lesson-detail-view final-test-intro';
    el.innerHTML = `
      <div class="lesson-header-card final-header">
        <span class="chapter-tag">${chapter.chapterId}</span>
        <h1 class="lesson-title">Bài kiểm tra tổng kết ${chapter.title}</h1>
        <div class="pass-rule-badge">
          Điều kiện đạt: Đúng từ ${finalTest.passRule.minCorrect}/${finalTest.passRule.total} câu (${finalTest.passRule.percentage}%)
        </div>
      </div>

      <div class="card-section">
        <h2 class="section-title">📋 Thông tin bài kiểm tra</h2>
        <p>Bài kiểm tra gồm <strong>${finalTest.questionIds.length} câu hỏi mới</strong> tổng hợp kiến thức của toàn bộ ${chapter.title}.</p>
        <ul class="test-rules-list">
          <li>Âm thanh phát ở tốc độ chuẩn 1.0x.</li>
          <li>Transcript và bản dịch sẽ chỉ hiển thị sau khi hoàn thành toàn bộ bài kiểm tra.</li>
          <li>Đạt từ 80% trở lên sẽ mở khóa chương tiếp theo!</li>
        </ul>
      </div>

      <div class="lesson-actions-card">
        <button class="btn-primary btn-large btn-start-final">
          🚀 Bắt đầu làm bài kiểm tra
        </button>
      </div>
    `;

    el.querySelector('.btn-start-final').onclick = () => {
      this.onStartQuiz(chapter.chapterId, finalTest.id, 'test');
    };

    this.container.innerHTML = '';
    this.container.appendChild(el);
  }
}
