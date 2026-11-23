import os

images_dir = "images/chapter-02"
os.makedirs(images_dir, exist_ok=True)

# 18 SVG descriptions and generator
svgs = {
    "ch02-l01-q01.svg": {
        "title": "Woman at Desk with Document",
        "brief": "Một nhân viên nữ đứng cạnh bàn, cầm một tờ giấy và nhìn chăm chú vào tờ giấy; trên bàn có laptop và cốc cà phê.",
        "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 400" width="100%" height="100%">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#f8fafc"/>
      <stop offset="100%" stop-color="#e2e8f0"/>
    </linearGradient>
    <linearGradient id="desk" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#94a3b8"/>
      <stop offset="100%" stop-color="#64748b"/>
    </linearGradient>
  </defs>
  <rect width="600" height="400" fill="url(#bg)"/>
  <rect y="320" width="600" height="80" fill="#cbd5e1"/>
  <!-- Office window / wall decor -->
  <rect x="50" y="40" width="160" height="180" rx="8" fill="#e0f2fe" stroke="#38bdf8" stroke-width="3"/>
  <line x1="130" y1="40" x2="130" y2="220" stroke="#38bdf8" stroke-width="2"/>
  <line x1="50" y1="130" x2="210" y2="130" stroke="#38bdf8" stroke-width="2"/>
  <!-- Desk -->
  <rect x="220" y="220" width="340" height="18" rx="3" fill="url(#desk)"/>
  <rect x="250" y="238" width="14" height="120" fill="#475569"/>
  <rect x="520" y="238" width="14" height="120" fill="#475569"/>
  <!-- Laptop on desk -->
  <rect x="360" y="175" width="80" height="45" rx="4" fill="#334155"/>
  <polygon points="350,220 450,220 440,215 360,215" fill="#64748b"/>
  <!-- Coffee cup -->
  <rect x="470" y="195" width="22" height="25" rx="3" fill="#0284c7"/>
  <path d="M 492 200 Q 500 207 492 215" stroke="#0284c7" stroke-width="3" fill="none"/>
  <!-- Woman standing -->
  <!-- Legs -->
  <rect x="160" y="230" width="18" height="120" fill="#1e293b"/>
  <rect x="185" y="230" width="18" height="120" fill="#1e293b"/>
  <!-- Torso / Dress -->
  <polygon points="150,150 215,150 220,230 145,230" fill="#0284c7"/>
  <!-- Head & Hair -->
  <circle cx="180" cy="115" r="22" fill="#fed7aa"/>
  <path d="M 160 115 Q 180 85 200 115 Q 205 95 180 90 Q 155 95 160 115" fill="#854d0e"/>
  <!-- Arms & Paper -->
  <path d="M 155 160 Q 185 190 205 180" stroke="#fed7aa" stroke-width="10" stroke-linecap="round" fill="none"/>
  <!-- Paper sheet held -->
  <rect x="195" y="160" width="30" height="40" rx="2" fill="#ffffff" stroke="#94a3b8" stroke-width="1.5" transform="rotate(-15 195 160)"/>
  <line x1="200" y1="172" x2="218" y2="167" stroke="#94a3b8" stroke-width="1.5"/>
  <line x1="201" y1="180" x2="219" y2="175" stroke="#94a3b8" stroke-width="1.5"/>
  <line x1="202" y1="188" x2="215" y2="184" stroke="#94a3b8" stroke-width="1.5"/>
  <!-- Caption banner -->
  <rect x="20" y="340" width="560" height="45" rx="6" fill="#0f172a" opacity="0.9"/>
  <text x="300" y="367" font-family="system-ui, sans-serif" font-size="14" font-weight="bold" fill="#f8fafc" text-anchor="middle">CH02-L01-Q01: Woman standing beside desk, reading document</text>
</svg>"""
    },
    "ch02-l01-q02.svg": {
        "title": "Two Colleagues at Large Display",
        "brief": "Hai nhân viên mặc trang phục công sở đang đứng cạnh một màn hình lớn; một người chỉ tay vào biểu đồ trên màn hình, người kia cầm sổ ghi chép.",
        "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 400" width="100%" height="100%">
  <defs>
    <linearGradient id="screen" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#1e293b"/>
      <stop offset="100%" stop-color="#0f172a"/>
    </linearGradient>
  </defs>
  <rect width="600" height="400" fill="#f1f5f9"/>
  <rect y="330" width="600" height="70" fill="#cbd5e1"/>
  <!-- Large Wall Monitor -->
  <rect x="60" y="50" width="260" height="170" rx="8" fill="url(#screen)" stroke="#475569" stroke-width="6"/>
  <!-- Chart on Screen -->
  <polyline points="90,170 140,120 180,140 230,90 280,110" fill="none" stroke="#38bdf8" stroke-width="4"/>
  <rect x="100" y="140" width="16" height="45" fill="#3b82f6" opacity="0.7"/>
  <rect x="130" y="110" width="16" height="75" fill="#3b82f6" opacity="0.7"/>
  <rect x="160" y="130" width="16" height="55" fill="#3b82f6" opacity="0.7"/>
  <rect x="190" y="80" width="16" height="105" fill="#3b82f6" opacity="0.7"/>
  <rect x="220" y="100" width="16" height="85" fill="#3b82f6" opacity="0.7"/>
  <!-- Person 1 (Pointing to chart) -->
  <rect x="340" y="230" width="18" height="120" fill="#1e293b"/>
  <rect x="365" y="230" width="18" height="120" fill="#1e293b"/>
  <polygon points="335,150 395,150 400,230 330,230" fill="#2563eb"/>
  <circle cx="365" cy="115" r="22" fill="#fed7aa"/>
  <!-- Arm pointing to screen -->
  <path d="M 345 160 Q 290 120 250 110" stroke="#fed7aa" stroke-width="10" stroke-linecap="round" fill="none"/>
  <!-- Person 2 (Holding notebook) -->
  <rect x="440" y="230" width="18" height="120" fill="#334155"/>
  <rect x="465" y="230" width="18" height="120" fill="#334155"/>
  <polygon points="435,150 495,150 490,230 430,230" fill="#475569"/>
  <circle cx="465" cy="115" r="22" fill="#fed7aa"/>
  <!-- Arm holding notebook -->
  <path d="M 445 165 Q 470 190 480 185" stroke="#fed7aa" stroke-width="9" stroke-linecap="round" fill="none"/>
  <rect x="470" y="170" width="28" height="35" rx="3" fill="#f59e0b" stroke="#b45309" stroke-width="1.5"/>
  <rect x="20" y="340" width="560" height="45" rx="6" fill="#0f172a" opacity="0.9"/>
  <text x="300" y="367" font-family="system-ui, sans-serif" font-size="14" font-weight="bold" fill="#f8fafc" text-anchor="middle">CH02-L01-Q02: Two staff standing by large display, one pointing</text>
</svg>"""
    },
    "ch02-l01-q03.svg": {
        "title": "Man Pushing Cart in Warehouse",
        "brief": "Một người đàn ông đẩy xe đẩy có nhiều thùng carton trong hành lang kho hàng; hai bên hành lang là kệ chứa hàng cao.",
        "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 400" width="100%" height="100%">
  <rect width="600" height="400" fill="#e2e8f0"/>
  <!-- Warehouse shelves perspective -->
  <polygon points="0,0 120,60 120,350 0,400" fill="#94a3b8" stroke="#475569" stroke-width="2"/>
  <polygon points="600,0 480,60 480,350 600,400" fill="#94a3b8" stroke="#475569" stroke-width="2"/>
  <!-- Shelf boxes left -->
  <rect x="15" y="80" width="80" height="40" fill="#d97706" rx="2"/>
  <rect x="20" y="140" width="75" height="45" fill="#b45309" rx="2"/>
  <rect x="10" y="210" width="85" height="50" fill="#d97706" rx="2"/>
  <!-- Floor -->
  <polygon points="120,350 480,350 600,400 0,400" fill="#cbd5e1"/>
  <!-- Cart with boxes -->
  <!-- Cart frame -->
  <rect x="260" y="270" width="140" height="12" fill="#475569"/>
  <circle cx="280" cy="295" r="14" fill="#0f172a"/>
  <circle cx="380" cy="295" r="14" fill="#0f172a"/>
  <line x1="260" y1="270" x2="220" y2="200" stroke="#475569" stroke-width="6" stroke-linecap="round"/>
  <!-- Cardboard boxes stacked on cart -->
  <rect x="270" y="200" width="60" height="70" fill="#b45309" stroke="#78350f" stroke-width="2"/>
  <rect x="335" y="210" width="55" height="60" fill="#d97706" stroke="#78350f" stroke-width="2"/>
  <rect x="290" y="140" width="65" height="60" fill="#d97706" stroke="#78350f" stroke-width="2"/>
  <!-- Man pushing cart -->
  <rect x="170" y="230" width="16" height="90" fill="#1e293b"/>
  <rect x="195" y="230" width="16" height="90" fill="#1e293b"/>
  <polygon points="160,160 215,160 210,230 165,230" fill="#0284c7"/>
  <circle cx="185" cy="130" r="20" fill="#fed7aa"/>
  <!-- Arms pushing cart handle -->
  <path d="M 185 170 L 220 200" stroke="#fed7aa" stroke-width="9" stroke-linecap="round"/>
  <rect x="20" y="340" width="560" height="45" rx="6" fill="#0f172a" opacity="0.9"/>
  <text x="300" y="367" font-family="system-ui, sans-serif" font-size="14" font-weight="bold" fill="#f8fafc" text-anchor="middle">CH02-L01-Q03: Man pushing cart with boxes in warehouse</text>
</svg>"""
    },
    "ch02-l01-q04.svg": {
        "title": "Meeting Room Discussion",
        "brief": "Ba người ngồi quanh bàn họp; một người đang nói và hai người còn lại nhìn người đó; trên bàn có tài liệu và chai nước.",
        "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 400" width="100%" height="100%">
  <rect width="600" height="400" fill="#f8fafc"/>
  <rect y="310" width="600" height="90" fill="#e2e8f0"/>
  <!-- Conference Table -->
  <ellipse cx="300" cy="270" rx="220" ry="45" fill="#64748b"/>
  <ellipse cx="300" cy="265" rx="215" ry="40" fill="#94a3b8"/>
  <!-- Table items -->
  <rect x="230" y="245" width="30" height="22" rx="2" fill="#ffffff" stroke="#cbd5e1"/>
  <rect x="340" y="245" width="30" height="22" rx="2" fill="#ffffff" stroke="#cbd5e1"/>
  <rect x="290" y="235" width="8" height="20" rx="3" fill="#38bdf8"/>
  <!-- Person 1 (Speaker on left) -->
  <ellipse cx="170" cy="220" rx="25" ry="35" fill="#2563eb"/>
  <circle cx="170" cy="155" r="22" fill="#fed7aa"/>
  <path d="M 180 185 Q 210 190 220 210" stroke="#fed7aa" stroke-width="8" stroke-linecap="round" fill="none"/>
  <!-- Person 2 (Center listening) -->
  <ellipse cx="300" cy="190" rx="25" ry="35" fill="#059669"/>
  <circle cx="300" cy="130" r="22" fill="#fed7aa"/>
  <!-- Person 3 (Right listening) -->
  <ellipse cx="430" cy="220" rx="25" ry="35" fill="#475569"/>
  <circle cx="430" cy="155" r="22" fill="#fed7aa"/>
  <rect x="20" y="340" width="560" height="45" rx="6" fill="#0f172a" opacity="0.9"/>
  <text x="300" y="367" font-family="system-ui, sans-serif" font-size="14" font-weight="bold" fill="#f8fafc" text-anchor="middle">CH02-L01-Q04: Three people around conference table in meeting</text>
</svg>"""
    },
    "ch02-l02-q01.svg": {
        "title": "Suitcase beside airport bench",
        "brief": "Một chiếc vali đặt cạnh ghế dài trong sảnh sân bay; phía sau là cửa sổ kính lớn nhìn ra đường băng.",
        "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 400" width="100%" height="100%">
  <rect width="600" height="400" fill="#f1f5f9"/>
  <!-- Airport window -->
  <rect x="40" y="30" width="520" height="180" fill="#bae6fd" stroke="#94a3b8" stroke-width="4"/>
  <!-- Runway & plane in distance -->
  <rect x="40" y="160" width="520" height="50" fill="#64748b"/>
  <polygon points="280,110 330,110 350,130 250,130" fill="#ffffff"/>
  <!-- Long Airport Bench -->
  <rect x="80" y="230" width="300" height="15" rx="3" fill="#334155"/>
  <rect x="100" y="245" width="12" height="75" fill="#475569"/>
  <rect x="350" y="245" width="12" height="75" fill="#475569"/>
  <!-- Suitcase beside bench -->
  <rect x="420" y="210" width="70" height="100" rx="8" fill="#0284c7" stroke="#0369a1" stroke-width="3"/>
  <!-- Suitcase handle & wheels -->
  <rect x="445" y="180" width="20" height="30" fill="none" stroke="#0369a1" stroke-width="4"/>
  <circle cx="435" cy="315" r="7" fill="#0f172a"/>
  <circle cx="475" cy="315" r="7" fill="#0f172a"/>
  <rect x="20" y="340" width="560" height="45" rx="6" fill="#0f172a" opacity="0.9"/>
  <text x="300" y="367" font-family="system-ui, sans-serif" font-size="14" font-weight="bold" fill="#f8fafc" text-anchor="middle">CH02-L02-Q01: Suitcase beside airport bench near window</text>
</svg>"""
    },
    "ch02-l02-q02.svg": {
        "title": "Desk Lamp and Box Under Desk",
        "brief": "Một chiếc đèn bàn đặt trên mặt bàn gỗ; bên dưới bàn có một thùng giấy.",
        "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 400" width="100%" height="100%">
  <rect width="600" height="400" fill="#f8fafc"/>
  <rect y="310" width="600" height="90" fill="#cbd5e1"/>
  <!-- Wooden Desk -->
  <rect x="120" y="180" width="360" height="20" rx="3" fill="#b45309"/>
  <rect x="145" y="200" width="18" height="120" fill="#78350f"/>
  <rect x="435" y="200" width="18" height="120" fill="#78350f"/>
  <!-- Desk Lamp on Desk -->
  <ellipse cx="220" cy="178" rx="25" ry="6" fill="#334155"/>
  <path d="M 220 178 Q 210 120 250 100" stroke="#334155" stroke-width="6" fill="none"/>
  <polygon points="240,85 270,110 230,115" fill="#f59e0b"/>
  <!-- Cardboard Box Under Desk -->
  <rect x="260" y="240" width="90" height="70" rx="4" fill="#d97706" stroke="#92400e" stroke-width="2"/>
  <line x1="260" y1="265" x2="350" y2="265" stroke="#92400e" stroke-width="2"/>
  <rect x="20" y="340" width="560" height="45" rx="6" fill="#0f172a" opacity="0.9"/>
  <text x="300" y="367" font-family="system-ui, sans-serif" font-size="14" font-weight="bold" fill="#f8fafc" text-anchor="middle">CH02-L02-Q02: Desk lamp on table, cardboard box underneath</text>
</svg>"""
    },
    "ch02-l02-q03.svg": {
        "title": "Row of Chairs along the wall",
        "brief": "Một hàng ghế được xếp dọc theo bức tường trong phòng chờ.",
        "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 400" width="100%" height="100%">
  <rect width="600" height="400" fill="#f1f5f9"/>
  <rect y="280" width="600" height="120" fill="#cbd5e1"/>
  <!-- Wall line -->
  <line x1="0" y1="280" x2="600" y2="280" stroke="#94a3b8" stroke-width="3"/>
  <!-- Row of chairs -->
  <!-- Chair 1 -->
  <rect x="70" y="180" width="90" height="60" rx="6" fill="#2563eb"/>
  <rect x="70" y="235" width="90" height="12" rx="3" fill="#1d4ed8"/>
  <rect x="80" y="247" width="8" height="55" fill="#334155"/>
  <rect x="142" y="247" width="8" height="55" fill="#334155"/>
  <!-- Chair 2 -->
  <rect x="190" y="180" width="90" height="60" rx="6" fill="#2563eb"/>
  <rect x="190" y="235" width="90" height="12" rx="3" fill="#1d4ed8"/>
  <rect x="200" y="247" width="8" height="55" fill="#334155"/>
  <rect x="262" y="247" width="8" height="55" fill="#334155"/>
  <!-- Chair 3 -->
  <rect x="310" y="180" width="90" height="60" rx="6" fill="#2563eb"/>
  <rect x="310" y="235" width="90" height="12" rx="3" fill="#1d4ed8"/>
  <rect x="320" y="247" width="8" height="55" fill="#334155"/>
  <rect x="382" y="247" width="8" height="55" fill="#334155"/>
  <!-- Chair 4 -->
  <rect x="430" y="180" width="90" height="60" rx="6" fill="#2563eb"/>
  <rect x="430" y="235" width="90" height="12" rx="3" fill="#1d4ed8"/>
  <rect x="440" y="247" width="8" height="55" fill="#334155"/>
  <rect x="502" y="247" width="8" height="55" fill="#334155"/>
  <rect x="20" y="340" width="560" height="45" rx="6" fill="#0f172a" opacity="0.9"/>
  <text x="300" y="367" font-family="system-ui, sans-serif" font-size="14" font-weight="bold" fill="#f8fafc" text-anchor="middle">CH02-L02-Q03: Row of chairs arranged along the wall</text>
</svg>"""
    },
    "ch02-l02-q04.svg": {
        "title": "Reception desk opposite elevator",
        "brief": "Một quầy tiếp tân nằm đối diện cửa thang máy; trên quầy có một chậu cây nhỏ và điện thoại để bàn.",
        "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 400" width="100%" height="100%">
  <rect width="600" height="400" fill="#f8fafc"/>
  <rect y="300" width="600" height="100" fill="#e2e8f0"/>
  <!-- Elevator in background -->
  <rect x="80" y="70" width="140" height="230" fill="#cbd5e1" stroke="#64748b" stroke-width="4"/>
  <line x1="150" y1="70" x2="150" y2="300" stroke="#64748b" stroke-width="3"/>
  <polygon points="140,55 150,45 160,55" fill="#0284c7"/>
  <!-- Reception desk -->
  <rect x="300" y="190" width="240" height="110" rx="6" fill="#0284c7"/>
  <rect x="290" y="180" width="260" height="15" rx="3" fill="#0369a1"/>
  <!-- Plant pot on desk -->
  <rect x="330" y="150" width="25" height="30" fill="#b45309"/>
  <circle cx="342" cy="140" r="15" fill="#16a34a"/>
  <!-- Desk phone -->
  <rect x="420" y="155" width="35" height="25" rx="3" fill="#1e293b"/>
  <rect x="20" y="340" width="560" height="45" rx="6" fill="#0f172a" opacity="0.9"/>
  <text x="300" y="367" font-family="system-ui, sans-serif" font-size="14" font-weight="bold" fill="#f8fafc" text-anchor="middle">CH02-L02-Q04: Reception counter opposite elevator doors</text>
</svg>"""
    },
    "ch02-l03-q01.svg": {
        "title": "Staff arranging chairs in conference hall",
        "brief": "Một nhân viên đang xếp các chiếc ghế thành hàng trong phòng hội nghị.",
        "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 400" width="100%" height="100%">
  <rect width="600" height="400" fill="#f1f5f9"/>
  <rect y="290" width="600" height="110" fill="#cbd5e1"/>
  <!-- Rows of chairs -->
  <rect x="60" y="210" width="60" height="50" fill="#3b82f6" rx="4"/>
  <rect x="140" y="210" width="60" height="50" fill="#3b82f6" rx="4"/>
  <rect x="220" y="210" width="60" height="50" fill="#3b82f6" rx="4"/>
  <!-- Staff arranging a chair -->
  <rect x="430" y="215" width="60" height="50" fill="#60a5fa" rx="4"/>
  <!-- Person -->
  <rect x="360" y="220" width="16" height="90" fill="#1e293b"/>
  <rect x="385" y="220" width="16" height="90" fill="#1e293b"/>
  <polygon points="350,150 405,150 400,220 355,220" fill="#d97706"/>
  <circle cx="375" cy="120" r="20" fill="#fed7aa"/>
  <!-- Hands holding chair -->
  <path d="M 375 160 L 430 215" stroke="#fed7aa" stroke-width="8" stroke-linecap="round"/>
  <rect x="20" y="340" width="560" height="45" rx="6" fill="#0f172a" opacity="0.9"/>
  <text x="300" y="367" font-family="system-ui, sans-serif" font-size="14" font-weight="bold" fill="#f8fafc" text-anchor="middle">CH02-L03-Q01: Staff member arranging chairs in meeting hall</text>
</svg>"""
    },
    "ch02-l03-q02.svg": {
        "title": "Clean Glass Windows Reflecting Sky",
        "brief": "Các cửa sổ kính lớn của một tòa nhà sạch, phản chiếu bầu trời; không có người trong ảnh.",
        "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 400" width="100%" height="100%">
  <rect width="600" height="400" fill="#e2e8f0"/>
  <!-- Glass Windows grid reflecting blue sky -->
  <rect x="40" y="40" width="160" height="260" fill="#38bdf8" stroke="#0284c7" stroke-width="6"/>
  <rect x="220" y="40" width="160" height="260" fill="#7dd3fc" stroke="#0284c7" stroke-width="6"/>
  <rect x="400" y="40" width="160" height="260" fill="#38bdf8" stroke="#0284c7" stroke-width="6"/>
  <!-- Sky reflection highlights -->
  <polygon points="50,60 180,60 120,180 50,180" fill="#ffffff" opacity="0.3"/>
  <polygon points="230,60 360,60 300,180 230,180" fill="#ffffff" opacity="0.3"/>
  <polygon points="410,60 540,60 480,180 410,180" fill="#ffffff" opacity="0.3"/>
  <rect x="20" y="340" width="560" height="45" rx="6" fill="#0f172a" opacity="0.9"/>
  <text x="300" y="367" font-family="system-ui, sans-serif" font-size="14" font-weight="bold" fill="#f8fafc" text-anchor="middle">CH02-L03-Q02: Large glass building windows reflecting sky (no people)</text>
</svg>"""
    },
    "ch02-l03-q03.svg": {
        "title": "Boxes Stacked Near Warehouse Door",
        "brief": "Các thùng hàng được xếp thành chồng gần cửa kho; không có nhân viên trong khung hình.",
        "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 400" width="100%" height="100%">
  <rect width="600" height="400" fill="#cbd5e1"/>
  <!-- Warehouse Roller Door on left -->
  <rect x="50" y="40" width="220" height="280" fill="#94a3b8" stroke="#475569" stroke-width="4"/>
  <line x1="50" y1="90" x2="270" y2="90" stroke="#64748b" stroke-width="2"/>
  <line x1="50" y1="140" x2="270" y2="140" stroke="#64748b" stroke-width="2"/>
  <line x1="50" y1="190" x2="270" y2="190" stroke="#64748b" stroke-width="2"/>
  <line x1="50" y1="240" x2="270" y2="240" stroke="#64748b" stroke-width="2"/>
  <!-- Stacks of Boxes -->
  <!-- Bottom row -->
  <rect x="310" y="240" width="80" height="70" fill="#b45309" stroke="#78350f" stroke-width="2"/>
  <rect x="400" y="240" width="80" height="70" fill="#d97706" stroke="#78350f" stroke-width="2"/>
  <rect x="490" y="240" width="80" height="70" fill="#b45309" stroke="#78350f" stroke-width="2"/>
  <!-- Middle row -->
  <rect x="350" y="170" width="80" height="70" fill="#d97706" stroke="#78350f" stroke-width="2"/>
  <rect x="440" y="170" width="80" height="70" fill="#b45309" stroke="#78350f" stroke-width="2"/>
  <!-- Top box -->
  <rect x="390" y="100" width="80" height="70" fill="#d97706" stroke="#78350f" stroke-width="2"/>
  <rect x="20" y="340" width="560" height="45" rx="6" fill="#0f172a" opacity="0.9"/>
  <text x="300" y="367" font-family="system-ui, sans-serif" font-size="14" font-weight="bold" fill="#f8fafc" text-anchor="middle">CH02-L03-Q03: Cargo boxes stacked near warehouse door (unattended)</text>
</svg>"""
    },
    "ch02-l03-q04.svg": {
        "title": "Man inspecting front wheel of bicycle",
        "brief": "Một người đàn ông đứng cạnh một chiếc xe đạp, tay đang kiểm tra bánh trước; xe đạp dựng bằng chân chống bên lề đường.",
        "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 400" width="100%" height="100%">
  <rect width="600" height="400" fill="#f8fafc"/>
  <rect y="290" width="600" height="110" fill="#94a3b8"/>
  <!-- Bicycle -->
  <circle cx="170" cy="260" r="45" fill="none" stroke="#334155" stroke-width="6"/>
  <circle cx="340" cy="260" r="45" fill="none" stroke="#334155" stroke-width="6"/>
  <!-- Bike Frame -->
  <polygon points="170,260 250,260 290,190 220,190" fill="none" stroke="#dc2626" stroke-width="6"/>
  <line x1="250" y1="260" x2="340" y2="260" stroke="#dc2626" stroke-width="6"/>
  <line x1="340" y1="260" x2="330" y2="170" stroke="#334155" stroke-width="6"/>
  <!-- Man inspecting front wheel -->
  <polygon points="380,240 430,240 420,310 370,310" fill="#1e293b"/>
  <ellipse cx="400" cy="200" rx="20" ry="30" fill="#0284c7"/>
  <circle cx="410" cy="150" r="18" fill="#fed7aa"/>
  <!-- Hand inspecting wheel -->
  <path d="M 400 200 L 345 250" stroke="#fed7aa" stroke-width="7" stroke-linecap="round"/>
  <rect x="20" y="340" width="560" height="45" rx="6" fill="#0f172a" opacity="0.9"/>
  <text x="300" y="367" font-family="system-ui, sans-serif" font-size="14" font-weight="bold" fill="#f8fafc" text-anchor="middle">CH02-L03-Q04: Man inspecting front wheel of bicycle by street</text>
</svg>"""
    },
    "ch02-final-q01.svg": {
        "title": "Placing folders onto bookshelf",
        "brief": "Một nhân viên đang đặt các tập hồ sơ lên giá sách trong văn phòng.",
        "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 400" width="100%" height="100%">
  <rect width="600" height="400" fill="#f1f5f9"/>
  <!-- Bookshelf -->
  <rect x="60" y="40" width="220" height="280" fill="#94a3b8" stroke="#475569" stroke-width="5"/>
  <line x1="60" y1="120" x2="280" y2="120" stroke="#475569" stroke-width="5"/>
  <line x1="60" y1="200" x2="280" y2="200" stroke="#475569" stroke-width="5"/>
  <!-- Folders on shelf -->
  <rect x="75" y="55" width="20" height="60" fill="#2563eb"/>
  <rect x="100" y="55" width="20" height="60" fill="#dc2626"/>
  <rect x="125" y="55" width="20" height="60" fill="#16a34a"/>
  <!-- Person placing folder -->
  <rect x="360" y="210" width="18" height="110" fill="#1e293b"/>
  <rect x="390" y="210" width="18" height="110" fill="#1e293b"/>
  <polygon points="350,130 420,130 410,210 355,210" fill="#0284c7"/>
  <circle cx="385" cy="100" r="22" fill="#fed7aa"/>
  <!-- Arm placing folder -->
  <path d="M 370 145 L 250 140" stroke="#fed7aa" stroke-width="9" stroke-linecap="round"/>
  <rect x="230" y="130" width="20" height="65" fill="#f59e0b" transform="rotate(10 230 130)"/>
  <rect x="20" y="340" width="560" height="45" rx="6" fill="#0f172a" opacity="0.9"/>
  <text x="300" y="367" font-family="system-ui, sans-serif" font-size="14" font-weight="bold" fill="#f8fafc" text-anchor="middle">CH02-FINAL-Q01: Staff placing folders onto office bookshelf</text>
</svg>"""
    },
    "ch02-final-q02.svg": {
        "title": "Bicycle parked against fence",
        "brief": "Một chiếc xe đạp dựng cạnh hàng rào kim loại trong công viên.",
        "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 400" width="100%" height="100%">
  <rect width="600" height="400" fill="#ecfdf5"/>
  <rect y="280" width="600" height="120" fill="#a7f3d0"/>
  <!-- Metal fence -->
  <line x1="50" y1="120" x2="550" y2="120" stroke="#64748b" stroke-width="4"/>
  <line x1="50" y1="200" x2="550" y2="200" stroke="#64748b" stroke-width="4"/>
  <!-- Vertical pickets -->
  <line x1="100" y1="90" x2="100" y2="280" stroke="#64748b" stroke-width="3"/>
  <line x1="200" y1="90" x2="200" y2="280" stroke="#64748b" stroke-width="3"/>
  <line x1="300" y1="90" x2="300" y2="280" stroke="#64748b" stroke-width="3"/>
  <line x1="400" y1="90" x2="400" y2="280" stroke="#64748b" stroke-width="3"/>
  <line x1="500" y1="90" x2="500" y2="280" stroke="#64748b" stroke-width="3"/>
  <!-- Bicycle parked against fence -->
  <circle cx="230" cy="260" r="45" fill="none" stroke="#1e293b" stroke-width="6"/>
  <circle cx="390" cy="260" r="45" fill="none" stroke="#1e293b" stroke-width="6"/>
  <polygon points="230,260 310,260 350,190 280,190" fill="none" stroke="#2563eb" stroke-width="6"/>
  <rect x="20" y="340" width="560" height="45" rx="6" fill="#0f172a" opacity="0.9"/>
  <text x="300" y="367" font-family="system-ui, sans-serif" font-size="14" font-weight="bold" fill="#f8fafc" text-anchor="middle">CH02-FINAL-Q02: Bicycle parked beside metal fence in park</text>
</svg>"""
    },
    "ch02-final-q03.svg": {
        "title": "Waiter carrying tray with glasses",
        "brief": "Một người phục vụ đang mang khay có hai cốc nước đến bàn khách.",
        "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 400" width="100%" height="100%">
  <rect width="600" height="400" fill="#fdf4ff"/>
  <rect y="310" width="600" height="90" fill="#f3e8ff"/>
  <!-- Waiter -->
  <rect x="180" y="220" width="16" height="100" fill="#1e293b"/>
  <rect x="205" y="220" width="16" height="100" fill="#1e293b"/>
  <polygon points="170,140 230,140 225,220 175,220" fill="#475569"/>
  <polygon points="195,140 205,140 200,165" fill="#ffffff"/>
  <circle cx="200" cy="110" r="22" fill="#fed7aa"/>
  <!-- Arm carrying tray -->
  <path d="M 215 155 Q 260 160 290 150" stroke="#fed7aa" stroke-width="9" stroke-linecap="round" fill="none"/>
  <!-- Tray with two water glasses -->
  <rect x="280" y="145" width="80" height="8" rx="2" fill="#0f172a"/>
  <rect x="300" y="125" width="14" height="20" rx="2" fill="#38bdf8"/>
  <rect x="330" y="125" width="14" height="20" rx="2" fill="#38bdf8"/>
  <!-- Customer table in background -->
  <rect x="420" y="240" width="120" height="15" fill="#b45309"/>
  <rect x="475" y="255" width="12" height="65" fill="#78350f"/>
  <rect x="20" y="340" width="560" height="45" rx="6" fill="#0f172a" opacity="0.9"/>
  <text x="300" y="367" font-family="system-ui, sans-serif" font-size="14" font-weight="bold" fill="#f8fafc" text-anchor="middle">CH02-FINAL-Q03: Waiter carrying tray with two glasses to table</text>
</svg>"""
    },
    "ch02-final-q04.svg": {
        "title": "Boxes stored under long table",
        "brief": "Một số hộp được xếp gọn bên dưới một chiếc bàn dài.",
        "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 400" width="100%" height="100%">
  <rect width="600" height="400" fill="#f8fafc"/>
  <rect y="310" width="600" height="90" fill="#e2e8f0"/>
  <!-- Long table -->
  <rect x="60" y="170" width="480" height="20" rx="4" fill="#475569"/>
  <rect x="85" y="190" width="16" height="130" fill="#334155"/>
  <rect x="495" y="190" width="16" height="130" fill="#334155"/>
  <!-- Several boxes underneath -->
  <rect x="140" y="245" width="75" height="65" fill="#d97706" stroke="#92400e" stroke-width="2"/>
  <rect x="230" y="235" width="85" height="75" fill="#b45309" stroke="#78350f" stroke-width="2"/>
  <rect x="330" y="255" width="70" height="55" fill="#d97706" stroke="#92400e" stroke-width="2"/>
  <rect x="20" y="340" width="560" height="45" rx="6" fill="#0f172a" opacity="0.9"/>
  <text x="300" y="367" font-family="system-ui, sans-serif" font-size="14" font-weight="bold" fill="#f8fafc" text-anchor="middle">CH02-FINAL-Q04: Several storage boxes arranged under long table</text>
</svg>"""
    },
    "ch02-final-q05.svg": {
        "title": "Delivery truck parked at loading bay",
        "brief": "Một chiếc xe tải đang đậu trước cửa kho, cửa sau xe mở và có thùng hàng bên trong.",
        "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 400" width="100%" height="100%">
  <rect width="600" height="400" fill="#f1f5f9"/>
  <rect y="290" width="600" height="110" fill="#94a3b8"/>
  <!-- Warehouse wall -->
  <rect x="40" y="30" width="180" height="260" fill="#64748b"/>
  <!-- Delivery Truck -->
  <rect x="200" y="110" width="220" height="150" fill="#0284c7" stroke="#0369a1" stroke-width="3"/>
  <!-- Truck open rear door with boxes inside -->
  <rect x="205" y="120" width="70" height="130" fill="#0f172a"/>
  <rect x="215" y="190" width="40" height="40" fill="#d97706"/>
  <!-- Truck cab on right -->
  <polygon points="420,160 480,160 510,220 510,260 420,260" fill="#0369a1"/>
  <!-- Wheels -->
  <circle cx="260" cy="280" r="25" fill="#0f172a"/>
  <circle cx="460" cy="280" r="25" fill="#0f172a"/>
  <rect x="20" y="340" width="560" height="45" rx="6" fill="#0f172a" opacity="0.9"/>
  <text x="300" y="367" font-family="system-ui, sans-serif" font-size="14" font-weight="bold" fill="#f8fafc" text-anchor="middle">CH02-FINAL-Q05: Delivery truck parked at dock with rear open</text>
</svg>"""
    },
    "ch02-final-q06.svg": {
        "title": "Technician checking office photocopier",
        "brief": "Một kỹ thuật viên đang cúi xuống kiểm tra bảng điều khiển của máy photocopy trong văn phòng.",
        "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 400" width="100%" height="100%">
  <rect width="600" height="400" fill="#f8fafc"/>
  <rect y="310" width="600" height="90" fill="#e2e8f0"/>
  <!-- Photocopier / Multifunction printer -->
  <rect x="120" y="150" width="150" height="160" rx="6" fill="#475569" stroke="#334155" stroke-width="3"/>
  <rect x="140" y="125" width="110" height="25" fill="#64748b"/>
  <!-- Control panel -->
  <rect x="230" y="155" width="30" height="20" fill="#38bdf8"/>
  <!-- Technician leaning down -->
  <rect x="360" y="240" width="18" height="80" fill="#1e293b"/>
  <rect x="390" y="240" width="18" height="80" fill="#1e293b"/>
  <polygon points="320,180 380,150 400,210 340,240" fill="#ea580c"/>
  <circle cx="310" cy="160" r="20" fill="#fed7aa"/>
  <!-- Hand inspecting control panel -->
  <path d="M 310 180 L 265 165" stroke="#fed7aa" stroke-width="8" stroke-linecap="round"/>
  <rect x="20" y="340" width="560" height="45" rx="6" fill="#0f172a" opacity="0.9"/>
  <text x="300" y="367" font-family="system-ui, sans-serif" font-size="14" font-weight="bold" fill="#f8fafc" text-anchor="middle">CH02-FINAL-Q06: Technician leaning to inspect copier panel</text>
</svg>"""
    }
}

for fname, data in svgs.items():
    fpath = os.path.join(images_dir, fname)
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(data["svg"].strip())
    print(f"Generated {fpath}")

print(f"Successfully generated all {len(svgs)} Part 1 SVG illustrations!")
