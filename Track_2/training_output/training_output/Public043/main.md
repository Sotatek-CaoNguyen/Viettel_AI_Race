# Public_043

# Ảnh trong máy tính

## Hệ màu RGB

RGB viết tắt của Red (đỏ), Green (xanh lục), Blue (xanh lam), là ba màu chính của ánh sáng khi tách ra từ lăng kính. Khi trộn ba màu trên theo tỉ lệ nhất định có thể tạo thành các màu khác nhau.
![](images/image1.png)
Hình 7.1: Thêm đỏ vào xanh lá cây tạo ra vàng; thêm vàng vào xanh lam tạo ra trắng [19]
Ví dụ khi bạn chọn màu ở [_đây._](https://www.w3schools.com/colors/colors_picker.asp) Khi bạn chọn một màu thì sẽ ra một bộ ba số tương ứng (r,g,b) Với mỗi bộ 3 số r, g, b nguyên trong khoảng [0, 255] sẽ cho ra một màu khác nhau. Do có 256 cách chọn r, 256 cách chọn màu g, 256 cách chọn b => tổng số màu có thể tạo ra bằng hệ màu RGB là: 256 * 256 * 256 = 16777216 màu !!!
![](images/image2.png)
Hình 7.2: màu được chọn là rgb(102, 255, 153), nghĩa là r=102, g=255, b=153.

## Ảnh màu

Ví dụ về ảnh màu trong hình 7.3
Khi bạn kích chuột phải vào ảnh trong máy tính, bạn chọn properties (mục cuối cùng), rồi chọn tab details
![](images/image3.png)
Bạn sẽ thấy chiều dài ảnh là 800 pixels (viết tắt px), chiều rộng 600 pixels, kích thước là 800 * 600. Trước giờ chỉ học đơn vị đo là mét hay centimet, pixel là gì nhỉ ?
Theo wiki, pixel (hay điểm ảnh) là một khối màu rất nhỏ và là đơn vị cơ bản nhất để tạo nên một bức ảnh kỹ thuật số.
Vậy bức ảnh trên kích thước 800 pixel * 600 pixel, có thể biểu diễn dưới dạng một ma trận kích thước 600 * 800 (vì định nghĩa ma trận là số hàng nhân số cột).
![](images/image4.png)
Hình 7.3: Mathematical bridge, Cambridge
Trong đó mỗi phần tử _w ij _là một pixel.
Như vậy có thể hiểu là mỗi pixel thì biểu diễn một màu và bức ảnh trên là sự kết hợp rất nhiều pixel. Hiểu đơn giản thì in bức ảnh ra, kẻ ô vuông như chơi cờ ca rô với 800 đường thẳng ở chiều dài, 600 đường ở chiều rộng, thì mỗi ô vuông là một pixel, biểu diễn một chấm màu.
Tuy nhiên để biểu diễn 1 màu ta cần 3 thông số (r,g,b) nên gọi _w ij _=( _r ij,gij,bij_) để biểu diễn dưới dạng ma trận thì sẽ như sau:
![](images/image5.png)
Hình 7.4: Ảnh màu kích thước 3*3 biểu diễn dạng ma trận, mỗi pixel biểu diễn giá trị (r,g,b)
Để tiện lưu trữ và xử lý không thể lưu trong 1 ma trận như thế kia mà sẽ tách mỗi giá trị màu trong mỗi pixel ra một ma trận riêng.
![](images/image6.png)
Hình 7.5: Tách ma trận trên thành 3 ma trận cùng kích thước: mỗi ma trận lưu giá trị từng màu khác nhau red, green, blue
Mỗi ma trận được tách ra được gọi là 1 channel nên ảnh màu được gọi là 3 channel: channel red, channel green, channel blue.
Tóm tắt: Ảnh màu là một ma trận các pixel mà mỗi pixel biểu diễn một điểm màu. Mỗi điểm màu được biểu diễn bằng bộ 3 số (r,g,b). Để tiện cho việc xử lý ảnh thì sẽ tách ma trận pixel ra 3 channel red, green, blue.

## Tensor là gì

Khi dữ liệu biểu diễn dạng 1 chiều, người ta gọi là vector, mặc định khi viết vector sẽ viết dưới dạng cột.
Khi dữ liệu dạng 2 chiều, người ta gọi là ma trận, kích thước là số hàng * số cột.
![](images/image7.png)
Hình 7.7: Vector v kích thước n, ma trận W kích thước m*n
Khi dữ liệu nhiều hơn 2 nhiều thì sẽ được gọi là tensor, ví dụ như dữ liệu có 3 chiều.
Để ý thì thấy là ma trận là sự kết hợp của các vector cùng kích thước. Xếp n vector kích thước m cạnh nhau thì sẽ được ma trận m*n. Thì tensor 3 chiều cũng là sự kết hợp của các ma trận cùng kích thước, xếp k ma trận kích thước m*n lên nhau sẽ được tensor kích thước m*n*k.
![](images/image8.png)
Hình 7.8: Hình hộp chữ nhật kích thước a*b*h
Tưởng tượng mặt đáy là một ma trận kích thước a * b, được tạo bởi b vector kích thước a. Cả hình hộp là tensor 3 chiều kích thước a*b*h, được tạo bởi xếp h ma trận kích thước a*b lên nhau.
Do đó biểu diễn ảnh màu trên máy tính ở phần trên sẽ được biểu diễn dưới dạng tensor 3 chiều kích thước 600*800*3 do có 3 ma trận (channel) màu red, green, blue kích thước 600*800 chồng lên nhau.
Ví dụ biểu diễn ảnh màu kích thước 28*28, biểu diễn dưới dạng tensor 28*28*3
![](images/image9.png)
Hình 7.9: Ảnh màu biểu diễn dưới dạng tensor [1]

## Ảnh xám

![](images/image10.png)

Hình 7.10: Ảnh xám của mathematical bridge
Tương tự ảnh màu, ảnh xám cũng có kích thước 800 pixel * 600 pixel, có thể biểu diễn dưới dạng một ma trận kích thước 600 * 800 (vì định nghĩa ma trận là số hàng nhân số cột).
Tuy nhiên mỗi pixel trong ảnh xám chỉ cần biểu diễn bằng một giá trị nguyên trong khoảng từ [0,255] thay vì (r,g,b) như trong ảnh màu. Do đó khi biểu diễn ảnh xám trong máy tính chỉ cần một ma trận là đủ.
![](images/image11.png)
Hình 7.11: Biểu diễn ảnh xám
Giá trị 0 là màu đen, 255 là màu trắng và giá trị pixel càng gần 0 thì càng tối và càng gần 255 thì càng sáng.

## Chuyển hệ màu của ảnh

Mỗi pixel trong ảnh màu được biểu diễn bằng 3 giá trị (r,g,b) còn trong ảnh xám chỉ cần 1 giá trị x để biểu diễn.
Khi chuyển từ ảnh màu sang ảnh xám ta có thể dùng công thức: x = r * 0.299 + g * 0.587 + b * 0.114.
Tuy nhiên khi chuyển ngược lại, bạn chỉ biết giá trị x và cần đi tìm r,g,b nên sẽ không chính xác.

# Phép tính convolution

## Convolution

Để cho dễ hình dung tôi sẽ lấy ví dụ trên ảnh xám, tức là ảnh được biểu diễn dưới dạng ma trận A kích thước m*n.
Ta định nghĩa kernel là một ma trận vuông kích thước k*k trong đó k là số lẻ. k có thể bằng 1, 3, 5, 7, 9,... Ví dụ kernel kích thước 3*3
![](images/image12.png)
Kí hiệu phép tính convolution (⊗), kí hiệu _Y_ = _X_ ⊗ _W_
Với mỗi phần tử _x ij _trong ma trận X lấy ra một ma trận có kích thước bằng kích thước của kernel W có phần tử _x ij _làm trung tâm (đây là vì sao kích thước của kernel thường lẻ) gọi là ma trận A. Sau đó tính tổng các phần tử của phép tính element-wise của ma trận A và ma trận W, rồi viết vào ma trận kết quả Y.
![](images/image13.png)
Ví dụ khi tính tại _x_ 22 (ô khoanh đỏ trong hình), ma trận A cùng kích thước với W, có _x_ 22 làm trung tâm có màu nền da cam như trong hình. Sau đó tính _y_ 11 = _sum_ ( _A_ ⊗ _W_ )= _x_ 11∗ _w_ 11+ _x_ 12∗ _w_ 12+ _x_ 13∗ _w_ 13+ _x_ 21∗ _w_ 21+ _x_ 22∗ _w_ 22+ _x_ 23∗ _w_ 23+ _x_ 31∗ _w_ 31+ _x_ 32∗ _w_ 32+ _x_ 33∗ _w_ 33 =4. Và làm tương tự với các phần tử còn lại trong ma trận.
Thế thì sẽ xử lý thế nào với phần tử ở viền ngoài như _x_ 11? Bình thường khi tính thì sẽ bỏ qua các phần tử ở viền ngoài, vì không tìm được ma trận A ở trong X.
Nên bạn để ý thấy ma trận Y có kích thước nhỏ hơn ma trận X. Kích thước của ma trận Y là (m-k+1) * (n-k+1).
![](images/image14.png)
Hình 7.12: Các bước thực hiện phép tính convolution cho ma trận X với kernel K ở trên

## Padding

Như ở trên thì mỗi lần thực hiện phép tính convolution xong thì kích thước ma trận Y đều nhỏ hơn X. Tuy nhiên giờ ta muốn ma trận Y thu được có kích thước bằng ma trận X => Tìm cách giải quyết cho các phần tử ở viền => Thêm giá trị 0 ở viền ngoài ma trận X.
![](images/image15.png)
Hình 7.13: Ma trận X khi thêm viền 0 bên ngoài
Rõ ràng là giờ đã giải quyết được vấn đề tìm A cho phần tử _x_ 11 , và ma trận Y thu được sẽ bằng
kích thước ma trận X ban đầu.
Phép tính này gọi là convolution với padding=1. Padding=k nghĩa là thêm k vector 0 vào mỗi phía (trên, dưới, trái, phải) của ma trận.

## Stride

Như ở trên ta thực hiện tuần tự các phần tử trong ma trận X, thu được ma trận Y cùng kích thước ma trận X, ta gọi là stride=1.
![](images/image16.png)
Hình 7.14: stride=1, padding=1
Tuy nhiên nếu stride=k (k > 1) thì ta chỉ thực hiện phép tính convolution trên các phần tử _x_ 1+ _i_ ∗ _k,_ 1+ _j_ ∗ _k_. Ví dụ k = 2.
![](images/image17.png)
Hình 7.15: padding=1, stride=2
Hiểu đơn giản là bắt đầu từ vị trí _x_ 11 sau đó nhảy k bước theo chiều dọc và ngang cho đến hết ma trận X.
Kích thước của ma trận Y là 3*3 đã giảm đi đáng kể so với ma trận X.
Công thức tổng quát cho phép tính convolution của ma trận X kích thước m*n với kernel kích thước k*k, stride = s, padding = p ra ma trận Y kích thước là
$$
(m−2k+ps+1)×(n−2k+ps+1)left( frac{m - 2k + p}{s} + 1 right) times left( frac{n - 2k + p}{s} + 1 right)
$$
Stride thường dùng để giảm kích thước của ma trận sau phép tính convolution.