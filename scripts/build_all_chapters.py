import re
import json
import os

# Pass rules mapping
PASS_RULES = {
    'CH01-L01': {'minCorrect': 3, 'total': 4, 'percentage': 75},
    'CH01-L02': {'minCorrect': 3, 'total': 4, 'percentage': 75},
    'CH01-L03': {'minCorrect': 4, 'total': 5, 'percentage': 80},
    'CH01-L04': {'minCorrect': 4, 'total': 5, 'percentage': 80},
    'CH01-L05': {'minCorrect': 10, 'total': 12, 'percentage': 83.3},
    'CH01-FINAL': {'minCorrect': 12, 'total': 15, 'percentage': 80},

    'CH02-L01': {'minCorrect': 3, 'total': 4, 'percentage': 75},
    'CH02-L02': {'minCorrect': 3, 'total': 4, 'percentage': 75},
    'CH02-L03': {'minCorrect': 3, 'total': 4, 'percentage': 75},
    'CH02-L04': {'minCorrect': 5, 'total': 6, 'percentage': 83.3},
    'CH02-L05': {'minCorrect': 6, 'total': 8, 'percentage': 75},
    'CH02-FINAL': {'minCorrect': 12, 'total': 15, 'percentage': 80},

    'CH03-L01': {'minCorrect': 5, 'total': 6, 'percentage': 83.3},
    'CH03-L02': {'minCorrect': 5, 'total': 6, 'percentage': 83.3},
    'CH03-L03': {'minCorrect': 5, 'total': 6, 'percentage': 83.3},
    'CH03-L04': {'minCorrect': 5, 'total': 6, 'percentage': 83.3},
    'CH03-L05': {'minCorrect': 5, 'total': 6, 'percentage': 83.3},
    'CH03-FINAL': {'minCorrect': 10, 'total': 12, 'percentage': 83.3},
}

def get_skill_group(tags, chapter_id, part):
    for t in tags:
        if t in ['contraction_weve', 'contraction', 'ed_ending', 'final_sound_s', 'plural_s']:
            return 'contractions_and_endings'
        if t in [
            'quarter_to', 'date_recognition', 'days_of_week', 'duration', 'money',
            'number_recognition', 'quantity', 'teen_ty_numbers', 'teen_ty_time',
            'time_choice', 'time_expression', 'time_recognition', 'time_response',
            'question_word_how_long', 'question_word_how_many', 'question_word_how_much',
            'question_word_when', 'when_response', 'business_hours'
        ]:
            return 'numbers_and_time'
        if t in [
            'question_word_where', 'question_word_who', 'question_word_why', 'which_question',
            'frequency_question', 'preference_question', 'yes_no_question', 'how_about',
            'would_you_like', 'would_you_mind', 'where_response', 'reason_expression',
            'reason_response', 'person_response', 'location_expression', 'location_response'
        ]:
            return 'question_words_and_types'
        if t.startswith('part1_') or t in [
            'present_continuous', 'passive_voice', 'being_v3', 'across_from', 'along_the_wall',
            'carrying', 'inspect', 'object_action', 'point_at', 'preposition_against',
            'preposition_beside', 'preposition_on', 'push_pull', 'underneath', 'vehicle_state',
            'action_verb', 'main_action', 'main_subject', 'supported_detail', 'past_participle',
            'present_perfect_passive'
        ]:
            return 'part1_photographs'
        if t.startswith('part3_') or t in [
            'appointment_vocabulary', 'business_vocabulary', 'contract_vocabulary',
            'department_vocabulary', 'meeting_vocabulary', 'transport_vocabulary'
        ]:
            return 'part3_conversations'
        if t in [
            'indirect_question', 'indirect_yes_no', 'choice_response', 'contextual_response',
            'invitation_response', 'polite_request', 'polite_response', 'problem_response',
            'problem_solution', 'request_response', 'statement_response', 'suggestion_response',
            'part2'
        ] or 'paraphrase' in t:
            return 'part2_responses'

    if chapter_id == 'CH01':
        return 'foundation_listening'
    elif chapter_id == 'CH02':
        return 'part1_photographs' if part == 1 else 'part2_responses'
    elif chapter_id == 'CH03':
        return 'part3_conversations'
    return 'general_listening'

def clean_text(s):
    if not s:
        return ""
    return s.strip().replace('`', '')

def parse_tags(text):
    m = re.search(r'\*\*Tags:\*\*\s*(.*)', text)
    if not m:
        return []
    raw = m.group(1)
    tags = re.findall(r'`([^`]+)`', raw)
    if not tags:
        tags = [t.strip() for t in raw.split(',') if t.strip()]
    return tags

def parse_options(text):
    options = {}
    for letter in ['A', 'B', 'C', 'D']:
        m = re.search(rf'-\s*{letter}[\.:]\s*(.+)', text)
        if m:
            options[letter] = m.group(1).strip()
    return options

def parse_wrong_reasons(text, options, correct_answer):
    wrong_reasons = {}
    m = re.search(r'\*\*Sai vì:\*\*\s*(.*)', text)
    if m:
        raw = m.group(1).strip()
        for opt in options.keys():
            if opt != correct_answer:
                pattern = rf'{opt}\s*[\:là\s]([^;A-D]+)'
                opt_m = re.search(pattern, raw)
                if opt_m:
                    wrong_reasons[opt] = f"{opt} {opt_m.group(1).strip()}"
                else:
                    wrong_reasons[opt] = raw
    for opt in options.keys():
        if opt != correct_answer and opt not in wrong_reasons:
            wrong_reasons[opt] = f"Lựa chọn ({opt}) không phù hợp với thông tin trong bài nghe."
    return wrong_reasons

# All questions list across all chapters to build audio manifest
all_audio_manifest = []

