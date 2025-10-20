# Public_015

# Bộ xử lý trung tâm – CPU

Bộ xử lý trung tâm (Central Proccesor Unit- CPU) điều khiển các thành phần của máy tính, xử lý dữ liệu. CPU hoạt động theo chương trình nằm trong bộ nhớ chính, nhận các lệnh từ bộ nhớ chính, giải mã lệnh để phát ra các tín hiệu điều khiển thực thi lệnh. Trong quá trình thực hiện lệnh, CPU có trao đổi với bộ nhớ chính và hệ thống vào ra. CPU có 3 bộ phận chính: khối điều khiển, khối tính toán số học và logic, và tập các thanh ghi (hình 3.2).

  * **Khối điều khiển** ( _Control Unit_ – CU):

* Nhận lệnh của chương trình từ bộ nhớ trong đưa vào CPU. Nó có nhiệm vụ giải mã các lệnh, tạo ra các tín hiệu điều khiển công việc của các bộ phận khác của máy tính theo yêu cầu của người sử dụng hoặc theo chương trình đã cài đặt..

  * **Khối tính toán số học và logic** ( _Arithmetic_ – _Logic Unit_ \- ALU)

* Bao gồm các thiết bị thực hiện các phép tính số học (cộng, trừ, nhân, chia, ...), các phép tính logic (AND, OR, NOT, XOR) và các phép tính quan hệ (so sánh lớn hơn, nhỏ hơn, bằng nhau, ...)

* Dữ liệu từ bộ nhớ hay các thiết bị vào-ra sẽ được chuyển vào các thanh ghi của CPU, rồi chuyển đến ALU. Tại đây, dữ liệu được tính toán rồi trả lại các thanh ghi và chuyển về bộ nhớ hay các thiết bị vào-ra.

* Độ dài từ của các toán hạng được đưa vào tính toán trực tiếp ở khối ALU. Độ dài phổ biến với các máy tính hiện nay là 32 hay 64 bit.

* Ban đầu ALU chỉ gồm khối tính toán số nguyên IU (Integer Unit). Để tăng khả năng tính toán nhất là trong dấu phẩy động. Khối tính toán hiện nay được bổ sung thêm khối tính toán dấu phẩy động FPU (Floating Point Unit)- hay còn gọi là bộ đồng xử lý (Co-proccesor Unit) .

  * **Tập các thanh ghi** ( _Registers_ )

* Được gắn chặt vào CPU bằng các mạch điện tử làm nhiệm vụ bộ nhớ trung gian cho CPU. Các thanh ghi mang các chức năng chuyên dụng giúp tăng tốc độ trao đổi thông tin

* trong máy tính. Trên các CPU hiện nay có từ vài chục đến vài trăm thanh ghi. Độ dài của các thanh ghi cũng khác nhau từ 8 đến 64 bit.

* Ngoài ra, CPU còn được gắn với một đồng hồ (clock) hay còn gọi là bộ tạo xung nhịp. Tần số đồng hồ càng cao thì tốc độ xử lý thông tin càng nhanh. Thường thì đồng hồ được gắn tương xứng với cấu hình máy và có các tần số dao động (cho các máy Pentium 4 trở lên) là 2.0 GHz, 2.2 GHz, ... hoặc cao hơn.


# Bộ vi xử lý (Microprocessor)

CPU được chế tạo trên một vi mạch và được gọi là bộ vi xử lý. Vì vậy, chúng ta có thể gọi CPU là bộ vi xử lý. Tuy nhiên, các bộ vi xử lý hiện nay có cấu trúc phức tạp hơn nhiều so với một CPU cơ bản.

# Bộ nhớ

Bộ nhớ là thiết bị lưu trữ thông tin trong quá trình máy tính xử lý. Bộ nhớ bao gồm bộ nhớ trong và bộ nhớ ngoài.

_Bộ nhớ trong_

Bộ nhớ trong ( _Internal Memory_ ) là những thành phần nhớ mà CPU có thể trao đổi trực tiếp: các lệnh mà CPU thực thi, các dữ liệu mà CPU sử dụng đều phải nằm trong bộ nhớ trong. Bộ nhớ trong có dung lượng không thật lớn song có tốc độ trao đổi thông tin cao.

_Bộ nhớ chính_

Là thành phần quan trọng nhất của bộ nhớ trong, vì vậy nhiều khi người ta đồng nhất bộ nhớ chính với bộ nhớ trong. Bộ nhớ chính tổ chức thành các ngăn theo byte và các ngăn nhớ này được đánh địa chỉ trực tiếp bởi CPU, có nghĩa là mỗi ngăn nhớ của bộ nhớ chính được gán một địa chỉ xác định. CPU muốn đọc/ghi vào ngăn nhớ nào, nó phải biết được địa chỉ của ngăn nhớ đó.

