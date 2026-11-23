/**
 * Progress & Derived State Calculation for TOEIC Listening 300
 * Complies with PROGRESS_STORAGE_SPEC.md v1.2
 */

export function rebuildDerived(state, courseData) {
  if (!state) return null;

  const runs = state.runs || [];
  const attempts = state.attempts || [];

  // 1. Group attempts by runId and questionId
  const attemptsByRun = new Map();
  const attemptsByQuestion = new Map();

  for (const att of attempts) {
    if (!attemptsByRun.has(att.runId)) {
      attemptsByRun.set(att.runId, []);
    }
    attemptsByRun.get(att.runId).push(att);

    if (!attemptsByQuestion.has(att.questionId)) {
      attemptsByQuestion.set(att.questionId, []);
    }
    attemptsByQuestion.get(att.questionId).push(att);
  }

  // 2. Determine passed lessons
  const passedLessons = new Set();
  const lessonScores = new Map();

  for (const run of runs) {
    if (run.status !== 'submitted') continue;
    const runAttempts = attemptsByRun.get(run.id) || [];
    const correctCount = runAttempts.filter(a => a.isCorrect).length;
    const totalCount = runAttempts.length;
    const pct = totalCount > 0 ? (correctCount / totalCount) * 100 : 0;

    const prevScore = lessonScores.get(run.lessonId) || { correctCount: 0, totalCount: 0, pct: 0 };
    if (pct > prevScore.pct) {
      lessonScores.set(run.lessonId, { correctCount, totalCount, pct });
    }

    // Check passRule if available
    let passed = false;
    // Determine passRule from courseData
    let passRule = null;
    if (courseData && courseData.chapters) {
      for (const ch of courseData.chapters) {
        if (ch.lessons) {
          const l = ch.lessons.find(x => x.lessonId === run.lessonId);
          if (l && l.passRule) passRule = l.passRule;
        }
        if (ch.finalTest && ch.finalTest.id === run.lessonId) {
          passRule = ch.finalTest.passRule;
        }
      }
    }

    if (passRule) {
      if (typeof passRule.minCorrect === 'number' && correctCount >= passRule.minCorrect) {
        passed = true;
      } else if (typeof passRule.percentage === 'number' && pct >= passRule.percentage) {
        passed = true;
      }
    } else {
      // Default: 80% or 3/4
      if (totalCount === 4) passed = correctCount >= 3;
      else if (totalCount === 8) passed = correctCount >= 6;
      else passed = pct >= 80;
    }

    if (passed) {
      passedLessons.add(run.lessonId);
    }
  }

  // 3. Determine chapter unlock status
  const chapterStatus = {
    CH01: { unlocked: true, completed: false, finalPassed: passedLessons.has('CH01-FINAL') },
    CH02: { unlocked: false, completed: false, finalPassed: passedLessons.has('CH02-FINAL') },
    CH03: { unlocked: false, completed: false, finalPassed: passedLessons.has('CH03-FINAL') }
  };

  // CH02 unlocks if CH01-FINAL is passed
  if (chapterStatus.CH01.finalPassed) {
    chapterStatus.CH02.unlocked = true;
  }
  // CH03 unlocks if CH02-FINAL is passed
  if (chapterStatus.CH02.finalPassed) {
    chapterStatus.CH03.unlocked = true;
  }

  // Check if all lessons in chapter are completed
  if (courseData && courseData.chapters) {
    for (const ch of courseData.chapters) {
      const chId = ch.id;
      if (chapterStatus[chId] && ch.lessons) {
        const allDone = ch.lessons.every(l => passedLessons.has(l.lessonId));
        chapterStatus[chId].completed = allDone && chapterStatus[chId].finalPassed;
      }
    }
  }

  // 4. Mistake Book & Error Recovery via skillGroup
  const mistakes = [];
  const skillGroupStats = {};

  for (const [qid, qAttempts] of attemptsByQuestion.entries()) {
    // Sort attempts chronologically
    qAttempts.sort((a, b) => new Date(a.answeredAt) - new Date(b.answeredAt));
    const lastAttempt = qAttempts[qAttempts.length - 1];

    // Find question metadata
    let qMeta = null;
    if (courseData && courseData.getQuestion) {
      qMeta = courseData.getQuestion(qid);
    } else if (courseData && courseData.chapters) {
      for (const ch of courseData.chapters) {
        if (ch.questions) {
          const found = ch.questions.find(q => q.id === qid);
          if (found) { qMeta = found; break; }
        }
      }
    }

    const qTags = (qMeta && qMeta.skillTags) ? qMeta.skillTags : (lastAttempt.skillTags || []);
    const qSkillGroup = (qMeta && qMeta.skillGroup) ? qMeta.skillGroup : (lastAttempt.skillGroup || 'general_listening');

    // Track skill group accuracy
    if (!skillGroupStats[qSkillGroup]) {
      skillGroupStats[qSkillGroup] = { correct: 0, total: 0 };
    }
    for (const a of qAttempts) {
      skillGroupStats[qSkillGroup].total++;
      if (a.isCorrect) skillGroupStats[qSkillGroup].correct++;
    }

    // Has ever failed?
    const hasFailed = qAttempts.some(a => !a.isCorrect);
    if (!hasFailed) continue;

    if (!lastAttempt.isCorrect) {
      // Currently wrong
      mistakes.push({
        questionId: qid,
        status: 'needs_review',
        lastAttempt,
        skillTags: qTags,
        skillGroup: qSkillGroup,
        groupId: lastAttempt.groupId,
        question: qMeta
      });
    } else {
      // Last attempt on this question was correct.
      // Now check if a mistake was resolved according to spec:
      // A mistake is formally resolved when a NEW question with the same skillTag OR skillGroup
      // (different question, different groupId if Part 3) was answered correctly at 1.0x without seeing transcript.
      const firstFailIdx = qAttempts.findIndex(a => !a.isCorrect);
      const failTime = new Date(qAttempts[firstFailIdx].answeredAt);

      const hasRecoveryEvidence = attempts.some(a => {
        if (a.questionId === qid) return false; // Must be a different question
        if (!a.isCorrect) return false;
        if (a.playbackRate < 1.0) return false;
        if (a.transcriptViewedBeforeAnswer) return false;
        if (new Date(a.answeredAt) <= failTime) return false;

        // If Part 3, must be different group
        if (lastAttempt.groupId && a.groupId && a.groupId === lastAttempt.groupId) {
          return false;
        }

        // Compare skillGroup or skillTag
        let otherQ = courseData && courseData.getQuestion ? courseData.getQuestion(a.questionId) : null;
        if (!otherQ && courseData && courseData.chapters) {
          for (const ch of courseData.chapters) {
            if (ch.questions) {
              const found = ch.questions.find(q => q.id === a.questionId);
              if (found) { otherQ = found; break; }
            }
          }
        }
        const otherGroup = otherQ ? otherQ.skillGroup : a.skillGroup;
        const otherTags = otherQ ? otherQ.skillTags : (a.skillTags || []);

        const sameGroup = otherGroup && otherGroup === qSkillGroup;
        const sameTag = otherTags && otherTags.some(t => qTags.includes(t));
        return sameGroup || sameTag;
      });

      mistakes.push({
        questionId: qid,
        status: hasRecoveryEvidence ? 'resolved' : 'practicing',
        lastAttempt,
        skillTags: qTags,
        skillGroup: qSkillGroup,
        groupId: lastAttempt.groupId,
        question: qMeta
      });
    }
  }

  // Calculate overall statistics
  const totalAttemptsCount = attempts.length;
  const totalCorrectCount = attempts.filter(a => a.isCorrect).length;
  const overallAccuracy = totalAttemptsCount > 0 ? totalCorrectCount / totalAttemptsCount : 0;

  return {
    passedLessons: Array.from(passedLessons),
    lessonScores: Object.fromEntries(lessonScores),
    chapterStatus,
    mistakes,
    openMistakesCount: mistakes.filter(m => m.status !== 'resolved').length,
    resolvedMistakesCount: mistakes.filter(m => m.status === 'resolved').length,
    totalAttemptsCount,
    totalCorrectCount,
    overallAccuracy,
    skillGroupStats
  };
}
