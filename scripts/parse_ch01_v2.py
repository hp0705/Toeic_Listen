#!/usr/bin/env python3
"""
Parser for revamped CHAPTER_01_CONTENT.md v2.0
Builds complete data/chapters/chapter-01.json
"""

import os
import re
import json

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD_PATH = os.path.join(ROOT_DIR, "CHAPTER_01_CONTENT.md")
OUT_PATH = os.path.join(ROOT_DIR, "data", "chapters", "chapter-01.json")

def parse_tags(text):
    return re.findall(r'`([a-z0-9_]+)`', text)

def clean_text(text):
    return text.strip().replace('\r\n', '\n').replace('\r', '\n')

def extract_wrong_reasons(wrong_text, options, correct_ans):
    wrong_reasons = {}
    for opt in options.keys():
        if opt == correct_ans:
            continue
        # Look for pattern like "A và C là..." or "A là..." or "- A: ..."
        m = re.search(rf'(?:^|\b|\W){opt}\s*(?:và\s+[A-D]\s*)?(?:là|nói|đổi|nghe|lặp|sai|không|chỉ|trả lời|[—:–])\s*([^.;\n]+)', wrong_text, re.IGNORECASE)
        if m:
            wrong_reasons[opt] = f"{opt} {m.group(1).strip()}"
        else:
            wrong_reasons[opt] = f"Lựa chọn {opt} không phù hợp với thông tin trong bài nghe."
    return wrong_reasons

def determine_skill_group(tags):
    tag_set = set(tags)
    if tag_set.intersection({"weak_form", "sentence_stress", "linking"}):
        return "weak_forms_and_linking"
    if tag_set.intersection({"final_s", "final_ed", "final_voicing", "final_consonant", "contraction", "negative_contraction"}):
        return "final_sounds_and_contractions"
    if tag_set.intersection({"teen_ty", "number_sequence", "money", "time_clock", "date_day", "duration", "number_correction"}):
        return "numbers_and_time"
    if any(t.startswith("wh_") for t in tags) or "indirect_q" in tag_set:
        return "question_words"
    if any(t.startswith("trap_") for t in tags) or tag_set.intersection({"choice_q", "yes_no_q", "tag_q", "statement_response", "request_response", "offer_response", "suggestion_response", "indirect_answer"}):
        return "part2_traps_and_strategies"
    if tag_set.intersection({"conv_gist", "conv_detail", "conv_action", "conv_next_action"}):
        return "short_conversations"
    return "foundation_listening"

def parse_abx_table(tbl_text):
    items = []
    lines = [l.strip() for l in tbl_text.strip().split('\n') if l.strip()]
    # header is lines[0], separator is lines[1]
    for line in lines[2:]:
        parts = [p.strip() for p in line.split('|')]
        # format: | ID | A | B | X (audio) | Đáp án | Tags |
        # len(parts) >= 7 (first and last are empty strings due to leading/trailing '|')
        valid_parts = [p for p in parts if p]
        if len(valid_parts) >= 6:
            item_id = valid_parts[0]
            text_a = valid_parts[1]
            text_b = valid_parts[2]
            text_x = valid_parts[3]
            ans = valid_parts[4].strip()
            tags = parse_tags(valid_parts[5])
            items.append({
                "id": item_id,
                "textA": text_a,
                "textB": text_b,
                "textX": text_x,
                "correctAnswer": ans,
                "tags": tags,
                "audioA": f"audio/chapter-01/{item_id.lower()}-a.mp3",
                "audioB": f"audio/chapter-01/{item_id.lower()}-b.mp3",
                "audioX": f"audio/chapter-01/{item_id.lower()}-x.mp3"
            })
    return items

