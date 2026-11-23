import re
import json
import os

# Skill Group mapping
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
        # Match - A. text or - A: text or - A text
        m = re.search(rf'-\s*{letter}[\.:]\s*(.+)', text)
        if m:
            options[letter] = m.group(1).strip()
    return options

def parse_wrong_reasons(text, options, correct_answer):
    wrong_reasons = {}
    m = re.search(r'\*\*Sai vì:\*\*\s*(.*)', text)
    if not m:
        return wrong_reasons
    raw = m.group(1).strip()
    # If the text has letters like A là... B là... or A: ... B: ...
    # We can split or assign to non-correct options
    for opt in options.keys():
        if opt != correct_answer:
            # Look for opt in raw, e.g., "A là..." or "A không..."
            pattern = rf'{opt}\s*[\:là\s]([^;A-D]+)'
            opt_m = re.search(pattern, raw)
            if opt_m:
                wrong_reasons[opt] = f"{opt} {opt_m.group(1).strip()}"
            else:
                wrong_reasons[opt] = raw
    return wrong_reasons

print("Parser core loaded.")
