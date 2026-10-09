# Báo cáo lab: chọn tracker cho 5 video

**Nhóm:** Cá nhân **Thành viên:** Dương Dương — MSSV 2A202602498

Detector cố định: `yolo26n.pt`, ảnh 640 px, Re-ID `osnet_x0_25_msmt17`. Không đổi các mục này trong bài nộp chính.

## 1. Cấu hình đã chọn

Mỗi video: tracker bạn nộp, `conf`, `iou`, điều bạn **nhìn thấy** trên video, và một cấu hình đã thử rồi loại.

| Video | Tracker | conf | iou | Quan sát khi xem video | Đã thử nhưng loại |
|---|---|---|---|---|---|
| video_1 (quảng trường, tĩnh, ban ngày) | strongsort | 0.15 | 0.5 | Ngưỡng thấp giữ thêm người nhỏ ở xa; Re-ID giúp nối danh tính tốt hơn và cho HOTA/IDF1 cao nhất trong các cấu hình đã chấm. | bytetrack, conf 0.3, iou 0.5: ít hộp giả hơn nhưng bỏ sót nhiều hơn, HOTA và IDF1 thấp hơn. |
| video_2 (phố đêm, tĩnh, rất đông) | strongsort | 0.3 | 0.5 | Giữ được nhiều người nhỏ trong vùng tối và các cụm đông; ID nhìn ổn định hơn khi người đi gần nhau. | strongsort, conf 0.15, iou 0.5: xuất hiện nhiều track ngắn và hộp nhiễu; conf 0.5 bỏ sót người nhỏ. |
| video_3 (camera di động, ảnh nhỏ) | strongsort | 0.3 | 0.5 | Re-ID hỗ trợ giữ danh tính khi camera dịch chuyển và người thay đổi vị trí mạnh trong ảnh; track quan sát được dài hơn ByteTrack. | bytetrack, conf 0.3, iou 0.5: ID bị tạo lại thường xuyên hơn khi chuyển động camera lớn. |
| video_4 (trong nhà, camera di chuyển) | strongsort | 0.3 | 0.5 | Theo được người đi trước camera khi kích thước hộp thay đổi; ngưỡng trung bình hạn chế hộp ngắn trên vùng phản chiếu. | strongsort, conf 0.15, iou 0.5: tăng nhiều track rất ngắn quanh nền và kính. |
| video_5 (trên xe bus, giao lộ đông) | bytetrack | 0.3 | 0.5 | Chuyển động của người tương đối đều giữa các frame; ByteTrack cho ít ID phân mảnh hơn và ít hộp dự đoán dư. | strongsort, conf 0.3, iou 0.5: tạo nhiều ID ngắn hơn khi góc nhìn và kích thước người đổi nhanh. |

## 2. Số liệu video_1

Dán bảng HOTA / MOTA / IDF1 do `scripts/evaluate_practice.py` in ra.

```text
HOTA:     29.184
MOTA:     19.897
IDF1:     32.572
CLR_TP:     5240
CLR_FN:    13341
CLR_FP:     1434
IDSW:        109
```

`video_2` đến `video_5` không có nhãn trong gói lab. Không điền số cho các video đó.

## 3. Phân tích

### Video 1

StrongSORT với `conf=0.15` cho HOTA và IDF1 cao nhất trong các lượt chấm, đồng thời bắt thêm người nhỏ ở xa. Re-ID có lợi khi người bị che một phần hoặc đi gần nhau, nhưng ngưỡng thấp cũng làm số hộp giả và số lần đổi ID tăng. Cấu hình này vẫn được chọn vì mức tăng recall và khả năng liên kết danh tính giúp HOTA tổng thể cao hơn ByteTrack và các ngưỡng `conf` lớn hơn.

### Video 3

Camera di chuyển làm vị trí hộp thay đổi mạnh nên giả thiết chuyển động của ByteTrack kém ổn định hơn. Trong 150 frame thử, StrongSORT tạo các track có độ dài trung vị lớn hơn và preview cho thấy ID bám người tốt hơn khi họ tiến sát camera. `conf=0.3` cân bằng giữa việc giữ người nhỏ và tránh các track ngắn xuất hiện khi hạ ngưỡng xuống `0.15`.

### Video 5

Ở góc nhìn từ xe, ByteTrack tạo ít ID phân mảnh hơn StrongSORT trong đoạn thử và không giữ nhiều hộp dự đoán dư khi người rời khung hình. Dù camera rung, chuyển động giữa các frame liên tiếp vẫn đủ đều để tracker theo chuyển động hoạt động tốt. Vì người thường nhỏ và ngoại hình thay đổi nhanh theo góc nhìn, Re-ID không đem lại lợi ích rõ bằng ở video 2–4.

## 4. Nếu có thêm thời gian

Mình sẽ quét `conf` mịn hơn quanh `0.15–0.30` cho video 1 và xem riêng các frame có che khuất để giảm 109 lần đổi ID. Với các video không có nhãn, mình sẽ đánh dấu các mốc ID nhảy trong preview rồi thử thêm BoTSORT để so sánh Re-ID với StrongSORT.
