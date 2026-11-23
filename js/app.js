/**
 * Main Application Controller for TOEIC Listening 300
 * Complies with SPEC_WEB_APP.md v2.3 and PROGRESS_STORAGE_SPEC.md v1.2
 */

import { storage } from './storage.js';
import { dataLoader } from './data-loader.js';
import { rebuildDerived } from './progress.js';
import { Router } from './router.js';
import { LessonView } from './lesson-view.js';
import { QuizController } from './quiz.js';
import { MistakeBookView } from './mistake-book.js';
import { HistoryView } from './history-view.js';
import { audioPlayer } from './audio-player.js';

class App {
  constructor() {
    this.router = new Router();
    this.appEl = document.getElementById('app');
    this.contentEl = document.getElementById('main-content');
    this.navLinks = document.querySelectorAll('.nav-link');

    this.lessonView = new LessonView({
      container: this.contentEl,
      dataLoader: dataLoader,
      onStartQuiz: (chapterId, lessonId, mode) => {
        this.router.navigate(`/quiz/${chapterId}/${lessonId}?mode=${mode}`);
      }
    });

    this.quizController = new QuizController({
      container: this.contentEl,
      dataLoader: dataLoader,
      onFinish: (run) => {
        this.router.navigate(`/path`);
      }
    });

    this.mistakeBookView = new MistakeBookView({
      container: this.contentEl,
      dataLoader: dataLoader,
      onPracticeMistake: async (qid, skillGroup) => {
        // Find chapter containing this question
        const q = dataLoader.getQuestion(qid);
        if (q) {
          this.router.navigate(`/quiz/${q.chapterId}/${q.lessonId}?mode=learn`);
        }
      }
    });

    this.historyView = new HistoryView({
      container: this.contentEl,
      dataLoader: dataLoader
    });
  }

  async init() {
    this.setupRoutes();
    this.setupNav();

    // Check backup reminder on startup
    this.checkBackupReminder();

    // Trigger initial route
    this.router.handleRoute();
  }

  checkBackupReminder() {
    const state = storage.loadState();
    const attempts = state.attempts || [];
    const lastBackupAt = state.settings ? state.settings.lastBackupAt : null;

    let showReminder = false;
    if (attempts.length >= 20 && !lastBackupAt) {
      showReminder = true;
    } else if (lastBackupAt) {
      const daysSince = (new Date() - new Date(lastBackupAt)) / (1000 * 60 * 60 * 24);
      if (daysSince >= 7 && attempts.length > 0) {
        showReminder = true;
      }
    }

    const banner = document.getElementById('backup-reminder-banner');
    if (banner) {
      if (showReminder) {
        banner.style.display = 'flex';
        banner.querySelector('.btn-banner-backup').onclick = () => {
          this.router.navigate('/history');
        };
        banner.querySelector('.btn-banner-close').onclick = () => {
          banner.style.display = 'none';
        };
      } else {
        banner.style.display = 'none';
      }
    }
  }

  setupNav() {
    window.addEventListener('hashchange', () => {
      audioPlayer.stop();
      const current = window.location.hash.split('?')[0] || '#/dashboard';
      this.navLinks.forEach(link => {
        if (link.getAttribute('href') === current) {
          link.classList.add('active');
        } else {
          link.classList.remove('active');
        }
      });
    });
  }

  setupRoutes() {
    this.router.addRoute('/dashboard', () => this.renderDashboard());
    this.router.addRoute('/path', () => this.renderLearningPath());
    this.router.addRoute('/lesson/:chapterId/:lessonId', (params) => {
      this.lessonView.render(params.chapterId, params.lessonId);
    });
    this.router.addRoute('/quiz/:chapterId/:lessonId', (params, query) => {
      const mode = query.get('mode') || 'learn';
      this.quizController.start(params.chapterId, params.lessonId, mode);
    });
    this.router.addRoute('/mistakes', () => this.mistakeBookView.render());
    this.router.addRoute('/history', () => this.historyView.render());
    this.router.addRoute('/about', () => this.renderAbout());
  }

