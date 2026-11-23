#!/usr/bin/env python3
"""
Comprehensive Parser for Chapter 2 v2.0
Integrates CHAPTER_02_CONTENT.md AND CHAPTER_02_BANK.md
Builds full data/chapters/chapter-02.json with 230 questions
"""

import os
import re
import json

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT_MD_PATH = os.path.join(ROOT_DIR, "CHAPTER_02_CONTENT.md")
BANK_MD_PATH = os.path.join(ROOT_DIR, "CHAPTER_02_BANK.md")
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
    "ACT": "Sai hành động — Đúng đối tượng nhưng động từ khác hình.",
    "ABS": "Vật/người không có trong ảnh — Nhắc đến chi tiết không nhìn thấy.",
    "LOC": "Sai vị trí — Nhầm vị trí hoặc giới từ không gian.",
    "PRG": "Sai thể/trạng thái — Nhầm hành động đang diễn ra với trạng thái tĩnh.",
    "INF": "Suy diễn quá mức — Tự suy diễn mục đích, nghề nghiệp hoặc chi tiết không thấy.",
    "OPP": "Sai chiều/ngược — Động từ diễn tả chiều ngược lại với thực tế.",
    # Part 2
    "P2-WHQ": "Sai loại câu hỏi — Trả lời sai loại thông tin câu hỏi yêu cầu.",
    "P2-REP": "Bẫy lặp từ — Lặp lại từ trong câu hỏi để gây cảm giác quen tai nhưng sai logic.",
    "P2-SND": "Bẫy âm tương tự — Dùng từ có phát âm na ná từ trong câu hỏi.",
    "P2-YNA": "Bẫy Yes/No — Trả lời Yes/No cho câu hỏi Wh- hoặc không phù hợp.",
    "P2-TNS": "Sai thì — Sai thì động từ hoặc mốc thời gian so với câu hỏi.",
    "P2-PER": "Sai chủ thể — Nhầm lẫn đại từ hoặc người thực hiện hành động.",
    "P2-REL": "Liên quan chủ đề — Cùng trường từ vựng nhưng không trả lời trọng tâm.",
    "P2-ASS": "Bẫy liên tưởng — Dùng từ gợi liên tưởng đến ngữ cảnh nhưng sai chức năng.",
    "WHQ": "Sai loại câu hỏi — Trả lời sai loại thông tin câu hỏi yêu cầu.",
    "REP": "Bẫy lặp từ — Lặp lại từ trong câu hỏi để gây cảm giác quen tai nhưng sai logic.",
    "SND": "Bẫy âm tương tự — Dùng từ có phát âm na ná từ trong câu hỏi.",
    "YNA": "Bẫy Yes/No — Trả lời Yes/No cho câu hỏi Wh- hoặc không phù hợp.",
    "TNS": "Sai thì — Sai thì động từ hoặc mốc thời gian so với câu hỏi.",
    "PER": "Sai chủ thể — Nhầm lẫn đại từ hoặc người thực hiện hành động.",
    "REL": "Liên quan chủ đề — Cùng trường từ vựng nhưng không trả lời trọng tâm.",
    "ASS": "Bẫy liên tưởng — Dùng từ gợi liên tưởng đến ngữ cảnh nhưng sai chức năng."
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
        if "L10" in lesson_id: return "part2_advanced_indirect"
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
            clean_content = re.sub(r'`[^`]+`', '', clean_content).strip()
            options[letter] = clean_content
        else:
            m_code = re.search(r'`([A-Z0-9_-]+)`', content)
            clean_content = re.sub(r'`[^`]+`', '', content).strip()
            options[letter] = clean_content

            if m_code:
                code = m_code.group(1)
                desc = DISTRACTOR_MAP.get(code, f"Bẫy {code} — Lựa chọn không phù hợp.")
                wrong_reasons[letter] = f"[{code}] {desc}"
            else:
                wrong_reasons[letter] = f"Lựa chọn {letter} không phù hợp với nội dung bài nghe."

    for letter in options:
        if letter != correct_ans and letter not in wrong_reasons:
            wrong_reasons[letter] = f"Lựa chọn {letter} không phù hợp với nội dung bài nghe."

    return options, correct_ans, wrong_reasons

