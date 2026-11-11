# HƯỚNG DẪN GÁN NHÃN DỮ LIỆU (ANNOTATION GUIDELINE)

**Dự án:** ReviewGuard VN: Detecting Deceptive Reviews and Suspicious Review Patterns in Vietnamese E-Commerce
**Phiên bản Taxonomy:** v2.0 (Tích hợp Đa phương thức, AI-generated, và Cấp độ cụm)
**Đối tượng sử dụng:** Nhóm nghiên cứu & Chuyên viên gán nhãn (Annotators)

## 1. Mục đích
Tài liệu này cung cấp định nghĩa, quy tắc định lượng và ví dụ nhằm chuẩn hóa quá trình gán nhãn cho tập dữ liệu trên sàn TMĐT Việt Nam. Mục tiêu là đạt hệ số đồng thuận $\kappa \ge 0.75$, phục vụ huấn luyện mô hình kết hợp Text-Image và Phân tích Cụm.

## 2. Hệ thống Nhãn Phân loại Cấp độ Đơn dòng (Review-level Taxonomy)

Mỗi đánh giá được phân tích dựa trên **Hình ảnh đính kèm** và **Nội dung văn bản** để ra 1 nhãn duy nhất.

### 2.1. Trustworthy (Đáng tin cậy)
* **Định nghĩa:** Phản ánh trải nghiệm thực tế. Hình/video tự quay chụp thật, ánh sáng tự nhiên.
* **Ví dụ:** *"Vải mát, form chuẩn, đường may không bị lỗi."* + Ảnh mặc áo thật.

### 2.2. Deceptive / Fake (Đánh giá bịa đặt / Seeding / AI-generated)
* **Định nghĩa:** Không có trải nghiệm thực. Đánh giá được thuê (seeding) hoặc do bot/AI tạo ra.
* **Dấu hiệu AI-generated (Mới):** Văn phong quá mượt mà, đúng ngữ pháp 100%, không có teencode, cấu trúc câu chia ý rõ ràng (vd: "Tóm lại,...", "Nhìn chung,..."), thái độ tích cực máy móc.
* **Dấu hiệu Hình ảnh:** Dùng y hệt ảnh quảng cáo của shop, ảnh stock trên mạng.

### 2.3. Spam / Advertising (Rác / Quảng cáo)
* **Định nghĩa:** Chứa thông tin quảng cáo, lôi kéo ra ngoài sàn.
* **Dấu hiệu:** Chứa banner quảng cáo, mã QR, link affiliate, SĐT vay vốn/tuyển dụng.

### 2.4. Off-topic (Lạc đề / Cày xu)
* **Định nghĩa:** Nội dung/Hình ảnh không liên quan đến sản phẩm để lách luật nhận xu.
* **Dấu hiệu:** Copy lời bài hát, công thức nấu ăn, ảnh màn hình đen, ảnh meme, ảnh idol.

### 2.5. Misleading / Manipulative (Gây hiểu lầm / Thao túng)
* **Định nghĩa:** Sự mâu thuẫn giữa Văn bản - Số sao, hoặc Văn bản - Hình ảnh.
* **Đào sâu Mâu thuẫn Đa phương thức (Cross-modal Contradiction):**
  * *Mâu thuẫn Thuộc tính (Attribute Mismatch):* Text viết "Màu xanh dương đẹp", ảnh chụp "Màu đỏ".
  * *Mâu thuẫn Thực thể (Entity Mismatch):* Text khen "Tai nghe nghe êm", ảnh chụp là "Cáp sạc".

---

## 3. Định lượng hóa các Khái niệm (Quantitative Thresholds)

Bảng quy tắc định lượng này giúp giải quyết dứt điểm các tranh cãi giữa trạng thái "Off-topic", "Nghèo nàn" và các nhãn khác.

