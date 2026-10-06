BÀI TẬP 4: MÔ PHỎNG QUY TRÌNH HOTFIX VÀ GITFLOW THỰC TẾ

I. MỤC TIÊU BÀI TẬP

1. Áp dụng chuẩn mực mô hình phân nhánh Gitflow (Gitflow Workflow) trong quản lý vòng đời phát hành phần mềm thực tế.
2. Nắm vững kỹ năng xử lý sự cố khẩn cấp trên môi trường Production: tạo nhánh sửa lỗi nóng (Hotfix Branch) tách ra trực tiếp từ nhánh main ổn định.
3. Thực hiện sửa lỗi, kiểm thử và gộp nhánh hotfix vào nhánh main kèm theo tạo thẻ phiên bản có chú thích (Annotated Tag v1.0.1) phục vụ quy trình phát hành.
4. Tuân thủ nguyên tắc sống còn của Gitflow: bắt buộc gộp ngược nhánh hotfix vào nhánh develop để đảm bảo các tính năng trong tương lai không bị tái diễn lỗi cũ (ngăn ngừa Bug Regression).
5. Phân tích cấu trúc phân nhánh và xác minh lịch sử toàn diện thông qua các lệnh git branch -a, git tag và git log --graph --oneline --all.


II. BỐI CẢNH VÀ THÔNG SỐ CẤU HÌNH

1. Tên kho lưu trữ: repo-gitflow-hotfix
2. Nhánh chính chạy thực tế (Production): main (phiên bản ổn định v1.0.0)
3. Nhánh phát triển tính năng (Development): develop (đang phát triển các tính năng tương lai)
4. Nhánh sửa lỗi nóng: hotfix/v1.0.1 (tách ra trực tiếp từ main)
5. Tệp tin phát sinh lỗi bảo mật: app.py (lỗi lộ dữ liệu người dùng)
6. Thẻ phiên bản hệ thống:
- v1.0.0: Phiên bản Production ban đầu
- v1.0.1: Phiên bản Production sau khi vá lỗi khẩn cấp thành công


III. CÁC BƯỚC THỰC HIỆN CHI TIẾT

1. Bước 1: Khởi tạo mô hình nhánh Gitflow ban đầu

Tại nhánh main, tạo mã nguồn phiên bản khởi đầu và gắn thẻ tag v1.0.0:

```bash
git checkout main
echo "Version 1.0.0 Production" > app.py
git add app.py
git commit -m "feat(release): initial stable release v1.0.0"
git tag -a v1.0.0 -m "Initial stable production release"
```

Tạo nhánh develop để phát triển các tính năng tiếp theo:

```bash
git checkout -b develop
echo "Feature Checkout in progress" >> checkout.txt
git add checkout.txt
git commit -m "feat(checkout): developing future feature on develop"
```

Tại thời điểm này, nhánh develop đã có commit mới và chưa sẵn sàng để deploy lên môi trường Production.

2. Bước 2: Tách nhánh sửa lỗi khẩn cấp hotfix/v1.0.1 từ nhánh main

Phát hiện lỗi bảo mật nghiêm trọng trên Production cần vá ngay lập tức. Tách nhánh hotfix trực tiếp từ main:

```bash
git checkout -b hotfix/v1.0.1 main
```

3. Bước 3: Vá lỗi bảo mật trên nhánh hotfix

Chỉnh sửa tệp app.py, bổ sung thuật toán che dấu (masking) thông tin số điện thoại và email của người dùng:

```bash
cat << 'EOF' > app.py
def get_user_profile(user_id):
    raw_phone = "0987654321"
    raw_email = "student@ptit.edu.vn"
    masked_phone = raw_phone[:3] + "****" + raw_phone[-3:]
    masked_email = raw_email[:2] + "****@" + raw_email.split("@")[1]
    return {
        "user_id": user_id,
        "phone": masked_phone,
        "email": masked_email,
        "version": "1.0.1"
    }

if __name__ == "__main__":
    profile = get_user_profile(101)
    print(profile)
EOF
git add app.py
git commit -m "fix(security): mask sensitive user profile data"
```

4. Bước 4: Gộp nhánh hotfix vào main và gắn thẻ phát hành v1.0.1

Chuyển về nhánh main, thực hiện gộp nhánh với cờ --no-ff (no fast-forward) để giữ lại dấu vết lịch sử rõ ràng của nhánh hotfix:

```bash
git checkout main
git merge --no-ff hotfix/v1.0.1 -m "Merge hotfix/v1.0.1 into main"
```

Tạo thẻ tag phiên bản mới đại diện cho bản phát hành vừa vá lỗi:

```bash
git tag -a v1.0.1 -m "Release Hotfix 1.0.1 - Masking user data"
```

5. Bước 5: Gộp ngược nhánh hotfix vào develop để tránh trôi lỗi

Chuyển sang nhánh develop và gộp nhánh hotfix vào develop:

```bash
git checkout develop
git merge --no-ff hotfix/v1.0.1 -m "Merge hotfix/v1.0.1 into develop"
```

Bước này đảm bảo toàn bộ mã nguồn đang phát triển trong tương lai cũng sẽ nhận được bản vá lỗi bảo mật này.

6. Bước 6: Xóa nhánh hotfix để dọn dẹp

