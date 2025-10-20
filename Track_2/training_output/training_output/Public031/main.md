# Public_031

# Điện trở (Resistor)

## Điện trở là gì? (What is a Resistor)

Điện trở (Resistor) là linh kiện điện tử thụ động tạo ra trở kháng (resistance), làm cản trở dòng chảy của các electron trong mạch điện.

Chúng được gọi là phần tử thụ động (passive) vì chỉ tiêu thụ năng lượng (consume power) mà không tạo ra năng lượng.

Điện trở thường được sử dụng trong các mạch như OP-AMP, vi điều khiển (microcontrollers) và các mạch tích hợp khác (IC – integrated circuits). Chúng dùng để hạn dòng (limit current), chia điện áp (divide voltages) và điều khiển các đường I/O (pull-up/pull-down lines).

## Đơn vị điện trở (Resistor Units)

Đơn vị đo điện trở là **Ohm (Ω)** , ký hiệu bằng chữ Hy Lạp Omega (Ω). Ohm đặt theo tên nhà vật lý Georg Simon Ohm (1784–1854), người đã nghiên cứu và phát hiện mối quan hệ giữa điện áp, dòng điện và điện trở (Luật Ohm).

Trong hệ SI, các tiền tố được dùng để biểu thị điện trở lớn hoặc nhỏ: kilo (kΩ), mega (MΩ), giga (GΩ) hoặc mili (mΩ).

**Ví dụ:**

  * 4.700 Ω = 4.7 kΩ

  * 5.600.000 Ω = 5.6 MΩ hoặc 5,600 kΩ


Tên các điện trở trong mạch thường bắt đầu bằng chữ **R** , mỗi điện trở có một số duy nhất.

## Ký hiệu điện trở trong sơ đồ mạch (Resistor Schematic Symbol)

Tất cả các điện trở có hai đầu nối. Trên sơ đồ mạch, điện trở được biểu thị theo hai tiêu chuẩn:

  * **Hình chữ nhật** : theo tiêu chuẩn IEC (International Electrotechnical Commission)

  * **Đường ngoằn ngoèo (zigzag)** : theo tiêu chuẩn IEEE (Institute of Electrical and Electronics Engineers)


Cả hai ký hiệu đều chấp nhận được. Hình chữ nhật thường được ưu tiên; dạng zigzag phổ biến ở Mỹ và châu Á. Số đỉnh zigzag tiêu chuẩn là 7, với 4 đỉnh trên và 3 đỉnh dưới.

## Thành phần điện trở (Resistor Composition)

Điện trở được chế tạo từ nhiều loại vật liệu, phổ biến là **màng carbon, kim loại hoặc oxit kim loại**. Một lớp vật liệu dẫn điện mỏng được quấn quanh và bao phủ bởi lớp cách điện.

  * **Màng dày** : rẻ nhưng ít chính xác

  * **Màng mỏng** : đắt hơn nhưng chính xác cao


**Ví dụ giá trị điện trở:**

  * 27 Ω, 330 Ω, 3.3 MΩ


Bên trong, màng carbon quấn quanh lõi cách điện. Nhiều lớp bọc → điện trở cao hơn.

## Ý nghĩa điện trở trong mạch điện (Resistor in Circuit)

Điện trở có thể thay thế nhiều thiết bị điện như bóng đèn hoặc động cơ. Trong mạch điện đốt nóng (electric heater circuit), sợi dây đốt nóng được xem như điện trở.

**Định luật Ohm:**

R=VIR = V/I

**Ví dụ:**

  * Tổng điện trở bình thường: RT=60 ΩR_T = 60\,\Omega (240 ÷ 4 = 60 Ω)

  * Khi dòng điện giảm còn 3 A, điện trở tăng: RT=240÷3=80 ΩR_T = 240 ÷ 3 = 80\,\Omega → báo hiệu mạch có vấn đề.


## Giá trị điện trở của dây dẫn (Resistance of Conductor)

Bốn yếu tố ảnh hưởng điện trở dây dẫn:

### Vật liệu (Material)

  * Dây dẫn tốt: đồng, bạc, nhôm

  * Cách điện: cao su, thủy tinh, sứ