```text
QUY TẮC ĐỊNH LƯỢNG VÀ PHÂN LOẠI VĂN BẢN/HÌNH ẢNH

1. ĐỊNH LƯỢNG VĂN BẢN RỖNG / NGHÈO NÀN (POOR TEXT):
   - Tiêu chí: Dưới 15 ký tự VÀ không tạo thành từ ngữ có nghĩa (vd: "hgdksj", "abcd", ".").
   - Xử lý: 
     + Nếu Ảnh Thật/Hợp lệ -> Nhãn: TRUSTWORTHY (Người dùng lười gõ chữ, nhưng ảnh thật).
     + Nếu Ảnh Rác/Không liên quan -> Nhãn: OFF-TOPIC.
     + Nếu Không có Ảnh -> Nhãn: UNCERTAIN (Bỏ qua mẫu này trong tập train, hoặc gán mức độ tin cậy thấp).

2. ĐỊNH LƯỢNG LẠC ĐỀ (OFF-TOPIC):
   - Tiêu chí Text: Chứa >80% nội dung là thơ, bài hát, công thức nấu ăn, hoặc cụm từ "đánh giá mang tính chất nhận xu".
   - Tiêu chí Ảnh: >90% diện tích ảnh là cảnh vật không liên quan, người nổi tiếng, meme.
   - Xử lý: Gán nhãn OFF-TOPIC (Bất kể số sao).

3. ĐỊNH LƯỢNG SEEDING / AI-GENERATED (DECEPTIVE):
   - Tiêu chí:
     + Chứa >3 từ khóa seeding điển hình: "shop tư vấn nhiệt tình", "sẽ ủng hộ tiếp", "giao hàng siêu tốc" lặp lại trong 1 template.
     + Đoạn văn >50 từ, không sai một lỗi chính tả/dấu câu nào, dùng cấu trúc liệt kê (1., 2., 3.) y hệt ChatGPT.
   - Xử lý: Gán nhãn DECEPTIVE / FAKE.
```

---

## 4. Quy trình Đánh giá Đa nguồn (Image-First Workflow)

1. **Bước 1 (Xác thực Hình ảnh):** 
   - Không ảnh $\rightarrow$ Xét Text.
   - Ảnh lạc đề (meme, màn hình đen) $\rightarrow$ Đưa vào `Uncertain`, xét Text. 
   - Ảnh copy mạng/shop $\rightarrow$ Cảnh báo `Deceptive`.
   - Ảnh sai sản phẩm $\rightarrow$ Cảnh báo `Misleading`.
2. **Bước 2 (Xử lý Uncertain & Text):** Dựa vào bảng "Quy tắc định lượng" ở Mục 3 để giải quyết. Text vô nghĩa + Ảnh meme = `Off-topic`. Text có ý nghĩa + Ảnh meme = `Trustworthy` (chỉ cày xu bằng ảnh).

---

## 5. Quy tắc Gán nhãn Cấp độ Cụm (Pattern-level Annotation)

Annotator sẽ được cung cấp một **Tập hợp đánh giá (Review Batch)** của cùng một sản phẩm/shop trong khoảng thời gian nhất định (vd: 1 tháng) để phát hiện hành vi tổ chức.

### 5.1. Nhóm Trùng lặp (Near-duplicate Cluster)
* **Định nghĩa:** Nhiều đánh giá (từ các tài khoản khác nhau) có nội dung chữ hoặc hình ảnh gần như y hệt nhau.
* **Tiêu chí định lượng (Threshold):** Nhóm từ 3 đánh giá trở lên, có độ tương đồng văn bản $\ge 85\%$ (Jaccard hoặc Cosine Similarity) HOẶC sử dụng chung 1 hình ảnh đính kèm.
* **Nhãn Cụm:** `Pattern: Near-duplicate`. (Kéo theo nhãn Đơn dòng của toàn bộ cụm này thành `Deceptive / Fake`).

### 5.2. Bùng nổ Thời gian (Time-burst Cluster)
* **Định nghĩa:** Sự gia tăng đột biến, bất thường của các đánh giá 5 sao trong một thời gian rất ngắn cho một sản phẩm.
* **Tiêu chí định lượng (Threshold):** $>70\%$ tổng số đánh giá của sản phẩm đó được đăng tải tập trung trong vòng 24 - 48 giờ, và $\ge 90\%$ trong số đó là đánh giá 5 sao.
* **Nhãn Cụm:** `Pattern: Time-burst`. 