def parse_dictation_table(tbl_text):
    items = []
    lines = [l.strip() for l in tbl_text.strip().split('\n') if l.strip()]
    for line in lines[2:]:
        valid_parts = [p.strip() for p in line.split('|') if p.strip()]
        if len(valid_parts) == 3:
            # | ID | Audio text | Tags |
            item_id = valid_parts[0]
            audio_text = valid_parts[1]
            tags = parse_tags(valid_parts[2])
            blanks = re.findall(r'\*\*(.*?)\*\*', audio_text)
            items.append({
                "id": item_id,
                "audioText": audio_text,
                "blanks": blanks,
                "answerInput": "; ".join(blanks),
                "tags": tags,
                "audioFile": f"audio/chapter-01/{item_id.lower()}.mp3"
            })
        elif len(valid_parts) >= 4:
            # | ID | Audio text | Đáp án nhập | Tags |
            item_id = valid_parts[0]
            audio_text = valid_parts[1]
            answer_input = valid_parts[2]
            tags = parse_tags(valid_parts[3])
            blanks = re.findall(r'\*\*(.*?)\*\*', audio_text)
            if not blanks:
                blanks = [answer_input]
            items.append({
                "id": item_id,
                "audioText": audio_text,
                "blanks": blanks,
                "answerInput": answer_input,
                "tags": tags,
                "audioFile": f"audio/chapter-01/{item_id.lower()}.mp3"
            })
    return items