def main():
    with open(CONTENT_MD_PATH, 'r', encoding='utf-8') as f:
        content_text = clean_text(f.read())
    with open(BANK_MD_PATH, 'r', encoding='utf-8') as f:
        bank_text = clean_text(f.read())

    print("Parsing CHAPTER_02_CONTENT.md and CHAPTER_02_BANK.md...")

    all_questions = []
    lessons_data = []

    # Map bank tables to lessons
    bank_part1_map = {
        "CH02-L01": ("## A1", "ch02-bnk-a"),
        "CH02-L02": ("## A2", "ch02-bnk-l"),
        "CH02-L03": ("## A3", "ch02-bnk-v")
    }
    bank_part2_map = {
        "CH02-L05": "## B1",
        "CH02-L06": "## B2",
        "CH02-L07": "## B3",
        "CH02-L08": "## B4",
        "CH02-L09": "## B5"
    }

    lesson_cfgs = [
        {"num": 1, "id": "CH02-L01", "title": "Part 1: Người và hành động", "minCorrect": 12, "total": 15, "percentage": 80.0, "part": 1},
        {"num": 2, "id": "CH02-L02", "title": "Part 1: Vị trí, đồ vật và ảnh không có người", "minCorrect": 12, "total": 15, "percentage": 80.0, "part": 1},
        {"num": 3, "id": "CH02-L03", "title": "Part 1: Bị động, trạng thái và bẫy suy diễn", "minCorrect": 12, "total": 15, "percentage": 80.0, "part": 1},
        {"num": 4, "id": "CH02-L04", "title": "Nghe thật: Âm thanh, nối âm, số và giọng", "minCorrect": 40, "total": 50, "percentage": 80.0, "part": 0},
        {"num": 5, "id": "CH02-L05", "title": "Part 2: Nhận loại câu hỏi trong 3 từ đầu (WH)", "minCorrect": 18, "total": 22, "percentage": 81.8, "part": 2},
        {"num": 6, "id": "CH02-L06", "title": "Part 2: Yes/No, Tag, Phủ định và Lựa chọn", "minCorrect": 18, "total": 22, "percentage": 81.8, "part": 2},
        {"num": 7, "id": "CH02-L07", "title": "Part 2: Câu hỏi gián tiếp, Yêu cầu, Đề nghị, Gợi ý", "minCorrect": 18, "total": 22, "percentage": 81.8, "part": 2},
        {"num": 8, "id": "CH02-L08", "title": "Part 2: Câu trần thuật và Câu trả lời gián tiếp", "minCorrect": 18, "total": 22, "percentage": 81.8, "part": 2},
        {"num": 9, "id": "CH02-L09", "title": "Part 2: Paraphrase và Bản đồ bẫy tổng hợp", "minCorrect": 18, "total": 22, "percentage": 81.8, "part": 2}
    ]

    for cfg in lesson_cfgs:
        l_num = cfg["num"]
        lid = cfg["id"]
        p_start = content_text.find(f"# BÀI {l_num}")
        p_next = content_text.find(f"# BÀI {l_num+1}") if l_num < 9 else content_text.find("# KIỂM TRA")
        l_chunk = content_text[p_start:p_next]

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
            # Lesson 4: Audio drills
            # 1. Core Dictations (D1 to D10)
            d_table_m = re.search(r'## 4\.6\. Drill A[^\n]+\n(.*?)(?=\n## 4\.7|\Z)', l_chunk, re.DOTALL)
            if d_table_m:
                d_lines = d_table_m.group(1).strip().split('\n')
                for line in d_lines:
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
                            "prompt": f"Nghe và chép lại câu (Chú ý: {d_note}):",
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

            # 2. Bank Dictations (D11 to D30)
            c1_m = re.search(r'## C1\. Dictation bổ sung[^\n]+\n(.*?)(?=\n## C2|\Z)', bank_text, re.DOTALL)
            if c1_m:
                lines = [l.strip() for l in c1_m.group(1).strip().split('\n') if l.strip().startswith('|')][2:]
                for line in lines:
                    parts = [p.strip() for p in line.split('|') if p.strip()]
                    if len(parts) >= 2 and parts[0].startswith('D'):
                        d_num = parts[0]
                        d_text = parts[1]
                        d_note = parts[2] if len(parts) > 2 else ""
                        qid = f"CH02-BNK-{d_num}"
                        lesson_qids.append(qid)

                        dictations.append({
                            "id": f"CH02-BNK-{d_num}",
                            "audioText": d_text,
                            "blanks": [d_note] if d_note else [d_text.split()[-1]],
                            "answerInput": d_text,
                            "tags": ["audio_drill", "dictation", "bank"],
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
                                    "voice": "us-male-01" if int(d_num[1:]) % 2 == 1 else "us-female-01",
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
                            "skillTags": ["audio_drill", "dictation", "bank"],
                            "skillGroup": "linking_and_weak_forms",
                            "difficulty": 2,
                            "revision": 2
                        })

            # 3. Bank Numbers/Time (N01 to N20)
            c2_m = re.search(r'## C2\. Số, giờ, giá[^\n]+\n(.*?)(?=\n## C3|\Z)', bank_text, re.DOTALL)
            if c2_m:
                lines = [l.strip() for l in c2_m.group(1).strip().split('\n') if l.strip().startswith('|')][2:]
                for line in lines:
                    parts = [p.strip() for p in line.split('|') if p.strip()]
                    if len(parts) >= 3 and parts[0].startswith('N'):
                        n_num = parts[0]
                        audio_text = parts[1]
                        ans_trap = parts[2]  # e.g. "13 (30)" or "$15 ($50)"

                        # Parse correct ans and trap
                        m_at = re.match(r'^(.*?)\s*\((.*?)\)$', ans_trap)
                        if m_at:
                            val_correct = m_at.group(1).strip()
                            val_trap = m_at.group(2).strip()
                        else:
                            val_correct = ans_trap.split()[0]
                            val_trap = ans_trap.split()[-1]

                        qid = f"CH02-BNK-{n_num}"
                        lesson_qids.append(qid)

                        opts = {
                            "A": val_correct,
                            "B": val_trap
                        }

                        all_questions.append({
                            "id": qid,
                            "groupId": None,
                            "chapterId": "CH02",
                            "lessonId": "CH02-L04",
                            "part": 0,
                            "taskType": "number_drill",
                            "prompt": f"Nghe audio và chọn con số/giờ/giá tiền đúng:",
                            "optionsVisibleBeforeAnswer": True,
                            "image": None,
                            "audioSegments": [
                                {
                                    "text": audio_text,
                                    "voice": "us-female-01" if int(n_num[1:]) % 2 == 1 else "us-male-01",
                                    "file": f"audio/chapter-02/{qid.lower()}.mp3",
                                    "pauseAfterMs": 0
                                }
                            ],
                            "options": opts,
                            "correctAnswer": "A",
                            "transcript": audio_text,
                            "translation": "",
                            "explanation": f"Từ nói trong audio là: '{audio_text}'. Đáp án đúng là {val_correct}. Bẫy nhầm: {val_trap}.",
                            "wrongReasons": {
                                "B": f"Bẫy số/giờ: '{val_trap}' là bẫy dễ nhầm âm hoặc nhầm cách đọc với '{val_correct}'."
                            },
                            "skillTags": ["number_listening", "teen_ty", "time_clock"],
                            "skillGroup": "numbers_and_time",
                            "difficulty": 1,
                            "revision": 2
                        })

        else:
            # 1. Parse core questions from CHAPTER_02_CONTENT.md
            q_matches = re.finditer(r'(#{3,4}\s+(CH02-L\d+-Q\d+)[^\n]*)\n(.*?)(?=\n#{3,4}\s+CH02-|\n### |\n## |\Z)', l_chunk, re.DOTALL)
            for qm in q_matches:
                header_line = qm.group(1).strip()
                qid = qm.group(2).strip()
                qblock = qm.group(3).strip()
                lesson_qids.append(qid)

                difficulty = 1
                if '★3' in header_line: difficulty = 3
                elif '★2' in header_line: difficulty = 2

                exp_m = re.search(r'\*\*Giải thích:\*\*\s*([^\n]+(?:\n[^\n*]+)*)', qblock)
                explanation = exp_m.group(1).strip() if exp_m else ""

                tags = parse_tags(qblock)
                opts, correct_ans, wrong_reasons = parse_options_and_reasons(qblock, explanation)

                if cfg["part"] == 1:
                    img_m = re.search(r'\*\*Ảnh:\*\*\s*([^\n]+)', qblock)
                    img_desc = img_m.group(1).strip() if img_m else ""

                    segments = []
                    for letter in ["A", "B", "C", "D"]:
                        if letter in opts:
                            segments.append({
                                "choiceId": letter,
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
                    q_text_m = re.search(r'\*\*Q:\*\*\s*([^\n]+)', qblock)
                    q_text = q_text_m.group(1).strip() if q_text_m else ""

                    segments = [
                        {
                            "choiceId": None,
                            "text": q_text,
                            "voice": "us-female-01" if "F" in header_line.split('→')[0] else "us-male-01",
                            "file": f"audio/chapter-02/{qid.lower()}-q.mp3",
                            "pauseAfterMs": 1500
                        }
                    ]
                    for letter in ["A", "B", "C"]:
                        if letter in opts:
                            segments.append({
                                "choiceId": letter,
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

            # 2. Parse BANK questions for this lesson
            if cfg["part"] == 1 and lid in bank_part1_map:
                sec_prefix, img_prefix = bank_part1_map[lid]
                sec_p = bank_text.find(sec_prefix)
                sec_end = bank_text.find("##", sec_p + 3) if bank_text.find("##", sec_p + 3) != -1 else len(bank_text)
                sec_chunk = bank_text[sec_p:sec_end]

                tbl_lines = [l.strip() for l in sec_chunk.split('\n') if l.strip().startswith('|')][2:]
                for row in tbl_lines:
                    cols = [c.strip() for c in row.split('|') if c.strip()]
                    if len(cols) >= 7:
                        # ID, Ảnh, A, B, C, D, Đ.án
                        item_code = cols[0]
                        img_desc = cols[1]
                        opt_a = cols[2]
                        opt_b = cols[3]
                        opt_c = cols[4]
                        opt_d = cols[5]
                        correct_ans = cols[6]

                        qid = f"CH02-BNK-{item_code}"
                        lesson_qids.append(qid)

                        opts = {}
                        wrong_reasons = {}
                        for ltr, raw_opt in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d)]:
                            m_code = re.search(r'`([A-Z0-9_-]+)`', raw_opt)
                            clean_opt = re.sub(r'`[^`]+`', '', raw_opt).strip()
                            opts[ltr] = clean_opt
                            if ltr != correct_ans:
                                if m_code:
                                    code = m_code.group(1)
                                    wrong_reasons[ltr] = f"[{code}] {DISTRACTOR_MAP.get(code, 'Lựa chọn không khớp với ảnh.')}"
                                else:
                                    wrong_reasons[ltr] = f"Lựa chọn {ltr} không phù hợp với chi tiết trong ảnh."

                        segments = []
                        for ltr in ["A", "B", "C", "D"]:
                            segments.append({
                                "choiceId": ltr,
                                "text": opts[ltr],
                                "voice": "us-female-01" if int(item_code[-1]) % 2 == 1 else "us-male-01",
                                "file": f"audio/chapter-02/{qid.lower()}-{ltr.lower()}.mp3",
                                "pauseAfterMs": 1000
                            })

                        all_questions.append({
                            "id": qid,
                            "groupId": None,
                            "chapterId": "CH02",
                            "lessonId": lid,
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
                            "explanation": f"Lựa chọn đúng ({correct_ans}): {opts[correct_ans]}. Mô tả chính xác đối tượng và hành động trong ảnh.",
                            "wrongReasons": wrong_reasons,
                            "skillTags": ["part1_bank", "photo_description"],
                            "skillGroup": determine_skill_group(1, [], lid),
                            "difficulty": 2,
                            "revision": 2
                        })

            elif cfg["part"] == 2 and lid in bank_part2_map:
                sec_prefix = bank_part2_map[lid]
                sec_p = bank_text.find(sec_prefix)
                sec_end = bank_text.find("##", sec_p + 3) if bank_text.find("##", sec_p + 3) != -1 else len(bank_text)
                sec_chunk = bank_text[sec_p:sec_end]

                tbl_lines = [l.strip() for l in sec_chunk.split('\n') if l.strip().startswith('|')][2:]
                for row in tbl_lines:
                    cols = [c.strip() for c in row.split('|') if c.strip()]
                    if len(cols) >= 6:
                        # ID, Q, A, B, C, Đ.án
                        item_code = cols[0]
                        q_text = cols[1]
                        opt_a = cols[2]
                        opt_b = cols[3]
                        opt_c = cols[4]
                        correct_ans = cols[5]

                        qid = f"CH02-BNK-{item_code}"
                        lesson_qids.append(qid)

                        opts = {}
                        wrong_reasons = {}
                        for ltr, raw_opt in [("A", opt_a), ("B", opt_b), ("C", opt_c)]:
                            m_code = re.search(r'`([A-Z0-9_-]+)`', raw_opt)
                            clean_opt = re.sub(r'`[^`]+`', '', raw_opt).strip()
                            opts[ltr] = clean_opt
                            if ltr != correct_ans:
                                if m_code:
                                    code = m_code.group(1)
                                    wrong_reasons[ltr] = f"[{code}] {DISTRACTOR_MAP.get(code, 'Phản hồi không phù hợp với câu hỏi.')}"
                                else:
                                    wrong_reasons[ltr] = f"Lựa chọn {ltr} không phù hợp với logic câu hỏi."

                        segments = [
                            {
                                "choiceId": None,
                                "text": q_text,
                                "voice": "us-female-01" if int(item_code[-1]) % 2 == 1 else "us-male-01",
                                "file": f"audio/chapter-02/{qid.lower()}-q.mp3",
                                "pauseAfterMs": 1500
                            }
                        ]
                        for ltr in ["A", "B", "C"]:
                            segments.append({
                                "choiceId": ltr,
                                "text": opts[ltr],
                                "voice": "us-male-01" if int(item_code[-1]) % 2 == 1 else "us-female-01",
                                "file": f"audio/chapter-02/{qid.lower()}-{ltr.lower()}.mp3",
                                "pauseAfterMs": 1000
                            })

                        all_questions.append({
                            "id": qid,
                            "groupId": None,
                            "chapterId": "CH02",
                            "lessonId": lid,
                            "part": 2,
                            "taskType": "part2_response",
                            "prompt": "Nghe câu hỏi và chọn câu phản hồi phù hợp nhất (Part 2):",
                            "optionsVisibleBeforeAnswer": False,
                            "image": None,
                            "audioSegments": segments,
                            "options": opts,
                            "correctAnswer": correct_ans,
                            "transcript": f"{q_text} / (A) {opts['A']} / (B) {opts['B']} / (C) {opts['C']}",
                            "translation": "",
                            "explanation": f"Lựa chọn ({correct_ans}) là phản hồi tự nhiên và chính xác nhất cho câu hỏi: '{q_text}'.",
                            "wrongReasons": wrong_reasons,
                            "skillTags": ["part2_bank", "response"],
                            "skillGroup": determine_skill_group(2, [], lid),
                            "difficulty": 2,
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
                "total": len(lesson_qids),
                "percentage": round((cfg["minCorrect"] / len(lesson_qids)) * 100, 1)
            }
        })

    # 2.5. Parse Section E (Part 2 độ khó gần đề thật, 40 câu H01-H40) -> CH02-L10
    print("Parsing Section E: Part 2 độ khó gần đề thật (H01-H40)...")
    p_sec_e = bank_text.find("# PHẦN E")
    if p_sec_e != -1:
        sec_e_chunk = bank_text[p_sec_e:]
        sec_e_qids = []
        for line in sec_e_chunk.split('\n'):
            line = line.strip()
            if not line.startswith('|') or 'ID' in line or '---' in line:
                continue
            cols = [c.strip() for c in line.split('|')[1:-1]]
            if len(cols) >= 6 and re.match(r'H\d+', cols[0]):
                item_code = cols[0]
                q_text = cols[1]
                opt_a = cols[2]
                opt_b = cols[3]
                opt_c = cols[4]
                correct_ans = cols[5]

                qid = f"CH02-BNK-{item_code}"
                sec_e_qids.append(qid)

                opts = {}
                wrong_reasons = {}
                for ltr, raw_opt in [("A", opt_a), ("B", opt_b), ("C", opt_c)]:
                    m_code = re.search(r'`([A-Z0-9_-]+)`', raw_opt)
                    clean_opt = re.sub(r'`[^`]+`', '', raw_opt).strip()
                    opts[ltr] = clean_opt
                    if ltr != correct_ans:
                        if m_code:
                            code = m_code.group(1)
                            wrong_reasons[ltr] = f"[{code}] {DISTRACTOR_MAP.get(code, 'Phản hồi không phù hợp với câu hỏi.')}"
                        else:
                            wrong_reasons[ltr] = f"Lựa chọn {ltr} không phù hợp với logic câu hỏi."

                num = int(item_code[1:])
                segments = [
                    {
                        "choiceId": None,
                        "text": q_text,
                        "voice": "us-female-01" if num % 2 == 1 else "us-male-01",
                        "file": f"audio/chapter-02/{qid.lower()}-q.mp3",
                        "pauseAfterMs": 1500
                    }
                ]
                for ltr in ["A", "B", "C"]:
                    segments.append({
                        "choiceId": ltr,
                        "text": opts[ltr],
                        "voice": "us-male-01" if num % 2 == 1 else "us-female-01",
                        "file": f"audio/chapter-02/{qid.lower()}-{ltr.lower()}.mp3",
                        "pauseAfterMs": 1000
                    })

                all_questions.append({
                    "id": qid,
                    "groupId": None,
                    "chapterId": "CH02",
                    "lessonId": "CH02-L10",
                    "part": 2,
                    "taskType": "part2_response",
                    "prompt": "Nghe câu hỏi và chọn câu phản hồi phù hợp nhất (Part 2 — Độ khó gần đề thật):",
                    "optionsVisibleBeforeAnswer": False,
                    "image": None,
                    "audioSegments": segments,
                    "options": opts,
                    "correctAnswer": correct_ans,
                    "transcript": f"{q_text} / (A) {opts['A']} / (B) {opts['B']} / (C) {opts['C']}",
                    "translation": "",
                    "explanation": f"Lựa chọn ({correct_ans}) là phản hồi tự nhiên và chính xác nhất cho câu hỏi: '{q_text}'.",
                    "wrongReasons": wrong_reasons,
                    "skillTags": ["part2_bank", "advanced", "indirect_response", "trap_avoidance"],
                    "skillGroup": "part2_advanced_indirect",
                    "difficulty": 3,
                    "revision": 2
                })

        lessons_data.append({
            "lessonId": "CH02-L10",
            "title": "Part 2 độ khó gần đề thật — Trả lời gián tiếp & Phản xạ bẫy",
            "objectives": [
                "Luyện tập 40 câu hỏi Part 2 độ khó cao với câu trả lời gián tiếp, thông tin mới và phản câu hỏi.",
                "Loại trừ triệt để bẫy lặp từ (REP), bẫy cùng chủ đề (REL), sai thì (TNS) và bẫy Yes/No (YNA).",
                "Đạt tối thiểu 30/40 câu (75%) ở tốc độ chuẩn 1.0x để sẵn sàng cho bài thi TOEIC thật."
            ],
            "teachingBlocks": [
                {
                    "type": "concept",
                    "title": "Chiến lược xử lý Part 2 độ khó cao trong đề thi thật",
                    "content": "Trong đề thi TOEIC thật, các câu Part 2 nâng cao thường không trả lời trực tiếp mà dùng câu trả lời gián tiếp, phản câu hỏi hoặc giải pháp thay thế. Các phương án sai thường cố tình lặp lại từ trong câu hỏi hoặc dùng từ cùng chủ đề để đánh lừa người học."
                },
                {
                    "type": "tip",
                    "title": "3 nguyên tắc vàng khi nghe Part 2 nâng cao",
                    "content": "1. Cảnh giác với bẫy lặp từ: Nếu câu trả lời lặp lại nguyên si từ nghe thấy trong câu hỏi, khả năng cao là bẫy (REP).\n2. Tuyệt đối không chọn Yes/No khi câu hỏi bắt đầu bằng Wh- (Who, Where, When, Why, How, What).\n3. Nghe trọn vẹn cả 3 phương án (A), (B), (C) trước khi đưa ra quyết định."
                }
            ],
            "dictations": [],
            "questionIds": sec_e_qids,
            "passRule": {
                "minCorrect": 30,
                "total": len(sec_e_qids),
                "percentage": round((30 / len(sec_e_qids)) * 100, 1)
            }
        })

    # 3. Parse Final Test (25 questions from CHAPTER_02_CONTENT.md)
    print("Parsing Final Test CH02-FINAL...")
    p_final = content_text.find("# KIỂM TRA CUỐI CHƯƠNG 2")
    final_chunk = content_text[p_final:]

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
                        "choiceId": letter,
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
                    "choiceId": None,
                    "text": q_text,
                    "voice": "us-female-01" if "F" in f_header.split('→')[0] else "us-male-01",
                    "file": f"audio/chapter-02/{qid.lower()}-q.mp3",
                    "pauseAfterMs": 1500
                }
            ]
            for letter in ["A", "B", "C"]:
                if letter in opts:
                    segments.append({
                        "choiceId": letter,
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
        "description": "Chiến thuật mô tả tranh Part 1, giải mã âm thực tế và phản xạ câu hỏi – phản hồi với 230 câu luyện tập chuyên sâu",
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
    for l in lessons_data:
        print(f"  {l['lessonId']}: {len(l['questionIds'])} questions (passRule: {l['passRule']})")

    with open(OUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(chapter_data, f, indent=2, ensure_ascii=False)
    print(f"Successfully wrote {OUT_PATH}!")

if __name__ == "__main__":
    main()
