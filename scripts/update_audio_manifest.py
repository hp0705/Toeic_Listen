#!/usr/bin/env python3
"""
Updates data/audio-manifest.json by collecting all audio files from all chapters.
"""

import os
import json

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def main():
    manifest_path = os.path.join(ROOT_DIR, "data", "audio-manifest.json")
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    all_items = []
    seen_outputs = set()

    for ch_num in ["01", "02", "03"]:
        ch_file = os.path.join(ROOT_DIR, "data", "chapters", f"chapter-{ch_num}.json")
        if not os.path.isfile(ch_file):
            continue

        with open(ch_file, "r", encoding="utf-8") as f:
            ch_data = json.load(f)

        ch_id = ch_data.get("chapterId", f"CH{ch_num}")

        # 1. Lessons
        for l in ch_data.get("lessons", []):
            # Examples
            for ex in l.get("examples", []):
                out = ex.get("audioFile")
                if out and out not in seen_outputs:
                    seen_outputs.add(out)
                    all_items.append({
                        "id": ex.get("id", f"{ch_id}-EX"),
                        "text": ex.get("text", ""),
                        "voice": "us-female-01",
                        "speed": 1.0,
                        "output": out
                    })
            # ABX
            for abx in l.get("abxExercises", []):
                if abx.get("audioA") and abx["audioA"] not in seen_outputs:
                    seen_outputs.add(abx["audioA"])
                    all_items.append({"id": f"{abx['id']}-A", "text": abx["textA"], "voice": "us-female-01", "speed": 1.0, "output": abx["audioA"]})
                if abx.get("audioB") and abx["audioB"] not in seen_outputs:
                    seen_outputs.add(abx["audioB"])
                    all_items.append({"id": f"{abx['id']}-B", "text": abx["textB"], "voice": "us-male-01", "speed": 1.0, "output": abx["audioB"]})
                if abx.get("audioX") and abx["audioX"] not in seen_outputs:
                    seen_outputs.add(abx["audioX"])
                    all_items.append({"id": f"{abx['id']}-X", "text": abx["textX"], "voice": "us-female-01", "speed": 1.0, "output": abx["audioX"]})
            # Dictations
            for d in l.get("dictations", []):
                out = d.get("audioFile")
                if out and out not in seen_outputs:
                    seen_outputs.add(out)
                    clean_text = d["audioText"].replace("**", "")
                    all_items.append({
                        "id": d["id"],
                        "text": clean_text,
                        "voice": "us-female-01",
                        "speed": 1.0,
                        "output": out
                    })

        # 2. Groups
        for g in ch_data.get("groups", []):
            out = g.get("audioFile")
            if out and out not in seen_outputs:
                seen_outputs.add(out)
                all_items.append({
                    "id": g["id"],
                    "text": g.get("transcript", ""),
                    "voice": "us-dialogue-01",
                    "speed": 1.0,
                    "output": out
                })

        # 3. Questions
        for q in ch_data.get("questions", []):
            segs = q.get("audioSegments") or []
            for idx, s in enumerate(segs):
                out = s.get("file")
                if out and out not in seen_outputs:
                    seen_outputs.add(out)
                    all_items.append({
                        "id": f"{q['id']}-S{idx+1}",
                        "text": s.get("text", ""),
                        "voice": s.get("voice", "us-female-01"),
                        "speed": 1.0,
                        "output": out
                    })

    manifest["items"] = all_items
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"Updated audio-manifest.json with {len(all_items)} audio items across chapters.")

if __name__ == "__main__":
    main()
