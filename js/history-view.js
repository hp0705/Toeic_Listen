/**
 * History & Backup View for TOEIC Listening 300
 * Complies with SPEC_WEB_APP.md section 5.7 and PROGRESS_STORAGE_SPEC.md
 */

import { storage } from './storage.js';
import { rebuildDerived } from './progress.js';
import { BackupManager } from './backup.js';

export class HistoryView {
  constructor(options = {}) {
    this.container = options.container;
    this.dataLoader = options.dataLoader;
  }

  async render() {
    if (!this.container) return;

    await this.dataLoader.loadAllChapters();
    const state = storage.loadState();
    const derived = rebuildDerived(state, this.dataLoader);
    const coachSummary = BackupManager.createCoachSummary(state, derived);

    const hasSnapshot = storage.hasSnapshot();
    const lastBackup = state.settings && state.settings.lastBackupAt 
      ? new Date(state.settings.lastBackupAt).toLocaleString('vi-VN')
      : 'Chưa từng sao lưu';

    const runs = [...(state.runs || [])].reverse();
    const attempts = [...(state.attempts || [])].reverse();

    const el = document.createElement('div');
    el.className = 'history-backup-view';

    el.innerHTML = `
      <div class="history-header-card">
        <h1 class="page-title">💾 Lịch sử học & Sao lưu tiến độ</h1>
        <p class="page-subtitle">Dữ liệu lưu 100% cục bộ trên trình duyệt. Hãy sao lưu định kỳ để tránh mất tiến độ khi dọn dẹp trình duyệt.</p>
      </div>

      <!-- Backup Controls Card -->
      <div class="card-section backup-actions-card">
        <h2 class="section-title">📦 Quản lý sao lưu</h2>
        <div class="backup-meta-row">
          <div>Lần sao lưu gần nhất: <strong>${lastBackup}</strong></div>
          <div>Tổng số lượt làm bài (Runs): <strong>${runs.length}</strong></div>
          <div>Tổng số câu đã làm (Attempts): <strong>${attempts.length}</strong></div>
        </div>

        <div class="backup-btn-grid">
          <button class="btn-primary btn-export">
            📥 Xuất bản sao lưu (JSON)
          </button>

          <label class="btn-secondary btn-import-label">
            📤 Nhập bản sao lưu (Gộp / Merge)
            <input type="file" accept=".json" class="file-import-input" style="display:none;"/>
          </label>

          <button class="btn-secondary btn-replace" title="Thay thế toàn bộ dữ liệu hiện tại bằng file">
            🔄 Nhập thay thế
          </button>

          ${hasSnapshot ? `
            <button class="btn-warning btn-undo">
              ↩ Hoàn tác lần nhập gần nhất
            </button>
          ` : ''}

          <button class="btn-danger btn-reset">
            ⚠️ Đặt lại toàn bộ tiến độ
          </button>
        </div>
      </div>

      <!-- Coach Summary -->
      ${coachSummary ? `
        <div class="card-section coach-summary-card">
          <div class="summary-header">
            <h2 class="section-title">📊 Tóm tắt tiến độ học tập (Coach Summary)</h2>
            <button class="btn-sm btn-copy-summary">📋 Sao chép tóm tắt</button>
          </div>
          <div class="summary-content">
            <pre class="summary-pre">${JSON.stringify(coachSummary, null, 2)}</pre>
          </div>
        </div>
      ` : ''}

      <!-- Recent Runs List -->
      <div class="card-section runs-list-card">
        <h2 class="section-title">⏱️ Các phiên làm bài gần đây</h2>
        ${runs.length === 0 ? `
          <p class="empty-msg">Chưa có bài làm nào.</p>
        ` : `
          <div class="runs-table-wrap">
            <table class="runs-table">
              <thead>
                <tr>
                  <th>Thời gian</th>
                  <th>Chương / Bài</th>
                  <th>Chế độ</th>
                  <th>Trạng thái</th>
                  <th>Số câu</th>
                </tr>
              </thead>
              <tbody>
                ${runs.slice(0, 15).map(r => `
                  <tr>
                    <td>${new Date(r.startedAt).toLocaleString('vi-VN')}</td>
                    <td><strong>${r.lessonId}</strong> (${r.chapterId})</td>
                    <td><span class="mode-tag ${r.mode}">${r.mode === 'learn' ? 'Luyện tập' : 'Kiểm tra'}</span></td>
                    <td><span class="status-tag ${r.status}">${r.status === 'submitted' ? 'Đã hoàn thành' : 'Đang làm'}</span></td>
                    <td>${r.optionOrders ? Object.keys(r.optionOrders).length : '-'}</td>
                  </tr>
                `).join('')}
              </tbody>
            </table>
          </div>
        `}
      </div>
    `;

    // Event Handlers
    el.querySelector('.btn-export').onclick = () => {
      BackupManager.exportBackup(this.dataLoader);
      this.render();
    };

    const importInput = el.querySelector('.file-import-input');
    importInput.onchange = (e) => {
      const file = e.target.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = (evt) => {
        try {
          const res = BackupManager.importBackup(evt.target.result, 'merge');
          alert(`Nhập gộp thành công! Đã thêm ${res.newRunsCount} lượt làm bài và ${res.newAttemptsCount} câu trả lời mới.`);
          this.render();
        } catch (err) {
          alert('Lỗi nhập dữ liệu: ' + err.message);
        }
      };
      reader.readAsText(file);
    };

    el.querySelector('.btn-replace').onclick = () => {
      const confirmed = confirm('CẢNH BÁO: Chế độ Thay thế sẽ ghi đè toàn bộ dữ liệu hiện tại bằng file nhập. Bạn có muốn tiếp tục?');
      if (!confirmed) return;

      const input = document.createElement('input');
      input.type = 'file';
      input.accept = '.json';
      input.onchange = (e) => {
        const file = e.target.files[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = (evt) => {
          try {
            const res = BackupManager.importBackup(evt.target.result, 'replace');
            alert(`Nhập thay thế thành công! Tổng cộng có ${res.totalRuns} bài làm và ${res.totalAttempts} câu trả lời.`);
            this.render();
          } catch (err) {
            alert('Lỗi: ' + err.message);
          }
        };
        reader.readAsText(file);
      };
      input.click();
    };

    const undoBtn = el.querySelector('.btn-undo');
    if (undoBtn) {
      undoBtn.onclick = () => {
        const restored = storage.restoreSnapshot();
        if (restored) {
          alert('Đã hoàn tác khôi phục dữ liệu trước lần nhập!');
          this.render();
        } else {
          alert('Không tìm thấy bản chụp hoàn tác.');
        }
      };
    }

    el.querySelector('.btn-reset').onclick = () => {
      const confirmed = confirm('CẢNH BÁO NGUY HIỂM: Bạn có chắc chắn muốn xóa toàn bộ lịch sử học tập để bắt đầu lại từ đầu?');
      if (confirmed) {
        storage.resetProgress();
        alert('Đã đặt lại tiến độ.');
        this.render();
      }
    };

    const copyBtn = el.querySelector('.btn-copy-summary');
    if (copyBtn) {
      copyBtn.onclick = () => {
        navigator.clipboard.writeText(JSON.stringify(coachSummary, null, 2)).then(() => {
          copyBtn.textContent = '✓ Đã sao chép!';
          setTimeout(() => { copyBtn.textContent = '📋 Sao chép tóm tắt'; }, 2000);
        });
      };
    }

    this.container.innerHTML = '';
    this.container.appendChild(el);
  }
}
