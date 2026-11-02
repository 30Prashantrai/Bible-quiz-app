"""Add mid-Scripture hard questions and balance answer positions."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

NEW_QUESTIONS = [
    {
        "id": "MID001",
        "en": {
            "question": "What did Joshua declare his household would do?",
            "options": ["Serve the Lord", "Build a palace", "Return to Egypt", "Follow the nations"],
            "correct_answer": "Serve the Lord",
            "category": "Teachings",
            "difficulty": "Hard",
            "bible_reference": "Joshua 24:15",
            "explanation": "Joshua declared that he and his household would serve the Lord.",
        },
        "ne": {
            "question": "यहोशूले आफ्नो घरानाले के गर्नेछ भनेर घोषणा गरे?",
            "options": ["परमप्रभुको सेवा गर्ने", "दरबार बनाउने", "मिश्र फर्कने", "जातिहरूलाई पछ्याउने"],
            "correct_answer": "परमप्रभुको सेवा गर्ने",
            "category": "Teachings",
            "difficulty": "Hard",
            "bible_reference": "यहोशू २४:१५",
            "explanation": "यहोशूले आफू र आफ्नो घरानाले परमप्रभुको सेवा गर्ने घोषणा गरे।",
        },
    },
    {
        "id": "MID002",
        "en": {
            "question": "Who judged Israel under a palm tree between Ramah and Bethel?",
            "options": ["Deborah", "Hannah", "Abigail", "Miriam"],
            "correct_answer": "Deborah",
            "category": "People",
            "difficulty": "Hard",
            "bible_reference": "Judges 4:4-5",
            "explanation": "Deborah was a prophetess who judged Israel under a palm tree.",
        },
        "ne": {
            "question": "रामाह र बेतेलको बीचमा खजुरको रूखमुनि इस्राएलको न्याय कसले गर्थिन्?",
            "options": ["दबोरा", "हन्ना", "अबिगेल", "मरियम"],
            "correct_answer": "दबोरा",
            "category": "People",
            "difficulty": "Hard",
            "bible_reference": "न्यायकर्ताहरू ४:४-५",
            "explanation": "दबोरा अगमवादिनी थिइन् र खजुरको रूखमुनि इस्राएलको न्याय गर्थिन्।",
        },
    },
    {
        "id": "MID003",
        "en": {
            "question": "What was the name of Ruth's son, an ancestor of David?",
            "options": ["Obed", "Jesse", "Boaz", "Mahlon"],
            "correct_answer": "Obed",
            "category": "People",
            "difficulty": "Hard",
            "bible_reference": "Ruth 4:13-17",
            "explanation": "Ruth gave birth to Obed, who became the grandfather of David.",
        },
        "ne": {
            "question": "दाऊदका पुर्खा रूथका छोराको नाम के थियो?",
            "options": ["ओबेद", "यिशै", "बोआज", "माहलोन"],
            "correct_answer": "ओबेद",
            "category": "People",
            "difficulty": "Hard",
            "bible_reference": "रूथ ४:१३-१७",
            "explanation": "रूथले ओबेदलाई जन्म दिइन्, जो दाऊदका हजुरबुबा बने।",
        },
    },
    {
        "id": "MID004",
        "en": {
            "question": "Whom did Saul seek at Endor?",
            "options": ["A medium", "A priest", "A prophetess from Shiloh", "A soldier"],
            "correct_answer": "A medium",
            "category": "Events",
            "difficulty": "Hard",
            "bible_reference": "1 Samuel 28:7",
            "explanation": "Saul asked his servants to find a woman who practiced as a medium at Endor.",
        },
        "ne": {
            "question": "शाऊलले एन्दोरमा कसलाई खोजे?",
            "options": ["एक तान्त्रिक स्त्री", "एक पूजाहारी", "शीलोकी अगमवादिनी", "एक सिपाही"],
            "correct_answer": "एक तान्त्रिक स्त्री",
            "category": "Events",
            "difficulty": "Hard",
            "bible_reference": "१ शमूएल २८:७",
            "explanation": "शाऊलले एन्दोरमा तान्त्रिक काम गर्ने एउटी स्त्री खोज्न आफ्ना सेवकहरूलाई भने।",
        },
    },
    {
        "id": "MID005",
        "en": {
            "question": "Which son of David was promised an enduring throne and would build the temple?",
            "options": ["Solomon", "Absalom", "Amnon", "Adonijah"],
            "correct_answer": "Solomon",
            "category": "Events",
            "difficulty": "Hard",
            "bible_reference": "2 Samuel 7:12-13",
            "explanation": "God promised David that his son would build the temple and have an established throne.",
        },
        "ne": {
            "question": "दाऊदका कुन छोरालाई स्थायी सिंहासनको प्रतिज्ञा गरियो र मन्दिर बनाउने थिए?",
            "options": ["सुलेमान", "अब्शालोम", "अम्नोन", "अदोनियाह"],
            "correct_answer": "सुलेमान",
            "category": "Events",
            "difficulty": "Hard",
            "bible_reference": "२ शमूएल ७:१२-१३",
            "explanation": "परमेश्वरले दाऊदका छोराले मन्दिर बनाउने र उसको सिंहासन स्थापित हुने प्रतिज्ञा गर्नुभयो।",
        },
    },
    {
        "id": "MID006",
        "en": {
            "question": "What did Elijah hear after the wind, earthquake, and fire?",
            "options": ["A gentle whisper", "A trumpet blast", "A loud song", "A rushing river"],
            "correct_answer": "A gentle whisper",
            "category": "Teachings",
            "difficulty": "Hard",
            "bible_reference": "1 Kings 19:11-12",
            "explanation": "The Lord spoke to Elijah through a gentle whisper after the dramatic signs.",
        },
        "ne": {
            "question": "हावा, भूकम्प र आगोपछि एलियाहले के सुने?",
            "options": ["मन्द स्वर", "तुरहीको आवाज", "ठूलो गीत", "बगिरहेको नदी"],
            "correct_answer": "मन्द स्वर",
            "category": "Teachings",
            "difficulty": "Hard",
            "bible_reference": "१ राजा १९:११-१२",
            "explanation": "ती शक्तिशाली घटनापछि परमप्रभुले एलियाहसँग मन्द स्वरद्वारा बोल्नुभयो।",
        },
    },
    {
        "id": "MID007",
        "en": {
            "question": "How many times did Naaman dip in the Jordan to be cleansed?",
            "options": ["Seven", "Three", "Five", "Twelve"],
            "correct_answer": "Seven",
            "category": "Miracles",
            "difficulty": "Hard",
            "bible_reference": "2 Kings 5:14",
            "explanation": "Naaman obeyed Elisha's instruction and dipped seven times in the Jordan.",
        },
        "ne": {
            "question": "निको हुन नामानले यर्दनमा कति पटक डुबुल्की लगाए?",
            "options": ["सात पटक", "तीन पटक", "पाँच पटक", "बाह्र पटक"],
            "correct_answer": "सात पटक",
            "category": "Miracles",
            "difficulty": "Hard",
            "bible_reference": "२ राजा ५:१४",
            "explanation": "नामानले एलिशाको आज्ञा मानेर यर्दनमा सात पटक डुबुल्की लगाए।",
        },
    },
    {
        "id": "MID008",
        "en": {
            "question": "What did the sons of Issachar understand?",
            "options": ["The times and what Israel should do", "How to build the temple", "The language of Egypt", "The number of Levites"],
            "correct_answer": "The times and what Israel should do",
            "category": "People",
            "difficulty": "Hard",
            "bible_reference": "1 Chronicles 12:32",
            "explanation": "The sons of Issachar understood the times and knew what Israel should do.",
        },
        "ne": {
            "question": "इस्साकारका छोराहरूले के बुझ्थे?",
            "options": ["समय र इस्राएलले गर्नुपर्ने कुरा", "मन्दिर कसरी बनाउने", "मिश्रको भाषा", "लेवीहरूको संख्या"],
            "correct_answer": "समय र इस्राएलले गर्नुपर्ने कुरा",
            "category": "People",
            "difficulty": "Hard",
            "bible_reference": "१ इतिहास १२:३२",
            "explanation": "इस्साकारका छोराहरूले समय बुझ्थे र इस्राएलले के गर्नुपर्छ भन्ने जान्दथे।",
        },
    },
    {
        "id": "MID009",
        "en": {
            "question": "What did Ezra set his heart to do?",
            "options": ["Study, practice, and teach the Law", "Become a king", "Build a fleet", "Count the soldiers"],
            "correct_answer": "Study, practice, and teach the Law",
            "category": "Teachings",
            "difficulty": "Hard",
            "bible_reference": "Ezra 7:10",
            "explanation": "Ezra devoted himself to studying, obeying, and teaching the Law of the Lord.",
        },
        "ne": {
            "question": "एज्राले आफ्नो हृदय कुन काममा लगाए?",
            "options": ["व्यवस्था अध्ययन, पालन र सिकाउन", "राजा बन्न", "जहाजहरूको बेडा बनाउन", "सिपाहीहरू गन्न"],
            "correct_answer": "व्यवस्था अध्ययन, पालन र सिकाउन",
            "category": "Teachings",
            "difficulty": "Hard",
            "bible_reference": "एज्रा ७:१०",
            "explanation": "एज्राले परमप्रभुको व्यवस्था अध्ययन गर्न, पालन गर्न र सिकाउन आफूलाई समर्पित गरे।",
        },
    },
    {
        "id": "MID010",
        "en": {
            "question": "What did Nehemiah urge the people to rebuild?",
            "options": ["The wall of Jerusalem", "The altar at Shiloh", "The palace of Babylon", "The road to Jericho"],
            "correct_answer": "The wall of Jerusalem",
            "category": "Events",
            "difficulty": "Hard",
            "bible_reference": "Nehemiah 2:17",
            "explanation": "Nehemiah urged the people to rebuild Jerusalem's wall and remove its disgrace.",
        },
        "ne": {
            "question": "नहेम्याहले मानिसहरूलाई के पुनर्निर्माण गर्न आग्रह गरे?",
            "options": ["यरूशलेमको पर्खाल", "शीलोको वेदी", "बाबेलको दरबार", "यरीहो जाने बाटो"],
            "correct_answer": "यरूशलेमको पर्खाल",
            "category": "Events",
            "difficulty": "Hard",
            "bible_reference": "नहेम्याह २:१७",
            "explanation": "नहेम्याहले यरूशलेमको पर्खाल पुनर्निर्माण गरेर त्यसको अपमान हटाउन आग्रह गरे।",
        },
    },
    {
        "id": "MID011",
        "en": {
            "question": "What does the psalmist call a lamp to his feet?",
            "options": ["God's word", "The temple lamp", "The sun", "A king's decree"],
            "correct_answer": "God's word",
            "category": "Teachings",
            "difficulty": "Hard",
            "bible_reference": "Psalm 119:105",
            "explanation": "The psalmist says God's word is a lamp to his feet and a light to his path.",
        },
        "ne": {
            "question": "भजनकारले आफ्नो खुट्टाका लागि केलाई बत्ती भनेका छन्?",
            "options": ["परमेश्वरको वचन", "मन्दिरको बत्ती", "सूर्य", "राजाको आज्ञा"],
            "correct_answer": "परमेश्वरको वचन",
            "category": "Teachings",
            "difficulty": "Hard",
            "bible_reference": "भजनसंग्रह ११९:१०५",
            "explanation": "भजनकारले परमेश्वरको वचनलाई आफ्नो खुट्टाका लागि बत्ती र बाटोका लागि ज्योति भनेका छन्।",
        },
    },
    {
        "id": "MID012",
        "en": {
            "question": "What two extremes did Agur ask God not to give him?",
            "options": ["Poverty and riches", "War and peace", "Youth and old age", "Famine and harvest"],
            "correct_answer": "Poverty and riches",
            "category": "Teachings",
            "difficulty": "Hard",
            "bible_reference": "Proverbs 30:8-9",
            "explanation": "Agur asked for neither poverty nor riches, but only his daily bread.",
        },
        "ne": {
            "question": "अगूरले परमेश्वरसँग कुन दुई चरम अवस्था नदिन बिन्ती गरे?",
            "options": ["गरिबी र धन", "युद्ध र शान्ति", "युवावस्था र वृद्धावस्था", "अकाल र फसल"],
            "correct_answer": "गरिबी र धन",
            "category": "Teachings",
            "difficulty": "Hard",
            "bible_reference": "हितोपदेश ३०:८-९",
            "explanation": "अगूरले गरिबी वा धन होइन, दैनिक भोजन मात्र दिन बिन्ती गरे।",
        },
    },
]


def reorder_options(record: dict, target_index: int) -> None:
    correct_index = record["options"].index(record["correct_answer"])
    if correct_index == target_index:
        return
    distractors = [option for index, option in enumerate(record["options"]) if index != correct_index]
    record["options"] = distractors[:target_index] + [record["correct_answer"]] + distractors[target_index:]


def main() -> None:
    banks = {
        lang: json.loads((ROOT / "data" / f"questions_{lang}.json").read_text(encoding="utf-8"))
        for lang in ("en", "ne")
    }
    existing = {record["id"] for record in banks["en"]}
    for question in NEW_QUESTIONS:
        if question["id"] in existing:
            continue
        banks["en"].append({"id": question["id"], **question["en"]})
        banks["ne"].append({"id": question["id"], **question["ne"]})

    by_id = {lang: {record["id"]: record for record in records} for lang, records in banks.items()}
    for index, question_id in enumerate(sorted(by_id["en"])):
        target = index % 4
        reorder_options(by_id["en"][question_id], target)
        reorder_options(by_id["ne"][question_id], target)

    for lang, records in banks.items():
        (ROOT / "data" / f"questions_{lang}.json").write_text(
            json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    print(f"English/Nepali records: {len(banks['en'])}")
    print("Answer positions balanced by stable A/B/C/D rotation.")


if __name__ == "__main__":
    main()
