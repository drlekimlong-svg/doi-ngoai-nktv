"""Đóng gói app Đối ngoại và sinh bản kế hoạch từ cùng một nguồn.

Nguồn:  nguon/ke-hoach.json  (khung đầu việc, các bảng, cấu hình app)
        nguon/app.src.html   (giao diện và mã)
Ra:     index.html                                       (app, một tệp, mở trực tiếp được)
        ../KE_HOACH_DOI_NGOAI_NAM_HOC_2026-2027.md       (bản kế hoạch để đọc và in)

Chạy:   python dong_goi.py
"""
import html
import io
import json
from datetime import date
from pathlib import Path

GOC = Path(__file__).resolve().parent
NGUON = GOC / "nguon"
THU = ["T2", "T3", "T4", "T5", "T6", "T7", "CN"]


def dmy(iso):
    return f"{iso[8:10]}/{iso[5:7]}/{iso[0:4]}" if iso else ""


def thu(iso):
    y, m, d = (int(x) for x in iso.split("-"))
    return THU[date(y, m, d).weekday()]


def o(s):
    return str(s or "").replace("|", "\\|").replace("\n", "<br>")


def dong_goi_app(seed_text, k):
    src = (NGUON / "app.src.html").read_text(encoding="utf-8")
    for cho in ("__SEED__", "__TIEU_DE__", "__PHU_DE__"):
        assert cho in src, f"Thiếu chỗ đặt {cho}"
    gon = json.dumps(json.loads(seed_text), ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    out = (src.replace("__TIEU_DE__", html.escape(k["app"]["tieuDe"]))
              .replace("__PHU_DE__", html.escape(k["app"]["phuDe"]))
              .replace("__SEED__", gon))
    io.open(GOC / "index.html", "w", encoding="utf-8", newline="\n").write(out)
    return len(out.encode("utf-8"))


def ban_ke_hoach(k):
    dv = k["dauViec"]
    so = {d["id"]: d["so"] for d in dv}
    bang = {b["id"]: b for b in k["bang"]}
    L = []
    a = L.append
    a(f"# KẾ HOẠCH ĐỐI NGOẠI NĂM HỌC {k['namHoc']}")
    a("")
    a(f"**Đơn vị:** {k['donVi']}  ")
    a(f"**Phiên bản khung:** {k['phienBan']}, lập ngày {dmy(k['ngayLap'])}  ")
    a("**Dùng cho:** cuộc họp triển khai kế hoạch Đối ngoại  ")
    a(f"**Trạng thái:** {k['trangThaiKhung']}")
    a("")
    a("Bản này sinh từ cùng nguồn dữ liệu với app (`app-doi-ngoai/`). Khi họp, ghi người phụ trách, hạn, chỉ tiêu và quyết định vào app rồi xuất biên bản; không cần điền tay vào bản này.")
    a("")
    a("## Cách đọc")
    a("")
    a("- **Việc cụ thể** là các việc đủ nhỏ để giao cho một người hoặc một nhà.")
    a(f"- **Hạn gợi ý** do agent đề xuất, tính từ ngày {dmy(k['ngayLap'])}, phần lớn đặt vào Chủ nhật. Ô để trống là việc phụ thuộc một mốc chưa có.")
    a("- **Cần chốt** là các câu hỏi nên có câu trả lời ngay trong cuộc họp.")
    a("- Mục 10 trong danh sách gốc gồm ba việc (Đường chạy truyền thống; quy chế đối ngoại; nhận diện các nhóm). Khung tách thành đầu việc 10, 11, 12 để giao người riêng.")
    a("- Ba đầu việc dùng chung **bảng chương trình** (1 timeline, 2 chỉ tiêu, 5 bản kế hoạch chuẩn). Trong app, bảng hiện ngay trong từng đầu việc và ở mục Chương trình, có timeline theo tháng.")
    a("")
    a(f"## Tổng quan {len(dv)} đầu việc")
    a("")
    a("| # | Đầu việc | Nhóm việc | Điều kiện khởi động | Mốc gợi ý đầu – cuối |")
    a("|---|---|---|---|---|")
    for d in dv:
        g = sorted(v["goiY"] for v in d["viec"] if v.get("goiY"))
        moc = f"{dmy(g[0])} – {dmy(g[-1])}" if g else ""
        a(f"| {d['so']} | {d['ten']} | {d['nhom']} | {d['dieuKien']} | {moc} |")
    a("")
    a("## Quan hệ giữa các việc")
    a("")
    for d in dv:
        if d.get("phuThuoc"):
            a(f"- Đầu việc {d['so']} ({d['ten']}) cần " + ", ".join(f"đầu việc {so[p]}" for p in d["phuThuoc"]) + ".")
    a("- Đầu việc 2 đặt chỉ tiêu trên danh sách chương trình của đầu việc 1; số thực tế sau mỗi chương trình nộp vào Hồ sơ năng lực CLB (đầu việc 6).")
    a("- Liên quan kế hoạch nội bộ (khung 1.0, 09/10/2026): đầu việc 5 dùng chung mẫu với Manual CLB (nội bộ 7) và tập huấn Junior (nội bộ 10); đầu việc 12 phối hợp với Mascot nhóm (nội bộ 1) và thẻ tên (nội bộ 3); quy chế ở đầu việc 11 đưa vào Manual CLB.")
    a("")
    a("## Căn cứ từ bộ kế hoạch 2025–2026")
    a("")
    a("Nguồn: thư mục `KẾ_HOẠCH_CLB/2025-2026/` (tài liệu nội bộ người dùng cung cấp ngày 12/10/2026). Số vé là số dự kiến bán trong kế hoạch, chưa phải số tham dự đã kiểm chứng.")
    a("")
    a("| Chương trình | Thời gian trong kế hoạch | Quy mô, vé |")
    a("|---|---|---|")
    a("| Kỹ năng khâu cơ bản 2025–2026 | Dự kiến 01/12–24/01; bán vé 24 và 26/12/2025; các buổi 06/01–24/01/2026 | 190 vé + 10 vé mời; early bird 65.000đ (50 vé), standard 80.000đ (140 vé); khoảng 60 học viên mỗi buổi thực hành, tối thiểu 22 tập huấn viên |")
    a("| X-quang bụng 2025–2026 | Dự kiến 16/03–05/04/2026 | 170 vé + 10 vé mời; early bird 65.000đ (40 vé), standard 80.000đ (130 vé); khoảng 60 học viên mỗi buổi |")
    a("| CT-scan bụng 2025–2026 | Bán vé 09–15/05/2026; học 19, 21, 26, 28/05/2026; lượng giá 02/06/2026 (kế hoạch tổ chức ghi 31/05/2026) | 80 vé + 5 vé mời, 100.000đ/vé; kế hoạch ghi 85 học viên thực tế; có quy định hoàn trả vé |")
    a("| Tuyển quân Gen12 (năm học này) | 14/10–22/11/2026; đóng form 26/10; phỏng vấn 14–15/11; buổi sinh hoạt đầu tiên của Junior 22/11 | Lịch truyền thông 9 bài fanpage, đã nạp vào bảng lịch đăng |")
    a("")
    a("## Căn cứ từ dữ liệu fanpage")
    a("")
    a("Nguồn: bộ dữ liệu Page cắt ngày 18/07/2026, trong bộ bàn giao 30/09/2026. Tháng nêu dưới đây là **tháng đăng bài**, không phải ngày tổ chức đã kiểm chứng. Nhãn chủ đề do bộ phân tích cũ gán, chưa phải danh mục CLB đã duyệt.")
    a("")
    a("- Tổng: 873 nội dung từ 22/03/2015 đến 08/07/2026. Follower hiển thị công khai 11K ngày 18/07/2026 (số làm tròn).")
    a("- 12 tháng trước ngày cắt: 115 nội dung. Theo nhãn chủ đề: Thông tin chung 42; Học thuật – đào tạo 28; Thành tựu – cột mốc 25; Tổng kết – recap 16; Sự kiện – cuộc thi 3; Tuyển thành viên 1.")
    a("- Số nội dung mỗi tháng trong 12 tháng đó dao động từ 1 (07/2025, 08/2025) đến 30 (05/2026); 02/2026 có 2. Bài dồn theo mùa chương trình và tuyển quân.")
    a("- Tháng đăng bài theo chương trình: xem cột căn cứ ở bảng chương trình (phụ lục A).")
    a("")
    a("## Điểm agent đề nghị lưu ý trước khi họp")
    a("")
    a("1. **Số follower.** 11K là số làm tròn hiển thị công khai ngày 18/07/2026. Cần lấy số chính xác từ Meta Business Suite trước khi đặt chỉ tiêu (việc 7.1).")
    a("2. **Chỉ tiêu học viên.** Số đang có chủ yếu là số vé dự kiến trong kế hoạch 2025–2026 (Khâu 190, X-quang 170, CT 80) và số của một mùa cụ thể (72 thí sinh Nhà Ngoại khoa trẻ mùa 3). Chưa có số tham dự và hoàn thành đã kiểm chứng; nên ghi rõ chỉ tiêu tính theo mức nào và giao người thu số thực tế sau mỗi chương trình.")
    a("3. **Bài giới thiệu các nhóm ngày 21/10/2026** trong lịch Tuyển quân Gen12 diễn ra trước khi bộ nhận diện ba cấp của các nhà được duyệt (kế hoạch nội bộ gợi ý duyệt 29/11). Cần chốt bài này dùng hình và mô tả nào (đầu việc 12).")
    a("4. **Bảng loại bài đăng** có 9 dòng là đề xuất của agent để thảo luận, không phải danh mục đang dùng.")
    a("5. **Đường chạy truyền thống – Kéo co:** hồ sơ chưa có dữ liệu về lần tham gia trước và thể lệ; việc đầu tiên là hỏi ban tổ chức giải.")
    a("6. **Ảnh và thông tin cá nhân trên fanpage:** bài về con người CLB, văn hóa nội bộ và recap cần xin phép người xuất hiện; bài học thuật không dùng thông tin hay hình ảnh nhận diện được người bệnh.")
    a("")
    for d in dv:
        a("---")
        a("")
        a(f"## {d['so']}. {d['ten']}")
        a("")
        a(f"**Nhóm việc:** {d['nhom']}  ")
        a(f"**Điều kiện khởi động:** {d['dieuKien']}")
        a("")
        a(f"**Mục tiêu.** {d['mucTieu']}")
        a("")
        if d.get("boiCanh"):
            a(f"**Đã có, cần biết.** {d['boiCanh']}")
            a("")
        if d.get("lienQuan"):
            a("**Liên quan:** " + ", ".join(f"đầu việc {so[x]}" for x in d["lienQuan"]) + ".")
            a("")
        if d.get("bang"):
            a("**Dùng bảng:** " + ", ".join(bang[x]["ten"] for x in d["bang"]) + " (xem phụ lục và app).")
            a("")
        a("**Sản phẩm đầu ra**")
        a("")
        for s in d["sanPham"]:
            a(f"- {s}")
        a("")
        a("**Việc cụ thể để phân công**")
        a("")
        a("| # | Việc | Hạn gợi ý | Phụ trách | Hạn chốt |")
        a("|---|---|---|---|---|")
        for i, v in enumerate(d["viec"], 1):
            g = f"{thu(v['goiY'])} {dmy(v['goiY'])}" if v.get("goiY") else (v.get("luuY") or "")
            a(f"| {d['so']}.{i} | {v['ten']} | {g} | | |")
        a("")
        a("**Cần chốt tại cuộc họp**")
        a("")
        for i, c in enumerate(d["canChot"], 1):
            a(f"{i}. {c}")
        a("")
        if d.get("theoNha"):
            a("**Theo dõi theo từng nhà:** " + "; ".join(d["theoNha"]) + ".")
            a("")
    a("---")
    a("")
    a("## Phụ lục. Các bảng trong app")
    for chu, b in zip("ABCDEFGH", k["bang"]):
        a("")
        a(f"### {chu}. {b['ten']}")
        a("")
        a(b.get("moTa", ""))
        a("")
        a("Các cột: " + "; ".join(c["nhan"] for c in b["cot"]) + ".")
        a("")
        if b.get("dong"):
            C = [c for c in b["cot"] if any(str(r.get(c["k"]) or "").strip() for r in b["dong"])]
            dep = lambda c, v: (f"{v[5:7]}/{v[:4]}" if c["kieu"] == "month" and v else dmy(v) if c["kieu"] == "date" and v else v)
            a("| " + " | ".join(c["nhan"] for c in C) + " |")
            a("|" + "---|" * len(C))
            for r in b["dong"]:
                a("| " + " | ".join(o(dep(c, r.get(c["k"]) or "")) for c in C) + " |")
            a("")
            a("Các ô có sẵn trong bảng lấy từ nguồn nêu ở phần căn cứ, hoặc là đề xuất của agent (bảng loại bài).")
        else:
            a("Bảng để trống, điền tại cuộc họp.")
    a("")
    a("## Lịch mốc gợi ý theo tháng")
    moc = sorted((v["goiY"], d["so"], i, v["ten"]) for d in dv for i, v in enumerate(d["viec"], 1) if v.get("goiY"))
    thang = ""
    for ngay, s, i, ten in moc:
        if ngay[:7] != thang:
            thang = ngay[:7]
            a("")
            a(f"### Tháng {thang[5:]}/{thang[:4]}")
            a("")
        a(f"- {thu(ngay)} {ngay[8:]}/{ngay[5:7]} · {s}.{i} {ten}")
    a("")
    a("## Lịch sử cập nhật")
    a("")
    a(f"- {dmy(k['ngayLap'])}: Lập khung bản 1.0 theo các vấn đề đối ngoại người dùng nêu; mục 10 tách thành ba đầu việc. Mục tiêu, việc cụ thể, câu cần chốt, hạn gợi ý và bảng loại bài là đề xuất của agent; căn cứ fanpage lấy từ dữ liệu Page cắt 18/07/2026.")
    for dong_ls in k.get("lichSu", []):
        a(f"- {dong_ls}")
    a("")
    return "\n".join(L)


def main():
    seed_text = (NGUON / "ke-hoach.json").read_text(encoding="utf-8")
    k = json.loads(seed_text)
    ids = [v["id"] for d in k["dauViec"] for v in d["viec"]]
    assert len(ids) == len(set(ids)), "Trùng mã việc"
    bang_ids = {b["id"] for b in k["bang"]}
    for d in k["dauViec"]:
        for p in d.get("phuThuoc", []) + d.get("lienQuan", []):
            assert any(x["id"] == p for x in k["dauViec"]), f"{d['id']} trỏ tới {p} không tồn tại"
        for b in d.get("bang", []):
            assert b in bang_ids, f"{d['id']} dùng bảng {b} không tồn tại"
    for b in k["bang"]:
        keys = {c["k"] for c in b["cot"]}
        for cfg in ("timeline", "lich"):
            if b.get(cfg):
                for kk, vv in b[cfg].items():
                    for x in (vv if isinstance(vv, list) else [vv]):
                        if kk != "nhan" or cfg == "timeline":
                            assert x in keys, f"{b['id']}.{cfg}.{kk} trỏ tới cột {x} không có"
    kb = dong_goi_app(seed_text, k)
    md = ban_ke_hoach(k)
    ten = f"KE_HOACH_DOI_NGOAI_NAM_HOC_{k['namHoc'].replace('–', '-')}.md"
    io.open(GOC.parent / ten, "w", encoding="utf-8", newline="\n").write(md)
    print(f"index.html: {kb / 1024:.0f} KB · {len(k['dauViec'])} đầu việc · {len(ids)} việc cụ thể · {len(k['bang'])} bảng · {ten}")


if __name__ == "__main__":
    main()
