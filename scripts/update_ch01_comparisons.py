import json

with open("data/chapters/chapter-01.json", "r", encoding="utf-8") as f:
    ch1 = json.load(f)

# CH01-L01 comparisons: Nhịp điệu câu: Content Words vs Function Words
ch1["lessons"][0]["comparisons"] = [
    {
        "title": "So sánh nhịp điệu: Từ mang nội dung (Nhấn to) vs Từ chức năng (Đọc lướt)",
        "tip": "Đừng cố nghe từng từ 'the, will, a'. Người bản xứ đọc dính các từ phụ và chỉ nhấn mạnh các từ mang nội dung chính.",
        "pairs": [
            {
                "wordA": "manager",
                "ipaA": "/ˈmæn.ə.dʒər/",
                "descA": "Từ nội dung: Nhấn to, rõ (quản lý)",
                "wordB": "the manager",
                "ipaB": "/ðə ˈmæn.ə.dʒər/",
                "descB": "'the' đọc lướt rất nhẹ, dính liền vào 'manager'"
            },
            {
                "wordA": "send",
                "ipaA": "/send/",
                "descA": "Động từ chính: Nhấn mạnh hành động (gửi)",
                "wordB": "will send",
                "ipaB": "/wɪl send/",
                "descB": "'will' đọc nhanh lướt qua"
            },
            {
                "wordA": "front desk",
                "ipaA": "/frʌnt desk/",
                "descA": "Cụm danh từ: Nhấn rõ địa điểm (quầy lễ tân)",
                "wordB": "at the front desk",
                "ipaB": "/ət ðə frʌnt desk/",
                "descB": "'at the' đọc lướt như một âm gió nhẹ"
            }
        ]
    }
]

