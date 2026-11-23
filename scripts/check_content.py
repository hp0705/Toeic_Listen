#!/usr/bin/env python3
"""
Content Validator for TOEIC Listening 300
Complies with SPEC_WEB_APP.md v2.3 section 12
"""

import os
import sys
import json
import re

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def validate():
    errors = []
    warnings = []
    print("=== STARTING TOEIC LISTENING 300 CONTENT VALIDATION ===")

    # 1. Check course.json
    course_path = os.path.join(ROOT_DIR, "data", "course.json")
    if not os.path.isfile(course_path):
        errors.append(f"Missing {course_path}")
        return errors, warnings

    with open(course_path, "r", encoding="utf-8") as f:
        try:
            course = json.load(f)
        except Exception as e:
            errors.append(f"Invalid JSON in {course_path}: {e}")
            return errors, warnings

    print(f"Loaded course.json: courseId={course.get('courseId')}, contentVersion={course.get('contentVersion')}, specVersion={course.get('specVersion')}")

    # 2. Check voices.json
    voices_path = os.path.join(ROOT_DIR, "data", "voices.json")
    if not os.path.isfile(voices_path):
        errors.append(f"Missing {voices_path}")
    else:
        with open(voices_path, "r", encoding="utf-8") as f:
            try:
                voices_data = json.load(f)
                profiles = voices_data.get("profiles", [])
                has_female = any(p.get("gender") == "female" and p.get("approved") for p in profiles)
                has_male = any(p.get("gender") == "male" and p.get("approved") for p in profiles)
                if not (has_female and has_male):
                    errors.append("data/voices.json must have at least one approved female and one approved male profile.")
                for p in profiles:
                    if not p.get("license") or not p.get("credit"):
                        warnings.append(f"Voice profile {p.get('id')} missing license or credit.")
            except Exception as e:
                errors.append(f"Invalid JSON in {voices_path}: {e}")

    # 3. Check each chapter
    all_question_ids = set()
    all_group_ids = set()
    chapters = course.get("chapters", [])

    for ch_meta in chapters:
        ch_id = ch_meta.get("id")
        ch_file = os.path.join(ROOT_DIR, "data", ch_meta.get("file"))
        if not os.path.isfile(ch_file):
            errors.append(f"Chapter file not found: {ch_file}")
            continue

        with open(ch_file, "r", encoding="utf-8") as f:
            try:
                ch_data = json.load(f)
            except Exception as e:
                errors.append(f"Invalid JSON in {ch_file}: {e}")
                continue

        print(f"\n--- Checking Chapter {ch_id} ---")

        # Check lessons and passRule
        lessons = ch_data.get("lessons", [])
        if not lessons:
            errors.append(f"{ch_id} has no lessons.")

        ch_question_ids = set()
        for l in lessons:
            lid = l.get("lessonId")
            if not lid:
                errors.append(f"{ch_id}: Lesson missing lessonId.")
            pass_rule = l.get("passRule")
            if not pass_rule:
                errors.append(f"{ch_id} Lesson {lid}: Missing passRule.")
            else:
                if "minCorrect" not in pass_rule or "total" not in pass_rule or "percentage" not in pass_rule:
                    errors.append(f"{ch_id} Lesson {lid}: Malformed passRule: {pass_rule}")

            qids = l.get("questionIds", [])
            if not qids:
                errors.append(f"{ch_id} Lesson {lid}: No questionIds.")
            for qid in qids:
                ch_question_ids.add(qid)

        # Check Final test
        final_test = ch_data.get("finalTest")
        if not final_test:
            errors.append(f"{ch_id}: Missing finalTest block.")
        else:
            ft_qids = final_test.get("questionIds", [])
            if not ft_qids:
                errors.append(f"{ch_id} FinalTest: No questionIds.")
            pass_rule = final_test.get("passRule")
            if not pass_rule:
                errors.append(f"{ch_id} FinalTest: Missing passRule.")
            # Check overlap between lesson questions and final test
            overlap = ch_question_ids.intersection(set(ft_qids))
            if overlap:
                errors.append(f"{ch_id}: Final test questions duplicate lesson questions: {overlap}")

        # Check groups (if Part 3/4)
        groups = ch_data.get("groups", [])
        group_map = {}
        for g in groups:
            gid = g.get("id")
            if not gid:
                errors.append(f"{ch_id}: Group missing id.")
            if gid in all_group_ids:
                errors.append(f"Duplicate group ID: {gid}")
            all_group_ids.add(gid)
            group_map[gid] = g

            # Check group turns
            turns = g.get("turns", [])
            if not turns:
                errors.append(f"Group {gid}: Has no turns.")
            last_end = -1
            for t in turns:
                start_ms = t.get("startMs", 0)
                end_ms = t.get("endMs", 0)
                if start_ms < last_end:
                    errors.append(f"Group {gid} turn {t.get('turn')}: Overlapping turn timestamp startMs {start_ms} < last_end {last_end}")
                if end_ms <= start_ms:
                    errors.append(f"Group {gid} turn {t.get('turn')}: Invalid endMs <= startMs")
                last_end = end_ms

            # Check questionIds (CH01 has 2 questions per short conversation, CH03 has 3)
            g_qids = g.get("questionIds", [])
            expected_count = 2 if ch_id == "CH01" else 3
            if len(g_qids) != expected_count:
                errors.append(f"Group {gid}: Expected {expected_count} questions, got {len(g_qids)}")

        # Check questions
        questions = ch_data.get("questions", [])
        answer_distribution = {"A": 0, "B": 0, "C": 0, "D": 0}

        for q in questions:
            qid = q.get("id")
            if not qid:
                errors.append(f"{ch_id}: Question missing id.")
                continue

            if qid in all_question_ids:
                errors.append(f"Duplicate question ID: {qid}")
            all_question_ids.add(qid)

            # Check required fields
            req_fields = [
                "chapterId", "lessonId", "part", "taskType", "prompt",
                "optionsVisibleBeforeAnswer", "options", "correctAnswer",
                "explanation", "wrongReasons", "skillTags", "skillGroup"
            ]
            for fld in req_fields:
                if fld not in q:
                    errors.append(f"Question {qid}: Missing required field '{fld}'")

            # Check options & answer
            options = q.get("options", {})
            correct = q.get("correctAnswer")
            if correct not in options:
                errors.append(f"Question {qid}: correctAnswer '{correct}' not in options {list(options.keys())}")
            else:
                answer_distribution[correct] = answer_distribution.get(correct, 0) + 1

            # Check wrongReasons
            wrong_reasons = q.get("wrongReasons", {})
            for opt in options.keys():
                if opt != correct and opt not in wrong_reasons:
                    errors.append(f"Question {qid}: Missing wrongReason for option '{opt}'")

            # Check image if Part 1
            if q.get("part") == 1:
                img = q.get("image")
                if not img:
                    errors.append(f"Part 1 Question {qid}: Missing image path.")
                else:
                    img_path = os.path.join(ROOT_DIR, img)
                    if not os.path.isfile(img_path):
                        errors.append(f"Part 1 Question {qid}: Image file not found at {img_path}")

            # Check group link if Part 3
            if q.get("part") == 3:
                gid = q.get("groupId")
                if not gid or gid not in group_map:
                    errors.append(f"Part 3 Question {qid}: groupId '{gid}' not found in chapter groups.")

            # Check optionsVisibleBeforeAnswer
            if q.get("part") in [1, 2] and q.get("optionsVisibleBeforeAnswer") is not False:
                warnings.append(f"Question {qid} (Part {q.get('part')}): optionsVisibleBeforeAnswer should normally be False so choices are hidden before audio answer.")

            # Check audioSegments path if exists
            audio_segs = q.get("audioSegments")
            if audio_segs:
                for seg in audio_segs:
                    fpath = seg.get("file", "")
                    if fpath.startswith("/") or fpath.startswith("http"):
                        errors.append(f"Question {qid}: Audio path must be relative: {fpath}")
                    if not fpath.endswith(".mp3"):
                        errors.append(f"Question {qid}: Audio file must end with .mp3: {fpath}")

            # Check hardcoded explanation warning
            exp = q.get("explanation", "")
            if re.search(r'đáp án\s+[A-D]\b', exp, re.IGNORECASE):
                warnings.append(f"Question {qid}: Explanation may contain fixed label 'đáp án A/B/C/D' which may conflict with option shuffling.")

        # Print answer distribution
        total_q = len(questions)
        print(f"Total questions in {ch_id}: {total_q}")
        print(f"Answer distribution: {answer_distribution}")

    # 4. Check total audio folder size
    audio_dir = os.path.join(ROOT_DIR, "audio")
    total_audio_bytes = 0
    if os.path.isdir(audio_dir):
        for root, _, files in os.walk(audio_dir):
            for file in files:
                total_audio_bytes += os.path.getsize(os.path.join(root, file))
    total_audio_mb = total_audio_bytes / (1024 * 1024)
    print(f"\nTotal audio size: {total_audio_mb:.2f} MB (Spec limit ~300 MB)")
    if total_audio_mb > 300:
        warnings.append(f"Audio directory size ({total_audio_mb:.2f} MB) exceeds recommended limit of 300 MB.")

    print("\n=== VALIDATION SUMMARY ===")
    print(f"Total Questions Verified: {len(all_question_ids)}")
    print(f"Total Part 3 Groups: {len(all_group_ids)}")
    print(f"Errors Found: {len(errors)}")
    print(f"Warnings Found: {len(warnings)}")

    if errors:
        print("\nERRORS:")
        for e in errors:
            print(f"  ❌ {e}")
    if warnings:
        print("\nWARNINGS:")
        for w in warnings:
            print(f"  ⚠️ {w}")

    return errors, warnings

if __name__ == "__main__":
    errs, warns = validate()
    if errs:
        sys.exit(1)
    else:
        print("\n✅ ALL VALIDATION CHECKS PASSED SUCCESSFULLY!")
        sys.exit(0)