  renderDataError(err) {
    this.contentEl.innerHTML = `
      <div class="card" style="text-align: center; padding: 40px 20px; max-width: 650px; margin: 40px auto;">
        <div style="font-size: 3rem; margin-bottom: 12px;">⚠️</div>
        <h2 style="color: #ef4444; margin-bottom: 12px;">Chưa tải được dữ liệu khóa học TOEIC!</h2>
        <p style="color: #64748b; margin-bottom: 20px;">Lỗi: <strong>${err.message || err}</strong></p>
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 16px; text-align: left; font-size: 0.95rem; line-height: 1.6; margin-bottom: 24px;">
          <strong style="color: #1e293b;">Hướng dẫn khắc phục:</strong>
          <ol style="margin-top: 8px; padding-left: 20px; color: #334155;">
            <li><strong>Chạy máy chủ web cục bộ:</strong> Trình duyệt chặn fetch khi mở file trực tiếp. Hãy chạy file <code>start_server.bat</code> hoặc mở terminal gõ: <code>python -m http.server 8000</code>.</li>
            <li><strong>Xóa cache trình duyệt:</strong> Nếu bạn từng chạy dự án khác trên localhost:8000, hãy nhấn tổ hợp phím <strong>Ctrl + Shift + R</strong> (hoặc <strong>Ctrl + F5</strong>) để tải mới hoàn toàn.</li>
          </ol>
        </div>
        <button class="btn btn-primary" onclick="window.location.reload()">🔄 Thử tải lại trang</button>
      </div>
    `;
  }

  async renderDashboard() {
    this.contentEl.innerHTML = '<div class="loading">Đang tải dữ liệu...</div>';
    try {
      await dataLoader.loadAllChapters();
      const course = await dataLoader.loadCourse();
      const state = storage.loadState();
      const derived = rebuildDerived(state, dataLoader);

    const totalPassed = derived.passedLessons.length;
    const totalQuestionsDone = derived.totalAttemptsCount;
    const accuracyPct = Math.round(derived.overallAccuracy * 100);

    // Find next lesson to study
    let nextChapterId = 'CH01';
    let nextLessonId = 'CH01-L01';
    let nextLessonTitle = 'Nghe từ mang thông tin chính';

    for (const ch of course.chapters) {
      const isUnlocked = derived.chapterStatus[ch.id] && derived.chapterStatus[ch.id].unlocked;
      if (!isUnlocked) continue;

      const chData = dataLoader.chapters.get(ch.id);
      if (!chData) continue;

      let found = false;
      for (const l of chData.lessons) {
        if (!derived.passedLessons.includes(l.lessonId)) {
          nextChapterId = ch.id;
          nextLessonId = l.lessonId;
          nextLessonTitle = l.title;
          found = true;
          break;
        }
      }
      if (found) break;

      // Check final test
      if (chData.finalTest && !derived.passedLessons.includes(chData.finalTest.id)) {
        nextChapterId = ch.id;
        nextLessonId = chData.finalTest.id;
        nextLessonTitle = chData.finalTest.title;
        break;
      }
    }

    const el = document.createElement('div');
    el.className = 'dashboard-view';
    el.innerHTML = `
      <!-- Welcome Hero -->
      <div class="hero-card">
        <div class="hero-content">
          <span class="hero-badge">Mục tiêu: TOEIC Listening 300/495</span>
          <h1 class="hero-title">Chào bạn! Hãy tiếp tục hành trình hôm nay.</h1>
          <p class="hero-subtitle">Phương pháp nghe hiểu theo phản xạ từ khóa, phân tích bẫy đề thi và chữa lỗi dứt điểm.</p>
          <div class="hero-action-row">
            <button class="btn-primary btn-large btn-continue-study">
              ▶ Tiếp tục học: <strong>${nextLessonId} — ${nextLessonTitle}</strong>
            </button>
            <button class="btn-secondary btn-large btn-view-mistakes">
              📕 Ôn câu sai (${derived.openMistakesCount})
            </button>
          </div>
        </div>
      </div>

      <!-- Stats Grid -->
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon">📚</div>
          <div class="stat-num">${totalPassed}</div>
          <div class="stat-label">Bài học đã vượt qua</div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">🎧</div>
          <div class="stat-num">${totalQuestionsDone}</div>
          <div class="stat-label">Lượt câu đã thực hiện</div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">🎯</div>
          <div class="stat-num">${accuracyPct}%</div>
          <div class="stat-label">Tỷ lệ chính xác tổng</div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">💡</div>
          <div class="stat-num">${derived.resolvedMistakesCount}</div>
          <div class="stat-label">Lỗi đã khắc phục</div>
        </div>
      </div>

      <!-- Quick Chapter Progress -->
      <div class="card-section">
        <h2 class="section-title">🗺️ Tiến độ các chương</h2>
        <div class="chapter-progress-grid">
          ${course.chapters.map(ch => {
            const chStatus = derived.chapterStatus[ch.id] || { unlocked: false, completed: false };
            const chData = dataLoader.chapters.get(ch.id);
            const totalL = chData ? chData.lessons.length + 1 : 6;
            const passedInCh = chData ? chData.lessons.filter(l => derived.passedLessons.includes(l.lessonId)).length + (derived.passedLessons.includes(`${ch.id}-FINAL`) ? 1 : 0) : 0;
            const chPct = Math.round((passedInCh / totalL) * 100);

            return `
              <div class="ch-card ${chStatus.unlocked ? 'unlocked' : 'locked'}">
                <div class="ch-card-header">
                  <span class="ch-tag">${ch.id}</span>
                  <span class="ch-lock-icon">${chStatus.unlocked ? (chStatus.completed ? '✓ Hoàn thành' : 'Đang học') : '🔒 Đã khóa'}</span>
                </div>
                <h3 class="ch-name">${ch.title}</h3>
                <p class="ch-desc">${ch.description}</p>
                <div class="ch-prog-bar">
                  <div class="ch-prog-fill" style="width: ${chPct}%"></div>
                </div>
                <div class="ch-prog-text">${passedInCh}/${totalL} phần hoàn thành (${chPct}%)</div>
              </div>
            `;
          }).join('')}
        </div>
      </div>
    `;

    el.querySelector('.btn-continue-study').onclick = () => {
      this.router.navigate(`/lesson/${nextChapterId}/${nextLessonId}`);
    };
    el.querySelector('.btn-view-mistakes').onclick = () => {
      this.router.navigate('/mistakes');
    };

    this.contentEl.innerHTML = '';
    this.contentEl.appendChild(el);
    } catch (err) {
      console.error('Render dashboard error:', err);
      this.renderDataError(err);
    }
  }