# CH01-L02 comparisons: Âm cuối & Dạng rút gọn
ch1["lessons"][1]["comparisons"] = [
    {
        "title": "So sánh âm cuối: Từ không có âm cuối vs Có âm cuối (-s/-es)",
        "tip": "Bỏ âm cuối sẽ nhầm số ít/số nhiều hoặc chia thì. Nghe kỹ âm xì gió /s/ hoặc rung /z/ ở cuối từ B.",
        "pairs": [
            {
                "wordA": "plan",
                "ipaA": "/plæn/",
                "descA": "kế hoạch (dừng ở âm mũi 'n', không xì)",
                "wordB": "plans",
                "ipaB": "/plænz/",
                "descB": "nhiều kế hoạch (có âm xì rung /z/ kéo dài)"
            },
            {
                "wordA": "work",
                "ipaA": "/wɜːrk/",
                "descA": "làm việc (nguyên thể)",
                "wordB": "works",
                "ipaB": "/wɜːrks/",
                "descB": "cô ấy làm việc (bật âm gió /s/ dứt khoát)"
            },
            {
                "wordA": "need",
                "ipaA": "/niːd/",
                "descA": "cần (dừng ở âm /d/)",
                "wordB": "needs",
                "ipaB": "/niːdz/",
                "descB": "anh ấy cần (có âm rung /z/ ở đuôi)"
            },
            {
                "wordA": "car",
                "ipaA": "/kɑːr/",
                "descA": "một chiếc ô tô",
                "wordB": "cars",
                "ipaB": "/kɑːrz/",
                "descB": "nhiều chiếc ô tô (âm xì rung /z/)"
            },
            {
                "wordA": "price",
                "ipaA": "/praɪs/",
                "descA": "giá cả (kết thúc bằng âm xì gió không rung /s/)",
                "wordB": "prize",
                "ipaB": "/praɪz/",
                "descB": "giải thưởng (kết thúc bằng âm rung thanh quản /z/)"
            }
        ]
    },
    {
        "title": "So sánh đuôi quá khứ: Không có -ed vs Có đuôi -ed",
        "tip": "Với động từ kết thúc bằng /t/ hoặc /d/ (như need, wait), khi thêm -ed sẽ tăng thêm 1 âm tiết đọc rõ 'did/tid'.",
        "pairs": [
            {
                "wordA": "miss",
                "ipaA": "/mɪs/",
                "descA": "bỏ lỡ (hiện tại - 1 âm tiết)",
                "wordB": "missed",
                "ipaB": "/mɪst/",
                "descB": "đã bỏ lỡ (bật âm /t/ dứt khoát ở cuối)"
            },
            {
                "wordA": "call",
                "ipaA": "/kɔːl/",
                "descA": "gọi điện (hiện tại)",
                "wordB": "called",
                "ipaB": "/kɔːld/",
                "descB": "đã gọi điện (bật âm /d/ nhẹ ở cuối)"
            },
            {
                "wordA": "need",
                "ipaA": "/niːd/",
                "descA": "cần (1 âm tiết: 'nít')",
                "wordB": "needed",
                "ipaB": "/ˈniː.dɪd/",
                "descB": "đã cần (2 âm tiết rõ ràng: 'nii-did')"
            },
            {
                "wordA": "wait",
                "ipaA": "/weɪt/",
                "descA": "chờ (1 âm tiết: 'uây-t')",
                "wordB": "waited",
                "ipaB": "/ˈweɪ.tɪd/",
                "descB": "đã chờ (2 âm tiết: 'way-tid')"
            },
            {
                "wordA": "stop",
                "ipaA": "/stɑːp/",
                "descA": "dừng (hiện tại)",
                "wordB": "stopped",
                "ipaB": "/stɑːpt/",
                "descB": "đã dừng (bật âm /p/ rồi /t/ dứt khoát)"
            }
        ]
    },
    {
        "title": "So sánh dạng đầy đủ vs Dạng rút gọn (Contractions)",
        "tip": "Đề thi TOEIC luôn đọc dạng rút gọn. Hãy tập nghe âm gió /v/, /l/, /z/ dính ngay sau đại từ.",
        "pairs": [
            {
                "wordA": "I have",
                "ipaA": "/aɪ hæv/",
                "descA": "dạng đầy đủ (2 từ rời)",
                "wordB": "I've",
                "ipaB": "/aɪv/",
                "descB": "dạng rút gọn (nghe như 'aiv', âm /v/ lướt nhẹ)"
            },
            {
                "wordA": "We have",
                "ipaA": "/wiː hæv/",
                "descA": "dạng đầy đủ",
                "wordB": "We've",
                "ipaB": "/wiːv/",
                "descB": "dạng rút gọn (nghe như 'wiiv')"
            },
            {
                "wordA": "We will",
                "ipaA": "/wiː wɪl/",
                "descA": "dạng đầy đủ",
                "wordB": "We'll",
                "ipaB": "/wiːl/",
                "descB": "dạng rút gọn (uốn lưỡi /l/ ở cuối)"
            },
            {
                "wordA": "They are",
                "ipaA": "/ðeɪ ɑːr/",
                "descA": "dạng đầy đủ",
                "wordB": "They're",
                "ipaB": "/ðer/",
                "descB": "dạng rút gọn (phát âm giống hệt 'their/there')"
            },
            {
                "wordA": "He is",
                "ipaA": "/hiː ɪz/",
                "descA": "dạng đầy đủ",
                "wordB": "He's",
                "ipaB": "/hiːz/",
                "descB": "dạng rút gọn (có âm xì rung /z/ ở đuôi)"
            },
            {
                "wordA": "Cannot",
                "ipaA": "/ˈkæn.ɒt/",
                "descA": "dạng đầy đủ (2 âm tiết)",
                "wordB": "Can't",
                "ipaB": "/kænt/",
                "descB": "dạng rút gọn (chặn hơi /t/ dứt khoát, khác 'can' /kən/ đọc nhẹ)"
            },
            {
                "wordA": "Will not",
                "ipaA": "/wɪl nɒt/",
                "descA": "dạng đầy đủ",
                "wordB": "Won't",
                "ipaB": "/woʊnt/",
                "descB": "dạng rút gọn (nguyên âm đổi thành 'o-u-n-t')"
            }
        ]
    }
]

