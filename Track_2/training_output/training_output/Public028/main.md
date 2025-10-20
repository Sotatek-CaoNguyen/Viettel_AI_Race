# Public_028

Sự phát triển của ngành công nghiệp điện tử như chúng ta thấy ngày nay bắt đầu với sự phát minh ra **Transistor**. Cách thức hoạt động của transistor có thể được hiểu dễ dàng nếu bạn đã có kiến thức về **Diode bán dẫn**. Việc thêm một lớp khác vào một diode mối nối P-N tạo thành một thiết bị **3 đầu cuối** được gọi là **Transistor**. Thuật ngữ transistor thường đề cập đến **Transistor Bipolar Junction (BJT)**.

Transistor đã được kiểm chứng thành công vào ngày **23/12/1947** tại Phòng thí nghiệm Bell, New Jersey. Ba cá nhân được ghi nhận phát minh ra transistor là **John Bardeen, William Shockley và Walter Brattain** , trong đó William Shockley đóng vai trò quan trọng trong việc phát minh.

**Các ứng dụng của Transistor lưỡng cực (BJT) bao gồm:**

  * Ti vi

  * Điện thoại di động

  * Máy tính

  * Thiết bị phát sóng vô tuyến

  * Bộ khuếch đại âm thanh …


# Cấu tạo – Ký hiệu

## Cấu tạo

Giống như diode mối nối P-N, một BJT cũng được tạo thành từ sự kết hợp của các lớp bán dẫn loại P và loại N. Tuy nhiên, transistor có thể chứa:

  * Một lớp P giữa hai lớp N → **Transistor NPN**

  * Một lớp N giữa hai lớp P → **Transistor PNP**


Transistor có ba thiết bị đầu cuối ( **3 chân ra** ):

  * **Emitter (Bộ phát)**

  * **Base (Cơ sở / Đế / Lớp nền)**

  * **Collector (Bộ thu)**


**Cấu tạo cụ thể:**

**Transistor NPN:**

  * Emitter kết nối với lớp N bên trái

  * Collector kết nối với lớp N bên phải

  * Base kết nối với lớp P ở giữa


**Transistor PNP:**

  * Emitter kết nối với lớp P bên trái

  * Collector kết nối với lớp P bên phải

  * Base kết nối với lớp N ở giữa


Transistor có **hai mối nối P-N** :

  1. **Emitter-Base (E-B)**

  2. **Base-Collector (B-C)**


## Thiết bị đầu cuối của BJT

  * **Emitter:**  
Cung cấp các điện tích. Emitter được pha tạp nặng để bơm nhiều hạt mang điện vào Base. Kích thước E > Base.

  * **Base:**  
Lớp giữa, rất mỏng, pha tạp nhẹ, nồng độ tạp chất thấp nhất.

  * **Collector:**  
Thu thập các hạt mang điện, pha tạp vừa phải. Kích thước lớn hơn Emitter và Base, để xử lý năng lượng và tản nhiệt tốt.


## Ký hiệu

Transistor được xem như **hai diode mắc chung Anode hoặc Cathode** :

  * **NPN:** chung Anode

  * **PNP:** chung Cathode


# Nguyên lý hoạt động

## Nguyên lý làm việc của Transistor NPN

Khi không có điện áp cấp cho transistor NPN → **không phân cực**.

  * **Lớp N (Emitter & Collector):** điện tử tự do là hạt dẫn đa số, lỗ trống là hạt mang điện thiểu số.

  * **Lớp P (Base):** điện tử tự do là hạt mang điện thiểu số, lỗ trống là hạt dẫn đa số.


Các hạt mang điện luôn di chuyển từ vùng nồng độ cao → nồng độ thấp:

  * Điện tử: từ N (n-region) → P (p-region)

  * Lỗ trống: từ P (p-region) → N (n-region)


Quá trình này tạo ra **vùng nghèo kiệt (depletion region)** tại mối nối **B-E** và **B-C**.

### Tại sao vùng nghèo kiệt thâm nhập nhiều hơn về phía pha tạp nhẹ?

  * Doping là quá trình thêm tạp chất vào chất bán dẫn để tăng dẫn điện.

  * **Pha tạp nặng:** nhiều hạt mang điện, dẫn điện cao

  * **Pha tạp nhẹ:** ít hạt mang điện, dẫn điện thấp


Trong **Transistor NPN** :

  * **Emitter (N):** pha tạp nặng → nhiều điện tử tự do

  * **Base (P):** pha tạp nhẹ → ít lỗ trống

  * **Collector (N):** pha tạp vừa phải → nồng độ giữa Emitter và Base


### Nguyên tử và ion trong bán dẫn

  * Nguyên tử nhường electron → **ion dương**

  * Nguyên tử nhận electron → **ion âm**

  * Nguyên tử cho electron → **nhà tài trợ (donor)**

  * Nguyên tử nhận electron → **người nhận (acceptor)**


## Mối nối B- E(Emitter-base junction)

### n lỗ trống từ Base sang Emitter:

  * Đồng thời, các **lỗ trống** trong vùng p (Base) di chuyển sang vùng n (Emitter).

  * Tuy nhiên, vì Emitter được pha tạp nặng, số lỗ trống đi vào Emitter chỉ là một phần rất nhỏ so với số electron đi sang Base.


### Tương tác nguyên tử tại mối nối

Tại **mối nối B-E** , khi các electron từ Emitter di chuyển vào Base:

  * Mỗi nguyên tử trong **n-region (Emitter)** nhường electron cho các nguyên tử lỗ trống trong **p-region (Base)**.

  * Ví dụ: nếu mỗi nguyên tử Emitter nhường **3 electron tự do** , thì **3 nguyên tử trong Base** sẽ nhận các electron này.

  * Khi nguyên tử Emitter nhường electron → trở thành **ion dương** , do mất electron.

  * Khi nguyên tử Base nhận electron → trở thành **ion âm** , do thêm electron vào lỗ trống.


Kết quả của quá trình này là:

  1. Hình thành **vùng nghèo kiệt (depletion region)** tại mối nối B-E:

* Vùng này chứa các **ion dương cố định** ở phía Emitter và **ion âm cố định** ở phía Base.

* Vùng nghèo kiệt này tạo ra một **điện trường nội** ngăn cản dòng electron và lỗ trống tự do tiếp tục khuếch tán một cách quá mức.

  2. Dòng điện chủ yếu là **electron từ Emitter sang Base** :

* Chỉ một phần nhỏ electron kết hợp với lỗ trống trong Base, số còn lại đi vào **Collector** nhờ hiệu ứng điện trường tại mối nối Base-Collector.


### Tóm tắt cơ chế hoạt động B-E

  * **Emitter:** cung cấp electron tự do với nồng độ cao.

  * **Base:** mỏng, pha tạp nhẹ, chứa lỗ trống nhưng ít electron.

  * **Khuếch tán:** electron từ Emitter sang Base, lỗ trống từ Base sang Emitter.

  * **Vùng nghèo kiệt:** ion dương Emitter và ion âm Base hình thành điện trường nội.

  * **Dòng điện chủ yếu:** từ Emitter sang Collector qua Base, cơ chế này giúp transistor hoạt động như **bộ khuếch đại dòng điện**.