Nội dung của ngăn nhớ là giá trị được ghi trong đó. Số bit được dùng để đánh địa chỉ của ngăn nhớ sẽ quyết định dung lượng tối đa của bộ nhớ chính. Thí dụ:

  * Dùng 16 bit địa chỉ thì dung lượng tối đa của bộ nhớ là 216 = 26 x 210 = 64KB

  * Bộ xử lý Pentium III có 36 bit địa chỉ, do đó có khả năng quản lý tối đa 26 x 230=64GB . _Chú ý:_ Nội dung của ngăn nhớ có thể thay đổi còn địa chỉ ngăn nhớ thì cố định.


Bộ nhớ chính của máy tính được thiết kế bằng bộ nhớ bán dẫn với 2 loại ROM và RAM, trong đó:

  * **ROM** ( **Read Only Memory** ) là Bộ nhớ chỉ đọc thông tin, dùng để lưu trữ các chương trình hệ thống, chương trình điều khiển việc nhập xuất cơ sở (ROM-BIOS : ROM-Basic Input/Output System). Thông tin trên ROM không thể thay đổi và không bị mất ngay cả khi không có điện.

  * **RAM** ( **Random Access Memory** ) là Bộ nhớ truy xuất ngẫu nhiên, được dùng để lưu trữ dữ liệu và chương trình trong quá trình thao tác và tính toán. RAM có đặc điểm là nội dung thông tin chứa trong nó sẽ mất đi khi mất điện hoặc tắt máy. Dung lượng bộ nhớ RAM cho các máy tính hiện nay thông thường vào khoảng 128 MB, 256 MB, 512 MB và có thể hơn nữa.


Ngoài ra, trong máy tính cũng còn phần bộ nhớ khác: _**Cache Memory**_ cũng thuộc bộ nhớ trong.

Bộ nhớ cache được đặt đệm giữa CPU và bộ nhớ trong nhằm làm tăng tốc độ trao đổi thông tin. Bộ nhớ cache thuộc bộ nhớ RAM, có dung lượng nhỏ. Nó chứa một phần chương trình và dữ liệu mà CPU đang xử lý, do vậy thay vì lấy lệnh và dữ liệu từ bộ nhớ chính, CPU sẽ lấy trên cache. Hầu hết các máy tính hiện nay đều có cache tích hợp trên chip vi xử lý.

_Bộ nhớ ngoài_

Bộ nhớ ngoài ( _External Memory_ ) Là thiết bị lưu trữ thông tin với dung lượng lớn, thông tin không bị mất khi không có điện. Các thông tin này có thể là phần mềm máy tính hay dữ liệu. Bộ nhớ ngoài được kết nối với hệ thống thông qua mô-đun nối ghép vào-ra. Như vậy, _bộ nhớ ngoài về chức năng thuộc bộ nhớ, song về cấu trúc nó lại thuộc hệ thống vào ra_. Có thể cất giữ và di chuyển bộ nhớ ngoài độc lập với máy tính. Hiện nay có các loại bộ nhớ ngoài phổ biến như:

  * Đĩa mềm (Floppy disk) : là loại đĩa đường kính 3.5 inch dung lượng 1.44 MB.

  * Đĩa cứng (Hard disk) : phổ biến là đĩa cứng có dung lượng 20 GB, 30 GB, 40 GB, 60 GB, và lớn hơn nữa.

  * Đĩa quang (Compact disk): loại 4.72 inch, là thiết bị phổ biến dùng để lưu trữ các phần mềm mang nhiều thông tin, hình ảnh, âm thanh và thường được sử dụng trong các phương tiện đa truyền thông (multimedia). Có hai loại phổ biến là: đĩa CD (dung lượng khoảng 700 MB) và DVD (dung lượng khoảng 4.7 GB).

  * Các loại bộ nhớ ngoài khác như thẻ nhớ (Memory Stick, Compact Flash Card), USB Flash Drive có dung lượng phổ biến là 32 MB, 64 MB, 128 MB, ...


![](images/image1.png)

**Hình I.2.1.1.c.** **Một số loại bộ** **nhớ**

# Hệ thống vào-ra

Chức năng của hệ thống vào-ra là trao đổi thông tin giữa máy tính với thế giới bên ngoài. Hệ thống vào-ra được xây dựng dựa trên hai thành phần: các _**thiết bị vào-ra**_ (IO devices) hay còn gọi là thiết bị ngoại vi (Peripheral devices) và các _**mô-đun ghép nối vào-ra**_ (IO Interface modules)

_Mô đun ghép nối vào ra_

Các thiết bị vào ra không kết nối trực tiếp với CPU mà được kết nối thông qua các mô-đun ghép nối vào-ra. Trong các mô đun ghép nối vào-ra có các cổng vào-ra IO Port), các cổng này cũng được đánh địa chỉ bởi CPU, có nghĩa là mỗi cổng cũng có một địa chỉ xác định. Mỗi thiết bị vào-ra kết nối với CPU thông qua cổng tương ứng với địa chỉ xác định.