# CH01-L03 comparisons: Số -teen vs -ty & Giờ hơn/kém
ch1["lessons"][2]["comparisons"] = [
    {
        "title": "So sánh bẫy số kinh điển: Đuôi -teen (13-19) vs Đuôi -ty (30-90)",
        "tip": "Quy tắc vàng: Đuôi -teen NHẤN TRỌNG ÂM Ở ÂM TIẾT 2 (kéo dài 'ti-i-n'); Đuôi -ty NHẤN Ở ÂM TIẾT ĐẦU (đuôi ty đọc cụt, nhẹ).",
        "pairs": [
            {
                "wordA": "fourteen",
                "ipaA": "/fɔːrˈtiːn/",
                "descA": "14 (Nhấn mạnh vào TEEN, ngân dài)",
                "wordB": "forty",
                "ipaB": "/ˈfɔːr.ti/",
                "descB": "40 (Nhấn mạnh vào FOR, đuôi ty cụt ngắn)"
            },
            {
                "wordA": "fifteen",
                "ipaA": "/fɪfˈtiːn/",
                "descA": "15 (Nhấn mạnh vào TEEN)",
                "wordB": "fifty",
                "ipaB": "/ˈfɪf.ti/",
                "descB": "50 (Nhấn mạnh vào FIF)"
            },
            {
                "wordA": "sixteen",
                "ipaA": "/sɪksˈtiːn/",
                "descA": "16 (Nhấn mạnh vào TEEN)",
                "wordB": "sixty",
                "ipaB": "/ˈsɪks.ti/",
                "descB": "60 (Nhấn mạnh vào SIX)"
            },
            {
                "wordA": "seventeen",
                "ipaA": "/ˌsev.ənˈtiːn/",
                "descA": "17 (Nhấn mạnh vào TEEN)",
                "wordB": "seventy",
                "ipaB": "/ˈsev.ən.ti/",
                "descB": "70 (Nhấn mạnh vào SEV)"
            },
            {
                "wordA": "eighteen",
                "ipaA": "/eɪˈtiːn/",
                "descA": "18 (Nhấn mạnh vào TEEN)",
                "wordB": "eighty",
                "ipaB": "/ˈeɪ.ti/",
                "descB": "80 (Nhấn mạnh vào EIGH)"
            },
            {
                "wordA": "nineteen",
                "ipaA": "/naɪnˈtiːn/",
                "descA": "19 (Nhấn mạnh vào TEEN)",
                "wordB": "ninety",
                "ipaB": "/ˈnaɪn.ti/",
                "descB": "90 (Nhấn mạnh vào NINE)"
            },
            {
                "wordA": "thirteen",
                "ipaA": "/θɜːrˈtiːn/",
                "descA": "13 (Nhấn mạnh vào TEEN)",
                "wordB": "thirty",
                "ipaB": "/ˈθɜːr.ti/",
                "descB": "30 (Nhấn mạnh vào THIR)"
            }
        ]
    },
    {
        "title": "So sánh cách nói giờ: Giờ hơn (past) vs Giờ kém (to)",
        "tip": "Để ý từ nối: 'past' là đã qua (giờ hơn); 'to' là hướng tới (còn bao nhiêu phút nữa đến giờ đó).",
        "pairs": [
            {
                "wordA": "quarter past three",
                "ipaA": "/ˈkwɔː.tər pɑːst θriː/",
                "descA": "3 giờ 15 phút (đã qua 3 giờ được 15 phút)",
                "wordB": "quarter to three",
                "ipaB": "/ˈkwɔː.tər tuː θriː/",
                "descB": "3 giờ kém 15 phút = 2:45 (còn 15 phút nữa đến 3 giờ)"
            },
            {
                "wordA": "half past three",
                "ipaA": "/hɑːf pɑːst θriː/",
                "descA": "3 giờ 30 phút (giờ rưỡi)",
                "wordB": "three o'clock",
                "ipaB": "/θriː əˈklɒk/",
                "descB": "3 giờ đúng"
            }
        ]
    }
]

