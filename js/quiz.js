/**
 * Quiz & Practice Controller for TOEIC Listening 300
 * Handles question presentation, option shuffling, optionsVisibleBeforeAnswer,
 * audio playback, attempt recording, and explanations.
 */

import { storage } from './storage.js';
import { audioPlayer } from './audio-player.js';

export class QuizController {
  constructor(options = {}) {
    this.dataLoader = options.dataLoader;
    this.onFinish = options.onFinish || (() => {});
    this.container = options.container;

    this.run = null;
    this.questions = [];
    this.groups = [];
    this.currentIndex = 0;
    this.currentGroupIndex = 0;
    this.mode = 'learn'; // 'learn' or 'test'
    this.viewedTranscript = false;
    this.answers = new Map(); // questionId -> selectedChoiceId (original ID)
    this.submitted = false;
  }

  shuffle(array) {
    const arr = [...array];
    for (let i = arr.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    return arr;
  }

  async start(chapterId, lessonId, mode = 'learn', existingRunId = null) {
    this.mode = mode;
    this.submitted = false;
    this.answers.clear();
    this.viewedTranscript = false;

    const chapter = await this.dataLoader.loadChapter(chapterId);

    // Determine question list
    if (lessonId.endsWith('-FINAL')) {
      const qids = chapter.finalTest.questionIds;
      this.questions = qids.map(id => this.dataLoader.getQuestion(id)).filter(Boolean);
    } else {
      const lesson = chapter.lessons.find(l => l.lessonId === lessonId);
      if (!lesson) throw new Error(`Lesson ${lessonId} not found`);
      this.questions = lesson.questionIds.map(id => this.dataLoader.getQuestion(id)).filter(Boolean);
    }

    if (this.questions.length === 0) {
      alert('Không tìm thấy câu hỏi cho bài học này.');
      return;
    }

    // Check if Part 3 groups exist
    const isPart3 = this.questions.some(q => q.part === 3 && q.groupId);
    if (isPart3) {
      const groupIds = [...new Set(this.questions.map(q => q.groupId).filter(Boolean))];
      this.groups = groupIds.map(gid => this.dataLoader.getGroup(gid)).filter(Boolean);
    } else {
      this.groups = [];
    }

    // Load or create run
    const state = storage.loadState();
    let currentRun = null;

    if (existingRunId) {
      currentRun = state.runs.find(r => r.id === existingRunId);
    }

    if (!currentRun || currentRun.status === 'submitted') {
      // Create new run
      const optionOrders = {};
      for (const q of this.questions) {
        const originalKeys = Object.keys(q.options);
        optionOrders[q.id] = this.shuffle(originalKeys);
      }

      currentRun = {
        id: `run-${Date.now()}-${Math.random().toString(36).substring(2, 7)}`,
        chapterId,
        lessonId,
        mode,
        startedAt: new Date().toISOString(),
        finishedAt: null,
        status: 'in_progress',
        optionOrders
      };

      state.runs.push(currentRun);
      storage.saveState(state);
    }

    this.run = currentRun;
    this.currentIndex = 0;
    this.currentGroupIndex = 0;
    audioPlayer.setRate(1.0);

    this.render();
  }

  getOptionOrder(questionId) {
    if (this.run && this.run.optionOrders && this.run.optionOrders[questionId]) {
      return this.run.optionOrders[questionId];
    }
    const q = this.dataLoader.getQuestion(questionId);
    return q ? Object.keys(q.options) : ['A', 'B', 'C', 'D'];
  }

  handleAnswer(questionId, displayedIndex) {
    if (this.mode === 'learn' && this.answers.has(questionId)) {
      return; // Already answered in learn mode
    }

    const order = this.getOptionOrder(questionId);
    const selectedOriginalId = order[displayedIndex];
    this.answers.set(questionId, selectedOriginalId);

    const q = this.dataLoader.getQuestion(questionId);
    const isCorrect = (selectedOriginalId === q.correctAnswer);

    // Save attempt
    const state = storage.loadState();
    const attempt = {
      id: `attempt-${Date.now()}-${Math.random().toString(36).substring(2, 7)}`,
      runId: this.run.id,
      questionId: q.id,
      groupId: q.groupId || null,
      chapterId: q.chapterId,
      lessonId: q.lessonId,
      part: q.part,
      mode: this.mode,
      selected: selectedOriginalId,
      optionOrder: order,
      isCorrect: isCorrect,
      questionRevision: q.revision || 1,
      answeredAt: new Date().toISOString(),
      transcriptViewedBeforeAnswer: this.viewedTranscript,
      playbackRate: audioPlayer.playbackRate,
      mistakeGroup: null
    };

    state.attempts.push(attempt);
    storage.saveState(state);

    if (this.mode === 'learn') {
      this.render();
    } else {
      // In test mode, advance or update UI
      this.render();
    }
  }

  submitTest() {
    this.submitted = true;
    const state = storage.loadState();
    const run = state.runs.find(r => r.id === this.run.id);
    if (run) {
      run.status = 'submitted';
      run.finishedAt = new Date().toISOString();
      storage.saveState(state);
    }
    this.render();
  }

  finishQuiz() {
    audioPlayer.stop();
    const state = storage.loadState();
    const run = state.runs.find(r => r.id === this.run.id);
    if (run && run.status !== 'submitted') {
      run.status = 'submitted';
      run.finishedAt = new Date().toISOString();
      storage.saveState(state);
    }
    this.onFinish(this.run);
  }

  render() {
    if (!this.container) return;
    this.container.innerHTML = '';

    const isPart3 = this.groups.length > 0;
    if (isPart3) {
      this.renderPart3Group();
    } else {
      this.renderSingleQuestion();
    }
  }

  renderSingleQuestion() {
    const q = this.questions[this.currentIndex];
    const total = this.questions.length;
    const order = this.getOptionOrder(q.id);
    const userAnswer = this.answers.get(q.id);
    const isAnswered = userAnswer !== undefined;
    const isCorrect = isAnswered && (userAnswer === q.correctAnswer);

    const card = document.createElement('div');
    card.className = 'quiz-card';

    // Header progress
    const header = document.createElement('div');
    header.className = 'quiz-header';
    header.innerHTML = `
      <div class="quiz-badge">Câu ${this.currentIndex + 1} / ${total} • ${this.mode === 'learn' ? 'Chế độ Luyện tập' : 'Chế độ Kiểm tra'}</div>
      <div class="quiz-skill-tag">${q.skillGroup ? q.skillGroup.replace(/_/g, ' ') : ''}</div>
    `;
    card.appendChild(header);

    // Audio Player Controls
    const playerBox = document.createElement('div');
    playerBox.className = 'player-box';

    const playBtn = document.createElement('button');
    playBtn.className = 'btn-play';
    playBtn.innerHTML = `<span>▶ Phát Audio</span>`;
    playBtn.onclick = () => {
      audioPlayer.playSegments(q.audioSegments, order);
    };
    playerBox.appendChild(playBtn);

    // Speed controls for Learn mode
    if (this.mode === 'learn') {
      const speedBox = document.createElement('div');
      speedBox.className = 'speed-toggles';
      speedBox.innerHTML = `
        <button class="btn-speed ${audioPlayer.playbackRate === 1.0 ? 'active' : ''}" data-rate="1.0">1.0x</button>
        <button class="btn-speed ${audioPlayer.playbackRate === 0.85 ? 'active' : ''}" data-rate="0.85">0.85x</button>
      `;
      speedBox.querySelectorAll('.btn-speed').forEach(btn => {
        btn.onclick = (e) => {
          const rate = parseFloat(e.target.dataset.rate);
          audioPlayer.setRate(rate);
          speedBox.querySelectorAll('.btn-speed').forEach(b => b.classList.remove('active'));
          e.target.classList.add('active');
        };
      });
      playerBox.appendChild(speedBox);
    }
    card.appendChild(playerBox);

    // Image if Part 1
    if (q.part === 1 && q.image) {
      const imgWrap = document.createElement('div');
      imgWrap.className = 'quiz-image-wrap';
      imgWrap.innerHTML = `<img src="${q.image}" alt="TOEIC Part 1 Image" class="part1-image"/>`;
      card.appendChild(imgWrap);
    }

    // Question Prompt
    if (q.prompt) {
      const promptEl = document.createElement('div');
      promptEl.className = 'quiz-prompt';
      promptEl.textContent = q.prompt;
      card.appendChild(promptEl);
    }

    // Options list
    const optionsWrap = document.createElement('div');
    optionsWrap.className = 'quiz-options';

    const labels = ['A', 'B', 'C', 'D'];
    const showOptionText = q.optionsVisibleBeforeAnswer || isAnswered || (this.mode === 'test' && this.submitted);

    order.forEach((optKey, idx) => {
      const optBtn = document.createElement('button');
      optBtn.className = 'quiz-option-btn';

      const label = labels[idx];
      const optText = q.options[optKey];

      if (isAnswered || (this.mode === 'test' && this.submitted)) {
        if (optKey === q.correctAnswer) {
          optBtn.classList.add('correct');
        } else if (optKey === userAnswer) {
          optBtn.classList.add('incorrect');
        }
      }

      if (showOptionText) {
        optBtn.innerHTML = `<span class="opt-label">${label}</span> <span class="opt-text">${optText}</span>`;
      } else {
        // Part 1 & 2: Hide text before answer to force listening!
        optBtn.innerHTML = `<span class="opt-label large">${label}</span>`;
      }

      optBtn.onclick = () => {
        if (!isAnswered || this.mode === 'test') {
          this.handleAnswer(q.id, idx);
        }
      };

      optionsWrap.appendChild(optBtn);
    });
    card.appendChild(optionsWrap);

    // Explanations (in Learn mode after answer, or Test mode after submission)
    if ((this.mode === 'learn' && isAnswered) || (this.mode === 'test' && this.submitted)) {
      const explainBox = document.createElement('div');
      explainBox.className = 'explanation-box';
      explainBox.innerHTML = `
        <div class="result-banner ${isCorrect ? 'banner-correct' : 'banner-wrong'}">
          ${isCorrect ? '✓ Chính xác!' : '✗ Chưa đúng!'} Đáp án đúng: <strong>${q.correctAnswer}</strong>
        </div>
        <div class="exp-section">
          <h4>Giải thích đáp án:</h4>
          <p>${q.explanation}</p>
        </div>
        ${q.wrongReasons && Object.keys(q.wrongReasons).length > 0 ? `
          <div class="exp-section">
            <h4>Phân tích phương án sai:</h4>
            <ul>
              ${Object.entries(q.wrongReasons).map(([k, r]) => `<li><strong>(${k}):</strong> ${r}</li>`).join('')}
            </ul>
          </div>
        ` : ''}
        <div class="exp-section transcript-section">
          <h4>Transcript & Bản dịch:</h4>
          <p class="transcript-text">${q.transcript}</p>
          ${q.translation ? `<p class="translation-text">${q.translation}</p>` : ''}
        </div>
      `;
      card.appendChild(explainBox);
    }

    // Navigation buttons
    const navBox = document.createElement('div');
    navBox.className = 'quiz-nav';

    if (this.currentIndex > 0) {
      const prevBtn = document.createElement('button');
      prevBtn.className = 'btn-secondary';
      prevBtn.textContent = '← Câu trước';
      prevBtn.onclick = () => {
        audioPlayer.stop();
        this.currentIndex--;
        this.render();
      };
      navBox.appendChild(prevBtn);
    }

    if (this.currentIndex < total - 1) {
      const nextBtn = document.createElement('button');
      nextBtn.className = 'btn-primary';
      nextBtn.textContent = 'Câu tiếp →';
      nextBtn.onclick = () => {
        audioPlayer.stop();
        this.currentIndex++;
        this.render();
      };
      navBox.appendChild(nextBtn);
    } else {
      const finishBtn = document.createElement('button');
      finishBtn.className = 'btn-finish';
      finishBtn.textContent = this.mode === 'test' ? 'Nộp bài kiểm tra' : 'Hoàn thành bài';
      finishBtn.onclick = () => {
        if (this.mode === 'test' && !this.submitted) {
          this.submitTest();
        } else {
          this.finishQuiz();
        }
      };
      navBox.appendChild(finishBtn);
    }

    card.appendChild(navBox);
    this.container.appendChild(card);
  }

  renderPart3Group() {
    const group = this.groups[this.currentGroupIndex];
    const totalGroups = this.groups.length;
    const groupQuestions = this.questions.filter(q => q.groupId === group.id);

    const allGroupAnswered = groupQuestions.every(q => this.answers.has(q.id));

    const card = document.createElement('div');
    card.className = 'quiz-card part3-card';

    // Header
    const header = document.createElement('div');
    header.className = 'quiz-header';
    header.innerHTML = `
      <div class="quiz-badge">Hội thoại ${this.currentGroupIndex + 1} / ${totalGroups} (Part 3)</div>
      <div class="quiz-skill-tag">${group.context || 'Hội thoại 2 người'}</div>
    `;
    card.appendChild(header);

    // Audio controls for group
    const playerBox = document.createElement('div');
    playerBox.className = 'player-box';

    const playBtn = document.createElement('button');
    playBtn.className = 'btn-play';
    playBtn.innerHTML = `<span>▶ Phát toàn bộ hội thoại</span>`;
    playBtn.onclick = () => {
      audioPlayer.playGroup(group.audioFile, 0, null, group.transcript);
    };
    playerBox.appendChild(playBtn);

    if (this.mode === 'learn') {
      const speedBox = document.createElement('div');
      speedBox.className = 'speed-toggles';
      speedBox.innerHTML = `
        <button class="btn-speed ${audioPlayer.playbackRate === 1.0 ? 'active' : ''}" data-rate="1.0">1.0x</button>
        <button class="btn-speed ${audioPlayer.playbackRate === 0.85 ? 'active' : ''}" data-rate="0.85">0.85x</button>
      `;
      speedBox.querySelectorAll('.btn-speed').forEach(btn => {
        btn.onclick = (e) => {
          const rate = parseFloat(e.target.dataset.rate);
          audioPlayer.setRate(rate);
          speedBox.querySelectorAll('.btn-speed').forEach(b => b.classList.remove('active'));
          e.target.classList.add('active');
        };
      });
      playerBox.appendChild(speedBox);
    }
    card.appendChild(playerBox);

    // List 3 questions of this conversation
    const questionsContainer = document.createElement('div');
    questionsContainer.className = 'part3-questions-container';

    groupQuestions.forEach((q, qIndex) => {
      const qBox = document.createElement('div');
      qBox.className = 'part3-q-item';

      const promptEl = document.createElement('div');
      promptEl.className = 'quiz-prompt';
      promptEl.innerHTML = `<strong>Câu ${qIndex + 1}:</strong> ${q.prompt}`;
      qBox.appendChild(promptEl);

      const order = this.getOptionOrder(q.id);
      const userAnswer = this.answers.get(q.id);
      const isAnswered = userAnswer !== undefined;
      const isCorrect = isAnswered && (userAnswer === q.correctAnswer);

      const optionsWrap = document.createElement('div');
      optionsWrap.className = 'quiz-options part3-options';

      const labels = ['A', 'B', 'C', 'D'];
      order.forEach((optKey, idx) => {
        const optBtn = document.createElement('button');
        optBtn.className = 'quiz-option-btn';
        const label = labels[idx];
        const optText = q.options[optKey];

        if (isAnswered || (this.mode === 'test' && this.submitted)) {
          if (optKey === q.correctAnswer) {
            optBtn.classList.add('correct');
          } else if (optKey === userAnswer) {
            optBtn.classList.add('incorrect');
          }
        }

        optBtn.innerHTML = `<span class="opt-label">${label}</span> <span class="opt-text">${optText}</span>`;
        optBtn.onclick = () => {
          if (!isAnswered || this.mode === 'test') {
            this.handleAnswer(q.id, idx);
          }
        };
        optionsWrap.appendChild(optBtn);
      });
      qBox.appendChild(optionsWrap);

      // Explanation if answered in Learn or submitted in Test
      if ((this.mode === 'learn' && isAnswered) || (this.mode === 'test' && this.submitted)) {
        const expBox = document.createElement('div');
        expBox.className = 'explanation-box';
        expBox.innerHTML = `
          <div class="result-banner ${isCorrect ? 'banner-correct' : 'banner-wrong'}">
            ${isCorrect ? '✓ Đúng!' : '✗ Sai!'} Đáp án đúng: <strong>${q.correctAnswer}</strong>
          </div>
          <p><strong>Giải thích:</strong> ${q.explanation}</p>
        `;
        qBox.appendChild(expBox);
      }

      questionsContainer.appendChild(qBox);
    });
    card.appendChild(questionsContainer);

    // Transcript & turns re-listen in Learn mode after all 3 answered
    if ((this.mode === 'learn' && allGroupAnswered) || (this.mode === 'test' && this.submitted)) {
      const transBox = document.createElement('div');
      transBox.className = 'explanation-box transcript-box';
      transBox.innerHTML = `
        <h3>Transcript hội thoại (Bấm vào từng lượt nói để nghe lại):</h3>
        <div class="turns-list">
          ${group.turns.map(t => `
            <div class="turn-item ${t.speakerId === 'W1' ? 'speaker-woman' : 'speaker-man'}" data-start="${t.startMs}" data-end="${t.endMs}" data-text="${t.text}">
              <span class="speaker-tag">${t.speakerId === 'W1' ? 'Woman (W1)' : 'Man (M1)'}:</span>
              <span class="turn-text">${t.text}</span>
              <button class="btn-turn-play">🔊</button>
            </div>
          `).join('')}
        </div>
        ${group.translation ? `
          <div class="exp-section">
            <h4>Bản dịch tiếng Việt:</h4>
            <pre class="translation-text">${group.translation}</pre>
          </div>
        ` : ''}
      `;

      // Turn click events
      transBox.querySelectorAll('.turn-item').forEach(item => {
        item.onclick = () => {
          const startMs = parseInt(item.dataset.start);
          const endMs = parseInt(item.dataset.end);
          const text = item.dataset.text;
          audioPlayer.playGroup(group.audioFile, startMs, endMs, text);
        };
      });

      card.appendChild(transBox);
    }

    // Nav
    const navBox = document.createElement('div');
    navBox.className = 'quiz-nav';

    if (this.currentGroupIndex > 0) {
      const prevBtn = document.createElement('button');
      prevBtn.className = 'btn-secondary';
      prevBtn.textContent = '← Hội thoại trước';
      prevBtn.onclick = () => {
        audioPlayer.stop();
        this.currentGroupIndex--;
        this.render();
      };
      navBox.appendChild(prevBtn);
    }

    if (this.currentGroupIndex < totalGroups - 1) {
      const nextBtn = document.createElement('button');
      nextBtn.className = 'btn-primary';
      nextBtn.textContent = 'Hội thoại tiếp →';
      nextBtn.onclick = () => {
        audioPlayer.stop();
        this.currentGroupIndex++;
        this.render();
      };
      navBox.appendChild(nextBtn);
    } else {
      const finishBtn = document.createElement('button');
      finishBtn.className = 'btn-finish';
      finishBtn.textContent = this.mode === 'test' ? 'Nộp bài kiểm tra' : 'Hoàn thành bài';
      finishBtn.onclick = () => {
        if (this.mode === 'test' && !this.submitted) {
          this.submitTest();
        } else {
          this.finishQuiz();
        }
      };
      navBox.appendChild(finishBtn);
    }

    card.appendChild(navBox);
    this.container.appendChild(card);
  }
}