Mỗi thiết bị vào-ra làm nhiệm vụ chuyển đổi thông tin từ một dạng vật lý nào đó về dạng dữ liệu phù hợp với máy tính hoặc ngược lại. các thiết bị ngoại vi thông dụng như bàn phím, màn hình, máy in hay một máy tính khác. Người ta có thể phân các thiết bị ngoại vi ra nhiều loại:

  * _Thiết bị thu nhận dữ liệu_ : Bàn phím, chuột, máy quét ảnh,…

  * _Thiết bị hiển thị dữ liệu_ : màn hình, máy in,…

  * _Thiết bị nhớ_ : các loại ổ đĩa

  * _Thiết bị truyền thông_ : modem

  * _Thiết bị hỗ trợ đa phương tiện_ : hệ thống âm thanh, hình ảnh,… Các thiết bị vào:

  * **Bàn phím** (Keyboard, thiết bị nhập chuẩn): là thiết bị nhập dữ liệu và câu lệnh, bàn phím máy vi tính phổ biến hiện nay là một bảng chứa 104 phím có các tác dụng khác nhau.

  * Có thể chia làm 3 nhóm phím chính:

  * Nhóm phím đánh máy: gồm các phím chữ, phím số và phím các ký tự đặc biệt (~,

  * !, @, #, $, %, ^,&, ?, ...).

  * Nhóm phím chức năng (function keypad): gồm các phím từ F1 đến F12 và các phím như ← ↑ → ↓ (phím di chuyển từng điểm), phím PgUp (lên trang màn hình), PgDn (xuống trang màn hình), Insert (chèn), Delete (xoá), Home (về đầu), End (về cuối)

  * Nhóm phím số (numeric keypad) như NumLock (cho các ký tự số), CapsLock (tạo các chữ in), ScrollLock (chế độ cuộn màn hình) thể hiện ở các đèn chỉ thị.


  * **Chuột** (Mouse): là thiết bị cần thiết phổ biến hiện nay, nhất là các máy tính chạy trong môi trường Windows. Con chuột có kích thước vừa nắm tay di chuyển trên một tấm phẳng (mouse pad) theo hướng nào thì dấu nháy hoặc mũi tên trên màn hình sẽ di chuyển theo hướng đó tương ứng với vị trí của của viên bi hoặc tia sáng (optical mouse) nằm dưới bụng của nó. Một số máy tính có con chuột được gắn trên bàn phím.

  * **Máy quét** (Scanner): là thiết bị dùng để nhập văn bản hay hình vẽ, hình chụp vào máy tính. Thông tin nguyên thuỷ trên giấy sẽ được quét thành các tín hiệu số tạo thành các tập tin ảnh (image file).


Các thiết bị ra:

  * **Màn hình** (Screen hay Monitor, thiết bị ra chuẩn): dùng để hiển thị thông tin cho người sử dụng xem. Thông tin được thể hiện ra màn hình bằng phương pháp ánh xạ bộ nhớ (memory mapping), với cách này màn hình chỉ việc đọc liên tục bộ nhớ và hiển thị (display) bất kỳ thông tin nào hiện có trong vùng nhớ ra màn hình.

  * Màn hình phổ biến hiện nay trên thị trường là màn hình màu SVGA 15”,17”, 19” với độ phân giải có thể đạt 1280 X 1024 pixel.

  * **Máy in** (Printer): là thiết bị ra để đưa thông tin ra giấy. Máy in phổ biến hiện nay là loại máy in ma trận điểm (dot matrix) loại 24 kim, máy in phun mực, máy in laser trắng đen hoặc màu.

  * **Máy chiếu** (Projector): chức năng tương tự màn hình, thường được sử dụng thay cho màn hình trong các buổi Seminar, báo cáo, thuyết trình, …


# Liên kết hệ thống (buses)

Giữa các thành phần của một hệ thống máy tính hay ngay trong một thành phần phức tạp như CPU cũng cần trao đổi với nhau. Nhiệm vụ này được thực thi bởi hệ thống kết nối mà chúng ta quen gọi là bus. Tuỳ theo nhiệm vụ của chúng mà chúng ta phân làm 3 loại chính:

  * **Bus điều khiển** (Control bus): chuyển các thông tin/tín hiệu điều khiển từ thành phần này đến thành phần khác: CPU phát tín hiệu để điều khiển bộ nhớ hay hệ thống vào-ra hoặc từ hệ thống vào-ra gửi tín hiệu yêu cầu đến CPU.

  * **Bus dữ liệu** (Data bus): làm nhiệm vụ chuyển tải dữ liệu (nội dung ngăn nhớ, kết quả xử lý) từ CPU đến bộ nhớ hay ngược lại hoặc từ bộ nhớ/CPU ra các thiết bị ngoại vi. Đây là loại bus 2 chiều. Các máy tính hiện nay thường có đường bit dữ liệu 32 hay 64 bit.

  * **Bus địa chỉ** (Address bus): chuyển tải địa chỉ của các ngăn nhớ khi muốn truy nhập (đọc/ghi) nội dung của ngăn nhớ đó hoặc là địa chỉ cổng của các thiết bị mà CPU cần trao đổi. Độ rộng (số bit) của bus địa chỉ cho biết dung lượng cực đại của bộ nhớ mà CPU có thể quản lý được. Với độ rộng là n thì dung lượng bộ nhớ tối đa sẽ là 2n.