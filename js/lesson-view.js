/**
 * Lesson View for TOEIC Listening 300
 * Renders lesson objectives, teaching blocks, comparisons, ABX discrimination,
 * dictation (nghe-chép), vocabulary, audio examples, and final test intro.
 */

import { audioPlayer } from './audio-player.js';

function formatMarkdown(content) {
  if (!content) return '';
  let html = content;

  // Convert markdown tables
  html = html.replace(/((?:\|[^\n]+\|\r?\n)+)/g, (tableMatch) => {
    const lines = tableMatch.trim().split(/\r?\n/).map(l => l.trim()).filter(Boolean);
    if (lines.length < 2) return tableMatch;

    const parseCells = (line) => {
      const parts = line.split('|');
      return parts.slice(1, -1).map(c => c.trim());
    };

    const headers = parseCells(lines[0]);
    const rows = lines.slice(2);

    let tbl = '<div class="table-responsive"><table class="vocab-table content-table"><thead><tr>';
    headers.forEach(h => {
      tbl += `<th>${h.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')}</th>`;
    });
    tbl += '</tr></thead><tbody>';

    rows.forEach(r => {
      const cells = parseCells(r);
      if (cells.length > 0) {
        tbl += '<tr>';
        cells.forEach(c => {
          let cellFormatted = c
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/`([^`]+)`/g, '<code>$1</code>');
          tbl += `<td>${cellFormatted}</td>`;
        });
        tbl += '</tr>';
      }
    });
    tbl += '</tbody></table></div>';
    return tbl;
  });

  // Convert bold, italic, code
  html = html
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/`([^`]+)`/g, '<code>$1</code>');

  // Convert bullet lists
  html = html.replace(/((?:^[ \t]*[-*][ \t]+[^\n]+\r?\n?)+)/gm, (listMatch) => {
    const items = listMatch.trim().split(/\r?\n/).map(l => l.replace(/^[ \t]*[-*][ \t]+/, '').trim());
    return `<ul class="teaching-list">${items.map(it => `<li>${it}</li>`).join('')}</ul>`;
  });

  // Convert numbered lists
  html = html.replace(/((?:^[ \t]*\d+\.[ \t]+[^\n]+\r?\n?)+)/gm, (listMatch) => {
    const items = listMatch.trim().split(/\r?\n/).map(l => l.replace(/^[ \t]*\d+\.[ \t]+/, '').trim());
    return `<ol class="teaching-list">${items.map(it => `<li>${it}</li>`).join('')}</ol>`;
  });

  // Convert double newlines to paragraph tags if not inside div/table
  html = html.split(/\n\n+/).map(p => {
    const trimmed = p.trim();
    if (trimmed.startsWith('<div') || trimmed.startsWith('<ul') || trimmed.startsWith('<ol') || trimmed.startsWith('<table')) {
      return trimmed;
    }
    return `<p style="margin: 0.6rem 0; line-height: 1.7;">${trimmed.replace(/\n/g, '<br>')}</p>`;
  }).join('');

  return html;
}

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
              <div class="teaching-content">${formatMarkdown(tb.content)}</div>
            </div>
          `).join('')}
        </div>
      ` : ''}

      <!-- Contrastive Listening / Minimal Pairs Comparisons -->
      ${lesson.comparisons && lesson.comparisons.length > 0 ? `
        <div class="card-section comparisons-section">
          <h2 class="section-title">⚡ Luyện nghe đối chiếu (Minimal Pairs)</h2>
          <p class="section-sub">Nghe so sánh trực tiếp hai từ/câu để tai nhận biết sự khác biệt tinh tế, tránh bẫy đề thi:</p>
          
          ${lesson.comparisons.map(comp => `
            <div class="comparison-group">
              <h3 class="comp-group-title">🔍 ${comp.title}</h3>
              ${comp.tip ? `<div class="comp-group-tip">💡 <strong>Mẹo nghe:</strong> ${comp.tip}</div>` : ''}
              
              <div class="comp-pairs-grid">
                ${comp.pairs.map(p => `
                  <div class="comp-pair-card">
                    <div class="pair-side side-a">
                      <div class="pair-header">
                        <span class="pair-word">${p.wordA}</span>
                        <span class="pair-ipa">${p.ipaA || ''}</span>
                      </div>
                      <div class="pair-desc">${p.descA}</div>
                      <button class="btn-play-word btn-play-a" data-text="${p.wordA}">▶ Nghe từ A</button>
                    </div>

                    <div class="pair-divider">
                      <button class="btn-play-both" data-text-a="${p.wordA}" data-text-b="${p.wordB}" title="Nghe từ A rồi đến từ B để so sánh">
                        ▶▶ Nghe A rồi B
                      </button>
                    </div>

                    <div class="pair-side side-b">
                      <div class="pair-header">
                        <span class="pair-word">${p.wordB}</span>
                        <span class="pair-ipa">${p.ipaB || ''}</span>
                      </div>
                      <div class="pair-desc">${p.descB}</div>
                      <button class="btn-play-word btn-play-b" data-text="${p.wordB}">▶ Nghe từ B</button>
                    </div>
                  </div>
                `).join('')}
              </div>
            </div>
          `).join('')}
        </div>
      ` : ''}

      <!-- ABX Discrimination Exercises -->
      ${lesson.abxExercises && lesson.abxExercises.length > 0 ? `
        <div class="card-section abx-section">
          <h2 class="section-title">⚡ Luyện nghe đối chiếu (ABX Discrimination)</h2>
          <p class="section-sub">Nghe A, nghe B, rồi nghe X (ẩn). Chọn xem X giống A hay B để rèn phản xạ nhận biết âm/từ chức năng tinh tế:</p>
          <div class="abx-grid">
            ${lesson.abxExercises.map(item => `
              <div class="abx-card" data-abx-id="${item.id}" data-answer="${item.correctAnswer}" data-text-a="${item.textA.replace(/"/g, '&quot;')}" data-text-b="${item.textB.replace(/"/g, '&quot;')}" data-text-x="${item.textX.replace(/"/g, '&quot;')}">
                <div class="abx-card-header">
                  <span class="abx-id-badge">${item.id}</span>
                  <div class="abx-tags">
                    ${(item.tags || []).map(t => `<span class="abx-tag">${t}</span>`).join('')}
                  </div>
                </div>
                <div class="abx-options-row">
                  <div class="abx-option-item">
                    <button class="abx-btn-audio btn-play-abx-a">▶ A</button>
                    <span>${item.textA}</span>
                  </div>
                  <div class="abx-option-item">
                    <button class="abx-btn-audio btn-play-abx-b">▶ B</button>
                    <span>${item.textB}</span>
                  </div>
                  <div class="abx-option-item">
                    <button class="abx-btn-audio btn-play-abx-x" style="background: #eef2ff; color: var(--primary);">❓ Nghe X (ẩn)</button>
                    <em>Âm thanh cần đoán</em>
                  </div>
                </div>
                <button class="abx-btn-play-all btn-play-abx-all">▶▶ Nghe chuỗi A → B → X</button>
                <div class="abx-decision-row">
                  <button class="abx-choice-btn btn-choice-a" data-choice="A">X giống A</button>
                  <button class="abx-choice-btn btn-choice-b" data-choice="B">X giống B</button>
                </div>
                <div class="abx-feedback" style="display:none;"></div>
              </div>
            `).join('')}
          </div>
        </div>
      ` : ''}

      <!-- Dictation Exercises -->
      ${lesson.dictations && lesson.dictations.length > 0 ? `
        <div class="card-section dictation-section">
          <h2 class="section-title">✍️ Luyện nghe-chép (Dictation)</h2>
          <p class="section-sub">Nghe audio và gõ các từ hoặc số còn thiếu vào ô trống. Giúp tai ép não nhận diện âm thật:</p>
          <div class="dictation-list">
            ${lesson.dictations.map((item) => {
              let partIdx = 0;
              const formattedSentence = item.audioText.replace(/\*\*(.*?)\*\*/g, (match, word) => {
                const p = `<input type="text" class="dictation-input" data-expected="${word.replace(/"/g, '&quot;')}" placeholder="..." autocomplete="off" />`;
                partIdx++;
                return p;
              });
              return `
                <div class="dictation-card" data-dict-id="${item.id}" data-audio-text="${item.audioText.replace(/"/g, '&quot;')}">
                  <div class="dictation-header">
                    <div style="display:flex; align-items:center; gap:0.5rem;">
                      <button class="abx-btn-audio btn-play-dict" data-file="${item.audioFile}" data-text="${item.audioText.replace(/\*\*/g, '').replace(/"/g, '&quot;')}">▶ Nghe câu</button>
                      <span class="abx-id-badge">${item.id}</span>
                    </div>
                    <div class="abx-tags">
                      ${(item.tags || []).map(t => `<span class="abx-tag">${t}</span>`).join('')}
                    </div>
                  </div>
                  <div class="dictation-sentence">${formattedSentence}</div>
                  <div class="dictation-actions">
                    <button class="btn-primary btn-check-dict" style="padding: 0.35rem 0.85rem; font-size: 0.85rem;">Kiểm tra</button>
                    <button class="btn-secondary btn-reveal-dict" style="padding: 0.35rem 0.85rem; font-size: 0.85rem;">Xem đáp án</button>
                  </div>
                  <div class="dictation-feedback" style="display:none;"></div>
                </div>
              `;
            }).join('')}
          </div>
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

    // Comparison audio play handlers
    el.querySelectorAll('.btn-play-word').forEach(btn => {
      btn.onclick = () => {
        const text = btn.dataset.text;
        audioPlayer.playWord(text);
      };
    });

    el.querySelectorAll('.btn-play-both').forEach(btn => {
      btn.onclick = () => {
        const textA = btn.dataset.textA;
        const textB = btn.dataset.textB;
        audioPlayer.playComparisonPair(textA, textB);
      };
    });

    // ABX handlers
    el.querySelectorAll('.abx-card').forEach(card => {
      const textA = card.dataset.textA;
      const textB = card.dataset.textB;
      const textX = card.dataset.textX;
      const correctAns = card.dataset.answer;
      const feedbackEl = card.querySelector('.abx-feedback');

      card.querySelector('.btn-play-abx-a').onclick = () => audioPlayer.playWord(textA);
      card.querySelector('.btn-play-abx-b').onclick = () => audioPlayer.playWord(textB);
      card.querySelector('.btn-play-abx-x').onclick = () => audioPlayer.playWord(textX);
      card.querySelector('.btn-play-abx-all').onclick = () => audioPlayer.playABXSequence(textA, textB, textX);

      const handleChoice = (chosen) => {
        const isRight = chosen === correctAns;
        const btnA = card.querySelector('.btn-choice-a');
        const btnB = card.querySelector('.btn-choice-b');
        btnA.className = 'abx-choice-btn btn-choice-a';
        btnB.className = 'abx-choice-btn btn-choice-b';

        const chosenBtn = chosen === 'A' ? btnA : btnB;
        if (isRight) {
          chosenBtn.classList.add('selected-correct');
          feedbackEl.className = 'abx-feedback feedback-correct';
          feedbackEl.innerHTML = `✅ Chính xác! X chính là (${correctAns}): <strong>${textX}</strong>`;
        } else {
          chosenBtn.classList.add('selected-wrong');
          feedbackEl.className = 'abx-feedback feedback-wrong';
          feedbackEl.innerHTML = `❌ Chưa đúng! X thực ra là (${correctAns}): <strong>${textX}</strong>. Hãy bấm "Nghe chuỗi" để so sánh lại nhé!`;
        }
        feedbackEl.style.display = 'block';
      };

      card.querySelector('.btn-choice-a').onclick = () => handleChoice('A');
      card.querySelector('.btn-choice-b').onclick = () => handleChoice('B');
    });

    // Dictation handlers
    el.querySelectorAll('.dictation-card').forEach(card => {
      const audioText = card.dataset.audioText;
      const playBtn = card.querySelector('.btn-play-dict');
      const checkBtn = card.querySelector('.btn-check-dict');
      const revealBtn = card.querySelector('.btn-reveal-dict');
      const feedbackEl = card.querySelector('.dictation-feedback');
      const inputs = card.querySelectorAll('.dictation-input');

      playBtn.onclick = () => {
        audioPlayer.playFileOrSpeech(playBtn.dataset.file, playBtn.dataset.text);
      };

      const checkInputs = () => {
        let correctCount = 0;
        inputs.forEach(inp => {
          const expected = (inp.dataset.expected || '').trim().toLowerCase().replace(/[.,/#!$%^&*;:{}=\-_`~()]/g, '');
          const val = inp.value.trim().toLowerCase().replace(/[.,/#!$%^&*;:{}=\-_`~()]/g, '');
          inp.classList.remove('correct', 'incorrect');
          if (expected === val) {
            inp.classList.add('correct');
            correctCount++;
          } else {
            inp.classList.add('incorrect');
          }
        });

        if (correctCount === inputs.length) {
          feedbackEl.className = 'dictation-feedback feedback-correct';
          feedbackEl.innerHTML = `🎉 Hoàn hảo! Bạn đã nghe và điền đúng tất cả các từ khóa.`;
        } else {
          feedbackEl.className = 'dictation-feedback feedback-wrong';
          feedbackEl.innerHTML = `Bạn đúng ${correctCount}/${inputs.length} ô. Ô màu đỏ chưa chính xác, hãy nghe lại hoặc bấm "Xem đáp án".`;
        }
        feedbackEl.style.display = 'block';
      };

      checkBtn.onclick = checkInputs;
      inputs.forEach(inp => {
        inp.onkeydown = (e) => {
          if (e.key === 'Enter') checkInputs();
        };
      });

      revealBtn.onclick = () => {
        inputs.forEach(inp => {
          inp.value = inp.dataset.expected || '';
          inp.classList.remove('incorrect');
          inp.classList.add('correct');
        });
        feedbackEl.className = 'dictation-feedback feedback-correct';
        feedbackEl.innerHTML = `Câu hoàn chỉnh: <strong>${audioText.replace(/\*\*/g, '')}</strong>`;
        feedbackEl.style.display = 'block';
      };
    });

    // Example audio play handlers
    el.querySelectorAll('.btn-play-sm').forEach(btn => {
      btn.onclick = () => {
        const file = btn.dataset.file;
        const text = btn.dataset.text;
        audioPlayer.playFileOrSpeech(file, text);
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
        <h2 class="section-title">📋 Cấu trúc bài kiểm tra (30 câu)</h2>
        <p>Bài kiểm tra đánh giá toàn diện năng lực nghe ở tốc độ chuẩn 1.0x không xem transcript:</p>
        <ul class="test-rules-list">
          <li><strong>Phần A — Nghe-chép (10 câu):</strong> Nghe và gõ lại số, giờ, ngày tháng, giá tiền và từ nối/âm cuối (Đạt ≥ 7/10).</li>
          <li><strong>Phần B — Part 2 phản hồi phù hợp (14 câu):</strong> Nghe câu hỏi và 3 phản hồi, chọn phản hồi đúng với đầy đủ các dạng bẫy (Đạt ≥ 10/14).</li>
          <li><strong>Phần C — Hội thoại ngắn (6 câu):</strong> 3 đoạn hội thoại 2 người, nắm ý chính và chi tiết quan trọng (Đạt ≥ 4/6).</li>
          <li><strong>Tổng điểm cần đạt:</strong> Đúng từ <strong>24/30 câu (80%)</strong> để qua chương và mở khóa chương tiếp theo.</li>
        </ul>
      </div>

      <div class="card-section warning-box">
        <h3 class="warning-title">⚠️ Lưu ý khi làm bài kiểm tra:</h3>
        <p>Không bấm xem transcript hoặc dừng bài giữa chừng. Hệ thống sẽ tự động chẩn đoán nhóm lỗi theo tag (Phụ lục A) để bạn ôn lại hiệu quả nhất.</p>
      </div>

      <div class="lesson-actions-card">
        <h3>Bắt đầu bài kiểm tra ngay?</h3>
        <div class="action-btn-row">
          <button class="btn-primary btn-large btn-start-final-test">
            <span class="btn-icon">🚀</span>
            <div class="btn-label-wrap">
              <strong>Bắt đầu làm bài kiểm tra (30 câu)</strong>
              <small>Tốc độ chuẩn 1.0x, nộp bài tính điểm</small>
            </div>
          </button>
        </div>
      </div>
    `;

    el.querySelector('.btn-start-final-test').onclick = () => {
      this.onStartQuiz(chapter.chapterId, finalTest.id, 'test');
    };

    this.container.innerHTML = '';
    this.container.appendChild(el);
  }
}
