# personal-wiki-hub

Kho kiến thức cá nhân được duy trì bởi LLM, theo mô hình [Karpathy LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) và mở rộng với các pattern từ [agentmemory](https://gist.github.com/rohitg00/2067ab416f7bbe447c1977edaaa681e2). Thiết kế cho Claude Code với Obsidian làm giao diện người dùng.

## Bắt đầu nhanh

```bash
# Kiểm tra cấu trúc vault
/wiki:setup --verify

# Thu thập và xử lý nguồn trong một bước
/wiki:capture https://example.com/article --ingest

# Duyệt nội dung wiki
/wiki:browse

# Hỏi wiki một câu hỏi
/wiki:query "Mô hình Karpathy LLM wiki là gì?"

# Kiểm tra tình trạng
/wiki:status
```

**Lần đầu?** Xem [INSTALLATION.md](INSTALLATION.md) để hướng dẫn cài đặt chi tiết.

## Kiến trúc

```
personal-wiki-hub/
├── raw/               # Nguồn bên ngoài (bất biến, người dùng thả vào)
│   ├── assets/        # Hình ảnh đính kèm
│   └── archive/       # Mục chưa xử lý >30 ngày
├── wiki/              # Kiến thức do LLM duy trì (tự động tạo)
│   ├── assets/        # Sơ đồ do LLM tạo
│   ├── meta/          # Dashboard, anti-patterns
│   ├── index.md       # Danh mục nội dung
│   ├── log.md         # Nhật ký hoạt động (prepend, mới nhất trước)
│   ├── hot.md         # Cache ngữ cảnh gần đây (<500 từ)
│   └── backlog.md     # Khái niệm đang chờ xử lý
├── notes/             # Suy nghĩ của người dùng (LLM chỉ đọc)
│   ├── daily/         # Nhật ký hàng ngày
│   ├── fleeting/      # Ghi chép nhanh, inbox
│   ├── reviews/       # Ghi chú đánh giá tuần
│   └── assets/        # Sơ đồ cá nhân
├── outputs/           # Artifacts do LLM tạo (câu trả lời, báo cáo, nghiên cứu)
├── projects/          # Kiến thức theo dự án
├── content/           # Bản nháp blog
├── sessions/          # Nhật ký phiên Claude Code
├── templates/         # Mẫu frontmatter
├── .claude/
│   ├── agents/        # wiki-* subagents (5)
│   ├── skills/        # wiki-* skills (12)
│   └── settings.json  # Hooks (hot cache, auto-commit)
├── bin/
│   └── setup-vault.sh # Script bootstrap Obsidian
└── CLAUDE.md          # Quản lý schema
```

**Chi tiết đầy đủ:** Xem [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)

---

## Tham chiếu Skills (12 skills)

**Vị trí:** `.claude/skills/wiki-*` (trong dự án)

| Skill | Mô tả |
|-------|-------|
| `/wiki:capture` | Thu thập nguồn bên ngoài (URL, PDF, clipboard) |
| `/wiki:ingest` | Xử lý nguồn thành các trang wiki |
| `/wiki:autoresearch` | Nghiên cứu web lặp lại với fact-check |
| `/wiki:query` | Tìm kiếm và trả lời từ wiki |
| `/wiki:browse` | Duyệt nội dung wiki |
| `/wiki:synthesize` | Phân tích đa trang, tìm connections |
| `/wiki:audit` | Kiểm tra sức khỏe vault |
| `/wiki:refresh` | Cập nhật trang cũ |
| `/wiki:index` | Xây dựng lại danh mục |
| `/wiki:link` | Thêm cross-links còn thiếu |
| `/wiki:setup` | Khởi tạo/xác minh vault |
| `/wiki:status` | Hiển thị metrics dashboard |

---

## Agents (5)

| Agent | Vai trò |
|-------|---------|
| `wiki-ingestor` | Trích xuất raw/ → wiki/ với theo dõi provenance |
| `wiki-librarian` | Tìm kiếm + trả lời với progressive disclosure |
| `wiki-synthesizer` | Phân tích đa trang, tối thiểu 3 nguồn |
| `wiki-auditor` | Kiểm tra sức khỏe, phát hiện hash drift |
| `wiki-crystallizer` | Trích xuất insights từ sessions/ |

---

## Schema Frontmatter

```yaml
---
title: Tiêu đề trang
type: summary | entity | concept | comparison | query-result | insight | decision
status: draft | active | stale | superseded
sources: [tên-file-nguồn.md, ...]
source_hashes: { tên-file-nguồn.md: "sha256-8-ký-tự-đầu" }
created: YYYY-MM-DD
updated: YYYY-MM-DD
confidence: low | medium | high
last_queried: YYYY-MM-DD
tags: [luôn-dùng-kebab-case-tiếng-anh]
---
```

### Mô tả loại trang

| Type | Mô tả |
|------|-------|
| `summary` | Tổng quan về nguồn hoặc chủ đề |
| `entity` | Công cụ, dự án, người, tổ chức cụ thể |
| `concept` | Pattern, nguyên tắc, kỹ thuật |
| `comparison` | So sánh có cấu trúc X vs Y |
| `query-result` | Câu trả lời được promote từ outputs/ |
| `insight` | Bài học rút ra từ sessions, debugging |
| `decision` | Ghi lại các quan điểm mâu thuẫn + giải quyết |

---

## Workflows Thường dùng

### Thêm kiến thức từ nguồn mới
```bash
/wiki:capture https://example.com/article --ingest
```

### Nghiên cứu từ kiến thức có sẵn
```bash
/wiki:browse --search "orchestration"
/wiki:query "X so sánh với Y như thế nào?" --deep --save
```

### Bảo trì hàng tuần
```bash
/wiki:status                    # Kiểm tra metrics
/wiki:audit --fix               # Sửa các vấn đề an toàn
/wiki:refresh --stale 60        # Cập nhật trang cũ
/wiki:link                      # Thêm cross-links
/wiki:index --full              # Xây dựng lại danh mục

# Graph + Backlog review
"compile this week"             # Xử lý raw/ files từ 7 ngày qua
"analyze graph health"          # Báo cáo orphans, hubs, clusters
"review backlog"                # Xử lý wiki/backlog.md
```

---

## Quy tắc Sở hữu

| Thư mục | Người viết | Người đọc | Ghi chú |
|---------|------------|-----------|---------|
| `raw/` | Người dùng | LLM | Bất biến sau khi thả |
| `wiki/` | **LLM** | Cả hai | Dẫn xuất từ raw/ + notes/ |
| `notes/` | **Người dùng** | Cả hai | LLM audit, không sửa đổi |
| `outputs/` | LLM | Cả hai | Có thể promote lên wiki/ |
| `projects/` | LLM compile | Cả hai | Từ codebases + sessions |
| `sessions/` | Auto-export | LLM | Chỉ đọc cho LLM |

---

## Trigger Phrases

| Cụm từ | Hoạt động |
|--------|-----------|
| `"ingest [file]"` | raw/ → wiki/ |
| `"compile this week"` | Xử lý raw/ gần đây |
| `"compile [project]"` | Cập nhật kiến thức dự án |
| `"crystallize [session]"` | Trích xuất insights từ session |
| `"query [question]"` | Tìm kiếm + trả lời |
| `"audit vault"` | Kiểm tra sức khỏe |
| `"analyze graph health"` | Phân tích graph Obsidian |
| `"refresh [page]"` | Cập nhật trang wiki |
| `"review backlog"` | Xử lý khái niệm pending |

---

## Tính năng v2

### Staleness nhận biết query
Các trang có `last_queried:` trong 30 ngày được miễn đánh dấu stale, ngay cả khi `updated:` đã >60 ngày.

### Theo dõi Supersession
Khi trang thay thế trang khác: đặt `superseded_by:` trên trang cũ, `supersedes:` trên trang mới. Hai chiều — auditor kiểm tra cả hai phía.

### Crystallization pipeline
Trích xuất kiến thức tái sử dụng từ nhật ký phiên Claude Code:
```
sessions/ → wiki-crystallizer → wiki/ (type: insight) + projects/*/knowledge/
```

### Graph Health
Trigger: `"analyze graph health"` — tạo báo cáo về:
- Trang orphan (không có inbound links)
- Trang hub (>10 inbound links)
- Clusters cô lập cần bridge concepts

### Concept Backlog
Cách tiếp cận hybrid — không tạo stub rỗng, nhưng theo dõi concepts:
- Concepts có ≥3 mentions → tạo trang wiki ngay
- Concepts có <3 mentions → thêm vào `wiki/backlog.md`