# CH01-L04 comparisons: Từ để hỏi dễ nhầm lẫn
ch1["lessons"][3]["comparisons"] = [
    {
        "title": "Bẫy số 1 đề thi: WHERE (Ở đâu) vs WHEN (Khi nào)",
        "tip": "Mẹo vàng phân biệt: WHERE miệng mở rộng, kết thúc bằng âm mở hoặc uốn lưỡi /r/; WHEN kết thúc bằng phụ âm mũi /n/ (đầu lưỡi ngậm chạm vòm miệng trên, luồng hơi dồn lên mũi).",
        "pairs": [
            {
                "wordA": "Where",
                "ipaA": "/wer/",
                "descA": "Ở ĐÂU (hỏi nơi chốn) -> Âm mở /wer/, miệng không ngậm lại",
                "wordB": "When",
                "ipaB": "/wen/",
                "descB": "KHI NÀO (hỏi thời gian) -> Âm mũi /wen/, đầu lưỡi ngậm chặn hơi"
            },
            {
                "wordA": "Where did you go?",
                "ipaA": "/wer dɪd juː ɡoʊ/",
                "descA": "Bạn đã đi đâu? (Trả lời bằng địa điểm: 'To the library')",
                "wordB": "When did you go?",
                "ipaB": "/wen dɪd juː ɡoʊ/",
                "descB": "Bạn đã đi khi nào? (Trả lời bằng thời gian: 'Yesterday afternoon')"
            },
            {
                "wordA": "Where is the meeting?",
                "ipaA": "/wer ɪz ðə ˈmiː.tɪŋ/ (nối âm: 'we-riz')",
                "descA": "Cuộc họp ở đâu? (Trả lời: 'In conference room B')",
                "wordB": "When is the meeting?",
                "ipaB": "/wen ɪz ðə ˈmiː.tɪŋ/ (nối âm: 'wen-niz')",
                "descB": "Cuộc họp khi nào? (Trả lời: 'At two o'clock')"
            }
        ]
    },
    {
        "title": "So sánh các cặp từ hỏi dễ nhầm: WHO vs WHOSE, WHY vs HOW",
        "tip": "WHOSE có âm xì /z/ cuối hỏi sở hữu; WHY nguyên âm /aɪ/ hỏi lý do; HOW nguyên âm /aʊ/ hỏi cách thức.",
        "pairs": [
            {
                "wordA": "Who",
                "ipaA": "/huː/",
                "descA": "AI? (Hỏi người/danh tính: 'Mr. Tanaka')",
                "wordB": "Whose",
                "ipaB": "/huːz/",
                "descB": "CỦA AI? (Hỏi chủ sở hữu, có âm xì /z/: 'It's mine')"
            },
            {
                "wordA": "Why",
                "ipaA": "/waɪ/",
                "descA": "TẠI SAO? (Nguyên âm /aɪ/, hỏi lý do: 'Because of the rain')",
                "wordB": "How",
                "ipaB": "/haʊ/",
                "descB": "NHƯ THẾ NÀO? (Nguyên âm /aʊ/, hỏi cách thức/phương tiện: 'By bus')"
            },
            {
                "wordA": "What",
                "ipaA": "/wʌt/",
                "descA": "CÁI GÌ? (Hỏi thông tin chung)",
                "wordB": "Which",
                "ipaB": "/wɪtʃ/",
                "descB": "CÁI NÀO? (Có âm bật gió /tʃ/ ở cuối, hỏi lựa chọn cụ thể)"
            }
        ]
    }
]

with open("data/chapters/chapter-01.json", "w", encoding="utf-8") as f:
    json.dump(ch1, f, ensure_ascii=False, indent=2)

print("Updated data/chapters/chapter-01.json with comprehensive comparison pairs!")
