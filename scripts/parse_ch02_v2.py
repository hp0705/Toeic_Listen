#!/usr/bin/env python3
"""
Parser for revamped CHAPTER_02_CONTENT.md v2.0
Builds complete data/chapters/chapter-02.json
"""

import os
import re
import json

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD_PATH = os.path.join(ROOT_DIR, "CHAPTER_02_CONTENT.md")
OUT_PATH = os.path.join(ROOT_DIR, "data", "chapters", "chapter-02.json")

DISTRACTOR_MAP = {
    # Part 1
    "P1-ACT": "Sai hành động — Đúng đối tượng nhưng động từ khác hình.",
    "P1-ABS": "Vật/người không có trong ảnh — Nhắc đến chi tiết không nhìn thấy.",
    "P1-LOC": "Sai vị trí — Nhầm vị trí hoặc giới từ không gian.",
    "P1-PRG": "Sai thể/trạng thái — Nhầm hành động đang diễn ra với trạng thái tĩnh.",
    "P1-INF": "Suy diễn quá mức — Tự suy diễn mục đích, nghề nghiệp hoặc chi tiết không thấy.",
    "P1-OPP": "Sai chiều/ngược — Động từ diễn tả chiều ngược lại với thực tế.",
    "P1-SND": "Nhầm âm tương tự — Nghe giống từ quen nhưng nghĩa hoàn toàn khác.",
    # Part 2
    "P2-WHQ": "Sai loại câu hỏi — Trả lời sai loại thông tin câu hỏi yêu cầu.",
    "P2-REP": "Bẫy lặp từ — Lặp lại từ trong câu hỏi để gây cảm giác quen tai nhưng sai logic.",
    "P2-SND": "Bẫy âm tương tự — Dùng từ có phát âm na ná từ trong câu hỏi.",
    "P2-YNA": "Bẫy Yes/No — Trả lời Yes/No cho câu hỏi Wh- hoặc không phù hợp.",
    "P2-TNS": "Sai thì — Sai thì động từ hoặc mốc thời gian so với câu hỏi.",
    "P2-PER": "Sai chủ thể — Nhầm lẫn đại từ hoặc người thực hiện hành động.",
    "P2-REL": "Liên quan chủ đề — Cùng trường từ vựng nhưng không trả lời trọng tâm.",
    "P2-ASS": "Bẫy liên tưởng — Dùng từ gợi liên tưởng đến ngữ cảnh nhưng sai chức năng."
}

def clean_text(text):
    return text.strip().replace('\r\n', '\n').replace('\r', '\n')

def parse_tags(text):
    return re.findall(r'`([A-Za-z0-9_-]+)`', text)

def determine_skill_group(part, tags, lesson_id):
    if part == 1:
        if "L01" in lesson_id: return "part1_people_and_actions"
        if "L02" in lesson_id: return "part1_objects_and_locations"
        if "L03" in lesson_id: return "part1_passive_and_state"
        return "part1_photographs"
    elif part == 0:
        return "linking_and_weak_forms"
    else:
        if "L05" in lesson_id: return "part2_wh_questions"
        if "L06" in lesson_id: return "part2_yes_no_choice"
        if "L07" in lesson_id: return "part2_indirect_requests"
        if "L08" in lesson_id: return "part2_statements_indirect"
        if "L09" in lesson_id: return "part2_paraphrase_traps"
        return "part2_traps_and_strategies"

def parse_options_and_reasons(options_raw, explanation):
    options = {}
    wrong_reasons = {}
    correct_ans = "A"

    for opt_match in re.finditer(r'-\s*([A-D])[.:]\s*([^\n]+)', options_raw):
        letter = opt_match.group(1)
        content = opt_match.group(2).strip()

        is_correct = '✓' in content
        if is_correct:
            correct_ans = letter
            clean_content = content.replace('✓', '').strip()
            # remove any trailing backticks
            clean_content = re.sub(r'`[^`]+`', '', clean_content).strip()
            options[letter] = clean_content
        else:
            # find distractor code if any
            m_code = re.search(r'`([A-Z0-9_-]+)`', content)
            clean_content = re.sub(r'`[^`]+`', '', content).strip()
            options[letter] = clean_content

            if m_code:
                code = m_code.group(1)
                desc = DISTRACTOR_MAP.get(code, f"Bẫy {code} — Lựa chọn không phù hợp.")
                wrong_reasons[letter] = f"[{code}] {desc}"
            else:
                wrong_reasons[letter] = f"Lựa chọn {letter} không phù hợp với nội dung bài nghe."

    # Fallback for any missing wrong reason
    for letter in options:
        if letter != correct_ans and letter not in wrong_reasons:
            wrong_reasons[letter] = f"Lựa chọn {letter} không phù hợp với nội dung bài nghe."

    return options, correct_ans, wrong_reasons