### Chiều dài (L)

  * Dây càng dài, điện trở càng cao.

  * Ví dụ: dây 2 m → điện trở gấp đôi dây 1 m


### Diện tích mặt cắt ngang (A)

  * Mặt cắt lớn → điện trở giảm.

  * Ví dụ: diện tích tăng gấp đôi → điện trở giảm phân nửa


### Nhiệt độ (T)

  * Nhiệt độ tăng → điện trở tăng.

  * Khó dự đoán so với các yếu tố khác.


**Công thức tính điện trở dây dẫn:**

R=ρLAR

Trong đó:

  * RR: điện trở (Ω)

  * ρ\rho: điện trở suất của vật liệu (Ω·m)

  * LL: chiều dài dây (m)

  * AA: diện tích mặt cắt ngang (m²)


## Mạch điện trở mắc nối tiếp (Resistor Series Circuits)

Trong **mạch nối tiếp** , các điện trở được kết nối từ đầu đến cuối, tạo thành một **đường dẫn duy nhất** cho dòng điện.

**Tổng điện trở mạch nối tiếp:**

RT=R1+R2+R3+…R_T = R_1 + R_2 + R_3 + \dots

**Ví dụ 1:** 3 điện trở nối tiếp

  * R1=2 Ω,R2=4 Ω,R3=6 ΩR_1 = 2\,\Omega, R_2 = 4\,\Omega, R_3 = 6\,\Omega

  * Dòng điện I=4 AI = 4\,A

  * Tổng điện trở: RT=2+4+6=12 ΩR_T = 2 + 4 + 6 = 12\,\Omega

  * Điện áp nguồn: E=I⋅RT=4×12=48 VE = I \cdot R_T = 4 \times 12 = 48\,V


**Ví dụ 2:** 3 điện trở nối tiếp với điện áp nguồn E=9 VE = 9\,V

  * R1=3 kΩ,R2=10 kΩ,R3=5 kΩR_1 = 3\,k\Omega, R_2 = 10\,k\Omega, R_3 = 5\,k\Omega

  * Dòng điện trong mạch:


Sau đó, điện áp rơi trên mỗi điện trở:

VR1=I⋅R1=0.5×3=1.5 VV_{R1} = I R_1 = 0.5 x3 = 1.5\,V VR2=I⋅R2=0.5×10=5 VV_{R2} = I R_2 = 0.5 x 10 = 5\,V VR3=I⋅R3=0.5×5=2.5 VV_{R3} = I R_3 = 0.5 x 5 = 2.5\,V

Tôi sẽ viết thêm một đoạn mở rộng về **mạch điện trở song song (parallel resistor circuits)** để nối tiếp tài liệu hiện tại:

## Mạch điện trở mắc song song (Resistor Parallel Circuits)

Trong **mạch điện song song** , các điện trở được kết nối sao cho cả hai đầu của chúng được nối trực tiếp vào cùng hai điểm, tạo ra **nhiều đường dẫn** cho dòng điện chảy. Điện áp trên mỗi điện trở trong mạch song song luôn bằng nhau, nhưng dòng điện phân chia theo giá trị điện trở của từng nhánh.

**Ví dụ:**  
Ba điện trở mắc song song: R1=6 ΩR_1 = 6 , R2=3 ΩR_2 = 3, R3=2 ΩR_3 = 2.  
Tổng điện trở: 1

Dòng điện tổng từ nguồn được chia theo tỉ lệ nghịch với điện trở từng nhánh:

Điều này giúp mạch **giảm tổng điện trở** so với bất kỳ điện trở riêng lẻ nào và **tăng khả năng phân phối dòng điện** cho các thiết bị nối vào nhánh khác nhau. Mạch song song phổ biến trong **hệ thống chiếu sáng, mạch nguồn và điện gia dụng** , nơi các tải cần hoạt động độc lập nhưng cùng điện áp.

**Ưu điểm của mạch song song:**

  * Nếu một nhánh hỏng, các nhánh khác vẫn hoạt động.

  * Dễ dàng điều chỉnh dòng điện cho từng nhánh bằng cách chọn điện trở phù hợp.


**Nhược điểm:**

  * Cần tính toán tổng điện trở cẩn thận, đặc biệt khi nhiều nhánh nối song song, để tránh dòng quá tải.