# --- PARSE CH01 ---
def parse_ch01():
    with open('CHAPTER_01_CONTENT.md', 'r', encoding='utf-8') as f:
        text = f.read()

    lessons_meta = [
        {"id": "CH01-L01", "title": "Nghe từ mang thông tin chính", "part": 0},
        {"id": "CH01-L02", "title": "Âm cuối và dạng rút gọn", "part": 0},
        {"id": "CH01-L03", "title": "Số, giờ, ngày tháng và giá tiền", "part": 0},
        {"id": "CH01-L04", "title": "Nhận diện từ để hỏi", "part": 0},
        {"id": "CH01-L05", "title": "Part 2 cơ bản: Chọn phản hồi phù hợp", "part": 2},
    ]

    # Split lessons
    # Pattern: # BÀI X — ...
    lesson_splits = re.split(r'\n#\s+BÀI\s+\d+\s+—\s+', text)
    # lesson_splits[0] is preamble
    # lesson_splits[1..5] are lessons 1..5
    # inside lesson_splits[5], final test is at `# KIỂM TRA CUỐI CHƯƠNG 1`
    final_test_raw = ""
    if len(lesson_splits) > 5 and '# KIỂM TRA CUỐI CHƯƠNG 1' in lesson_splits[5]:
        parts = lesson_splits[5].split('# KIỂM TRA CUỐI CHƯƠNG 1')
        lesson_splits[5] = parts[0]
        final_test_raw = parts[1]

    lessons = []
    questions = []

    for idx, l_meta in enumerate(lessons_meta):
        l_raw = lesson_splits[idx + 1] if idx + 1 < len(lesson_splits) else ""
        lid = l_meta["id"]

        # Parse objectives
        obj_m = re.search(r'##\s+Mục tiêu\s*\n([\s\S]*?)(?=##|\Z)', l_raw)
        objectives = []
        if obj_m:
            for l in obj_m.group(1).splitlines():
                l = l.strip()
                if l.startswith('- ') or l.startswith('* '):
                    objectives.append(l[2:].strip())

        # Parse teaching blocks
        # e.g. ## 1.1. Title ... ## 1.2. Title ...
        teachingBlocks = []
        tb_matches = re.findall(r'(##\s+\d+\.\d+\.\s+([^\n]+)\n([\s\S]*?)(?=##|\Z))', l_raw)
        for _, tb_title, tb_body in tb_matches:
            if "Từ vựng" not in tb_title and "Audio mẫu" not in tb_title and "Bài luyện" not in tb_title:
                teachingBlocks.append({
                    "title": tb_title.strip(),
                    "content": tb_body.strip()
                })

        # Parse vocabulary table
        vocab = []
        vocab_m = re.search(r'##\s+\d+\.\d+\.\s+Từ vựng[^\n]*\n([\s\S]*?)(?=##|\Z)', l_raw)
        if vocab_m:
            table_lines = [l.strip() for l in vocab_m.group(1).splitlines() if '|' in l and '---' not in l]
            for row in table_lines[1:]:
                cols = [c.strip() for c in row.split('|')[1:-1]]
                if len(cols) >= 2:
                    vocab.append({
                        "word": cols[0],
                        "meaning": cols[1],
                        "example": cols[2] if len(cols) > 2 else ""
                    })

        # Parse examples audio
        examples = []
        ex_m = re.search(r'##\s+\d+\.\d+\.\s+Audio mẫu[^\n]*\n([\s\S]*?)(?=##|\Z)', l_raw)
        if ex_m:
            table_lines = [l.strip() for l in ex_m.group(1).splitlines() if '|' in l and '---' not in l]
            for row in table_lines[1:]:
                cols = [c.strip() for c in row.split('|')[1:-1]]
                if len(cols) >= 3:
                    ex_id = cols[0]
                    ex_text = cols[1]
                    ex_trans = cols[2]
                    audio_file = f"audio/chapter-01/{ex_id.lower()}.mp3"
                    examples.append({
                        "id": ex_id,
                        "text": ex_text,
                        "translation": ex_trans,
                        "audioFile": audio_file
                    })
                    all_audio_manifest.append({
                        "id": ex_id,
                        "text": ex_text,
                        "voice": "us-female-01",
                        "speed": 1.0,
                        "output": audio_file
                    })

        # Parse practice questions
        # Pattern: ### Câu X — QID
        q_raws = re.findall(r'(###\s+Câu\s+\d+\s+—\s+(CH01-L0\d-Q\d+)[\s\S]*?(?=###\s+Câu|###\s+Tự kiểm tra|\Z))', l_raw)
        l_qids = []
        for q_full, qid in q_raws:
            l_qids.append(qid)

            # Check if Part 2 or Foundation
            if lid == "CH01-L05":
                # Part 2
                q_prompt = "Nghe câu hỏi và chọn phản hồi phù hợp."
                audio_q_m = re.search(r'\*\*Audio question:\*\*\s*(.+)', q_full)
                q_text = audio_q_m.group(1).strip() if audio_q_m else ""

                # Responses
                resp_matches = re.findall(r'-\s*([A-C]):\s*(.+)', q_full)
                options = {k: v.strip() for k, v in resp_matches}

                ans_m = re.search(r'\*\*Đáp án:\*\*\s*([A-C])', q_full)
                ans = ans_m.group(1) if ans_m else "A"

                exp_m = re.search(r'\*\*Giải thích:\*\*\s*(.+)', q_full)
                exp = exp_m.group(1).strip() if exp_m else ""

                tags = parse_tags(q_full)
                wrong_reasons = parse_wrong_reasons(q_full, options, ans)

                # Audio segments
                audio_segments = [
                    {"text": q_text, "voice": "us-female-01", "file": f"audio/chapter-01/{qid.lower()}-01.mp3", "pauseAfterMs": 500}
                ]
                all_audio_manifest.append({"id": f"{qid}-01", "text": q_text, "voice": "us-female-01", "speed": 1.0, "output": f"audio/chapter-01/{qid.lower()}-01.mp3"})

                for idx_opt, (k_opt, v_opt) in enumerate(options.items(), start=2):
                    audio_segments.append({
                        "text": v_opt,
                        "choiceId": k_opt,
                        "voice": "us-female-01",
                        "file": f"audio/chapter-01/{qid.lower()}-0{idx_opt}.mp3",
                        "pauseAfterMs": 500 if idx_opt < 4 else 0
                    })
                    all_audio_manifest.append({"id": f"{qid}-0{idx_opt}", "text": v_opt, "voice": "us-female-01", "speed": 1.0, "output": f"audio/chapter-01/{qid.lower()}-0{idx_opt}.mp3"})

                transcript = f"{q_text} / " + " / ".join([f"({k}) {v}" for k, v in options.items()])
                translation_m = re.search(r'\*\*Dịch:\*\*\s*(.+)', q_full)
                translation = translation_m.group(1).strip() if translation_m else ""

                q_obj = {
                    "id": qid,
                    "groupId": None,
                    "chapterId": "CH01",
                    "lessonId": lid,
                    "part": 2,
                    "taskType": "question_response",
                    "prompt": q_prompt,
                    "optionsVisibleBeforeAnswer": False,
                    "image": None,
                    "audioSegments": audio_segments,
                    "options": options,
                    "correctAnswer": ans,
                    "transcript": transcript,
                    "translation": translation,
                    "explanation": exp,
                    "wrongReasons": wrong_reasons,
                    "skillTags": tags,
                    "skillGroup": get_skill_group(tags, "CH01", 2),
                    "difficulty": 1,
                    "revision": 1
                }
                questions.append(q_obj)
            else:
                # Foundation: CH01-L01 to L04
                audio_m = re.search(r'\*\*Audio:\*\*\s*`?([^`\n]+)`?', q_full)
                audio_text = audio_m.group(1).strip() if audio_m else ""

                prompt_m = re.search(r'\*\*Câu hỏi:\*\*\s*(.+)', q_full)
                prompt_text = prompt_m.group(1).strip() if prompt_m else ""

                options = parse_options(q_full)
                ans_m = re.search(r'\*\*Đáp án:\*\*\s*([A-D])', q_full)
                ans = ans_m.group(1) if ans_m else "A"

                exp_m = re.search(r'\*\*Giải thích:\*\*\s*(.+)', q_full)
                exp = exp_m.group(1).strip() if exp_m else ""

                tags = parse_tags(q_full)
                wrong_reasons = parse_wrong_reasons(q_full, options, ans)

                audio_file = f"audio/chapter-01/{qid.lower()}.mp3"
                audio_segments = [
                    {"text": audio_text, "voice": "us-female-01", "file": audio_file, "pauseAfterMs": 0}
                ]
                all_audio_manifest.append({"id": qid, "text": audio_text, "voice": "us-female-01", "speed": 1.0, "output": audio_file})

                trans_m = re.search(r'\*\*Transcript:\*\*\s*(.+)', q_full)
                transcript = trans_m.group(1).strip() if trans_m else audio_text

                trans_vn_m = re.search(r'\*\*Dịch:\*\*\s*(.+)', q_full)
                translation = trans_vn_m.group(1).strip() if trans_vn_m else ""

                q_obj = {
                    "id": qid,
                    "groupId": None,
                    "chapterId": "CH01",
                    "lessonId": lid,
                    "part": 0,
                    "taskType": "foundation_listening",
                    "prompt": prompt_text,
                    "optionsVisibleBeforeAnswer": True,
                    "image": None,
                    "audioSegments": audio_segments,
                    "options": options,
                    "correctAnswer": ans,
                    "transcript": transcript,
                    "translation": translation,
                    "explanation": exp,
                    "wrongReasons": wrong_reasons,
                    "skillTags": tags,
                    "skillGroup": get_skill_group(tags, "CH01", 0),
                    "difficulty": 1,
                    "revision": 1
                }
                questions.append(q_obj)

        lessons.append({
            "lessonId": lid,
            "title": l_meta["title"],
            "objectives": objectives,
            "teachingBlocks": teachingBlocks,
            "vocabulary": vocab,
            "examples": examples,
            "questionIds": l_qids,
            "passRule": PASS_RULES[lid]
        })

    # Parse CH01-FINAL
    final_qids = []
    if final_test_raw:
        final_qs = re.findall(r'(##\s+Câu\s+\d+\s+—\s+(CH01-FINAL-Q\d+)[\s\S]*?(?=##\s+Câu|##\s+Đáp|\Z))', final_test_raw)
        for f_full, qid in final_qs:
            final_qids.append(qid)

            # Check if Q13-Q15 (Part 2) or Q01-Q12 (Foundation)
            q_num = int(qid.split('-Q')[-1])
            is_part2 = q_num >= 13

            options = parse_options(f_full)
            ans_m = re.search(r'\*\*Đáp án:\*\*\s*([A-D])\.?\s*(.*)', f_full)
            ans = ans_m.group(1) if ans_m else "A"
            exp = ans_m.group(2).strip() if ans_m else "Đáp án đúng theo bài nghe."

            tags = parse_tags(f_full)
            wrong_reasons = {}
            for opt in options.keys():
                if opt != ans:
                    wrong_reasons[opt] = f"Lựa chọn {opt} không phù hợp với thông tin trong đoạn audio."

            if is_part2:
                q_text_m = re.search(r'\*\*Audio question:\*\*\s*(.+)', f_full)
                q_text = q_text_m.group(1).strip() if q_text_m else ""
                audio_segments = [
                    {"text": q_text, "voice": "us-female-01", "file": f"audio/chapter-01/{qid.lower()}-01.mp3", "pauseAfterMs": 500}
                ]
                all_audio_manifest.append({"id": f"{qid}-01", "text": q_text, "voice": "us-female-01", "speed": 1.0, "output": f"audio/chapter-01/{qid.lower()}-01.mp3"})

                for idx_opt, (k_opt, v_opt) in enumerate(options.items(), start=2):
                    audio_segments.append({
                        "text": v_opt,
                        "choiceId": k_opt,
                        "voice": "us-female-01",
                        "file": f"audio/chapter-01/{qid.lower()}-0{idx_opt}.mp3",
                        "pauseAfterMs": 500 if idx_opt < 4 else 0
                    })
                    all_audio_manifest.append({"id": f"{qid}-0{idx_opt}", "text": v_opt, "voice": "us-female-01", "speed": 1.0, "output": f"audio/chapter-01/{qid.lower()}-0{idx_opt}.mp3"})

                transcript = f"{q_text} / " + " / ".join([f"({k}) {v}" for k, v in options.items()])
                q_obj = {
                    "id": qid,
                    "groupId": None,
                    "chapterId": "CH01",
                    "lessonId": "CH01-FINAL",
                    "part": 2,
                    "taskType": "question_response",
                    "prompt": "Nghe câu hỏi và chọn phản hồi phù hợp.",
                    "optionsVisibleBeforeAnswer": False,
                    "image": None,
                    "audioSegments": audio_segments,
                    "options": options,
                    "correctAnswer": ans,
                    "transcript": transcript,
                    "translation": "",
                    "explanation": exp,
                    "wrongReasons": wrong_reasons,
                    "skillTags": tags,
                    "skillGroup": get_skill_group(tags, "CH01", 2),
                    "difficulty": 2,
                    "revision": 1
                }
            else:
                audio_m = re.search(r'\*\*Audio:\*\*\s*`?([^`\n]+)`?', f_full)
                audio_text = audio_m.group(1).strip() if audio_m else ""
                prompt_m = re.search(r'\*\*(?:Hỏi|Câu hỏi):\*\*\s*(.+)', f_full)
                prompt_text = prompt_m.group(1).strip() if prompt_m else "Chọn đáp án đúng nhất:"

                audio_file = f"audio/chapter-01/{qid.lower()}.mp3"
                audio_segments = [
                    {"text": audio_text, "voice": "us-female-01", "file": audio_file, "pauseAfterMs": 0}
                ]
                all_audio_manifest.append({"id": qid, "text": audio_text, "voice": "us-female-01", "speed": 1.0, "output": audio_file})

                q_obj = {
                    "id": qid,
                    "groupId": None,
                    "chapterId": "CH01",
                    "lessonId": "CH01-FINAL",
                    "part": 0,
                    "taskType": "foundation_listening",
                    "prompt": prompt_text,
                    "optionsVisibleBeforeAnswer": True,
                    "image": None,
                    "audioSegments": audio_segments,
                    "options": options,
                    "correctAnswer": ans,
                    "transcript": audio_text,
                    "translation": "",
                    "explanation": exp,
                    "wrongReasons": wrong_reasons,
                    "skillTags": tags,
                    "skillGroup": get_skill_group(tags, "CH01", 0),
                    "difficulty": 2,
                    "revision": 1
                }
            questions.append(q_obj)

    ch01_data = {
        "chapterId": "CH01",
        "title": "Nền tảng nghe",
        "description": "Bắt từ khóa, âm cuối, số giờ và ý câu hỏi",
        "specVersion": "2.3",
        "contentVersion": "1.0.0",
        "lessons": lessons,
        "questions": questions,
        "finalTest": {
            "id": "CH01-FINAL",
            "title": "Kiểm tra cuối chương 1",
            "questionIds": final_qids,
            "passRule": PASS_RULES['CH01-FINAL']
        }
    }

    with open('data/chapters/chapter-01.json', 'w', encoding='utf-8') as f:
        json.dump(ch01_data, f, ensure_ascii=False, indent=2)
    print(f"Parsed CH01: {len(lessons)} lessons, {len(questions)} questions")