def main():
    with open(MD_PATH, 'r', encoding='utf-8') as f:
        raw_text = clean_text(f.read())

    print("Parsing CHAPTER_01_CONTENT.md v2.0...")

    # Build lessons
    lessons_data = []
    all_questions = []
    groups_data = []

    # Lesson meta config
    lesson_configs = [
        {"num": 1, "id": "CH01-L01", "title": "Nhịp câu, từ khóa và dạng đọc yếu", "minCorrect": 5, "total": 6, "percentage": 83.3},
        {"num": 2, "id": "CH01-L02", "title": "Âm cuối, nối âm và dạng rút gọn", "minCorrect": 5, "total": 6, "percentage": 83.3},
        {"num": 3, "id": "CH01-L03", "title": "Số, giờ, ngày tháng và giá tiền", "minCorrect": 5, "total": 6, "percentage": 83.3},
        {"num": 4, "id": "CH01-L04", "title": "Từ để hỏi và loại thông tin cần tìm", "minCorrect": 6, "total": 8, "percentage": 75.0},
        {"num": 5, "id": "CH01-L05", "title": "Part 2 thực chiến: Chọn phản hồi phù hợp", "minCorrect": 13, "total": 16, "percentage": 81.25},
        {"num": 6, "id": "CH01-L06", "title": "Hội thoại ngắn: Cầu nối sang Part 3", "minCorrect": 5, "total": 6, "percentage": 83.3}
    ]

    for idx, cfg in enumerate(lesson_configs):
        l_num = cfg["num"]
        p_start = raw_text.find(f"# BÀI {l_num}")
        p_next = raw_text.find(f"# BÀI {l_num+1}") if l_num < 6 else raw_text.find("# KIỂM TRA")
        l_chunk = raw_text[p_start:p_next]

        # Extract objectives
        obj_m = re.search(r'## Mục tiêu\s*\n((?:- [^\n]+\n?)+)', l_chunk)
        objectives = [o.strip()[2:].strip() for o in obj_m.group(1).split('\n') if o.strip()] if obj_m else []

        # Extract teaching blocks
        # Any ## x.y. before ABX / Nghe-chép / Bài luyện
        teaching_blocks = []
        tb_matches = re.finditer(r'## (\d+\.\d+\.\s*[^\n]+)\n(.*?)(?=\n## |\n# |\Z)', l_chunk, re.DOTALL)
        for tbm in tb_matches:
            tb_title = tbm.group(1).strip()
            tb_content = tbm.group(2).strip()
            # Skip ABX, dictation, exercise sections from teaching blocks
            if any(k in tb_title.lower() for k in ["abx", "nghe đối chiếu", "nghe-chép", "bài luyện", "hội thoại luyện tập"]):
                continue
            teaching_blocks.append({
                "title": tb_title,
                "content": tb_content
            })

        # Extract vocabulary (if present)
        vocabulary = []
        vocab_tbl = re.search(r'\| Từ/cụm \| Nghĩa \| Cụm thường gặp \|\n\|[-|\s]+\|\n((?:\|[^\n]+\|\n?)+)', l_chunk)
        if vocab_tbl:
            for vline in vocab_tbl.group(1).strip().split('\n'):
                vparts = [p.strip() for p in vline.split('|') if p.strip()]
                if len(vparts) >= 2:
                    vocabulary.append({
                        "word": vparts[0],
                        "meaning": vparts[1],
                        "example": vparts[2] if len(vparts) > 2 else ""
                    })

        # Extract ABX exercises
        abx_exercises = []
        abx_tbl = re.search(r'(\| ID \| A \| B \| X \(audio\) \| Đáp án \| Tags \|\n\|[-|\s]+\|\n(?:\|[^\n]+\|\n?)+)', l_chunk)
        if abx_tbl:
            abx_exercises = parse_abx_table(abx_tbl.group(1))

        # Extract Dictation exercises
        dictations = []
        dict_tbl = re.search(r'(\| ID \| Audio text[^\n]+\|\n\|[-|\s]+\|\n(?:\|[^\n]+\|\n?)+)', l_chunk)
        if dict_tbl:
            dictations = parse_dictation_table(dict_tbl.group(1))

        # Extract practice questions for this lesson
        lesson_qids = []

        if l_num in [1, 2, 3]:
            # L01 - L03: Foundation Listening MCQ
            q_matches = re.finditer(r'### (CH01-L0\d-Q\d+)\n(.*?)(?=\n### |\n# |\Z)', l_chunk, re.DOTALL)
            for qm in q_matches:
                qid = qm.group(1).strip()
                qblock = qm.group(2).strip()
                lesson_qids.append(qid)

                audio_m = re.search(r'\*\*Audio:\*\*\s*`([^`]+)`', qblock)
                audio_text = audio_m.group(1).strip() if audio_m else ""

                prompt_m = re.search(r'\*\*Question:\*\*\s*([^\n]+)', qblock)
                prompt_text = prompt_m.group(1).strip() if prompt_m else ""

                ans_m = re.search(r'\*\*Đáp án:\*\*\s*([A-D])', qblock)
                correct_ans = ans_m.group(1).strip() if ans_m else "A"

                exp_m = re.search(r'\*\*Giải thích:\*\*\s*([^\n]+(?:\n[^\n*]+)*)', qblock)
                explanation = exp_m.group(1).strip() if exp_m else ""

                wrong_m = re.search(r'\*\*Sai vì:\*\*\s*([^\n]+(?:\n[^\n*]+)*)', qblock)
                wrong_str = wrong_m.group(1).strip() if wrong_m else ""

                tags = parse_tags(qblock[qblock.find('**Tags:**'):] if '**Tags:**' in qblock else "")
                opts = dict(re.findall(r'-\s*([A-D])[.:]\s*([^\n]+)', qblock))

                wrong_reasons = extract_wrong_reasons(wrong_str, opts, correct_ans)

                all_questions.append({
                    "id": qid,
                    "groupId": None,
                    "chapterId": "CH01",
                    "lessonId": cfg["id"],
                    "part": 0,
                    "taskType": "foundation_listening",
                    "prompt": prompt_text,
                    "optionsVisibleBeforeAnswer": True,
                    "image": None,
                    "audioSegments": [
                        {
                            "text": audio_text,
                            "voice": "us-female-01" if int(qid[-1]) % 2 == 1 else "us-male-01",
                            "file": f"audio/chapter-01/{qid.lower()}.mp3",
                            "pauseAfterMs": 0
                        }
                    ],
                    "options": opts,
                    "correctAnswer": correct_ans,
                    "transcript": audio_text,
                    "translation": "",
                    "explanation": explanation,
                    "wrongReasons": wrong_reasons,
                    "skillTags": tags,
                    "skillGroup": determine_skill_group(tags),
                    "difficulty": 1,
                    "revision": 2
                })

        elif l_num in [4, 5]:
            # L04 & L05: Part 2 format
            q_matches = re.finditer(r'### (CH01-L0\d-Q\d+)(?:[^\n]*)\n(.*?)(?=\n### |\n# |\Z)', l_chunk, re.DOTALL)
            for qm in q_matches:
                qid = qm.group(1).strip()
                qblock = qm.group(2).strip()
                lesson_qids.append(qid)

                q_audio_m = re.search(r'\*\*Audio question:\*\*\s*([^\n]+)', qblock)
                q_audio = q_audio_m.group(1).strip() if q_audio_m else ""

                ans_m = re.search(r'\*\*Đáp án:\*\*\s*([A-D])', qblock)
                correct_ans = ans_m.group(1).strip() if ans_m else "A"

                exp_m = re.search(r'\*\*Giải thích:\*\*\s*([^\n]+(?:\n[^\n*]+)*)', qblock)
                explanation = exp_m.group(1).strip() if exp_m else ""

                wrong_m = re.search(r'\*\*Sai vì:\*\*\s*([^\n]+(?:\n[^\n*]+)*)', qblock)
                wrong_str = wrong_m.group(1).strip() if wrong_m else ""

                tags = parse_tags(qblock[qblock.find('**Tags:**'):] if '**Tags:**' in qblock else "")
                opts = dict(re.findall(r'-\s*([A-D])[.:]\s*([^\n]+)', qblock))
                wrong_reasons = extract_wrong_reasons(wrong_str, opts, correct_ans)

                segments = [
                    {
                        "text": q_audio,
                        "voice": "us-female-01",
                        "file": f"audio/chapter-01/{qid.lower()}-q.mp3",
                        "pauseAfterMs": 1500
                    }
                ]
                for letter in ["A", "B", "C"]:
                    if letter in opts:
                        segments.append({
                            "text": f"({letter}) {opts[letter]}",
                            "voice": "us-male-01" if letter == "B" else "us-female-01",
                            "file": f"audio/chapter-01/{qid.lower()}-{letter.lower()}.mp3",
                            "pauseAfterMs": 1200
                        })

                all_questions.append({
                    "id": qid,
                    "groupId": None,
                    "chapterId": "CH01",
                    "lessonId": cfg["id"],
                    "part": 2,
                    "taskType": "part2_response",
                    "prompt": "Nghe câu hỏi và chọn câu phản hồi phù hợp nhất (Mark your answer on your answer sheet):",
                    "optionsVisibleBeforeAnswer": False,
                    "image": None,
                    "audioSegments": segments,
                    "options": opts,
                    "correctAnswer": correct_ans,
                    "transcript": f"{q_audio} / (A) {opts.get('A','')} / (B) {opts.get('B','')} / (C) {opts.get('C','')}",
                    "translation": "",
                    "explanation": explanation,
                    "wrongReasons": wrong_reasons,
                    "skillTags": tags,
                    "skillGroup": determine_skill_group(tags),
                    "difficulty": 1 if l_num == 4 else 2,
                    "revision": 2
                })

        elif l_num == 6:
            # L06: Short conversations
            c_matches = re.finditer(r'### (CH01-L06-C\d+)\n(.*?)(?=\n### |\n# |\Z)', l_chunk, re.DOTALL)
            for cm in c_matches:
                cid = cm.group(1).strip()
                cblock = cm.group(2).strip()

                # Extract conversation turns
                # Lines starting with **W:** or **M:**
                dialogue_lines = []
                turns = []
                t_idx = 1
                for line in cblock.split('\n'):
                    m_turn = re.match(r'\*\*(W|M|W1|M1):\*\*\s*(.+)', line.strip())
                    if m_turn:
                        spk = m_turn.group(1)
                        spk_id = "W1" if spk.startswith("W") else "M1"
                        stext = m_turn.group(2).strip()
                        dialogue_lines.append(f"{spk_id}: {stext}")
                        turns.append({
                            "turn": t_idx,
                            "speakerId": spk_id,
                            "text": stext,
                            "pauseAfterMs": 400,
                            "startMs": (t_idx - 1) * 4500,
                            "endMs": t_idx * 4500 - 400
                        })
                        t_idx += 1

                # Extract Q1 and Q2
                q_matches_c = re.finditer(r'\*\*Q(\d+)\s*\((CH01-L06-C\d+-Q\d+)\):\*\*\s*([^\n]+)\n(.*?)(?=\*\*Q\d+|\Z)', cblock, re.DOTALL)
                c_qids = []
                for qmc in q_matches_c:
                    q_num = qmc.group(1)
                    qid = qmc.group(2)
                    prompt_text = qmc.group(3).strip()
                    sub_block = qmc.group(4).strip()
                    c_qids.append(qid)
                    lesson_qids.append(qid)

                    ans_m = re.search(r'\*\*Đáp án:\*\*\s*([A-D])', sub_block)
                    correct_ans = ans_m.group(1).strip() if ans_m else "A"

                    exp_m = re.search(r'\*\*Giải thích:\*\*\s*([^\n]+(?:\n[^\n*]+)*)', sub_block)
                    explanation = exp_m.group(1).strip() if exp_m else ""

                    wrong_m = re.search(r'\*\*Sai vì:\*\*\s*([^\n]+(?:\n[^\n*]+)*)', sub_block)
                    wrong_str = wrong_m.group(1).strip() if wrong_m else ""

                    tags = parse_tags(sub_block[sub_block.find('**Tags:**'):] if '**Tags:**' in sub_block else "")
                    opts = dict(re.findall(r'-\s*([A-D])[.:]\s*([^\n]+)', sub_block))
                    wrong_reasons = extract_wrong_reasons(wrong_str, opts, correct_ans)

                    all_questions.append({
                        "id": qid,
                        "groupId": cid,
                        "chapterId": "CH01",
                        "lessonId": "CH01-L06",
                        "part": 3,
                        "taskType": "conversation_question",
                        "prompt": prompt_text,
                        "optionsVisibleBeforeAnswer": True,
                        "image": None,
                        "audioSegments": None,
                        "options": opts,
                        "correctAnswer": correct_ans,
                        "transcript": " / ".join(dialogue_lines),
                        "translation": "",
                        "explanation": explanation,
                        "wrongReasons": wrong_reasons,
                        "skillTags": tags,
                        "skillGroup": determine_skill_group(tags),
                        "difficulty": 1,
                        "revision": 2
                    })

                groups_data.append({
                    "id": cid,
                    "chapterId": "CH01",
                    "lessonId": "CH01-L06",
                    "part": 3,
                    "groupType": "short_conversation",
                    "context": "Hội thoại ngắn 2 người",
                    "speakers": [
                        {"speakerId": "W1", "label": "Woman", "gender": "female"},
                        {"speakerId": "M1", "label": "Man", "gender": "male"}
                    ],
                    "voiceAssignment": {
                        "W1": "us-female-01",
                        "M1": "us-male-01"
                    },
                    "turns": turns,
                    "audioFile": f"audio/chapter-01/{cid.lower()}.mp3",
                    "transcript": " / ".join(dialogue_lines),
                    "translation": "",
                    "questionIds": c_qids,
                    "revision": 2
                })

        lessons_data.append({
            "lessonId": cfg["id"],
            "title": cfg["title"],
            "objectives": objectives,
            "teachingBlocks": teaching_blocks,
            "vocabulary": vocabulary,
            "abxExercises": abx_exercises,
            "dictations": dictations,
            "questionIds": lesson_qids,
            "passRule": {
                "minCorrect": cfg["minCorrect"],
                "total": cfg["total"],
                "percentage": cfg["percentage"]
            }
        })

    # Now parse KIỂM TRA CUỐI CHƯƠNG 1 (30 câu)
    print("Parsing Final Test...")
    p_final = raw_text.find("# KIỂM TRA CUỐI CHƯƠNG")
    final_chunk = raw_text[p_final:]

    final_qids = []

    # Final Part A: Dictation (10 questions)
    p_fa = final_chunk.find("## PHẦN A — NGHE-CHÉP (10 câu)")
    p_fb = final_chunk.find("## PHẦN B — PART 2 (14 câu)")
    fa_chunk = final_chunk[p_fa:p_fb]
    fa_tbl = re.search(r'(\| ID \| Audio text[^\n]+\|\n\|[-|\s]+\|\n(?:\|[^\n]+\|\n?)+)', fa_chunk)
    if fa_tbl:
        fa_items = parse_dictation_table(fa_tbl.group(1))
        for item in fa_items:
            qid = item["id"]
            final_qids.append(qid)
            # Create a question entry for dictation
            # In order to allow both flexible typing and options validation, we set taskType: "dictation"
            all_questions.append({
                "id": qid,
                "groupId": None,
                "chapterId": "CH01",
                "lessonId": "CH01-FINAL",
                "part": 0,
                "taskType": "dictation",
                "prompt": f"Nghe và điền từ/số còn thiếu vào chỗ trống:",
                "optionsVisibleBeforeAnswer": False,
                "image": None,
                "audioSegments": [
                    {
                        "text": re.sub(r'\*\*(.*?)\*\*', r'\1', item["audioText"]),
                        "voice": "us-female-01" if int(qid[-1]) % 2 == 1 else "us-male-01",
                        "file": f"audio/chapter-01/{qid.lower()}.mp3",
                        "pauseAfterMs": 0
                    }
                ],
                "options": {
                    "ANSWER": item["answerInput"]
                },
                "correctAnswer": "ANSWER",
                "audioText": item["audioText"],
                "blanks": item["blanks"],
                "answerInput": item["answerInput"],
                "transcript": item["audioText"],
                "translation": "",
                "explanation": f"Đáp án chính xác: {item['answerInput']}",
                "wrongReasons": {},
                "skillTags": item["tags"],
                "skillGroup": determine_skill_group(item["tags"]),
                "difficulty": 2,
                "revision": 2
            })

    # Final Part B: Part 2 (14 questions)
    p_fc = final_chunk.find("## PHẦN C — HỘI THOẠI NGẮN (6 câu)")
    fb_chunk = final_chunk[p_fb:p_fc]
    fb_matches = re.finditer(r'### (CH01-FINAL-B\d+)\n(.*?)(?=\n### |\n## |\Z)', fb_chunk, re.DOTALL)
    for fbm in fb_matches:
        qid = fbm.group(1).strip()
        qblock = fbm.group(2).strip()
        final_qids.append(qid)

        q_audio_m = re.search(r'\*\*Audio question:\*\*\s*([^\n]+)', qblock)
        q_audio = q_audio_m.group(1).strip() if q_audio_m else ""

        ans_m = re.search(r'\*\*Đáp án:\*\*\s*([A-D])', qblock)
        correct_ans = ans_m.group(1).strip() if ans_m else "A"

        exp_m = re.search(r'\*\*Giải thích:\*\*\s*([^\n]+(?:\n[^\n*]+)*)', qblock)
        explanation = exp_m.group(1).strip() if exp_m else ""

        wrong_m = re.search(r'\*\*Sai vì:\*\*\s*([^\n]+(?:\n[^\n*]+)*)', qblock)
        wrong_str = wrong_m.group(1).strip() if wrong_m else ""

        tags = parse_tags(qblock[qblock.find('**Tags:**'):] if '**Tags:**' in qblock else "")
        opts = dict(re.findall(r'-\s*([A-D])[.:]\s*([^\n]+)', qblock))
        wrong_reasons = extract_wrong_reasons(wrong_str, opts, correct_ans)

        segments = [
            {
                "text": q_audio,
                "voice": "us-female-01",
                "file": f"audio/chapter-01/{qid.lower()}-q.mp3",
                "pauseAfterMs": 1500
            }
        ]
        for letter in ["A", "B", "C"]:
            if letter in opts:
                segments.append({
                    "text": f"({letter}) {opts[letter]}",
                    "voice": "us-male-01" if letter == "B" else "us-female-01",
                    "file": f"audio/chapter-01/{qid.lower()}-{letter.lower()}.mp3",
                    "pauseAfterMs": 1200
                })

        all_questions.append({
            "id": qid,
            "groupId": None,
            "chapterId": "CH01",
            "lessonId": "CH01-FINAL",
            "part": 2,
            "taskType": "part2_response",
            "prompt": "Nghe câu hỏi và chọn câu phản hồi phù hợp nhất (Part 2):",
            "optionsVisibleBeforeAnswer": False,
            "image": None,
            "audioSegments": segments,
            "options": opts,
            "correctAnswer": correct_ans,
            "transcript": f"{q_audio} / (A) {opts.get('A','')} / (B) {opts.get('B','')} / (C) {opts.get('C','')}",
            "translation": "",
            "explanation": explanation,
            "wrongReasons": wrong_reasons,
            "skillTags": tags,
            "skillGroup": determine_skill_group(tags),
            "difficulty": 2,
            "revision": 2
        })

    # Final Part C: Short conversations (3 conversations x 2 questions = 6 questions)
    fc_chunk = final_chunk[p_fc:]
    fc_matches = re.finditer(r'### (CH01-FINAL-C\d+)\n(.*?)(?=\n### |\n# |\Z)', fc_chunk, re.DOTALL)
    for fcm in fc_matches:
        cid = fcm.group(1).strip()
        cblock = fcm.group(2).strip()

        dialogue_lines = []
        turns = []
        t_idx = 1
        for line in cblock.split('\n'):
            m_turn = re.match(r'\*\*(W|M|W1|M1):\*\*\s*(.+)', line.strip())
            if m_turn:
                spk = m_turn.group(1)
                spk_id = "W1" if spk.startswith("W") else "M1"
                stext = m_turn.group(2).strip()
                dialogue_lines.append(f"{spk_id}: {stext}")
                turns.append({
                    "turn": t_idx,
                    "speakerId": spk_id,
                    "text": stext,
                    "pauseAfterMs": 400,
                    "startMs": (t_idx - 1) * 4500,
                    "endMs": t_idx * 4500 - 400
                })
                t_idx += 1

        q_matches_fc = re.finditer(r'\*\*Q(\d+)\s*\((CH01-FINAL-C\d+-Q\d+)\):\*\*\s*([^\n]+)\n(.*?)(?=\*\*Q\d+|\Z)', cblock, re.DOTALL)
        c_qids = []
        for qmc in q_matches_fc:
            q_num = qmc.group(1)
            qid = qmc.group(2)
            prompt_text = qmc.group(3).strip()
            sub_block = qmc.group(4).strip()
            c_qids.append(qid)
            final_qids.append(qid)

            ans_m = re.search(r'\*\*Đáp án:\*\*\s*([A-D])', sub_block)
            correct_ans = ans_m.group(1).strip() if ans_m else "A"

            exp_m = re.search(r'\*\*Giải thích:\*\*\s*([^\n]+(?:\n[^\n*]+)*)', sub_block)
            explanation = exp_m.group(1).strip() if exp_m else ""

            wrong_m = re.search(r'\*\*Sai vì:\*\*\s*([^\n]+(?:\n[^\n*]+)*)', sub_block)
            wrong_str = wrong_m.group(1).strip() if wrong_m else ""

            tags = parse_tags(sub_block[sub_block.find('**Tags:**'):] if '**Tags:**' in sub_block else "")
            opts = dict(re.findall(r'-\s*([A-D])[.:]\s*([^\n]+)', sub_block))
            wrong_reasons = extract_wrong_reasons(wrong_str, opts, correct_ans)

            all_questions.append({
                "id": qid,
                "groupId": cid,
                "chapterId": "CH01",
                "lessonId": "CH01-FINAL",
                "part": 3,
                "taskType": "conversation_question",
                "prompt": prompt_text,
                "optionsVisibleBeforeAnswer": True,
                "image": None,
                "audioSegments": None,
                "options": opts,
                "correctAnswer": correct_ans,
                "transcript": " / ".join(dialogue_lines),
                "translation": "",
                "explanation": explanation,
                "wrongReasons": wrong_reasons,
                "skillTags": tags,
                "skillGroup": determine_skill_group(tags),
                "difficulty": 2,
                "revision": 2
            })

        groups_data.append({
            "id": cid,
            "chapterId": "CH01",
            "lessonId": "CH01-FINAL",
            "part": 3,
            "groupType": "short_conversation",
            "context": "Hội thoại ngắn cuối chương",
            "speakers": [
                {"speakerId": "W1", "label": "Woman", "gender": "female"},
                {"speakerId": "M1", "label": "Man", "gender": "male"}
            ],
            "voiceAssignment": {
                "W1": "us-female-01",
                "M1": "us-male-01"
            },
            "turns": turns,
            "audioFile": f"audio/chapter-01/{cid.lower()}.mp3",
            "transcript": " / ".join(dialogue_lines),
            "translation": "",
            "questionIds": c_qids,
            "revision": 2
        })

    chapter_data = {
        "chapterId": "CH01",
        "title": "Nền tảng nghe thật — nhịp câu, âm cuối, số/giờ, từ để hỏi và phản hồi Part 2",
        "description": "Nền tảng nghe thật cho người Việt: nhịp câu, dạng đọc yếu, âm cuối, số giờ ngày tiền, từ để hỏi, bẫy Part 2 và hội thoại ngắn",
        "specVersion": "2.3",
        "contentVersion": "2.0.0",
        "lessons": lessons_data,
        "groups": groups_data,
        "questions": all_questions,
        "finalTest": {
            "id": "CH01-FINAL",
            "title": "Kiểm tra cuối chương 1 (30 câu)",
            "questionIds": final_qids,
            "passRule": {
                "minCorrect": 24,
                "total": 30,
                "percentage": 80.0,
                "sectionRules": {
                    "partA": {"minCorrect": 7, "total": 10},
                    "partB": {"minCorrect": 10, "total": 14},
                    "partC": {"minCorrect": 4, "total": 6}
                }
            }
        }
    }

    print(f"Total Lessons: {len(lessons_data)}")
    print(f"Total Groups: {len(groups_data)}")
    print(f"Total Questions: {len(all_questions)}")
    print(f"Final Test Question IDs: {len(final_qids)}")

    with open(OUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(chapter_data, f, indent=2, ensure_ascii=False)
    print(f"Successfully wrote {OUT_PATH}!")

if __name__ == "__main__":
    main()
