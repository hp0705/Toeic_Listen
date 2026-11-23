import fs from 'fs';
import path from 'path';

// Mock localStorage
const store = {};
global.localStorage = {
  getItem: (key) => store[key] || null,
  setItem: (key, val) => { store[key] = String(val); },
  removeItem: (key) => { delete store[key]; },
  clear: () => { for (const k in store) delete store[k]; }
};

import { storage } from '../js/storage.js';
import { rebuildDerived } from '../js/progress.js';

let passed = 0;
let failed = 0;

function assert(name, condition, details = "") {
  if (condition) {
    passed++;
    console.log(`✅ PASS: ${name}`);
  } else {
    failed++;
    console.error(`❌ FAIL: ${name} (${details})`);
  }
}

async function run() {
  console.log("=== RUNNING STORAGE & DERIVED PROGRESS TESTS ===");

  // Test 1: Khởi tạo state mặc định
  const def = storage.createDefaultState();
  assert(
    "1. Khởi tạo state mặc định",
    def.schemaVersion === 2 && def.specVersion === '2.3' && Array.isArray(def.runs) && Array.isArray(def.attempts),
    "schemaVersion=2, specVersion=2.3, runs=[], attempts=[]"
  );

  // Test 2: Lưu và nạp state từ LocalStorage
  storage.saveState(def);
  const loaded = storage.loadState();
  assert(
    "2. Lưu và nạp state từ LocalStorage",
    loaded && loaded.schemaVersion === 2 && loaded.courseId === 'toeic-listening-300'
  );

  // Test 3: Ghi nhận run và attempt
  const runId = "test-run-01";
  loaded.runs.push({
    id: runId,
    chapterId: "CH01",
    lessonId: "CH01-L01",
    mode: "learn",
    startedAt: new Date().toISOString(),
    finishedAt: new Date().toISOString(),
    status: "submitted"
  });
  loaded.attempts.push({
    id: "att-01",
    runId: runId,
    questionId: "CH01-L01-Q01",
    isCorrect: true,
    skillTags: ["time_expression"],
    skillGroup: "numbers_and_time"
  });
  storage.saveState(loaded);
  const reloaded = storage.loadState();
  assert(
    "3. Ghi nhận run và attempt vào state",
    reloaded.runs.length === 1 && reloaded.attempts.length === 1 && reloaded.attempts[0].isCorrect === true
  );

  // Test 4: Rebuild derived state
  const coursePath = path.resolve('./data/course.json');
  const courseData = JSON.parse(fs.readFileSync(coursePath, 'utf-8'));
  const ch1Path = path.resolve('./data/chapters/chapter-01.json');
  const ch1Data = JSON.parse(fs.readFileSync(ch1Path, 'utf-8'));
  courseData.chapters = [ch1Data];

  const derived = rebuildDerived(reloaded, courseData);
  assert(
    "4. Tính derived state thành công",
    derived && derived.chapterStatus && derived.chapterStatus.CH01.unlocked === true
  );

  // Test 5: Mở khóa CH02 khi đạt CH01-FINAL
  const finalRunId = "run-final-01";
  reloaded.runs.push({
    id: finalRunId,
    chapterId: "CH01",
    lessonId: "CH01-FINAL",
    mode: "test",
    status: "submitted"
  });
  // Add 25 correct attempts for final
  for (let i = 1; i <= 25; i++) {
    reloaded.attempts.push({
      id: `att-final-${i}`,
      runId: finalRunId,
      questionId: `CH01-FINAL-Q${i}`,
      isCorrect: true,
      skillTags: ["test_tag"],
      skillGroup: "numbers_and_time"
    });
  }
  const derivedWithFinal = rebuildDerived(reloaded, courseData);
  assert(
    "5. Mở khóa CH02 khi đạt bài kiểm tra cuối CH01 (>= 24 câu đúng)",
    derivedWithFinal.chapterStatus.CH02.unlocked === true,
    `CH02 unlocked: ${derivedWithFinal.chapterStatus.CH02.unlocked}`
  );

  // Test 6: Sổ tay lỗi ghi nhận câu sai
  const tFail = new Date(Date.now() - 60000).toISOString();
  reloaded.attempts.push({
    id: "att-mistake-01",
    runId: "run-mistake",
    questionId: "CH01-L01-Q02",
    isCorrect: false,
    answeredAt: tFail,
    skillTags: ["weak_form"],
    skillGroup: "weak_forms_and_linking"
  });
  const derivedMistake = rebuildDerived(reloaded, courseData);
  assert(
    "6. Sổ tay lỗi ghi nhận câu sai (needs_review)",
    derivedMistake.mistakes.length === 1 && derivedMistake.mistakes[0].status === "needs_review",
    `status: ${derivedMistake.mistakes[0]?.status}`
  );

  // Test 7: Khắc phục lỗi khi làm lại đúng và có câu mới cùng skillGroup ở 1.0x
  // 7a: User re-does the question itself correctly
  reloaded.attempts.push({
    id: "att-mistake-retry",
    runId: "run-mistake",
    questionId: "CH01-L01-Q02",
    isCorrect: true,
    answeredAt: new Date(Date.now() - 30000).toISOString(),
    skillTags: ["weak_form"],
    skillGroup: "weak_forms_and_linking"
  });
  // 7b: User answers another question in the same skillGroup correctly at 1.0x without seeing transcript
  reloaded.attempts.push({
    id: "att-recovery-01",
    runId: "run-recovery",
    questionId: "CH01-L01-Q03",
    isCorrect: true,
    playbackRate: 1.0,
    transcriptViewedBeforeAnswer: false,
    answeredAt: new Date().toISOString(),
    skillTags: ["weak_form"],
    skillGroup: "weak_forms_and_linking"
  });
  const derivedRecovered = rebuildDerived(reloaded, courseData);
  assert(
    "7. Tự động khắc phục lỗi khi làm đúng câu cùng skillGroup ở 1.0x (resolved)",
    derivedRecovered.mistakes[0].status === "resolved",
    `status: ${derivedRecovered.mistakes[0]?.status}`
  );

  console.log(`\nTests Summary: ${passed} Passed, ${failed} Failed.`);
  if (failed > 0) process.exit(1);
}

run();