  async renderLearningPath() {
    this.contentEl.innerHTML = '<div class="loading">Đang tải lộ trình...</div>';
    try {
      await dataLoader.loadAllChapters();
      const course = await dataLoader.loadCourse();
      const state = storage.loadState();
      const derived = rebuildDerived(state, dataLoader);

    const el = document.createElement('div');
    el.className = 'learning-path-view';

    el.innerHTML = `
      <div class="path-header-card">
        <h1 class="page-title">🗺️ Lộ trình học TOEIC Listening 300</h1>
        <p class="page-subtitle">Hoàn thành bài kiểm tra cuối chương với tỷ lệ từ 80% trở lên để mở khóa chương tiếp theo.</p>
      </div>

      <div class="chapters-timeline">
        ${course.chapters.map(ch => {
          const chStatus = derived.chapterStatus[ch.id] || { unlocked: false, completed: false };
          const chData = dataLoader.chapters.get(ch.id);
          const isUnlocked = chStatus.unlocked;

          return `
            <div class="chapter-block ${isUnlocked ? 'unlocked' : 'locked'}">
              <div class="chapter-block-header">
                <div class="ch-title-wrap">
                  <span class="ch-pill">${ch.id}</span>
                  <h2>${ch.title}</h2>
                </div>
                <div class="ch-status-badge ${isUnlocked ? 'badge-open' : 'badge-lock'}">
                  ${isUnlocked ? (chStatus.completed ? '★ Đã hoàn thành chương' : '🔓 Đang mở') : '🔒 Cần đạt chương trước'}
                </div>
              </div>

              ${chData ? `
                <div class="lessons-grid">
                  ${chData.lessons.map(l => {
                    const isPassed = derived.passedLessons.includes(l.lessonId);
                    const bestScore = derived.lessonScores[l.lessonId];
                    return `
                      <div class="lesson-card ${isPassed ? 'passed' : ''} ${!isUnlocked ? 'disabled' : ''}" data-chid="${ch.id}" data-lid="${l.lessonId}">
                        <div class="l-card-header">
                          <span class="l-id">${l.lessonId}</span>
                          <span class="l-status-icon">${isPassed ? '✓ Đạt' : 'Chưa đạt'}</span>
                        </div>
                        <h4 class="l-title">${l.title}</h4>
                        <div class="l-meta">
                          <span>${l.questionIds.length} câu</span>
                          <span>Yêu cầu: ${l.passRule.minCorrect}/${l.passRule.total} (${l.passRule.percentage}%)</span>
                        </div>
                        ${bestScore ? `
                          <div class="l-score">Điểm cao nhất: <strong>${bestScore.correctCount}/${bestScore.totalCount}</strong> (${Math.round(bestScore.pct)}%)</div>
                        ` : ''}
                      </div>
                    `;
                  }).join('')}

                  <!-- Final Test Card -->
                  ${chData.finalTest ? `
                    <div class="lesson-card final-test-card ${derived.passedLessons.includes(chData.finalTest.id) ? 'passed' : ''} ${!isUnlocked ? 'disabled' : ''}" data-chid="${ch.id}" data-lid="${chData.finalTest.id}">
                      <div class="l-card-header">
                        <span class="l-id">${chData.finalTest.id}</span>
                        <span class="l-status-icon">${derived.passedLessons.includes(chData.finalTest.id) ? '✓ Đạt Final' : 'Kiểm tra tổng'}</span>
                      </div>
                      <h4 class="l-title">${chData.finalTest.title}</h4>
                      <div class="l-meta">
                        <span>${chData.finalTest.questionIds.length} câu mới</span>
                        <span>Yêu cầu: ${chData.finalTest.passRule.minCorrect}/${chData.finalTest.passRule.total} (80%)</span>
                      </div>
                    </div>
                  ` : ''}
                </div>
              ` : ''}
            </div>
          `;
        }).join('')}
      </div>
    `;

    // Lesson click handlers
    el.querySelectorAll('.lesson-card').forEach(card => {
      card.onclick = () => {
        if (card.classList.contains('disabled')) {
          alert('Chương này đang bị khóa. Hãy hoàn thành các chương trước để mở khóa!');
          return;
        }
        const chid = card.dataset.chid;
        const lid = card.dataset.lid;
        this.router.navigate(`/lesson/${chid}/${lid}`);
      };
    });

    this.contentEl.innerHTML = '';
    this.contentEl.appendChild(el);
    } catch (err) {
      console.error('Render learning path error:', err);
      this.renderDataError(err);
    }
  }