# --- PARSE CH02 ---
def parse_ch02():
    with open('CHAPTER_02_CONTENT.md', 'r', encoding='utf-8') as f:
        text = f.read()

    lessons_meta = [
        {"id": "CH02-L01", "title": "Part 1: Người và hành động", "part": 1},
        {"id": "CH02-L02", "title": "Part 1: Vị trí và đồ vật", "part": 1},
        {"id": "CH02-L03", "title": "Part 1: Bị động và bẫy suy diễn", "part": 1},
        {"id": "CH02-L04", "title": "Part 2: Câu hỏi gián tiếp và giao tiếp", "part": 2},
        {"id": "CH02-L05", "title": "Part 2: Paraphrase và phản hồi tự nhiên", "part": 2},
    ]

    lesson_splits = re.split(r'\n#\s+BÀI\s+\d+\s+—\s+', text)
    final_test_raw = ""
    if len(lesson_splits) > 5 and '# KIỂM TRA CUỐI CHƯƠNG 2' in lesson_splits[5]:
        parts = lesson_splits[5].split('# KIỂM TRA CUỐI CHƯƠNG 2')
        lesson_splits[5] = parts[0]
        final_test_raw = parts[1]

    lessons = []
    questions = []

    for idx, l_meta in enumerate(lessons_meta):
        l_raw = lesson_splits[idx + 1] if idx + 1 < len(lesson_splits) else ""
        lid = l_meta["id"]
        is_part1 = l_meta["part"] == 1

        obj_m = re.search(r'##\s+Mục tiêu\s*\n([\s\S]*?)(?=##|\Z)', l_raw)
        objectives = []
        if obj_m:
            for l in obj_m.group(1).splitlines():
                l = l.strip()
                if l.startswith('- ') or l.startswith('* '):
                    objectives.append(l[2:].strip())

        teachingBlocks = []
        tb_matches = re.findall(r'(##\s+\d+\.\d+\.\s+([^\n]+)\n([\s\S]*?)(?=##|\Z))', l_raw)
        for _, tb_title, tb_body in tb_matches:
            if "Từ vựng" not in tb_title and "Audio mẫu" not in tb_title and "Bài luyện" not in tb_title:
                teachingBlocks.append({
                    "title": tb_title.strip(),
                    "content": tb_body.strip()
                })

        vocab = []
        vocab_m = re.search(r'##\s+\d+\.\d+\.\s+Từ vựng[^\n]*\n([\s\S]*?)(?=##|\Z)', l_raw)
        if vocab_m:
            table_lines = [l.strip() for l in vocab_m.group(1).splitlines() if '|' in l and '---' not in l]
            for row in table_lines[1:]:
                cols = [c.strip() for c in row.split('|')[1:-1]]
                if len(cols) >= 2:
                    vocab.append({
                        "word": cols[0],
                        "meaning": cols[1],
                        "example": cols[2] if len(cols) > 2 else ""
                    })

        examples = []
        ex_m = re.search(r'##\s+\d+\.\d+\.\s+Audio mẫu[^\n]*\n([\s\S]*?)(?=##|\Z)', l_raw)
        if ex_m:
            table_lines = [l.strip() for l in ex_m.group(1).splitlines() if '|' in l and '---' not in l]
            for row in table_lines[1:]:
                cols = [c.strip() for c in row.split('|')[1:-1]]
                if len(cols) >= 3:
                    ex_id = cols[0]
                    ex_text = cols[1]
                    ex_trans = cols[2]
                    audio_file = f"audio/chapter-02/{ex_id.lower()}.mp3"
                    examples.append({
                        "id": ex_id,
                        "text": ex_text,
                        "translation": ex_trans,
                        "audioFile": audio_file
                    })
                    all_audio_manifest.append({"id": ex_id, "text": ex_text, "voice": "us-female-01", "speed": 1.0, "output": audio_file})

        q_raws = re.findall(r'(###\s+Câu\s+\d+\s+—\s+(CH02-L0\d-Q\d+)[\s\S]*?(?=###\s+Câu|###\s+Tự kiểm tra|\Z))', l_raw)
        l_qids = []
        for q_full, qid in q_raws:
            l_qids.append(qid)

            ans_m = re.search(r'\*\*Đáp án:\*\*\s*([A-D])', q_full)
            ans = ans_m.group(1) if ans_m else "A"

            exp_m = re.search(r'\*\*Giải thích:\*\*\s*(.+)', q_full)
            exp = exp_m.group(1).strip() if exp_m else ""

            tags = parse_tags(q_full)

            if is_part1:
                # Part 1: has image brief, 4 statements A, B, C, D
                resp_matches = re.findall(r'-\s*([A-D]):\s*(.+)', q_full)
                options = {k: v.strip() for k, v in resp_matches}
                image_path = f"images/chapter-02/{qid.lower()}.svg"

                audio_segments = []
                for idx_opt, (k_opt, v_opt) in enumerate(options.items(), start=1):
                    seg_file = f"audio/chapter-02/{qid.lower()}-0{idx_opt}.mp3"
                    audio_segments.append({
                        "text": v_opt,
                        "choiceId": k_opt,
                        "voice": "us-female-01",
                        "file": seg_file,
                        "pauseAfterMs": 500 if idx_opt < 4 else 0
                    })
                    all_audio_manifest.append({"id": f"{qid}-0{idx_opt}", "text": v_opt, "voice": "us-female-01", "speed": 1.0, "output": seg_file})

                transcript = " ".join([f"({k}) {v}" for k, v in options.items()])
                wrong_reasons = parse_wrong_reasons(q_full, options, ans)

                q_obj = {
                    "id": qid,
                    "groupId": None,
                    "chapterId": "CH02",
                    "lessonId": lid,
                    "part": 1,
                    "taskType": "photograph_description",
                    "prompt": "Nghe 4 câu mô tả và chọn câu đúng nhất cho bức tranh.",
                    "optionsVisibleBeforeAnswer": False,
                    "image": image_path,
                    "audioSegments": audio_segments,
                    "options": options,
                    "correctAnswer": ans,
                    "transcript": transcript,
                    "translation": "",
                    "explanation": exp,
                    "wrongReasons": wrong_reasons,
                    "skillTags": tags,
                    "skillGroup": get_skill_group(tags, "CH02", 1),
                    "difficulty": 1,
                    "revision": 1
                }
                questions.append(q_obj)
            else:
                # Part 2: audio question + 3 responses
                audio_q_m = re.search(r'\*\*Audio question:\*\*\s*(.+)', q_full)
                q_text = audio_q_m.group(1).strip() if audio_q_m else ""

                resp_matches = re.findall(r'-\s*([A-C]):\s*(.+)', q_full)
                options = {k: v.strip() for k, v in resp_matches}
                wrong_reasons = parse_wrong_reasons(q_full, options, ans)

                audio_segments = [
                    {"text": q_text, "voice": "us-female-01", "file": f"audio/chapter-02/{qid.lower()}-01.mp3", "pauseAfterMs": 500}
                ]
                all_audio_manifest.append({"id": f"{qid}-01", "text": q_text, "voice": "us-female-01", "speed": 1.0, "output": f"audio/chapter-02/{qid.lower()}-01.mp3"})

                for idx_opt, (k_opt, v_opt) in enumerate(options.items(), start=2):
                    seg_file = f"audio/chapter-02/{qid.lower()}-0{idx_opt}.mp3"
                    audio_segments.append({
                        "text": v_opt,
                        "choiceId": k_opt,
                        "voice": "us-female-01",
                        "file": seg_file,
                        "pauseAfterMs": 500 if idx_opt < 4 else 0
                    })
                    all_audio_manifest.append({"id": f"{qid}-0{idx_opt}", "text": v_opt, "voice": "us-female-01", "speed": 1.0, "output": seg_file})

                transcript = f"{q_text} / " + " / ".join([f"({k}) {v}" for k, v in options.items()])

                q_obj = {
                    "id": qid,
                    "groupId": None,
                    "chapterId": "CH02",
                    "lessonId": lid,
                    "part": 2,
                    "taskType": "question_response",
                    "prompt": "Nghe câu hỏi và chọn phản hồi phù hợp.",
                    "optionsVisibleBeforeAnswer": False,
                    "image": None,
                    "audioSegments": audio_segments,
                    "options": options,
                    "correctAnswer": ans,
                    "transcript": transcript,
                    "translation": "",
                    "explanation": exp,
                    "wrongReasons": wrong_reasons,
                    "skillTags": tags,
                    "skillGroup": get_skill_group(tags, "CH02", 2),
                    "difficulty": 1,
                    "revision": 1
                }
                questions.append(q_obj)

        lessons.append({
            "lessonId": lid,
            "title": l_meta["title"],
            "objectives": objectives,
            "teachingBlocks": teachingBlocks,
            "vocabulary": vocab,
            "examples": examples,
            "questionIds": l_qids,
            "passRule": PASS_RULES[lid]
        })

    # Parse CH02-FINAL (Q01-Q06: Part 1; Q07-Q15: Part 2)
    final_qids = []
    if final_test_raw:
        final_qs = re.findall(r'(###\s+Câu\s+\d+\s+—\s+(CH02-FINAL-Q\d+)[\s\S]*?(?=###\s+Câu|##\s+Đáp|\Z))', final_test_raw)
        for f_full, qid in final_qs:
            final_qids.append(qid)
            q_num = int(qid.split('-Q')[-1])
            is_p1 = q_num <= 6

            ans_m = re.search(r'\*\*Đáp án:\*\*\s*([A-D])\.?\s*(.*)', f_full)
            ans = ans_m.group(1) if ans_m else "A"
            exp = ans_m.group(2).strip() if ans_m and ans_m.group(2) else "Đáp án đúng theo bài nghe."

            exp_extra = re.search(r'\*\*Giải thích:\*\*\s*(.+)', f_full)
            if exp_extra:
                exp = exp_extra.group(1).strip()

            tags = parse_tags(f_full)

            if is_p1:
                # Part 1 final
                resp_matches = re.findall(r'-\s*([A-D]):\s*(.+)', f_full)
                options = {k: v.strip() for k, v in resp_matches}
                image_path = f"images/chapter-02/{qid.lower()}.svg"

                audio_segments = []
                for idx_opt, (k_opt, v_opt) in enumerate(options.items(), start=1):
                    seg_file = f"audio/chapter-02/{qid.lower()}-0{idx_opt}.mp3"
                    audio_segments.append({
                        "text": v_opt,
                        "choiceId": k_opt,
                        "voice": "us-female-01",
                        "file": seg_file,
                        "pauseAfterMs": 500 if idx_opt < 4 else 0
                    })
                    all_audio_manifest.append({"id": f"{qid}-0{idx_opt}", "text": v_opt, "voice": "us-female-01", "speed": 1.0, "output": seg_file})

                transcript = " ".join([f"({k}) {v}" for k, v in options.items()])
                wrong_reasons = parse_wrong_reasons(f_full, options, ans)
                for opt in options.keys():
                    if opt != ans and opt not in wrong_reasons:
                        wrong_reasons[opt] = f"Mô tả ({opt}) không chính xác so với chi tiết trong tranh."

                q_obj = {
                    "id": qid,
                    "groupId": None,
                    "chapterId": "CH02",
                    "lessonId": "CH02-FINAL",
                    "part": 1,
                    "taskType": "photograph_description",
                    "prompt": "Nghe 4 câu mô tả và chọn câu đúng nhất cho bức tranh.",
                    "optionsVisibleBeforeAnswer": False,
                    "image": image_path,
                    "audioSegments": audio_segments,
                    "options": options,
                    "correctAnswer": ans,
                    "transcript": transcript,
                    "translation": "",
                    "explanation": exp,
                    "wrongReasons": wrong_reasons,
                    "skillTags": tags,
                    "skillGroup": get_skill_group(tags, "CH02", 1),
                    "difficulty": 2,
                    "revision": 1
                }
            else:
                # Part 2 final
                q_text_m = re.search(r'\*\*Audio question:\*\*\s*(.+)', f_full)
                q_text = q_text_m.group(1).strip() if q_text_m else ""
                resp_matches = re.findall(r'-\s*([A-C]):\s*(.+)', f_full)
                options = {k: v.strip() for k, v in resp_matches}

                audio_segments = [
                    {"text": q_text, "voice": "us-female-01", "file": f"audio/chapter-02/{qid.lower()}-01.mp3", "pauseAfterMs": 500}
                ]
                all_audio_manifest.append({"id": f"{qid}-01", "text": q_text, "voice": "us-female-01", "speed": 1.0, "output": f"audio/chapter-02/{qid.lower()}-01.mp3"})

                for idx_opt, (k_opt, v_opt) in enumerate(options.items(), start=2):
                    seg_file = f"audio/chapter-02/{qid.lower()}-0{idx_opt}.mp3"
                    audio_segments.append({
                        "text": v_opt,
                        "choiceId": k_opt,
                        "voice": "us-female-01",
                        "file": seg_file,
                        "pauseAfterMs": 500 if idx_opt < 4 else 0
                    })
                    all_audio_manifest.append({"id": f"{qid}-0{idx_opt}", "text": v_opt, "voice": "us-female-01", "speed": 1.0, "output": seg_file})

                transcript = f"{q_text} / " + " / ".join([f"({k}) {v}" for k, v in options.items()])
                wrong_reasons = parse_wrong_reasons(f_full, options, ans)
                for opt in options.keys():
                    if opt != ans and opt not in wrong_reasons:
                        wrong_reasons[opt] = f"Phản hồi ({opt}) không phù hợp với ý định câu hỏi."

                q_obj = {
                    "id": qid,
                    "groupId": None,
                    "chapterId": "CH02",
                    "lessonId": "CH02-FINAL",
                    "part": 2,
                    "taskType": "question_response",
                    "prompt": "Nghe câu hỏi và chọn phản hồi phù hợp.",
                    "optionsVisibleBeforeAnswer": False,
                    "image": None,
                    "audioSegments": audio_segments,
                    "options": options,
                    "correctAnswer": ans,
                    "transcript": transcript,
                    "translation": "",
                    "explanation": exp,
                    "wrongReasons": wrong_reasons,
                    "skillTags": tags,
                    "skillGroup": get_skill_group(tags, "CH02", 2),
                    "difficulty": 2,
                    "revision": 1
                }
            questions.append(q_obj)

    ch02_data = {
        "chapterId": "CH02",
        "title": "Part 1 và Part 2 mở rộng",
        "description": "Mô tả tranh, câu hỏi gián tiếp và phản hồi tự nhiên",
        "specVersion": "2.3",
        "contentVersion": "1.0.0",
        "lessons": lessons,
        "questions": questions,
        "finalTest": {
            "id": "CH02-FINAL",
            "title": "Kiểm tra cuối chương 2",
            "questionIds": final_qids,
            "passRule": PASS_RULES['CH02-FINAL']
        }
    }

    with open('data/chapters/chapter-02.json', 'w', encoding='utf-8') as f:
        json.dump(ch02_data, f, ensure_ascii=False, indent=2)
    print(f"Parsed CH02: {len(lessons)} lessons, {len(questions)} questions")