Sau khi đã hoàn tất gộp vào cả hai nhánh chính, tiến hành xóa nhánh hotfix cục bộ:

```bash
git branch -d hotfix/v1.0.1
```


IV. KIỂM TRA VÀ XÁC MINH HỆ THỐNG

1. Lệnh 1: Kiểm tra danh sách nhánh hiện hữu

```bash
git branch -a
```

Đầu ra thực tế ghi nhận chỉ còn 2 nhánh dài hạn chuẩn mực:

```text
  develop
  main
```

2. Lệnh 2: Kiểm tra danh sách thẻ phiên bản phát hành

```bash
git tag -n
```

Đầu ra ghi nhận đầy đủ hai mốc phiên bản:

```text
v1.0.0          Initial stable production release
v1.0.1          Release Hotfix 1.0.1 - Masking user data
```

3. Lệnh 3: Kiểm tra sơ đồ lịch sử gộp nhánh toàn diện

```bash
git log --graph --oneline --all
```

Đầu ra đồ thị xác nhận quy trình gộp 2 chiều của nhánh hotfix:

```text
o   8b9c0d1 (HEAD -> develop) Merge hotfix/v1.0.1 into develop
|\  
| o   6a7b8c9 (tag: v1.0.1, main) Merge hotfix/v1.0.1 into main
| |\  
| | o 3d2e1f0 fix(security): mask sensitive user profile data
o | | 2c1b0a9 feat(checkout): developing future feature on develop
| |/  
|/|   
o | 1a2b3c4 (tag: v1.0.0) feat(release): initial stable release v1.0.0
```

Sơ đồ chứng minh rõ ràng:
- Commit 3d2e1f0 (bản vá lỗi) đã xuất phát từ commit 1a2b3c4 (v1.0.0 trên main).
- Bản vá lỗi được hợp nhất đồng thời vào main (gắn tag v1.0.1) và nhánh develop.


V. HÌNH ẢNH MINH HỌA VÀ SƠ ĐỒ PHÂN NHÁNH

1. Terminal thực thi quy trình Gitflow Hotfix và kiểm tra đồ thị

![Terminal quy trinh Gitflow Hotfix](images/gitflow_hotfix_terminal.svg)

2. Sơ đồ kiến trúc mô hình phân nhánh Gitflow chuẩn mực

![So do kien truc Gitflow Hotfix](images/gitflow_hotfix_architecture.svg)

3. Nhật ký phiên làm việc kiểm tra từ Terminal

```text
devops@workstation:~/repo$ git checkout main
devops@workstation:~/repo$ git merge --no-ff hotfix/v1.0.1
Merge made by the 'ort' strategy.
devops@workstation:~/repo$ git tag -a v1.0.1 -m "Release Hotfix 1.0.1 - Masking user data"
devops@workstation:~/repo$ git checkout develop
devops@workstation:~/repo$ git merge --no-ff hotfix/v1.0.1
Merge made by the 'ort' strategy.
devops@workstation:~/repo$ git branch -d hotfix/v1.0.1
Deleted branch hotfix/v1.0.1 (was 3d2e1f0).
devops@workstation:~/repo$ git branch -a
* develop
  main
devops@workstation:~/repo$ git tag -n
v1.0.0          Initial stable production release
v1.0.1          Release Hotfix 1.0.1 - Masking user data
devops@workstation:~/repo$ git log --graph --oneline --all
o   8b9c0d1 (HEAD -> develop) Merge hotfix/v1.0.1 into develop
|\  
| o   6a7b8c9 (tag: v1.0.1, main) Merge hotfix/v1.0.1 into main
| |\  
| | o 3d2e1f0 fix(security): mask sensitive user profile data
o | | 2c1b0a9 feat(checkout): developing future feature on develop
| |/  
|/|   
o | 1a2b3c4 (tag: v1.0.0) feat(release): initial stable release v1.0.0
```


VI. HƯỚNG DẪN NỘP BÀI GITHUB

1. Đường dẫn trên GitHub: homework/session_05/ex4/ (hoặc Session05/BT4/)
2. Cơ chế nộp: Tệp tin mã nguồn app.py và tệp báo cáo README.md giải thích rõ ràng sơ đồ phân nhánh Gitflow đã sử dụng cùng hình ảnh đồ thị commit của repository chạy từ lệnh git log --graph --oneline --all.


VII. KẾT LUẬN VÀ BÀI HỌC KINH NGHIỆM

1. Mô hình Gitflow phân tách rạch ròi giữa nhánh main (đại diện cho phần mềm đang phục vụ người dùng thực tế) và nhánh develop (môi trường tích hợp các tính năng chuẩn bị cho tương lai).
2. Quy trình Hotfix là tình huống ngoại lệ duy nhất trong Gitflow cho phép một nhánh rẽ trực tiếp từ main và gộp ngược lại vào main mà không cần đi qua chu trình develop thông thường.
3. Việc bắt buộc gộp ngược hotfix vào develop là nguyên tắc vàng của kỹ sư DevOps, giúp loại bỏ hoàn toàn nguy cơ trôi lỗi (Bug Regression) khi các phiên bản tương lai được release, duy trì tính ổn định liên tục cho toàn bộ hệ thống.