  async renderAbout() {
    this.contentEl.innerHTML = `
      <div class="about-view card-section">
        <h1 class="page-title">ℹ️ Giới thiệu & Bản quyền âm thanh</h1>
        <p><strong>TOEIC Listening 300</strong> là ứng dụng web học tập miễn phí, hoạt động 100% cục bộ trên trình duyệt qua GitHub Pages.</p>
        
        <h3>Giấy phép mã nguồn & Nguyên tắc</h3>
        <ul>
          <li>Mã nguồn static web: HTML5, CSS3, JavaScript ES6+ thuần túy.</li>
          <li>Không thu thập dữ liệu người dùng, không tài khoản, không cloud database.</li>
          <li>Lịch sử lưu trong LocalStorage thiết bị, hỗ trợ xuất/nhập sao lưu file JSON.</li>
        </ul>

        <h3>Bản quyền giọng đọc (Voice Models & License)</h3>
        <p>Ứng dụng chỉ sử dụng các mô hình âm thanh có giấy phép cho phép tái phân phối công khai âm thanh đã tổng hợp:</p>
        <ul>
          <li><strong>Giọng Nữ (us-female-01):</strong> Dựa trên Lessac Dataset (Giấy phép BSD-3-Clause).</li>
          <li><strong>Giọng Nam (us-male-01):</strong> Dựa trên Ryan Voice Corpus (Giấy phép Public Domain / CC0).</li>
        </ul>
        <p><em>Lưu ý: Bộ câu hỏi và tài liệu được biên soạn nhằm mục đích giáo dục, mô phỏng kỹ năng đề thi TOEIC Listening, không phải đề thi chính thức từ ETS.</em></p>
      </div>
    `;
  }
}

const app = new App();
window.addEventListener('DOMContentLoaded', () => {
  app.init();
});