# --- PARSE CH03 (Part 3 groups) ---
def parse_ch03():
    with open('CHAPTER_03_CONTENT.md', 'r', encoding='utf-8') as f:
        text = f.read()

    lessons_meta = [
        {"id": "CH03-L01", "title": "Cấu trúc Part 3 và nghe mục đích hội thoại"},
        {"id": "CH03-L02", "title": "Địa điểm, nghề nghiệp, quan hệ người nói"},
        {"id": "CH03-L03", "title": "Chi tiết: thời gian, số, đồ vật"},
        {"id": "CH03-L04", "title": "Vấn đề, yêu cầu, đề nghị, việc tiếp theo"},
        {"id": "CH03-L05", "title": "Paraphrase và bẫy trong Part 3"},
    ]

    lesson_splits = re.split(r'\n#\s+BÀI\s+\d+\s+—\s+', text)
    final_test_raw = ""
    if len(lesson_splits) > 5 and '# KIỂM TRA CUỐI CHƯƠNG 3' in lesson_splits[5]:
        parts = lesson_splits[5].split('# KIỂM TRA CUỐI CHƯƠNG 3')
        lesson_splits[5] = parts[0]
        final_test_raw = parts[1]

    lessons = []
    groups = []
    questions = []

    for idx, l_meta in enumerate(lessons_meta):
        l_raw = lesson_splits[idx + 1] if idx + 1 < len(lesson_splits) else ""
        lid = l_meta["id"]

        obj_m = re.search(r'##\s+Mục tiêu\s*\n([\s\S]*?)(?=##|\Z)', l_raw)
        objectives = []
        if obj_m:
            for l in obj_m.group(1).splitlines():
                l = l.strip()
                if l.startswith('- ') or l.startswith('* '):
                    objectives.append(l[2:].strip())

        teachingBlocks = []
        tb_matches = re.findall(r'(##\s+\d+\.\d+\.\s+([^\n]+)\n([\s\S]*?)(?=##|\Z))', l_raw)
        for _, tb_title, tb_body in tb_matches:
            if "Từ vựng" not in tb_title and "Hội thoại" not in tb_title and "Bài luyện" not in tb_title:
                teachingBlocks.append({
                    "title": tb_title.strip(),
                    "content": tb_body.strip()
                })

        vocab = []
        vocab_m = re.search(r'##\s+\d+\.\d+\.\s+Từ vựng[^\n]*\n([\s\S]*?)(?=##|\Z)', l_raw)
        if vocab_m:
            table_lines = [l.strip() for l in vocab_m.group(1).splitlines() if '|' in l and '---' not in l]
            for row in table_lines[1:]:
                cols = [c.strip() for c in row.split('|')[1:-1]]
                if len(cols) >= 2:
                    vocab.append({
                        "word": cols[0],
                        "meaning": cols[1],
                        "example": cols[2] if len(cols) > 2 else ""
                    })

        # Parse groups (Conversations): ### Hội thoại X — CH03-Lxx-Gyy
        grp_matches = re.findall(r'(###\s+Hội thoại\s+\d+\s+—\s+(CH03-L0\d-G\d+)[\s\S]*?(?=###\s+Hội thoại|###\s+Tự kiểm tra|\Z))', l_raw)
        l_qids = []

        for grp_full, gid in grp_matches:
            ctx_m = re.search(r'\*\*Bối cảnh:\*\*\s*(.+)', grp_full)
            context = ctx_m.group(1).strip() if ctx_m else ""

            # Parse audio turns
            # - W1: ... or - M1: ...
            script_m = re.search(r'\*\*Audio script:\*\*\s*\n([\s\S]*?)(?=\*\*Dịch:\*\*|\n####|\Z)', grp_full)
            turns = []
            turn_lines = []
            if script_m:
                for line in script_m.group(1).splitlines():
                    t_m = re.search(r'-\s*(W1|M1):\s*(.+)', line)
                    if t_m:
                        turn_lines.append((t_m.group(1), t_m.group(2).strip()))

            cur_ms = 0
            for t_idx, (spk, spk_text) in enumerate(turn_lines, start=1):
                # Estimate ~65ms per word + 300ms base
                word_count = len(spk_text.split())
                dur_ms = int(word_count * 320) + 400
                turns.append({
                    "turn": t_idx,
                    "speakerId": spk,
                    "text": spk_text,
                    "pauseAfterMs": 450,
                    "startMs": cur_ms,
                    "endMs": cur_ms + dur_ms
                })
                cur_ms += dur_ms + 450

            # Translation
            trans_m = re.search(r'\*\*Dịch:\*\*\s*\n([\s\S]*?)(?=\n####|\Z)', grp_full)
            translation = trans_m.group(1).strip() if trans_m else ""
            transcript = " / ".join([f"{spk}: {txt}" for spk, txt in turn_lines])

            # Questions in this group
            # #### Câu X — QID
            q_matches = re.findall(r'(####\s+Câu\s+\d+\s+—\s+(CH03-L0\d-Q\d+)[\s\S]*?(?=####\s+Câu|\Z))', grp_full)
            grp_qids = []

            for q_full, qid in q_matches:
                grp_qids.append(qid)
                l_qids.append(qid)

                prompt_m = re.search(r'\*\*Question:\*\*\s*(.+)', q_full)
                prompt = prompt_m.group(1).strip() if prompt_m else ""

                resp_matches = re.findall(r'-\s*([A-D]):\s*(.+)', q_full)
                options = {k: v.strip() for k, v in resp_matches}

                ans_m = re.search(r'\*\*Đáp án:\*\*\s*([A-D])', q_full)
                ans = ans_m.group(1) if ans_m else "A"

                exp_m = re.search(r'\*\*Giải thích:\*\*\s*(.+)', q_full)
                exp = exp_m.group(1).strip() if exp_m else ""

                tags = parse_tags(q_full)
                wrong_reasons = parse_wrong_reasons(q_full, options, ans)

                q_obj = {
                    "id": qid,
                    "groupId": gid,
                    "chapterId": "CH03",
                    "lessonId": lid,
                    "part": 3,
                    "taskType": "conversation_question",
                    "prompt": prompt,
                    "optionsVisibleBeforeAnswer": True,
                    "image": None,
                    "audioSegments": None,
                    "options": options,
                    "correctAnswer": ans,
                    "transcript": transcript,
                    "translation": translation,
                    "explanation": exp,
                    "wrongReasons": wrong_reasons,
                    "skillTags": tags,
                    "skillGroup": get_skill_group(tags, "CH03", 3),
                    "difficulty": 1,
                    "revision": 1
                }
                questions.append(q_obj)

            audio_file = f"audio/chapter-03/{gid.lower()}.mp3"
            all_audio_manifest.append({
                "id": gid,
                "text": transcript,
                "voice": "mixed",
                "speed": 1.0,
                "output": audio_file,
                "turns": turns
            })

            groups.append({
                "id": gid,
                "chapterId": "CH03",
                "lessonId": lid,
                "part": 3,
                "groupType": "conversation",
                "context": context,
                "speakers": [
                    {"speakerId": "W1", "label": "Woman", "gender": "female"},
                    {"speakerId": "M1", "label": "Man", "gender": "male"}
                ],
                "voiceAssignment": {"W1": "us-female-01", "M1": "us-male-01"},
                "turns": turns,
                "audioFile": audio_file,
                "transcript": transcript,
                "translation": translation,
                "questionIds": grp_qids,
                "revision": 1
            })

        lessons.append({
            "lessonId": lid,
            "title": l_meta["title"],
            "objectives": objectives,
            "teachingBlocks": teachingBlocks,
            "vocabulary": vocab,
            "examples": [],
            "questionIds": l_qids,
            "passRule": PASS_RULES[lid]
        })

    # Parse CH03-FINAL (4 conversations: G01 to G04, 12 questions)
    final_qids = []
    if final_test_raw:
        grp_matches = re.findall(r'(###\s+Hội thoại\s+final\s+\d+\s+—\s+(CH03-FINAL-G\d+)[\s\S]*?(?=###\s+Hội thoại|##\s+Đáp|\Z))', final_test_raw)
        for grp_full, gid in grp_matches:
            ctx_m = re.search(r'\*\*Bối cảnh:\*\*\s*(.+)', grp_full)
            context = ctx_m.group(1).strip() if ctx_m else ""

            script_m = re.search(r'\*\*Audio script:\*\*\s*\n([\s\S]*?)(?=\*\*Dịch:\*\*|\n####|\Z)', grp_full)
            turns = []
            turn_lines = []
            if script_m:
                for line in script_m.group(1).splitlines():
                    t_m = re.search(r'-\s*(W1|M1):\s*(.+)', line)
                    if t_m:
                        turn_lines.append((t_m.group(1), t_m.group(2).strip()))

            cur_ms = 0
            for t_idx, (spk, spk_text) in enumerate(turn_lines, start=1):
                word_count = len(spk_text.split())
                dur_ms = int(word_count * 320) + 400
                turns.append({
                    "turn": t_idx,
                    "speakerId": spk,
                    "text": spk_text,
                    "pauseAfterMs": 450,
                    "startMs": cur_ms,
                    "endMs": cur_ms + dur_ms
                })
                cur_ms += dur_ms + 450

            trans_m = re.search(r'\*\*Dịch:\*\*\s*\n([\s\S]*?)(?=\n####|\Z)', grp_full)
            translation = trans_m.group(1).strip() if trans_m else ""
            transcript = " / ".join([f"{spk}: {txt}" for spk, txt in turn_lines])

            q_matches = re.findall(r'(####\s+Câu\s+\d+\s+—\s+(CH03-FINAL-Q\d+)[\s\S]*?(?=####\s+Câu|\Z))', grp_full)
            grp_qids = []

            for q_full, qid in q_matches:
                grp_qids.append(qid)
                final_qids.append(qid)

                prompt_m = re.search(r'\*\*Question:\*\*\s*(.+)', q_full)
                prompt = prompt_m.group(1).strip() if prompt_m else ""

                resp_matches = re.findall(r'-\s*([A-D]):\s*(.+)', q_full)
                options = {k: v.strip() for k, v in resp_matches}

                ans_m = re.search(r'\*\*Đáp án:\*\*\s*([A-D])\.?\s*(.*)', q_full)
                ans = ans_m.group(1) if ans_m else "A"
                exp = ans_m.group(2).strip() if ans_m and ans_m.group(2) else "Đáp án đúng theo bài nghe."

                exp_extra = re.search(r'\*\*Giải thích:\*\*\s*(.+)', q_full)
                if exp_extra:
                    exp = exp_extra.group(1).strip()

                tags = parse_tags(q_full)
                wrong_reasons = parse_wrong_reasons(q_full, options, ans)
                for opt in options.keys():
                    if opt != ans and opt not in wrong_reasons:
                        wrong_reasons[opt] = f"Lựa chọn ({opt}) không phù hợp với nội dung hội thoại."

                q_obj = {
                    "id": qid,
                    "groupId": gid,
                    "chapterId": "CH03",
                    "lessonId": "CH03-FINAL",
                    "part": 3,
                    "taskType": "conversation_question",
                    "prompt": prompt,
                    "optionsVisibleBeforeAnswer": True,
                    "image": None,
                    "audioSegments": None,
                    "options": options,
                    "correctAnswer": ans,
                    "transcript": transcript,
                    "translation": translation,
                    "explanation": exp,
                    "wrongReasons": wrong_reasons,
                    "skillTags": tags,
                    "skillGroup": get_skill_group(tags, "CH03", 3),
                    "difficulty": 2,
                    "revision": 1
                }
                questions.append(q_obj)

            audio_file = f"audio/chapter-03/{gid.lower()}.mp3"
            all_audio_manifest.append({
                "id": gid,
                "text": transcript,
                "voice": "mixed",
                "speed": 1.0,
                "output": audio_file,
                "turns": turns
            })

            groups.append({
                "id": gid,
                "chapterId": "CH03",
                "lessonId": "CH03-FINAL",
                "part": 3,
                "groupType": "conversation",
                "context": context,
                "speakers": [
                    {"speakerId": "W1", "label": "Woman", "gender": "female"},
                    {"speakerId": "M1", "label": "Man", "gender": "male"}
                ],
                "voiceAssignment": {"W1": "us-female-01", "M1": "us-male-01"},
                "turns": turns,
                "audioFile": audio_file,
                "transcript": transcript,
                "translation": translation,
                "questionIds": grp_qids,
                "revision": 1
            })

    ch03_data = {
        "chapterId": "CH03",
        "title": "Part 3 cơ bản: hội thoại hai người",
        "description": "Mục đích, địa điểm, chi tiết, vấn đề và hành động tiếp theo",
        "specVersion": "2.3",
        "contentVersion": "1.0.0",
        "lessons": lessons,
        "groups": groups,
        "questions": questions,
        "finalTest": {
            "id": "CH03-FINAL",
            "title": "Kiểm tra cuối chương 3",
            "questionIds": final_qids,
            "passRule": PASS_RULES['CH03-FINAL']
        }
    }

    with open('data/chapters/chapter-03.json', 'w', encoding='utf-8') as f:
        json.dump(ch03_data, f, ensure_ascii=False, indent=2)
    print(f"Parsed CH03: {len(lessons)} lessons, {len(groups)} groups, {len(questions)} questions")

# Execute all parsers
parse_ch01()
parse_ch02()
parse_ch03()

# Save audio manifest
manifest_data = {
    "specVersion": "2.3",
    "encoding": "CBR",
    "bitrate": "64k",
    "channels": 1,
    "sampleRate": 24000,
    "items": all_audio_manifest
}
with open('data/audio-manifest.json', 'w', encoding='utf-8') as f:
    json.dump(manifest_data, f, ensure_ascii=False, indent=2)

print(f"Saved data/audio-manifest.json with {len(all_audio_manifest)} items.")