def main():
    with open(MD_PATH, 'r', encoding='utf-8') as f:
        raw_text = clean_text(f.read())

    print("Parsing CHAPTER_02_CONTENT.md v2.0...")

    all_questions = []
    lessons_data = []

    # 1. Parse Lessons 1 to 9
    lesson_cfgs = [
        {"num": 1, "id": "CH02-L01", "title": "Part 1: Người và hành động", "minCorrect": 4, "total": 5, "percentage": 80.0, "part": 1},
        {"num": 2, "id": "CH02-L02", "title": "Part 1: Vị trí, đồ vật và ảnh không có người", "minCorrect": 4, "total": 5, "percentage": 80.0, "part": 1},
        {"num": 3, "id": "CH02-L03", "title": "Part 1: Bị động, trạng thái và bẫy suy diễn", "minCorrect": 4, "total": 5, "percentage": 80.0, "part": 1},
        {"num": 4, "id": "CH02-L04", "title": "Nghe thật: Âm thanh, nối âm, số và giọng", "minCorrect": 8, "total": 10, "percentage": 80.0, "part": 0},
        {"num": 5, "id": "CH02-L05", "title": "Part 2: Nhận loại câu hỏi trong 3 từ đầu (WH)", "minCorrect": 5, "total": 6, "percentage": 83.3, "part": 2},
        {"num": 6, "id": "CH02-L06", "title": "Part 2: Yes/No, Tag, Phủ định và Lựa chọn", "minCorrect": 5, "total": 6, "percentage": 83.3, "part": 2},
        {"num": 7, "id": "CH02-L07", "title": "Part 2: Câu hỏi gián tiếp, Yêu cầu, Đề nghị, Gợi ý", "minCorrect": 5, "total": 6, "percentage": 83.3, "part": 2},
        {"num": 8, "id": "CH02-L08", "title": "Part 2: Câu trần thuật và Câu trả lời gián tiếp", "minCorrect": 5, "total": 6, "percentage": 83.3, "part": 2},
        {"num": 9, "id": "CH02-L09", "title": "Part 2: Paraphrase và Bản đồ bẫy tổng hợp", "minCorrect": 5, "total": 6, "percentage": 83.3, "part": 2}
    ]

    for cfg in lesson_cfgs:
        l_num = cfg["num"]
        p_start = raw_text.find(f"# BÀI {l_num}")
        p_next = raw_text.find(f"# BÀI {l_num+1}") if l_num < 9 else raw_text.find("# KIỂM TRA")
        l_chunk = raw_text[p_start:p_next]

        # Extract objectives
        obj_m = re.search(r'## Mục tiêu\s*\n((?:- [^\n]+\n?)+)', l_chunk)
        objectives = [o.strip()[2:].strip() for o in obj_m.group(1).split('\n') if o.strip()] if obj_m else []

        # Extract teaching blocks
        teaching_blocks = []
        tb_matches = re.finditer(r'## (\d+\.\d+\.\s*[^\n]+)\n(.*?)(?=\n## |\n# |\Z)', l_chunk, re.DOTALL)
        for tbm in tb_matches:
            tb_title = tbm.group(1).strip()
            tb_content = tbm.group(2).strip()
            if any(k in tb_title.lower() for k in ["bài luyện", "drill", "tự kiểm tra"]):
                continue
            teaching_blocks.append({
                "title": tb_title,
                "content": tb_content
            })

        lesson_qids = []
        dictations = []

        if l_num == 4:
            # Special Lesson 4: Audio decoding drills
            # Parse Drill A (Dictations D1-D10)
            d_table_m = re.search(r'## 4\.6\. Drill A[^\n]+\n(.*?)(?=\n## 4\.7|\Z)', l_chunk, re.DOTALL)
            if d_table_m:
                d_lines = d_table_m.group(1).strip().split('\n')
                for line in d_lines:
                    # | D1 | Could you tell me where the personnel office is? | couldja |
                    parts = [p.strip() for p in line.split('|') if p.strip()]
                    if len(parts) >= 2 and parts[0].startswith('D'):
                        d_num = parts[0]
                        d_text = parts[1]
                        d_note = parts[2] if len(parts) > 2 else ""
                        qid = f"CH02-L04-Q{int(d_num[1:]):02d}"
                        lesson_qids.append(qid)

                        dictations.append({
                            "id": f"CH02-L04-{d_num}",
                            "audioText": d_text,
                            "blanks": [d_note] if d_note else [d_text.split()[-1]],
                            "answerInput": d_text,
                            "tags": ["audio_drill", "dictation", "linking"],
                            "audioFile": f"audio/chapter-02/{qid.lower()}.mp3"
                        })

                        all_questions.append({
                            "id": qid,
                            "groupId": None,
                            "chapterId": "CH02",
                            "lessonId": "CH02-L04",
                            "part": 0,
                            "taskType": "dictation",
                            "prompt": f"Nghe và chép lại câu (Chú ý hiện tượng: {d_note}):",
                            "optionsVisibleBeforeAnswer": False,
                            "image": None,
                            "audioSegments": [
                                {
                                    "text": d_text,
                                    "voice": "us-female-01" if int(d_num[1:]) % 2 == 1 else "us-male-01",
                                    "file": f"audio/chapter-02/{qid.lower()}.mp3",
                                    "pauseAfterMs": 0
                                }
                            ],
                            "options": {
                                "ANSWER": d_text
                            },
                            "correctAnswer": "ANSWER",
                            "audioText": d_text,
                            "blanks": [d_text],
                            "answerInput": d_text,
                            "transcript": d_text,
                            "translation": "",
                            "explanation": f"Hiện tượng cần chú ý: {d_note}. Câu hoàn chỉnh: {d_text}",
                            "wrongReasons": {},
                            "skillTags": ["audio_drill", "dictation", "linking"],
                            "skillGroup": "linking_and_weak_forms",
                            "difficulty": 2,
                            "revision": 2
                        })
        else:
            # Lessons 1-3 (Part 1) and Lessons 5-9 (Part 2)
            q_matches = re.finditer(r'(#{3,4}\s+(CH02-L\d+-Q\d+)[^\n]*)\n(.*?)(?=\n#{3,4}\s+CH02-|\n### |\n## |\Z)', l_chunk, re.DOTALL)
            for qm in q_matches:
                header_line = qm.group(1).strip()
                qid = qm.group(2).strip()
                qblock = qm.group(3).strip()
                lesson_qids.append(qid)

                # Header details: e.g. "CH02-L01-Q01 · US-M · ★1" or "CH02-L05-Q01 · US-F → UK-M · ★1"
                difficulty = 1
                if '★3' in header_line: difficulty = 3
                elif '★2' in header_line: difficulty = 2

                exp_m = re.search(r'\*\*Giải thích:\*\*\s*([^\n]+(?:\n[^\n*]+)*)', qblock)
                explanation = exp_m.group(1).strip() if exp_m else ""

                tags = parse_tags(qblock)
                opts, correct_ans, wrong_reasons = parse_options_and_reasons(qblock, explanation)

                if cfg["part"] == 1:
                    # Part 1 Photograph
                    img_m = re.search(r'\*\*Ảnh:\*\*\s*([^\n]+)', qblock)
                    img_desc = img_m.group(1).strip() if img_m else ""

                    # Build audio segments for options A, B, C, D
                    segments = []
                    for letter in ["A", "B", "C", "D"]:
                        if letter in opts:
                            segments.append({
                                "text": opts[letter],
                                "voice": "us-female-01" if "F" in header_line else "us-male-01",
                                "file": f"audio/chapter-02/{qid.lower()}-{letter.lower()}.mp3",
                                "pauseAfterMs": 1000
                            })

                    all_questions.append({
                        "id": qid,
                        "groupId": None,
                        "chapterId": "CH02",
                        "lessonId": cfg["id"],
                        "part": 1,
                        "taskType": "photo_description",
                        "prompt": "Look at the photo and choose the best description:",
                        "optionsVisibleBeforeAnswer": False,
                        "image": f"images/chapter-02/{qid.lower()}.svg",
                        "imageDescription": img_desc,
                        "audioSegments": segments,
                        "options": opts,
                        "correctAnswer": correct_ans,
                        "transcript": " / ".join([f"({k}) {v}" for k, v in opts.items()]),
                        "translation": img_desc,
                        "explanation": explanation,
                        "wrongReasons": wrong_reasons,
                        "skillTags": tags or ["part1_photo"],
                        "skillGroup": determine_skill_group(1, tags, cfg["id"]),
                        "difficulty": difficulty,
                        "revision": 2
                    })

                else:
                    # Part 2 Question-Response
                    q_text_m = re.search(r'\*\*Q:\*\*\s*([^\n]+)', qblock)
                    q_text = q_text_m.group(1).strip() if q_text_m else ""

                    segments = [
                        {
                            "text": q_text,
                            "voice": "us-female-01" if "US-F" in header_line or "UK-F" in header_line or "CA-F" in header_line or "AU-F" in header_line else "us-male-01",
                            "file": f"audio/chapter-02/{qid.lower()}-q.mp3",
                            "pauseAfterMs": 1500
                        }
                    ]
                    for letter in ["A", "B", "C"]:
                        if letter in opts:
                            segments.append({
                                "text": opts[letter],
                                "voice": "us-male-01" if "M" in header_line else "us-female-01",
                                "file": f"audio/chapter-02/{qid.lower()}-{letter.lower()}.mp3",
                                "pauseAfterMs": 1000
                            })

                    all_questions.append({
                        "id": qid,
                        "groupId": None,
                        "chapterId": "CH02",
                        "lessonId": cfg["id"],
                        "part": 2,
                        "taskType": "part2_response",
                        "prompt": "Nghe câu hỏi và chọn câu phản hồi phù hợp nhất (Part 2):",
                        "optionsVisibleBeforeAnswer": False,
                        "image": None,
                        "audioSegments": segments,
                        "options": opts,
                        "correctAnswer": correct_ans,
                        "transcript": f"{q_text} / (A) {opts.get('A','')} / (B) {opts.get('B','')} / (C) {opts.get('C','')}",
                        "translation": "",
                        "explanation": explanation,
                        "wrongReasons": wrong_reasons,
                        "skillTags": tags or ["part2_response"],
                        "skillGroup": determine_skill_group(2, tags, cfg["id"]),
                        "difficulty": difficulty,
                        "revision": 2
                    })

        lessons_data.append({
            "lessonId": cfg["id"],
            "title": cfg["title"],
            "objectives": objectives,
            "teachingBlocks": teaching_blocks,
            "dictations": dictations,
            "questionIds": lesson_qids,
            "passRule": {
                "minCorrect": cfg["minCorrect"],
                "total": cfg["total"],
                "percentage": cfg["percentage"]
            }
        })

    # 2. Parse Final Test (25 questions)
    print("Parsing Final Test CH02-FINAL...")
    p_final = raw_text.find("# KIỂM TRA CUỐI CHƯƠNG 2")
    final_chunk = raw_text[p_final:]

    final_qids = []
    final_matches = re.finditer(r'(#{3,4}\s+(CH02-FINAL-Q\d+)[^\n]*)\n(.*?)(?=\n#{3,4}\s+CH02-FINAL|\n## |\Z)', final_chunk, re.DOTALL)

    for fm in final_matches:
        f_header = fm.group(1).strip()
        qid = fm.group(2).strip()
        fblock = fm.group(3).strip()
        final_qids.append(qid)

        q_num = int(qid.split('-Q')[-1])
        is_part1 = q_num <= 6

        exp_m = re.search(r'\*\*Giải thích:\*\*\s*([^\n]+(?:\n[^\n*]+)*)', fblock)
        explanation = exp_m.group(1).strip() if exp_m else ""

        tags = parse_tags(fblock)
        opts, correct_ans, wrong_reasons = parse_options_and_reasons(fblock, explanation)

        if is_part1:
            img_m = re.search(r'\*\*Ảnh:\*\*\s*([^\n]+)', fblock)
            img_desc = img_m.group(1).strip() if img_m else ""

            segments = []
            for letter in ["A", "B", "C", "D"]:
                if letter in opts:
                    segments.append({
                        "text": opts[letter],
                        "voice": "us-female-01" if "F" in f_header else "us-male-01",
                        "file": f"audio/chapter-02/{qid.lower()}-{letter.lower()}.mp3",
                        "pauseAfterMs": 1000
                    })

            all_questions.append({
                "id": qid,
                "groupId": None,
                "chapterId": "CH02",
                "lessonId": "CH02-FINAL",
                "part": 1,
                "taskType": "photo_description",
                "prompt": "Look at the photo and choose the best description:",
                "optionsVisibleBeforeAnswer": False,
                "image": f"images/chapter-02/{qid.lower()}.svg",
                "imageDescription": img_desc,
                "audioSegments": segments,
                "options": opts,
                "correctAnswer": correct_ans,
                "transcript": " / ".join([f"({k}) {v}" for k, v in opts.items()]),
                "translation": img_desc,
                "explanation": explanation or "Nghe và quan sát ảnh để loại bỏ các bẫy hành động, vật không có.",
                "wrongReasons": wrong_reasons,
                "skillTags": tags or ["part1_photo"],
                "skillGroup": "part1_photographs",
                "difficulty": 2,
                "revision": 2
            })
        else:
            q_text_m = re.search(r'\*\*Q:\*\*\s*([^\n]+)', fblock)
            q_text = q_text_m.group(1).strip() if q_text_m else ""

            segments = [
                {
                    "text": q_text,
                    "voice": "us-female-01" if "F" in f_header.split('→')[0] else "us-male-01",
                    "file": f"audio/chapter-02/{qid.lower()}-q.mp3",
                    "pauseAfterMs": 1500
                }
            ]
            for letter in ["A", "B", "C"]:
                if letter in opts:
                    segments.append({
                        "text": opts[letter],
                        "voice": "us-male-01" if "M" in f_header else "us-female-01",
                        "file": f"audio/chapter-02/{qid.lower()}-{letter.lower()}.mp3",
                        "pauseAfterMs": 1000
                    })

            all_questions.append({
                "id": qid,
                "groupId": None,
                "chapterId": "CH02",
                "lessonId": "CH02-FINAL",
                "part": 2,
                "taskType": "part2_response",
                "prompt": "Nghe câu hỏi và chọn câu phản hồi phù hợp nhất (Part 2):",
                "optionsVisibleBeforeAnswer": False,
                "image": None,
                "audioSegments": segments,
                "options": opts,
                "correctAnswer": correct_ans,
                "transcript": f"{q_text} / (A) {opts.get('A','')} / (B) {opts.get('B','')} / (C) {opts.get('C','')}",
                "translation": "",
                "explanation": explanation or "Lựa chọn phản hồi tự nhiên, tránh bẫy lặp từ và bẫy âm.",
                "wrongReasons": wrong_reasons,
                "skillTags": tags or ["part2_response"],
                "skillGroup": "part2_traps_and_strategies",
                "difficulty": 2,
                "revision": 2
            })

    chapter_data = {
        "chapterId": "CH02",
        "title": "Part 1 và Part 2 — nghe thật: mô tả ảnh, âm thanh thực tế, câu hỏi – phản hồi",
        "description": "Chiến thuật mô tả tranh Part 1, giải mã âm thực tế và phản xạ 3 giây câu hỏi – phản hồi Part 2",
        "specVersion": "2.3",
        "contentVersion": "2.0.0",
        "lessons": lessons_data,
        "questions": all_questions,
        "finalTest": {
            "id": "CH02-FINAL",
            "title": "Kiểm tra cuối chương 2 (25 câu)",
            "questionIds": final_qids,
            "passRule": {
                "minCorrect": 20,
                "total": 25,
                "percentage": 80.0,
                "sectionRules": {
                    "part1": {"minCorrect": 5, "total": 6},
                    "part2": {"minCorrect": 15, "total": 19}
                }
            }
        }
    }

    print(f"Total Lessons: {len(lessons_data)}")
    print(f"Total Questions: {len(all_questions)}")
    print(f"Final Test Question IDs: {len(final_qids)}")

    with open(OUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(chapter_data, f, indent=2, ensure_ascii=False)
    print(f"Successfully wrote {OUT_PATH}!")

if __name__ == "__main__":
    main()
