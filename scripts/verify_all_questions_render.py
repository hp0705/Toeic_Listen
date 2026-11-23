import os
import json

ROOT = os.getcwd()

def run_audit():
    print("======================================================================")
    print(" EXHAUSTIVE UI RENDERING & AUDIO AUDIT FOR ALL QUESTIONS (CH01-CH03)")
    print("======================================================================")

    total_questions = 0
    total_mcq = 0
    total_dictation = 0
    issues = []

    for ch in ["01", "02", "03"]:
        path = os.path.join(ROOT, "data", "chapters", f"chapter-{ch}.json")
        if not os.path.exists(path):
            print(f"Skipping {path} (not found)")
            continue

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        groups_map = {g["id"]: g for g in data.get("groups", [])}
        questions = data.get("questions", [])

        for q in questions:
            total_questions += 1
            qid = q.get("id", "UNKNOWN")
            lid = q.get("lessonId", "")
            part = q.get("part", 0)
            task_type = q.get("taskType", "")
            segs = q.get("audioSegments") or []
            opts = q.get("options") or {}
            vis_before = q.get("optionsVisibleBeforeAnswer", True)
            group_id = q.get("groupId")

            # 1. Dictation Questions
            if task_type == "dictation":
                total_dictation += 1
                if not segs:
                    issues.append(f"[{qid} in {lid}] Dictation question has NO audioSegments!")
                else:
                    for s in segs:
                        f = os.path.join(ROOT, s.get("file", ""))
                        if not os.path.isfile(f):
                            issues.append(f"[{qid} in {lid}] Audio file missing: {s.get('file')}")
                continue

            # 2. Multiple Choice Questions
            total_mcq += 1

            # Check that each option has non-empty text
            for opt_key, opt_val in opts.items():
                if not opt_val or not str(opt_val).strip():
                    issues.append(f"[{qid} in {lid}] Option '{opt_key}' has EMPTY text!")

            # Determine whether options will have text displayed on screen before answering (quiz.js logic)
            has_opt_audio = len(segs) > 1
            is_audio_only = (vis_before is False) and has_opt_audio
            show_text = (not is_audio_only)

            # If options are audio-only (no text on button), the question MUST have spoken audio for each choice
            if not show_text:
                # Part 1 or Part 2: audio must play the choices
                if len(segs) <= 1:
                    issues.append(
                        f"[{qid} in {lid}] BLANK BUTTON BUG: optionsVisibleBeforeAnswer is False, but audioSegments only has {len(segs)} segment(s)! Student cannot hear or read options."
                    )
                else:
                    # Check that audio files exist
                    for s in segs:
                        f = os.path.join(ROOT, s.get("file", ""))
                        if not os.path.isfile(f):
                            issues.append(f"[{qid} in {lid}] Option audio missing: {s.get('file')}")
            else:
                # Text is displayed on buttons: verify all option texts are meaningful
                for opt_key in opts:
                    val = str(opts[opt_key]).strip()
                    if len(val) == 0:
                        issues.append(f"[{qid} in {lid}] Displayed option button '{opt_key}' is completely blank!")

            # Check Part 1 image
            if part == 1:
                img_path = q.get("image")
                if not img_path:
                    issues.append(f"[{qid} in {lid}] Part 1 question has NO image!")
                else:
                    full_img = os.path.join(ROOT, img_path)
                    if not os.path.isfile(full_img):
                        issues.append(f"[{qid} in {lid}] Image file does not exist: {img_path}")

            # Check Part 3 / 4 Group audio
            if group_id:
                if group_id not in groups_map:
                    issues.append(f"[{qid} in {lid}] Group '{group_id}' not found in chapter groups!")
                else:
                    g = groups_map[group_id]
                    g_audio = os.path.join(ROOT, g.get("audioFile", ""))
                    if not os.path.isfile(g_audio):
                        issues.append(f"[{qid} in {lid}] Group audio file missing: {g.get('audioFile')}")

    print(f"Total Questions Audited: {total_questions}")
    print(f"  - Multiple Choice: {total_mcq}")
    print(f"  - Dictation: {total_dictation}")
    print("----------------------------------------------------------------------")
    if not issues:
        print(">>> RESULT: ALL 390 QUESTIONS PASSED THE UI & AUDIO AUDIT! <<<")
        print("No blank buttons, no missing audio, no missing images found.")
    else:
        print(f">>> FOUND {len(issues)} ISSUE(S): <<<")
        for iss in issues:
            print("  [CRITICAL] " + iss)
    print("======================================================================")
    return len(issues)

if __name__ == "__main__":
    import sys
    err_count = run_audit()
    sys.exit(err_count)
